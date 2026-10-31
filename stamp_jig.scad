// Stamping jig for a round metal tag and square-shank letter punches.
// OpenSCAD version of stamp_jig.py, with the same parameters and geometry. Remix by foxhamachi of "Guide for 8mm
// letter/number stamps" by JinPrints (printables.com, CC BY 4.0).
//
// Parts (x = along a row of text, y = down the tag, z = up; the jig sits on a steel bench block):
//   base     rail with the punch slot on two feet, open underneath so it sits down over the sled.
//            A rigid V tooth inside each foot drops into the sled's notches, one per row.
//   carriage holds the punch in a centered hole. Its bumps fit into the rail dimples one letter
//            apart and sit a quarter letter off-center, so turning the carriage end for end shifts
//            the punch half a letter. Turn it so the word facing you matches the row: ODD for an
//            odd letter count, EVEN for even. Center letters line up with the tick on the rail.
//   sled     the tag lies in a through-pocket directly on the bench block, held by a pin (pointing
//            down) through the tag hole.
//
// Defaults are for 3mm (1/8") letter stamps with 5.95mm square shanks (OWDEN 36-piece set, see
// README.md) on a 25mm x 0.85mm aluminum tag with a 3mm hole (Framendino 10-pack tag blanks, see
// README.md).
//
// Export one part at a time (set `part`), in print orientation. All sizes in mm.

/* [Part to show] */
part = "all"; // [all, base, carriage, sled, assembly]

/* [Tag] */
tag_diameter = 25;
tag_thickness = 0.85;
tag_hole_diameter = 3.0;
tag_hole_from_top = 3.5;        // tag top edge to the hole center

/* [Stamps] */
punch_width = 5.95;             // square shank, across the flats
punch_clearance = 0.15;         // per side, nominal punch fit: sizes the rail slot and the parts around it
bottom_guide_clearance = 0.125; // per side, carriage hole at the bottom: sets where the letter lands
top_guide_clearance = 0.175;    // per side, carriage hole at the top: keeps the punch upright
hole_relief = 0.3;              // extra per side in the middle of the carriage hole, between the guides

/* [Stamped Text layout] */
letter_pitch = 2.4;             // pitch: letter center to letter center along a row
row_pitch = 4.2;                // line spacing: row center to row center
first_row_from_top = 8.8;       // tag top edge to the center of row 1
letter_height = 3.0;            // stamped character size
letter_width = 2.0;             // widest stamped character
edge_margin = 1.0;              // keep letters this far inside the tag edge
hole_letters = true;            // a letter each side of the tag hole: adds a sled notch at the hole
                                // and narrows the pin tab to clear the letters

/* [Fit] */
tag_pocket_clearance = 0.15;    // per side, around the tag in the sled pocket
pin_clearance = 0.1;            // per side, pin in the tag hole
sled_clearance = 0.1;           // per side, sled between the feet
tab_clearance = 0.4;            // gap between the tag top and the sled's pin tab; more makes the pin taller
sled_headroom = 0.8;            // gap between the sled top and the rail; 0.5 of it allows for the
                                // rough rail underside left by the bridge supports
detent_clearance = 0.15;        // extra depth in each sled notch
bump_clearance = 0.1;           // per side, carriage nub in a rail dimple

/* [Sizes] */
sled_thickness = 2.2;
sled_handle_length = 27.5;      // sled beyond the bottom of the tag pocket
rail_thickness = 6;
carriage_height = 20;
carriage_wall = 4;              // carriage material either side of the punch hole
guide_length = 5;               // close-fitting part of the punch hole at each end of the carriage
foot_width = 8;
foot_chamfer = 1.0;             // 45-degree chamfer on the vertical corners of the feet
detent_depth = 1.5;             // how far each V tooth reaches in from its foot
bump_height = 1.5;              // carriage nubs (half-ellipsoids); the rail dimples are deeper
dimple_land = 0.3;              // ridge left between neighboring rail dimples
label_height = 3.5;           // ODD / EVEN lettering on the carriage front and back faces
label_depth = 1.0;
tick_depth = 1.0;               // center ticks on the rail and carriage
label_stroke = 0.6;             // engraved line width

