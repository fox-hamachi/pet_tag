"""Stamping jig for a round metal tag and square-shank letter punches.
Python version of stamp_jig.scad, with the same parameters and geometry. Remix by foxhamachi of "Guide for 8mm
letter/number stamps" by JinPrints (printables.com, CC BY 4.0).

Parts (x = along a row of text, y = down the tag, z = up; the jig sits on a steel bench block):
  base     rail with the punch slot on two feet, open underneath so it sits down over the sled.
           A rigid V tooth inside each foot drops into the sled's notches, one per row.
  carriage holds the punch in a centered hole. Its bumps fit into the rail dimples one letter
           apart and sit a quarter letter off-center, so turning the carriage end for end shifts
           the punch half a letter. Turn it so the word facing you matches the row: ODD for an
           odd letter count, EVEN for even. Center letters line up with the tick on the rail.
  sled     the tag lies in a through-pocket directly on the bench block, held by a pin (pointing
           down) through the tag hole.

Defaults are for 3mm (1/8") letter stamps with 5.95mm square shanks (OWDEN 36-piece set, see
README.md) on a 25mm x 0.85mm aluminum tag with a 3mm hole (Framendino 10-pack tag blanks, see
README.md).

Parameters are in 3mm_punch_25mm_tag.yaml. For other stamps or tags, write a config with only the
values that differ and pass it; name=value arguments override single values on top.
Writes stamp_jig_{base,carriage,sled}.stl in print orientation. All sizes in mm.
usage: python3 stamp_jig.py [out_dir] [config.yaml] [name=value ...]   e.g. punch_width=8 letter_pitch=3.2
"""
import math, os, sys
import numpy as np, trimesh, yaml
from manifold3d import Manifold, CrossSection

version = "1.0.0"

# parameters: the default config (3mm_punch_25mm_tag.yaml, next to this script), then an optional
# config of your own that sets only what differs, then name=value overrides
default_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "3mm_punch_25mm_tag.yaml")
config_paths = [arg for arg in sys.argv[1:] if arg.endswith((".yaml", ".yml"))]
with open(default_config) as config_file:
    params = yaml.safe_load(config_file)
for config_path in config_paths:
    with open(config_path) as config_file:
        overrides = yaml.safe_load(config_file) or {}
    unknown = set(overrides) - set(params)
    if unknown:
        sys.exit(f"{config_path}: unknown parameters {', '.join(sorted(unknown))}; choose from: {', '.join(params)}")
    params.update(overrides)
args = [arg for arg in sys.argv[1:] if "=" not in arg and arg not in config_paths]
for arg in sys.argv[1:]:
    if "=" in arg:
        name, value = arg.split("=", 1)
        if name not in params:
            sys.exit(f"unknown parameter {name}; choose from: {', '.join(params)}")
        params[name] = yaml.safe_load(value)   # 8 stays an integer, 3.2 a float, false a boolean
globals().update(params)

tag_rad = tag_diameter/2
punch_hole = punch_width + 2*punch_clearance
half_letter_shift = letter_pitch/4             # bump offset; turning the carriage doubles it
dimple_rad = (letter_pitch - dimple_land)/2
bump_rad = dimple_rad - bump_clearance
bump_stretch = bump_height/bump_rad               # nubs and dimples are spheres stretched this much in z

pin_dia = tag_hole_diameter - 2*pin_clearance
pin_y = tag_rad - tag_hole_from_top               # sled coordinates: tag center at the origin
tab_reach = tag_hole_from_top + pin_dia/2 + tab_margin   # pin tab, measured in from the tag top edge
# letters beside the hole sit on the nearest click position (a multiple of half a pitch) that clears it
hole_half_steps = math.ceil((tag_hole_diameter/2 + hole_letter_gap + letter_width/2)/(letter_pitch/2))
hole_letter_x = hole_half_steps*letter_pitch/2
tab_width = min(pin_dia + 2*tab_side_margin, 2*(hole_letter_x - letter_width/2 - hole_tab_gap)) if hole_letters \
            else pin_dia + 2*tab_side_margin

