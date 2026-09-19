"""Render compact CPU/Cycles review images for the current Marmalade blend."""

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
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 16
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 640
    scene.render.resolution_y = 640
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False

    if scene.world is None:
        scene.world = bpy.data.worlds.new("Marmalade_Review_World")
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (0.035, 0.027, 0.020, 1.0)
    background.inputs["Strength"].default_value = 0.32

    for name in ("Marmalade_HighRes_Source", "Marmalade_Retopo_Proxy", "Marmalade_RigGuide"):
        obj = bpy.data.objects.get(name)
        if obj:
            obj.hide_render = True
    candidate = bpy.data.objects.get("Marmalade_QuadBase_Candidate")
    if candidate:
        candidate.hide_render = False

    camera_data = bpy.data.cameras.new("Marmalade_Review_Camera")
    camera_data.type = "ORTHO"
    camera = bpy.data.objects.new("Marmalade_Review_Camera", camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera

    target = Vector((-0.10, -0.08, 0.49))
    add_area("Marmalade_Review_Key", target + Vector((-1.2, -1.1, 1.7)), 700, 1.3, target)
    add_area("Marmalade_Review_Fill", target + Vector((1.1, 0.4, 1.0)), 420, 1.5, target)
    add_area("Marmalade_Review_Rim", target + Vector((0.7, 1.0, 1.5)), 550, 1.0, target)

    views = [
        ("body-side", target + SIDE * 2.2 + Vector((0, 0, 0.14)), target, 1.15),
        ("body-front", target + FORWARD * 2.2 + Vector((0, 0, 0.10)), target, 1.15),
        (
            "face-front",
            Vector((-0.34, -0.28, 0.74)) + FORWARD * 1.2,
            Vector((-0.34, -0.28, 0.74)),
            0.48,
        ),
    ]
    for name, location, look_at, scale in views:
        camera.location = location
        camera_data.ortho_scale = scale
        aim_at(camera, look_at)
        scene.render.filepath = str(out / f"{name}.png")
        bpy.ops.render.render(write_still=True)

    face_root = bpy.data.objects.get("Marmalade_FaceRoot")
    if face_root:
        face_camera = views[-1]
        camera.location = face_camera[1]
        camera_data.ortho_scale = face_camera[3]
        aim_at(camera, face_camera[2])
        tests = {
            "face-gaze-left": {"lookX": -1.0, "lookY": 0.0, "blink": 0.0, "focus": 0.0},
            "face-gaze-right": {"lookX": 1.0, "lookY": 0.0, "blink": 0.0, "focus": 0.0},
            "face-blink": {"lookX": 0.0, "lookY": 0.0, "blink": 1.0, "focus": 0.0},
            "face-focus": {"lookX": 0.0, "lookY": 0.0, "blink": 0.0, "focus": 1.0},
        }
        for name, values in tests.items():
            for key, value in values.items():
                face_root[key] = value
            face_root.update_tag(refresh={"OBJECT"})
            scene.frame_set(scene.frame_current + 1)
            bpy.context.evaluated_depsgraph_get().update()
            scene.render.filepath = str(out / f"{name}.png")
            bpy.ops.render.render(write_still=True)
        for key in ("lookX", "lookY", "blink", "focus"):
            face_root[key] = 0.0

    print(f"Rendered Marmalade review images to {out}")


if __name__ == "__main__":
    main()