/* [Hidden] */
version = "1.0.0";
$fn = 48;                       // segments for round shapes; the tag pocket and engraving pen set their own
// fixed sizes (not worth exposing as parameters)
letter_width_ratio = 2/3;       // stamp font proportions, as in ../layout/cat_tag.py: letter width
letter_pitch_ratio = 0.8;       // and letter pitch, both as fractions of the letter height
pin_tip_chamfer = 0.4;          // 45-degree chamfer on the tip of the sled pin
tab_margin = 0.5;               // pin tab material beyond the pin, toward the tag center
tab_side_margin = 2.6;          // pin tab material either side of the pin
hole_letter_gap = 0.5;          // least gap between the tag hole and a letter beside it
hole_tab_gap = 0.4;             // pin tab edge to a letter beside the hole, room for the punch's tapered tip
tab_overlap = 0.85;             // how far the pin tab reaches past the tag pocket onto the sled frame
sled_notch_wall = 2.2;          // sled material outside the bottom of each notch
sled_top_margin = 3.5;          // sled beyond the tag top edge
rail_side_wall = 6;             // rail material either side of the punch slot
bump_row_offset = 3;            // bump and dimple rows: distance out from the punch hole edge
foot_overhang = 16;             // feet run this far past the rail at each end, to guide the sled
slot_end_clearance = 0.2;       // slot length beyond the outermost punch positions, at each end
lead_in = 0.8;                  // depth and width of the 45-degree lead-in at the top of the punch hole
slot_lead_in = 0.5;             // depth and width of the 45-degree chamfer on the rail slot's long top edges
label_top_margin = 1.2;         // carriage top to the top of the ODD / EVEN label
tick_label_gap = 0.8;           // gap between the carriage label and the tick below it
tick_width = 0.4;               // center ticks on the rail and carriage
rail_tick_inset = 1.5;          // rail ticks start this far above the tunnel
grip_groove_count = 5;          // grip grooves across the top of the sled handle
grip_groove_width = 0.8;        // along the handle
grip_groove_pitch = 2;          // groove to groove
grip_groove_length = 16;        // across the handle
grip_groove_depth = 0.5;        // into the sled top
grip_groove_start = 3;          // handle end to the first groove

tag_rad = tag_diameter/2;
punch_hole = punch_width + 2*punch_clearance;
half_letter_shift = letter_pitch/4;            // bump offset; turning the carriage doubles it
dimple_rad = (letter_pitch - dimple_land)/2;
bump_rad = dimple_rad - bump_clearance;
bump_stretch = bump_height/bump_rad;              // nubs and dimples are spheres stretched this much in z

pin_dia = tag_hole_diameter - 2*pin_clearance;
pin_y = tag_rad - tag_hole_from_top;              // sled coordinates: tag center at the origin
tab_reach = tag_hole_from_top + pin_dia/2 + tab_margin;  // pin tab, measured in from the tag top edge
// letters beside the hole sit on the nearest click position (a multiple of half a pitch) that clears it
hole_half_steps = ceil((tag_hole_diameter/2 + hole_letter_gap + letter_width/2)/(letter_pitch/2));
hole_letter_x = hole_half_steps*letter_pitch/2;
tab_width = hole_letters ? min(pin_dia + 2*tab_side_margin, 2*(hole_letter_x - letter_width/2 - hole_tab_gap))
                         : pin_dia + 2*tab_side_margin;

// as many rows and letters as fit on the tag inside edge_margin; the sled gets a notch per row and
// the slot is long enough for the widest row (50 rows is only a search limit)
fit_rad = tag_rad - edge_margin;
row_count = len([for (row = [0:49]) if (first_row_from_top + row*row_pitch + letter_height/2 <= 2*tag_rad - edge_margin) row]);
row_y = [for (row = [0:row_count-1]) tag_rad - first_row_from_top - row*row_pitch];
row_letters = [for (y = row_y) floor((2*sqrt(max(0, pow(fit_rad, 2) - pow(abs(y) + letter_height/2, 2))) - letter_width)/letter_pitch) + 1];
max_letters_per_row = max(row_letters);
notch_y = concat(row_y, hole_letters ? [pin_y] : []);   // sled notches: one per row, plus the hole row