# as many rows and letters as fit on the tag inside edge_margin; the sled gets a notch per row and
# the slot is long enough for the widest row (50 rows is only a search limit)
fit_rad = tag_rad - edge_margin
row_count = len([row for row in range(50) if first_row_from_top + row*row_pitch + letter_height/2 <= 2*tag_rad - edge_margin])
row_y = [tag_rad - first_row_from_top - row*row_pitch for row in range(row_count)]
row_letters = [int((2*math.sqrt(max(0, fit_rad**2 - (abs(y) + letter_height/2)**2)) - letter_width)//letter_pitch) + 1
               for y in row_y]
max_letters_per_row = max(row_letters)
notch_y = row_y + ([pin_y] if hole_letters else [])   # sled notches: one per row, plus the hole row

notch_depth = detent_depth - sled_clearance + detent_clearance
sled_wall = notch_depth + sled_notch_wall
sled_width = 2*tag_rad + 2*tag_pocket_clearance + 2*sled_wall
sled_top_y = tag_rad + sled_top_margin
sled_bottom_y = -tag_rad - sled_handle_length
tunnel_width = sled_width + 2*sled_clearance
tunnel_height = sled_thickness + sled_headroom

rail_width = punch_hole + 2*rail_side_wall
bump_row_y = punch_hole/2 + bump_row_offset
base_length = tunnel_width + 2*foot_width
foot_length = rail_width + 2*foot_overhang
rail_top = tunnel_height + rail_thickness
slot_length = (max_letters_per_row - 1)*letter_pitch + punch_hole + 2*slot_end_clearance
carriage_width = punch_hole + 2*carriage_wall
label_pitch = label_height*letter_pitch_ratio
label_width = label_height*letter_width_ratio
label_top = carriage_height - label_top_margin
tick_top = label_top - label_height - tick_label_gap   # punch-center tick runs up to below the label
bottom_guide_half = punch_width/2 + bottom_guide_clearance   # carriage hole half-widths
top_guide_half = punch_width/2 + top_guide_clearance
relief_half = punch_hole/2 + hole_relief
front_label_width = 4*label_pitch + label_width
front_label_left = -base_length/4 - front_label_width/2   # FRONT, centered on the left half of the rail

# bump and dimple positions, one letter pitch apart: every candidate step (the ranges are only search
# limits) that fits on the carriage with 0.1mm to spare, or on the rail with 0.2mm
bump_x = [x for step in range(-10, 11) for x in [-half_letter_shift + step*letter_pitch]
          if abs(x) + bump_rad <= carriage_width/2 - 0.1]
dimple_x = [x for step in range(-40, 41) for x in [-half_letter_shift + step*letter_pitch]
            if abs(x) + dimple_rad <= base_length/2 - 0.2]

# design checks; the small numbers in them are the least material or clearance to leave, in mm
assert first_row_from_top - punch_hole/2 > tab_reach + 0.2, \
    "row 1 is so close to the tag hole that the punch would land on the pin tab"
assert slot_length/2 + carriage_width/2 <= base_length/2, "rail too short for max_letters_per_row"
assert 3*label_pitch + label_width <= carriage_width - 1, "EVEN label too wide for the carriage"
assert sled_thickness - tag_thickness - tab_clearance >= 0.8, "pin tab too thin"
assert not hole_letters or tab_width/2 >= pin_dia/2 + 0.6, "no room for the pin tab between the hole letters"
assert not hole_letters or math.hypot(hole_letter_x + letter_width/2, pin_y + letter_height/2) <= fit_rad, \
    "letters beside the tag hole run past edge_margin"
assert tick_top >= 2, "carriage too short for the label and tick"
assert carriage_height - 2*guide_length >= 2*hole_relief + 1, "carriage too short for the punch guides"
assert front_label_left >= -base_length/2 + 1 and front_label_left + front_label_width <= -1, \
    "FRONT label does not fit between the rail end and the center tick"
assert label_height + 1 <= rail_thickness, "rail too thin for the FRONT label"
print(f"stamp jig v{version}: rows {row_count}, letters per row {row_letters}; "
      f"sled {sled_width:g} x {sled_top_y - sled_bottom_y:g}, base {base_length:g} x {foot_length:g} x "
      f"{rail_top:g}, carriage {carriage_width:g} x {rail_width:g} x {carriage_height:g}")
if hole_letters:
    print(f"hole row: carriage on {'EVEN' if hole_half_steps % 2 else 'ODD'}, click {(hole_half_steps + 1)//2} "
          f"each side of center (x = +/-{hole_letter_x:g}); pin tab {tab_width:g} wide")

# ---- helpers ----
# cutters run 1mm past the faces they cut through, and hull end slices are 0.01 thick, so the
# booleans never leave paper-thin skins
def box(x0, x1, y0, y1, z0, z1):
    return Manifold.cube((x1 - x0, y1 - y0, z1 - z0)).translate((x0, y0, z0))

def chamfered_box(x0, x1, y0, y1, z0, z1, chamfer):
    """box with its four vertical edges chamfered at 45 degrees"""
    pts = [(x0 + chamfer, y0), (x1 - chamfer, y0), (x1, y0 + chamfer), (x1, y1 - chamfer),
           (x1 - chamfer, y1), (x0 + chamfer, y1), (x0, y1 - chamfer), (x0, y0 + chamfer)]
    return Manifold.extrude(CrossSection([pts]), z1 - z0).translate((0, 0, z0))

def cylinder(radius, height, top_radius=None, segments=fn):
    return Manifold.cylinder(height, radius, radius if top_radius is None else top_radius, segments)

def sphere(radius):
    return Manifold.sphere(radius, fn)

def v_prism(x_edge, side, depth, y, z0, z1):
    """90-degree V, apex at (x_edge - side*depth, y) pointing toward -side, from x_edge outward; z0..z1.
    It starts 0.1 behind x_edge so it fuses with the face there."""
    pts = [(x_edge + side*0.1, y - depth - 0.1), (x_edge - side*depth, y), (x_edge + side*0.1, y + depth + 0.1)]
    if sum(pt[0]*next_pt[1] - next_pt[0]*pt[1] for pt, next_pt in zip(pts, pts[1:] + pts[:1])) < 0:
        pts = pts[::-1]                       # CrossSection wants counter-clockwise
    return Manifold.extrude(CrossSection([pts]), z1 - z0).translate((0, 0, z0))

def union(parts):
    return sum(parts[1:], parts[0])

# carriage lettering, from ../layout/stamp_font.py: strokes in a unit box, x right, y down
LABEL_GLYPHS = {
    "D": [[(0.0, 0.0), (0.0, 1.0), (0.45, 1.0), (0.45, 1.0), (0.546, 0.992), (0.638, 0.97), (0.725, 0.933), (0.804, 0.883), (0.871, 0.821), (0.926, 0.75), (0.967, 0.671), (0.992, 0.587), (1.0, 0.5), (0.992, 0.413), (0.967, 0.329), (0.926, 0.25), (0.871, 0.179), (0.804, 0.117), (0.725, 0.067), (0.638, 0.03), (0.546, 0.008), (0.45, 0.0), (0.0, 0.0)]],
    "E": [[(1.0, 0.0), (0.0, 0.0), (0.0, 1.0), (1.0, 1.0)], [(0.0, 0.5), (0.75, 0.5)]],
    "F": [[(1, 0), (0, 0), (0, 1)], [(0, 0.5), (0.75, 0.5)]],
    "N": [[(0.0, 1.0), (0.0, 0.0), (1.0, 1.0), (1.0, 0.0)]],
    "O": [[(1.0, 0.5), (0.992, 0.587), (0.97, 0.671), (0.933, 0.75), (0.883, 0.821), (0.821, 0.883), (0.75, 0.933), (0.671, 0.97), (0.587, 0.992), (0.5, 1.0), (0.413, 0.992), (0.329, 0.97), (0.25, 0.933), (0.179, 0.883), (0.117, 0.821), (0.067, 0.75), (0.03, 0.671), (0.008, 0.587), (0.0, 0.5), (0.008, 0.413), (0.03, 0.329), (0.067, 0.25), (0.117, 0.179), (0.179, 0.117), (0.25, 0.067), (0.329, 0.03), (0.413, 0.008), (0.5, 0.0), (0.587, 0.008), (0.671, 0.03), (0.75, 0.067), (0.821, 0.117), (0.883, 0.179), (0.933, 0.25), (0.97, 0.329), (0.992, 0.413), (1.0, 0.5)]],
    "R": [[(0, 1), (0, 0), (0.6, 0), (0.6, 0.0), (0.669, 0.004), (0.737, 0.016), (0.8, 0.035), (0.857, 0.061), (0.906, 0.093), (0.946, 0.13), (0.976, 0.171), (0.994, 0.215), (1.0, 0.26), (0.994, 0.305), (0.976, 0.349), (0.946, 0.39), (0.906, 0.427), (0.857, 0.459), (0.8, 0.485), (0.737, 0.504), (0.669, 0.516), (0.6, 0.52), (0, 0.52)], [(0.5, 0.52), (1, 1)]],
    "T": [[(0, 0), (1, 0)], [(0.5, 0), (0.5, 1)]],
    "V": [[(0.0, 0.0), (0.5, 1.0), (1.0, 0.0)]],
}

def text_segments(text, height, left, top):
    """Line segments of text in a plane (u right, v up), letters height tall from (left, top)."""
    width = height*letter_width_ratio
    return [(pts[point], pts[point+1])
            for index, ch in enumerate(text) for stroke in LABEL_GLYPHS[ch]
            for pts in [[(left + index*height*letter_pitch_ratio + label_stroke/2 + gx*(width - label_stroke),
                          top - label_stroke/2 - gy*(height - label_stroke)) for gx, gy in stroke]]
            for point in range(len(pts) - 1)]

def pen(u, v, face):
    """Engraving tool at (u, v) on the carriage front (face -1) or back (face 1), as seen from
    outside it: u along x, v up."""
    tool = Manifold.cylinder(label_depth + 1, label_stroke/2, label_stroke/2, 12)   # 12 sides: plenty for a thin stroke
    return tool.rotate((-face*90, 0, 0)).translate((u if face < 0 else -u, face*(rail_width/2 - label_depth), v))

def engrave(text, face, height, left, top):
    return union([Manifold.batch_hull([pen(*start_pt, face), pen(*end_pt, face)])
                  for start_pt, end_pt in text_segments(text, height, left, top)])

# ---- parts, in assembled position ----
def base():
    body = union([chamfered_box(-base_length/2, -tunnel_width/2, -foot_length/2, foot_length/2, 0, tunnel_height, foot_chamfer),
                  chamfered_box(tunnel_width/2, base_length/2, -foot_length/2, foot_length/2, 0, tunnel_height, foot_chamfer),
                  box(-base_length/2, base_length/2, -rail_width/2, rail_width/2, tunnel_height, rail_top)]
                 + [v_prism(side*tunnel_width/2, side, detent_depth, 0, 0, tunnel_height + 0.1) for side in (-1, 1)])  # V teeth
    body -= box(-slot_length/2, slot_length/2, -punch_hole/2, punch_hole/2, tunnel_height - 1, rail_top + 1)
    body -= Manifold.batch_hull([   # chamfer on the slot's long top edges, so the punch can't catch leaving the carriage
        box(-slot_length/2, slot_length/2, -punch_hole/2, punch_hole/2, rail_top - slot_lead_in, rail_top - slot_lead_in + 0.01),
        box(-slot_length/2, slot_length/2, -punch_hole/2 - slot_lead_in - 0.01, punch_hole/2 + slot_lead_in + 0.01,
            rail_top + 0.01, rail_top + 0.02)])
    for x in dimple_x:
        for y in (-bump_row_y, bump_row_y):
            body -= sphere(dimple_rad).scale((1, 1, bump_stretch)).translate((x, y, rail_top))
    for side in (-1, 1):   # center ticks, front and back
        y_inner, y_outer = side*(rail_width/2 - tick_depth), side*(rail_width/2 + 1)
        body -= box(-tick_width/2, tick_width/2, min(y_inner, y_outer), max(y_inner, y_outer), tunnel_height + rail_tick_inset, rail_top + 1)
    body -= engrave("FRONT", -1, label_height, front_label_left, rail_top - 1)
    return body

def carriage():
    """Bump side down on the rail top, z = 0."""
    body = box(-carriage_width/2, carriage_width/2, -rail_width/2, rail_width/2, 0, carriage_height)
    for x in bump_x:
        for y in (-bump_row_y, bump_row_y):
            body += sphere(bump_rad).scale((1, 1, bump_stretch)).translate((x, y, 0)) ^ \
                    box(x - 1 - bump_rad, x + 1 + bump_rad, y - 1 - bump_rad, y + 1 + bump_rad, -bump_height - 1, 0)
    guide_top = carriage_height - guide_length
    body -= box(-bottom_guide_half, bottom_guide_half, -bottom_guide_half, bottom_guide_half, -1, guide_length + 0.01)
    body -= box(-top_guide_half, top_guide_half, -top_guide_half, top_guide_half, guide_top - 0.01, carriage_height + 1)
    body -= Manifold.batch_hull([   # relief between the guides, with 45-degree transitions
        box(-bottom_guide_half, bottom_guide_half, -bottom_guide_half, bottom_guide_half, guide_length, guide_length + 0.01),
        box(-relief_half, relief_half, -relief_half, relief_half,
            guide_length + relief_half - bottom_guide_half, guide_top - (relief_half - top_guide_half)),
        box(-top_guide_half, top_guide_half, -top_guide_half, top_guide_half, guide_top - 0.01, guide_top)])
    body -= Manifold.batch_hull([   # 45-degree lead-in at the top of the punch hole
        box(-top_guide_half, top_guide_half, -top_guide_half, top_guide_half, carriage_height - lead_in, carriage_height - lead_in + 0.01),
        box(-top_guide_half - lead_in - 0.01, top_guide_half + lead_in + 0.01, -top_guide_half - lead_in - 0.01, top_guide_half + lead_in + 0.01,
            carriage_height + 0.01, carriage_height + 0.02)])
    for side, word in ((-1, "ODD"), (1, "EVEN")):   # front face: ODD; turned end for end: EVEN
        body -= engrave(word, side, label_height, -((len(word) - 1)*label_pitch + label_width)/2, label_top)
        y_inner, y_outer = side*(rail_width/2 - tick_depth), side*(rail_width/2 + 1)
        body -= box(-tick_width/2, tick_width/2, min(y_inner, y_outer), max(y_inner, y_outer), 0, tick_top)   # punch-center tick
    return body

def sled():
    """Tag center at the origin, tag top toward +y, bench-block side at z = 0."""
    body = box(-sled_width/2, sled_width/2, sled_bottom_y, sled_top_y, 0, sled_thickness)
    body -= cylinder(tag_rad + tag_pocket_clearance, sled_thickness + 2, segments=120).translate((0, 0, -1))   # finer than fn: the tag fits it closely
    for y in notch_y:
        for side in (-1, 1):
            body -= v_prism(side*sled_width/2, side, notch_depth, y, -1, sled_thickness + 1)
    for groove in range(grip_groove_count):
        groove_y = sled_bottom_y + grip_groove_start + grip_groove_pitch*groove
        body -= box(-grip_groove_length/2, grip_groove_length/2, groove_y, groove_y + grip_groove_width,
                    sled_thickness - grip_groove_depth, sled_thickness + 1)
    # tab over the hole margin, with the pin pointing down to the bench block
    body += box(-tab_width/2, tab_width/2, tag_rad - tab_reach, tag_rad + tag_pocket_clearance + tab_overlap,
                tag_thickness + tab_clearance, sled_thickness)
    body += (cylinder(pin_dia/2, tag_thickness + tab_clearance - pin_tip_chamfer).translate((0, 0, pin_tip_chamfer))
             + cylinder(pin_dia/2 - pin_tip_chamfer, pin_tip_chamfer, pin_dia/2)).translate((0, pin_y, 0))   # chamfered tip
    return body

# ---- print orientation (carriage and sled flipped onto their flat faces) ----
def carriage_print(): return carriage().rotate((180, 0, 0)).translate((0, 0, carriage_height))
def sled_print():     return sled().rotate((180, 0, 0)).translate((0, 0, sled_thickness))

def write(model, path):
    mesh = model.to_mesh()
    tri_mesh = trimesh.Trimesh(mesh.vert_properties[:, :3], mesh.tri_verts)
    tri_mesh.export(path)
    print(f"{path}: {len(tri_mesh.faces)} triangles, {tri_mesh.volume:.0f} mm^3, size {np.round(tri_mesh.extents, 2).tolist()}, "
          f"watertight={tri_mesh.is_watertight}")

if __name__ == "__main__":
    out = args[0] if args else "."
    for name, make_part in (("base", base), ("carriage", carriage_print), ("sled", sled_print)):
        write(make_part(), os.path.join(out, f"stamp_jig_{name}.stl"))
