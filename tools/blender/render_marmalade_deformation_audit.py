"""Render the disposable Marmalade joint-range audit at its authored frames."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


ANGLE = math.radians(39.997320722)
SIDE = Vector((-math.sin(ANGLE), math.cos(ANGLE), 0.0))


def aim_at(obj, target):
    obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()


def main():
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if not args:
        raise RuntimeError("Pass output directory after --")
    out = Path(args[0]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 12
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 640
    scene.render.resolution_y = 640
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    if scene.world is None:
        scene.world = bpy.data.worlds.new("Audit_World")
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.025, 0.020, 0.017, 1.0)
    bg.inputs["Strength"].default_value = 0.34

    for collection_name in ("00_SOURCE_HIGHRES", "10_RETOPOLOGY", "15_FACE_PARTS", "20_RIG"):
        collection = bpy.data.collections.get(collection_name)
        if collection:
            for obj in collection.all_objects:
                if obj is not None:
                    obj.hide_render = True
    audit = bpy.data.objects["Marmalade_DeformAudit"]
    audit.hide_render = False

    target = Vector((-0.08, -0.07, 0.48))
    camera_data = bpy.data.cameras.new("Audit_Camera")
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = 1.18
    camera = bpy.data.objects.new("Audit_Camera", camera_data)
    scene.collection.objects.link(camera)
    camera.location = target + SIDE * 2.2 + Vector((0.0, 0.0, 0.10))
    aim_at(camera, target)
    scene.camera = camera

    for name, offset, energy, size in (
        ("Audit_Key", Vector((-1.2, -1.1, 1.7)), 650, 1.3),
        ("Audit_Fill", Vector((1.1, 0.4, 1.0)), 380, 1.5),
        ("Audit_Rim", Vector((0.7, 1.0, 1.5)), 500, 1.0),
    ):
        data = bpy.data.lights.new(name, "AREA")
        data.energy = energy
        data.size = size
        light = bpy.data.objects.new(name, data)
        scene.collection.objects.link(light)
        light.location = target + offset
        aim_at(light, target)

    frames = {1: "neutral", 12: "front-leg-range", 24: "rear-leg-range", 36: "head-neck-range", 48: "tail-range"}
    for frame, name in frames.items():
        scene.frame_set(frame)
        scene.render.filepath = str(out / f"{frame:02d}-{name}.png")
        bpy.ops.render.render(write_still=True)
    print(f"Rendered deformation audit to {out}")


if __name__ == "__main__":
    main()