notch_depth = detent_depth - sled_clearance + detent_clearance;
sled_wall = notch_depth + sled_notch_wall;
sled_width = 2*tag_rad + 2*tag_pocket_clearance + 2*sled_wall;
sled_top_y = tag_rad + sled_top_margin;
sled_bottom_y = -tag_rad - sled_handle_length;
tunnel_width = sled_width + 2*sled_clearance;
tunnel_height = sled_thickness + sled_headroom;

rail_width = punch_hole + 2*rail_side_wall;
bump_row_y = punch_hole/2 + bump_row_offset;
base_length = tunnel_width + 2*foot_width;
foot_length = rail_width + 2*foot_overhang;
rail_top = tunnel_height + rail_thickness;
slot_length = (max_letters_per_row - 1)*letter_pitch + punch_hole + 2*slot_end_clearance;
carriage_width = punch_hole + 2*carriage_wall;
label_pitch = label_height*letter_pitch_ratio;
label_width = label_height*letter_width_ratio;
label_top = carriage_height - label_top_margin;
tick_top = label_top - label_height - tick_label_gap;   // punch-center tick runs up to below the label
bottom_guide_half = punch_width/2 + bottom_guide_clearance;   // carriage hole half-widths
top_guide_half = punch_width/2 + top_guide_clearance;
relief_half = punch_hole/2 + hole_relief;
front_label_width = 4*label_pitch + label_width;
front_label_left = -base_length/4 - front_label_width/2;   // FRONT, centered on the left half of the rail

// bump and dimple positions, one letter pitch apart: every candidate step (the ranges are only search
// limits) that fits on the carriage with 0.1mm to spare, or on the rail with 0.2mm
bump_x = [for (step = [-10:10]) let (x = -half_letter_shift + step*letter_pitch)
          if (abs(x) + bump_rad <= carriage_width/2 - 0.1) x];
dimple_x = [for (step = [-40:40]) let (x = -half_letter_shift + step*letter_pitch)
            if (abs(x) + dimple_rad <= base_length/2 - 0.2) x];

// design checks; the small numbers in them are the least material or clearance to leave, in mm
assert(first_row_from_top - punch_hole/2 > tab_reach + 0.2,
       "row 1 is so close to the tag hole that the punch would land on the pin tab");
assert(slot_length/2 + carriage_width/2 <= base_length/2, "rail too short for max_letters_per_row");
assert(3*label_pitch + label_width <= carriage_width - 1, "EVEN label too wide for the carriage");
assert(sled_thickness - tag_thickness - tab_clearance >= 0.8, "pin tab too thin");
assert(!hole_letters || tab_width/2 >= pin_dia/2 + 0.6, "no room for the pin tab between the hole letters");
assert(!hole_letters || norm([hole_letter_x + letter_width/2, pin_y + letter_height/2]) <= fit_rad,
       "letters beside the tag hole run past edge_margin");
assert(tick_top >= 2, "carriage too short for the label and tick");
assert(carriage_height - 2*guide_length >= 2*hole_relief + 1, "carriage too short for the punch guides");
assert(front_label_left >= -base_length/2 + 1 && front_label_left + front_label_width <= -1,
       "FRONT label does not fit between the rail end and the center tick");
assert(label_height + 1 <= rail_thickness, "rail too thin for the FRONT label");
echo(str("stamp jig v", version, ": rows ", row_count, ", letters per row ", row_letters, "; sled ", sled_width, " x ", sled_top_y - sled_bottom_y, ", base ", base_length, " x ",
         foot_length, " x ", rail_top, ", carriage ", carriage_width, " x ", rail_width, " x ",
         carriage_height));
if (hole_letters)
    echo(str("hole row: carriage on ", hole_half_steps % 2 == 1 ? "EVEN" : "ODD", ", click ", floor((hole_half_steps + 1)/2),
             " each side of center (x = +/-", hole_letter_x, "); pin tab ", tab_width, " wide"));

