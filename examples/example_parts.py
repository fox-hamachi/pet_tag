"""Example tag and letter punch for showing the stamp jig assembled; not printed parts.
Tag, hole, punch and letter sizes, and the row and letter positions, come from stamp_jig.py and its
config (3mm_punch_25mm_tag.yaml, plus any config or name=value overrides on the command line).

  example_tag.stl    tag lying flat, center at the origin, back face at z = 0, hole toward +y,
                     stamped with tag_text where the jig puts the letters: rows on its notches,
                     letters on its pitch, each row centered.
  example_punch.stl  punch standing up, letter face at z = 0 centered on the origin, letter top
                     toward +y so it stamps upright on the tag. In the jig the face rests on the
                     tag top (z = tag_thickness) under the carriage hole.
usage: python3 example_parts.py [out_dir] [letter] [tag_text] [config.yaml] [name=value ...]
       (tag_text rows separated by "/")
"""
import os, sys
import numpy as np, trimesh
from manifold3d import Manifold, CrossSection

here = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(here, ".."), os.path.join(here, "..", "..", "layout")]
from stamp_font import GLYPHS
import stamp_jig as jig         # sizes and layout, from the jig's config and command-line overrides
from stamp_jig import (tag_diameter, tag_thickness, tag_hole_diameter, tag_hole_from_top, punch_width,
                       letter_height, letter_width, letter_pitch)

tag_text = "CAT/555 555/0100"   # placeholder name and phone
stamp_depth = 0.2               # stamped letter depth in the tag
punch_length = 63.5             # 2-1/2"
letter_stroke = 0.09*letter_height   # as in cat_tag.py
letter_relief = 0.6             # raised letter on the punch face
tip_width = 4.0                 # square face the letter stands on
taper_length = 6.0              # shank to face
end_chamfer = 0.8               # striking end

def tag():
    tag_rad = tag_diameter/2
    disc = Manifold.cylinder(tag_thickness, tag_rad, tag_rad, 180)
    hole = Manifold.cylinder(tag_thickness + 2, tag_hole_diameter/2, tag_hole_diameter/2, 48) \
        .translate((0, tag_rad - tag_hole_from_top, -1))
    return disc - hole - stamped(tag_text)

def stamped(text):
    """Letter grooves in the tag top: row n on the jig's row n, letters on its pitch, each row centered."""
    rows = text.upper().split("/")
    if len(rows) > jig.row_count:
        sys.exit(f"{len(rows)} rows of text, but the jig has {jig.row_count}")
    pen = lambda x, y: Manifold.cylinder(stamp_depth + 1, letter_stroke/2, letter_stroke/2, 12) \
        .translate((x, y, tag_thickness - stamp_depth))
    cuts = []
    for row_index, row in enumerate(rows):
        x0 = -((len(row) - 1)*letter_pitch + letter_width)/2
        top = jig.row_y[row_index] + letter_height/2
        for column, ch in enumerate(row):
            for stroke in GLYPHS.get(ch, []):
                pts = [(x0 + column*letter_pitch + letter_stroke/2 + gx*(letter_width - letter_stroke),
                        top - letter_stroke/2 - gy*(letter_height - letter_stroke)) for gx, gy in stroke]
                cuts += [Manifold.batch_hull([pen(*start_pt), pen(*end_pt)]) for start_pt, end_pt in zip(pts, pts[1:])]
    return sum(cuts[1:], cuts[0])

def letter(ch):
    """Raised stroke letter from z = 0 (the striking face) up to letter_relief. Laid out to read from
    above, so it stamps upright (seen from below, on the punch, it looks mirrored like a real one)."""
    segs = []
    for stroke in GLYPHS[ch]:
        pts = [(-letter_width/2 + letter_stroke/2 + gx*(letter_width - letter_stroke),
                letter_height/2 - letter_stroke/2 - gy*(letter_height - letter_stroke)) for gx, gy in stroke]
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            segs.append(CrossSection.batch_hull([CrossSection.circle(letter_stroke/2, 12).translate((xa, ya)),
                                                 CrossSection.circle(letter_stroke/2, 12).translate((xb, yb))]))
    return Manifold.extrude(sum(segs[1:], segs[0]), letter_relief)

def punch(ch):
    z_tip = letter_relief
    z_shank = z_tip + taper_length
    square = lambda width: CrossSection.square((width, width), True)
    taper = Manifold.extrude(square(tip_width), taper_length, scale_top=(punch_width/tip_width, punch_width/tip_width)) \
        .translate((0, 0, z_tip))
    shank = Manifold.extrude(square(punch_width), punch_length - z_shank - end_chamfer).translate((0, 0, z_shank))
    top = Manifold.extrude(square(punch_width), end_chamfer,
                           scale_top=((punch_width - 2*end_chamfer)/punch_width,)*2) \
        .translate((0, 0, punch_length - end_chamfer))
    return letter(ch) + taper + shank + top

def write(model, path):
    mesh = model.to_mesh()
    tri_mesh = trimesh.Trimesh(mesh.vert_properties[:, :3], mesh.tri_verts)
    tri_mesh.export(path)
    print(f"{path}: {len(tri_mesh.faces)} triangles, size {np.round(tri_mesh.extents, 2).tolist()}, watertight={tri_mesh.is_watertight}")

if __name__ == "__main__":
    args = jig.args   # positional arguments, without the config and name=value overrides
    out = args[0] if len(args) > 0 else "."
    ch = args[1].upper() if len(args) > 1 else "A"
    tag_text = args[2] if len(args) > 2 else tag_text
    write(tag(), os.path.join(out, "example_tag.stl"))
    write(punch(ch), os.path.join(out, "example_punch.stl"))
