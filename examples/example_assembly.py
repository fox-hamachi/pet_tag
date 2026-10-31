"""Stamp jig assembled with the example tag and punch, as one 3MF (units: mm) for importing into
CAD (Onshape, Fusion) or a slicer. Each part is a named, colored object in assembled position, with
row 1 under the punch: base, carriage on the rail, sled with the tag in its pocket, punch on the tag.
usage: python3 example_assembly.py [out_dir] [name=value ...]   (jig parameters as for stamp_jig.py)
"""
import os, sys, zipfile

sys.path[:0] = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")]
import stamp_jig as jig        # reads the name=value overrides from sys.argv
import example_parts as examples

sled_shift = (0, -jig.row_y[0], 0)   # row 1 under the punch, as in the stamp_jig.scad assembly view
parts = [   # (name, color, model)
    ("base", "#D9DCDF", jig.base()),
    ("carriage", "#F26B1D", jig.carriage().translate((0, 0, jig.rail_top))),
    ("sled", "#1F4FD8", jig.sled().translate(sled_shift)),
    ("tag", "#C0161B", examples.tag().translate(sled_shift)),
    ("punch", "#8A8D91", examples.punch("A").translate((0, 0, jig.tag_thickness))),
]

def object_xml(object_id, name, color_index, model):
    mesh = model.to_mesh()
    vertices = "".join(f'<vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>' for x, y, z in mesh.vert_properties[:, :3])
    triangles = "".join(f'<triangle v1="{v1}" v2="{v2}" v3="{v3}"/>' for v1, v2, v3 in mesh.tri_verts)
    return (f'<object id="{object_id}" type="model" name="{name}" pid="1" pindex="{color_index}">'
            f'<mesh><vertices>{vertices}</vertices><triangles>{triangles}</triangles></mesh></object>')

def write_3mf(path):
    colors = "".join(f'<base name="{name}" displaycolor="{color}"/>' for name, color, _ in parts)
    objects = "".join(object_xml(index + 2, name, index, model) for index, (name, _, model) in enumerate(parts))
    items = "".join(f'<item objectid="{index + 2}"/>' for index in range(len(parts)))
    model_xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                 '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
                 f'<resources><basematerials id="1">{colors}</basematerials>{objects}</resources>'
                 f'<build>{items}</build></model>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as package:
        package.writestr("[Content_Types].xml",
                         '<?xml version="1.0" encoding="UTF-8"?>\n'
                         '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                         '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                         '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
                         '</Types>')
        package.writestr("_rels/.rels",
                         '<?xml version="1.0" encoding="UTF-8"?>\n'
                         '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                         '<Relationship Target="/3D/3dmodel.model" Id="rel0" '
                         'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        package.writestr("3D/3dmodel.model", model_xml)
    print(f"{path}: {', '.join(name for name, _, _ in parts)}")

if __name__ == "__main__":
    out = jig.args[0] if jig.args else "."
    write_3mf(os.path.join(out, "example_assembly.3mf"))