// ---- helpers ----
// cutters run 1mm past the faces they cut through, and hull end slices are 0.01 thick, so the
// booleans never leave paper-thin skins
module box(x0, x1, y0, y1, z0, z1) { translate([x0, y0, z0]) cube([x1 - x0, y1 - y0, z1 - z0]); }

// box with its four vertical edges chamfered at 45 degrees
module chamfered_box(x0, x1, y0, y1, z0, z1, chamfer) {
    translate([0, 0, z0]) linear_extrude(z1 - z0)
        polygon([[x0 + chamfer, y0], [x1 - chamfer, y0], [x1, y0 + chamfer], [x1, y1 - chamfer],
                 [x1 - chamfer, y1], [x0 + chamfer, y1], [x0, y1 - chamfer], [x0, y0 + chamfer]]);
}

// 90-degree V, apex at (x_edge - side*depth, y) pointing toward -side, from x_edge outward; z0..z1.
// It starts 0.1 behind x_edge so it fuses with the face there.
module v_prism(x_edge, side, depth, y, z0, z1) {
    translate([0, 0, z0]) linear_extrude(z1 - z0)
        polygon([[x_edge + side*0.1, y - depth - 0.1], [x_edge - side*depth, y], [x_edge + side*0.1, y + depth + 0.1]]);
}

// carriage lettering, from ../layout/stamp_font.py: strokes in a unit box, x right, y down
LABEL_GLYPHS = [
    ["D", [[[0, 0], [0, 1], [0.45, 1], [0.45, 1], [0.546, 0.992], [0.638, 0.97], [0.725, 0.933], [0.804, 0.883], [0.871, 0.821], [0.926, 0.75], [0.967, 0.671], [0.992, 0.587], [1, 0.5], [0.992, 0.413], [0.967, 0.329], [0.926, 0.25], [0.871, 0.179], [0.804, 0.117], [0.725, 0.067], [0.638, 0.03], [0.546, 0.008], [0.45, 0], [0, 0]]]],
    ["E", [[[1, 0], [0, 0], [0, 1], [1, 1]], [[0, 0.5], [0.75, 0.5]]]],
    ["F", [[[1, 0], [0, 0], [0, 1]], [[0, 0.5], [0.75, 0.5]]]],
    ["N", [[[0, 1], [0, 0], [1, 1], [1, 0]]]],
    ["O", [[[1, 0.5], [0.992, 0.587], [0.97, 0.671], [0.933, 0.75], [0.883, 0.821], [0.821, 0.883], [0.75, 0.933], [0.671, 0.97], [0.587, 0.992], [0.5, 1], [0.413, 0.992], [0.329, 0.97], [0.25, 0.933], [0.179, 0.883], [0.117, 0.821], [0.067, 0.75], [0.03, 0.671], [0.008, 0.587], [0, 0.5], [0.008, 0.413], [0.03, 0.329], [0.067, 0.25], [0.117, 0.179], [0.179, 0.117], [0.25, 0.067], [0.329, 0.03], [0.413, 0.008], [0.5, 0], [0.587, 0.008], [0.671, 0.03], [0.75, 0.067], [0.821, 0.117], [0.883, 0.179], [0.933, 0.25], [0.97, 0.329], [0.992, 0.413], [1, 0.5]]]],
    ["R", [[[0, 1], [0, 0], [0.6, 0], [0.6, 0], [0.669, 0.004], [0.737, 0.016], [0.8, 0.035], [0.857, 0.061], [0.906, 0.093], [0.946, 0.13], [0.976, 0.171], [0.994, 0.215], [1, 0.26], [0.994, 0.305], [0.976, 0.349], [0.946, 0.39], [0.906, 0.427], [0.857, 0.459], [0.8, 0.485], [0.737, 0.504], [0.669, 0.516], [0.6, 0.52], [0, 0.52]], [[0.5, 0.52], [1, 1]]]],
    ["T", [[[0, 0], [1, 0]], [[0.5, 0], [0.5, 1]]]],
    ["V", [[[0, 0], [0.5, 1], [1, 0]]]]
];
function glyph(ch) = [for (entry = LABEL_GLYPHS) if (entry[0] == ch) entry[1]][0];

