"""Render side-view contact sequences for Marmalade walk and trot proofs."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


ANGLE = math.radians(39.997320722)
FORWARD = Vector((-math.cos(ANGLE), -math.sin(ANGLE), 0.0))
SIDE = Vector((-math.sin(ANGLE), math.cos(ANGLE), 0.0))
LABELS = ("front.L", "front.R", "rear.L", "rear.R")


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


def activate_gait(rig, gait):
    rig.animation_data.action = bpy.data.actions[f"Marmalade_{gait}_Body_v01"]
    for label in LABELS:
        control = bpy.data.objects[f"CTRL_paw_ik.{label}"]
        control.animation_data.action = bpy.data.actions[f"Marmalade_{gait}_Paw_{label}_v01"]


def main():
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if not args:
        raise RuntimeError("Pass output directory after --")
    out = Path(args[0]).resolve()
    out.mkdir(parents=True, exist_ok=True)

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 520
    scene.render.resolution_y = 520
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (0.050, 0.037, 0.024, 1.0)
    background.inputs["Strength"].default_value = 0.16

    for obj in list(bpy.data.objects):
        if obj.name.startswith("Marmalade_GaitReview_"):
            bpy.data.objects.remove(obj, do_unlink=True)

    body = bpy.data.objects["Marmalade_WeightedCandidate_v01"]
    face_root = bpy.data.objects["Marmalade_FaceRoot"]
    rig = bpy.data.objects["Marmalade_ProductionRig_v01"]
    allowed = {body.name}
    allowed.update(child.name for child in face_root.children_recursive if not child.name.startswith("PartyHat"))
    for obj in bpy.data.objects:
        if obj.type in {"MESH", "CURVE"}:
            obj.hide_render = obj.name not in allowed
    for key in ("lookX", "lookY", "blink", "focus"):
        face_root[key] = 0.0

    # Matte contact plane.
    bpy.ops.mesh.primitive_plane_add(size=3.0, location=(0.0, 0.0, -0.004))
    floor = bpy.context.object
    floor.name = "Marmalade_GaitReview_Floor"
    floor_mat = bpy.data.materials.get("Marmalade_GaitReview_FloorMat") or bpy.data.materials.new("Marmalade_GaitReview_FloorMat")
    floor_mat.diffuse_color = (0.10, 0.075, 0.045, 1.0)
    floor.data.materials.append(floor_mat)

    camera_data = bpy.data.cameras.new("Marmalade_GaitReview_Camera")
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = 1.18
    camera = bpy.data.objects.new("Marmalade_GaitReview_Camera", camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    target = Vector((-0.09, -0.08, 0.48)) + FORWARD * 0.07
    camera.location = target + SIDE * 2.2 + Vector((0, 0, 0.05))
    aim_at(camera, target)
    add_area("Marmalade_GaitReview_Key", target + SIDE * 0.8 + FORWARD * 0.8 + Vector((0, 0, 1.3)), 100, 1.5, target)
    add_area("Marmalade_GaitReview_Fill", target - SIDE * 0.8 + Vector((0, 0, 0.7)), 50, 1.5, target)
    add_area("Marmalade_GaitReview_Rim", target - FORWARD * 0.9 + Vector((0, 0, 1.2)), 65, 1.1, target)

    sequences = {
        "walk": ("WalkContact", [1, 5, 9, 13, 17, 21, 25, 29, 33]),
        "trot": ("TrotContact", [1, 4, 7, 10, 13, 16, 19, 22, 25]),
    }
    for prefix, (gait, frames) in sequences.items():
        activate_gait(rig, gait)
        for frame in frames:
            scene.frame_set(frame)
            bpy.context.evaluated_depsgraph_get().update()
            scene.render.filepath = str(out / f"{prefix}-{frame:02d}.png")
            bpy.ops.render.render(write_still=True)

    activate_gait(rig, "WalkContact")
    scene.frame_set(1)
    print({"output": str(out), "walk_frames": sequences["walk"][1], "trot_frames": sequences["trot"][1]})


if __name__ == "__main__":
    main()
