"""Render neutral orthographic marking views of the weighted Marmalade candidate."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


ANGLE = math.radians(39.997320722)
FORWARD = Vector((-math.cos(ANGLE), -math.sin(ANGLE), 0.0))
SIDE = Vector((-math.sin(ANGLE), math.cos(ANGLE), 0.0))


def aim_at(obj, target):
    obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()


def add_area(name, location, energy, size, target):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = energy
    data.shape = "DISK"
    data.size = size
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = location
    aim_at(obj, target)
    return obj


def main():
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if not args:
        raise RuntimeError("Pass output directory after --")
    out = Path(args[0]).resolve()
    out.mkdir(parents=True, exist_ok=True)

    scene = bpy.context.scene
    scene.frame_set(1)
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 720
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False

    if scene.world is None:
        scene.world = bpy.data.worlds.new("Marmalade_Marking_World")
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (0.055, 0.040, 0.025, 1.0)
    background.inputs["Strength"].default_value = 0.18

    candidate = bpy.data.objects.get("Marmalade_WeightedCandidate_v01")
    if candidate is None:
        raise RuntimeError("Marmalade_WeightedCandidate_v01 is missing")
    for obj in bpy.data.objects:
        if obj.type in {"MESH", "CURVE"}:
            obj.hide_render = obj != candidate
    candidate.hide_render = False

    for obj in list(bpy.data.objects):
        if obj.type in {"LIGHT", "CAMERA"} and obj.name.startswith("Marmalade_Marking_"):
            bpy.data.objects.remove(obj, do_unlink=True)

    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = candidate.evaluated_get(depsgraph)
    corners = [evaluated.matrix_world @ Vector(corner) for corner in evaluated.bound_box]
    low = Vector((min(v.x for v in corners), min(v.y for v in corners), min(v.z for v in corners)))
    high = Vector((max(v.x for v in corners), max(v.y for v in corners), max(v.z for v in corners)))
    target = (low + high) * 0.5
    extent = max(high.x - low.x, high.y - low.y, high.z - low.z)

    camera_data = bpy.data.cameras.new("Marmalade_Marking_Camera")
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = extent * 1.18
    camera = bpy.data.objects.new("Marmalade_Marking_Camera", camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera

    add_area("Marmalade_Marking_Key", target + FORWARD * 1.3 + SIDE * 0.8 + Vector((0, 0, 1.4)), 95, 1.6, target)
    add_area("Marmalade_Marking_Fill", target - SIDE * 1.3 + Vector((0, 0, 0.8)), 45, 1.8, target)
    add_area("Marmalade_Marking_Rim", target - FORWARD * 1.1 + Vector((0, 0, 1.3)), 70, 1.2, target)

    views = [
        ("front", FORWARD),
        ("left-side", SIDE),
        ("back", -FORWARD),
        ("right-side", -SIDE),
        ("three-quarter", (FORWARD + SIDE).normalized()),
    ]
    for name, direction in views:
        camera.location = target + direction * (extent * 2.4) + Vector((0, 0, extent * 0.04))
        aim_at(camera, target)
        scene.render.filepath = str(out / f"{name}.png")
        bpy.ops.render.render(write_still=True)

    print({"output": str(out), "views": [name for name, _ in views], "ortho_scale": camera_data.ortho_scale})


if __name__ == "__main__":
    main()
