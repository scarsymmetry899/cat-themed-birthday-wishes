"""Render assembled Marmalade neutral, gaze, blink, and focus validation."""

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
    scene.world.use_nodes = True
    world = scene.world.node_tree.nodes.get("Background")
    world.inputs["Color"].default_value = (0.055, 0.040, 0.025, 1.0)
    world.inputs["Strength"].default_value = 0.18

    for obj in list(bpy.data.objects):
        if obj.type in {"LIGHT", "CAMERA"} and obj.name.startswith("Marmalade_FaceReview_"):
            bpy.data.objects.remove(obj, do_unlink=True)

    body = bpy.data.objects.get("Marmalade_WeightedCandidate_v01")
    root = bpy.data.objects.get("Marmalade_FaceRoot")
    if not body or not root:
        raise RuntimeError("Marked body or face root is missing")
    # Validation values must not be overridden by the Looking Around action.
    if root.animation_data:
        root.animation_data.action = None
    allowed = {body.name}
    allowed.update(child.name for child in root.children_recursive if not child.name.startswith("PartyHat"))
    for obj in bpy.data.objects:
        if obj.type in {"MESH", "CURVE"}:
            obj.hide_render = obj.name not in allowed

    camera_data = bpy.data.cameras.new("Marmalade_FaceReview_Camera")
    camera_data.type = "ORTHO"
    camera = bpy.data.objects.new("Marmalade_FaceReview_Camera", camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    target = Vector((-0.34, -0.285, 0.735))
    add_area("Marmalade_FaceReview_Key", target + FORWARD * 1.0 + SIDE * 0.7 + Vector((0, 0, 1.0)), 85, 1.2, target)
    add_area("Marmalade_FaceReview_Fill", target - SIDE * 1.0 + Vector((0, 0, 0.5)), 40, 1.4, target)
    add_area("Marmalade_FaceReview_Rim", target - FORWARD * 0.8 + Vector((0, 0, 0.9)), 55, 1.0, target)

    tests = {
        "neutral": {"lookX": 0.0, "lookY": 0.0, "blink": 0.0, "focus": 0.0},
        "gaze-left": {"lookX": -1.0, "lookY": 0.0, "blink": 0.0, "focus": 0.0},
        "gaze-right": {"lookX": 1.0, "lookY": 0.0, "blink": 0.0, "focus": 0.0},
        "blink-mid": {"lookX": 0.0, "lookY": 0.0, "blink": 0.5, "focus": 0.0},
        "blink-closed": {"lookX": 0.0, "lookY": 0.0, "blink": 1.0, "focus": 0.0},
        "focus": {"lookX": 0.0, "lookY": 0.0, "blink": 0.0, "focus": 1.0},
    }
    camera.location = target + FORWARD * 1.25 + Vector((0, 0, 0.035))
    camera_data.ortho_scale = 0.54
    aim_at(camera, target)
    for name, values in tests.items():
        for key, value in values.items():
            root[key] = value
        scene.frame_set(scene.frame_current + 1)
        bpy.context.evaluated_depsgraph_get().update()
        scene.render.filepath = str(out / f"{name}.png")
        bpy.ops.render.render(write_still=True)

    for key in ("lookX", "lookY", "blink", "focus"):
        root[key] = 0.0
    print({"output": str(out), "tests": list(tests)})


if __name__ == "__main__":
    main()
