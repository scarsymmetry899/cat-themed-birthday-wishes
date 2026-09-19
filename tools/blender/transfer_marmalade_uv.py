"""Transfer Tripo UVs/material to the corrective Marmalade mesh by projection."""

from __future__ import annotations

import sys
from pathlib import Path

import bpy


SOURCE = "Marmalade_TextureProjection_Source"
TARGET = "Marmalade_WeightedCandidate_v01"


def main():
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if not args:
        raise RuntimeError("Pass output .blend path after --")
    output = Path(args[0]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    source = bpy.data.objects[SOURCE]
    target = bpy.data.objects[TARGET]
    if not source.data.uv_layers:
        raise RuntimeError("High-resolution source has no UV layer")
    while target.data.uv_layers:
        target.data.uv_layers.remove(target.data.uv_layers[0])
    target.data.uv_layers.new(name=source.data.uv_layers.active.name)

    modifier = target.modifiers.new("Transfer_Source_UV", "DATA_TRANSFER")
    modifier.object = source
    modifier.use_object_transform = True
    modifier.use_loop_data = True
    modifier.data_types_loops = {"UV"}
    modifier.loop_mapping = "POLYINTERP_NEAREST"
    modifier.layers_uv_select_src = source.data.uv_layers.active.name
    modifier.layers_uv_select_dst = target.data.uv_layers.active.name
    modifier.mix_mode = "REPLACE"
    modifier.mix_factor = 1.0
    modifier.use_max_distance = True
    modifier.max_distance = 0.025

    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    target.select_set(True)
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=modifier.name)

    target.data.materials.clear()
    for material in source.data.materials:
        target.data.materials.append(material)
    target["uv_source"] = SOURCE
    target["uv_transfer_method"] = "POLYINTERP_NEAREST, max distance 0.025m"
    target["texture_status"] = "source projection; canonical markings repaint pending"
    bpy.context.scene["marmalade_pipeline_stage"] = "textured-corrective-audit-v01"
    bpy.context.scene["marmalade_next_gate"] = "side/back marking repaint and deformation correction"
    bpy.ops.wm.save_as_mainfile(filepath=str(output), check_existing=False)
    print({
        "output": str(output),
        "uv_layers": [layer.name for layer in target.data.uv_layers],
        "materials": [material.name for material in target.data.materials],
    })


if __name__ == "__main__":
    main()
