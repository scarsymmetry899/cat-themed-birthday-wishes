"""Import the untouched Tripo Marmalade GLB into an isolated Blender source file.

Run with Blender in background mode. The script deliberately creates a fresh file so
an unrelated scene open in the interactive Blender session is never modified.
"""

from __future__ import annotations

import json
from pathlib import Path

import bpy
from mathutils import Vector


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_GLB = (
    REPO_ROOT
    / "assets"
    / "character"
    / "3d"
    / "source"
    / "marmalade-tripo-highdetail-v01.glb"
)
OUTPUT_BLEND = (
    REPO_ROOT
    / "assets"
    / "character"
    / "3d"
    / "blender"
    / "marmalade-source-audit-v01.blend"
)


def main() -> None:
    if not SOURCE_GLB.is_file():
        raise FileNotFoundError(SOURCE_GLB)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(SOURCE_GLB))

    scene = bpy.context.scene
    scene.name = "Marmalade_Source_Audit"
    mesh_objects = [obj for obj in scene.objects if obj.type == "MESH"]

    if len(mesh_objects) == 1:
        mesh_objects[0].name = "Marmalade_HighRes_Source"
        mesh_objects[0].data.name = "Marmalade_HighRes_Source_Mesh"

    bounds_min = Vector((float("inf"),) * 3)
    bounds_max = Vector((float("-inf"),) * 3)
    for obj in mesh_objects:
        for corner in obj.bound_box:
            world_corner = obj.matrix_world @ Vector(corner)
            for axis in range(3):
                bounds_min[axis] = min(bounds_min[axis], world_corner[axis])
                bounds_max[axis] = max(bounds_max[axis], world_corner[axis])

    OUTPUT_BLEND.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT_BLEND))

    summary = {
        "blend_file": str(OUTPUT_BLEND),
        "object_count": len(scene.objects),
        "mesh_count": len(mesh_objects),
        "total_vertices": sum(len(obj.data.vertices) for obj in mesh_objects),
        "total_edges": sum(len(obj.data.edges) for obj in mesh_objects),
        "total_faces": sum(len(obj.data.polygons) for obj in mesh_objects),
        "bounds_min": [round(value, 6) for value in bounds_min],
        "bounds_max": [round(value, 6) for value in bounds_max],
        "dimensions": [
            round(value, 6) for value in (bounds_max - bounds_min)
        ],
        "meshes": [
            {
                "name": obj.name,
                "vertices": len(obj.data.vertices),
                "faces": len(obj.data.polygons),
                "materials": [
                    material.name if material else None
                    for material in obj.data.materials
                ],
                "uv_layers": [layer.name for layer in obj.data.uv_layers],
                "shape_keys": (
                    list(obj.data.shape_keys.key_blocks.keys())
                    if obj.data.shape_keys
                    else []
                ),
            }
            for obj in mesh_objects
        ],
        "materials": [material.name for material in bpy.data.materials],
        "images": [
            {
                "name": image.name,
                "size": list(image.size),
                "packed": bool(image.packed_file),
            }
            for image in bpy.data.images
        ],
        "armatures": [
            obj.name for obj in scene.objects if obj.type == "ARMATURE"
        ],
    }
    print("MARMALADE_AUDIT=" + json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