// line segments of text in a plane (u right, v up), letters height tall from (left, top)
function text_segments(text, height, left, top) = let (width = height*letter_width_ratio)
    [for (index = [0:len(text)-1], stroke = glyph(text[index]))
        let (pts = [for (glyph_pt = stroke) [left + index*height*letter_pitch_ratio + label_stroke/2 + glyph_pt[0]*(width - label_stroke),
                                             top - label_stroke/2 - glyph_pt[1]*(height - label_stroke)]])
        for (point = [0:len(pts)-2]) [pts[point], pts[point+1]]];

// engraving tool at (u, v) on the carriage front (face -1) or back (face 1), as seen from
// outside it: u along x, v up
module pen(u, v, face) {
    translate([face < 0 ? u : -u, face*(rail_width/2 - label_depth), v]) rotate([-face*90, 0, 0])
        cylinder(r = label_stroke/2, h = label_depth + 1, $fn = 12);   // 12 sides: plenty for a thin stroke
}

module engrave(text, face, height, left, top) {
    for (seg = text_segments(text, height, left, top)) hull() { pen(seg[0][0], seg[0][1], face); pen(seg[1][0], seg[1][1], face); }
}

// ---- parts, in assembled position ----
module base() {
    difference() {
        union() {
            for (side = [-1, 1]) chamfered_box(side < 0 ? -base_length/2 : tunnel_width/2, side < 0 ? -tunnel_width/2 : base_length/2,
                                               -foot_length/2, foot_length/2, 0, tunnel_height, foot_chamfer);
            box(-base_length/2, base_length/2, -rail_width/2, rail_width/2, tunnel_height, rail_top);
            for (side = [-1, 1]) v_prism(side*tunnel_width/2, side, detent_depth, 0, 0, tunnel_height + 0.1);   // V teeth
        }
        box(-slot_length/2, slot_length/2, -punch_hole/2, punch_hole/2, tunnel_height - 1, rail_top + 1);
        hull() {   // chamfer on the slot's long top edges, so the punch can't catch leaving the carriage
            box(-slot_length/2, slot_length/2, -punch_hole/2, punch_hole/2, rail_top - slot_lead_in, rail_top - slot_lead_in + 0.01);
            box(-slot_length/2, slot_length/2, -punch_hole/2 - slot_lead_in - 0.01, punch_hole/2 + slot_lead_in + 0.01,
                rail_top + 0.01, rail_top + 0.02);
        }
        for (x = dimple_x, y = [-bump_row_y, bump_row_y]) translate([x, y, rail_top]) scale([1, 1, bump_stretch]) sphere(dimple_rad);
        for (side = [-1, 1]) {   // center ticks, front and back
            y_inner = side*(rail_width/2 - tick_depth); y_outer = side*(rail_width/2 + 1);
            box(-tick_width/2, tick_width/2, min(y_inner, y_outer), max(y_inner, y_outer), tunnel_height + rail_tick_inset, rail_top + 1);
        }
        engrave("FRONT", -1, label_height, front_label_left, rail_top - 1);
    }
}

