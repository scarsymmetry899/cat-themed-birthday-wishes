"""Create a UV-preserving lightweight source for texture projection."""

from __future__ import annotations

import sys
from pathlib import Path

import bpy


SOURCE = "Marmalade_HighRes_Source"
OUTPUT = "Marmalade_TextureProjection_Source"


def main():
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if not args:
        raise RuntimeError("Pass output .blend path after --")
    output_path = Path(args[0]).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    source = bpy.data.objects[SOURCE]
    old = bpy.data.objects.get(OUTPUT)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)

    projection = source.copy()
    projection.data = source.data.copy()
    projection.name = OUTPUT
    projection.data.name = f"{OUTPUT}_Mesh"
    projection.hide_viewport = True
    projection.hide_render = True
    bpy.data.collections["90_REFERENCE"].objects.link(projection)
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    projection.select_set(True)
    bpy.context.view_layer.objects.active = projection
    modifier = projection.modifiers.new("UV_Preserving_Decimate", "DECIMATE")
    modifier.decimate_type = "COLLAPSE"
    modifier.ratio = 0.055
    modifier.use_collapse_triangulate = True
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    projection["purpose"] = "UV/material projection source only"
    projection["source_faces"] = len(source.data.polygons)
    projection["projection_faces"] = len(projection.data.polygons)
    projection["uv_layers"] = ", ".join(layer.name for layer in projection.data.uv_layers)
    bpy.context.scene["marmalade_texture_projection_source"] = OUTPUT
    bpy.ops.wm.save_as_mainfile(filepath=str(output_path), check_existing=False)
    print({
        "output": str(output_path),
        "faces": len(projection.data.polygons),
        "uv_layers": [layer.name for layer in projection.data.uv_layers],
    })


if __name__ == "__main__":
    main()