module carriage() {   // bump side down on the rail top, z = 0
    difference() {
        union() {
            box(-carriage_width/2, carriage_width/2, -rail_width/2, rail_width/2, 0, carriage_height);
            for (x = bump_x, y = [-bump_row_y, bump_row_y])
                intersection() { translate([x, y, 0]) scale([1, 1, bump_stretch]) sphere(bump_rad); box(x - 1 - bump_rad, x + 1 + bump_rad, y - 1 - bump_rad, y + 1 + bump_rad, -bump_height - 1, 0); }
        }
        guide_top = carriage_height - guide_length;
        box(-bottom_guide_half, bottom_guide_half, -bottom_guide_half, bottom_guide_half, -1, guide_length + 0.01);
        box(-top_guide_half, top_guide_half, -top_guide_half, top_guide_half, guide_top - 0.01, carriage_height + 1);
        hull() {   // relief between the guides, with 45-degree transitions
            box(-bottom_guide_half, bottom_guide_half, -bottom_guide_half, bottom_guide_half, guide_length, guide_length + 0.01);
            box(-relief_half, relief_half, -relief_half, relief_half,
                guide_length + relief_half - bottom_guide_half, guide_top - (relief_half - top_guide_half));
            box(-top_guide_half, top_guide_half, -top_guide_half, top_guide_half, guide_top - 0.01, guide_top);
        }
        hull() {   // 45-degree lead-in at the top of the punch hole
            box(-top_guide_half, top_guide_half, -top_guide_half, top_guide_half, carriage_height - lead_in, carriage_height - lead_in + 0.01);
            box(-top_guide_half - lead_in - 0.01, top_guide_half + lead_in + 0.01, -top_guide_half - lead_in - 0.01, top_guide_half + lead_in + 0.01,
                carriage_height + 0.01, carriage_height + 0.02);
        }
        for (side_word = [[-1, "ODD"], [1, "EVEN"]]) {   // front face: ODD; turned end for end: EVEN
            side = side_word[0]; word = side_word[1];
            engrave(word, side, label_height, -((len(word) - 1)*label_pitch + label_width)/2, label_top);
            y_inner = side*(rail_width/2 - tick_depth); y_outer = side*(rail_width/2 + 1);
            box(-tick_width/2, tick_width/2, min(y_inner, y_outer), max(y_inner, y_outer), 0, tick_top);   // punch-center tick
        }
    }
}

module sled() {   // tag center at the origin, tag top toward +y, bench-block side at z = 0
    difference() {
        box(-sled_width/2, sled_width/2, sled_bottom_y, sled_top_y, 0, sled_thickness);
        translate([0, 0, -1]) cylinder(r = tag_rad + tag_pocket_clearance, h = sled_thickness + 2, $fn = 120);   // finer than $fn: the tag fits it closely
        for (y = notch_y, side = [-1, 1]) v_prism(side*sled_width/2, side, notch_depth, y, -1, sled_thickness + 1);
        for (groove = [0:grip_groove_count-1]) let (groove_y = sled_bottom_y + grip_groove_start + grip_groove_pitch*groove)
            box(-grip_groove_length/2, grip_groove_length/2, groove_y, groove_y + grip_groove_width,
                sled_thickness - grip_groove_depth, sled_thickness + 1);
    }
    // tab over the hole margin, with the pin pointing down to the bench block
    box(-tab_width/2, tab_width/2, tag_rad - tab_reach, tag_rad + tag_pocket_clearance + tab_overlap,
        tag_thickness + tab_clearance, sled_thickness);
    translate([0, pin_y, 0]) {
        translate([0, 0, pin_tip_chamfer]) cylinder(d = pin_dia, h = tag_thickness + tab_clearance - pin_tip_chamfer);
        cylinder(d1 = pin_dia - 2*pin_tip_chamfer, d2 = pin_dia, h = pin_tip_chamfer);   // chamfered tip
    }
}

module tag() {
    difference() {
        cylinder(r = tag_rad, h = tag_thickness, $fn = 120);
        translate([0, pin_y, -1]) cylinder(d = tag_hole_diameter, h = 3);
    }
}

// ---- print orientation (carriage and sled flipped onto their flat faces) ----
module carriage_print() { translate([0, 0, carriage_height]) rotate([180, 0, 0]) carriage(); }
module sled_print()     { translate([0, 0, sled_thickness]) rotate([180, 0, 0]) sled(); }

if (part == "base") base();
else if (part == "carriage") carriage_print();
else if (part == "sled") sled_print();
else if (part == "assembly") {
    color("lightgray") base();
    color("orange") translate([0, 0, rail_top]) carriage();
    translate([0, -row_y[0], 0]) { color("royalblue") sled(); color("silver") tag(); }
}
else {
    base();
    translate([base_length/2 + carriage_width/2 + 6, 0, 0]) carriage_print();
    translate([0, foot_length/2 + (sled_top_y - sled_bottom_y)/2 + 6, 0])
        translate([0, (sled_top_y + sled_bottom_y)/2, 0]) sled_print();
}
