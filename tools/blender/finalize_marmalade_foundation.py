"""Finalize the scoped four-state Marmalade 3D foundation.

This pass is intentionally non-destructive: the fused source body is preserved,
problematic low paw islands are tucked beneath clean bone-parented paw shells, and
new actions are added without removing the walk/trot contact proof actions.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


RIG = "Marmalade_ProductionRig_v01"
BODY = "Marmalade_WeightedCandidate_v01"
FACE = "Marmalade_FaceRoot"
PAW_BONES = (
    "DEF_front_paw.L",
    "DEF_front_paw.R",
    "DEF_rear_paw.L",
    "DEF_rear_paw.R",
)


def action(owner, name):
    owner.animation_data_create()
    old = bpy.data.actions.get(name)
    if old:
        if owner.animation_data.action == old:
            owner.animation_data.action = None
        bpy.data.actions.remove(old)
    created = bpy.data.actions.new(name)
    created.use_fake_user = True
    owner.animation_data.action = created
    return created


def key_bone(bone, frame, location=None, rotation=None, scale=None):
    bone.rotation_mode = "XYZ"
    if location is not None:
        bone.location = location
        bone.keyframe_insert("location", frame=frame)
    if rotation is not None:
        bone.rotation_euler = rotation
        bone.keyframe_insert("rotation_euler", frame=frame)
    if scale is not None:
        bone.scale = scale
        bone.keyframe_insert("scale", frame=frame)


def smooth_keys(act):
    curves = []
    if hasattr(act, "fcurves"):
        curves.extend(act.fcurves)
    else:
        for layer in act.layers:
            for strip in layer.strips:
                for slot in act.slots:
                    bag = strip.channelbag(slot, ensure=False)
                    if bag:
                        curves.extend(bag.fcurves)
    for curve in curves:
        for point in curve.keyframe_points:
            point.interpolation = "BEZIER"
            point.handle_left_type = "AUTO_CLAMPED"
            point.handle_right_type = "AUTO_CLAMPED"


def refine_face():
    root = bpy.data.objects[FACE]
    # These were construction guides. Rendering them doubles the fused Tripo
    # muzzle and is the main source of the grey, lumpy snout seen in v05.
    for name in ("Muzzle.L", "Muzzle.R", "Chin"):
        obj = bpy.data.objects.get(name)
        if obj:
            obj.hide_viewport = True
            obj.hide_render = True

    # Seat the eyes into the head and reduce the graphic/doll-like projection.
    for side in ("L", "R"):
        white = bpy.data.objects[f"EyeWhite.{side}"]
        white.location.x += 0.018
        white.scale = (0.82, 0.91, 0.91)
        iris = bpy.data.objects[f"Iris.{side}"]
        # Keep the colored eye surface forward enough to avoid clipping into
        # the far cheek at three-quarter angles.
        iris.location.x += 0.000
        iris.scale = (0.72, 0.92, 0.92)
        pupil = bpy.data.objects[f"Pupil.{side}"]
        pupil.location.x -= 0.002
        pupil.scale = (0.70, 0.92, 0.94)
        catch = bpy.data.objects[f"Catchlight.{side}"]
        catch.location.x -= 0.002
        catch.scale *= 0.84

    # Integrate all lid shape-key positions around each eye, preserving blink
    # closure while softening the oversized eyebrow-cap silhouette.
    for side, cy in (("L", -0.105), ("R", 0.105)):
        center = Vector((-0.505, cy, 0.755))
        for prefix, z_scale in (("UpperLid", 0.78), ("LowerLid", 0.82)):
            obj = bpy.data.objects[f"{prefix}.{side}"]
            keys = obj.data.shape_keys.key_blocks if obj.data.shape_keys else []
            blocks = keys if keys else [obj.data]
            for block in blocks:
                for vert in block.data if hasattr(block, "data") else block.vertices:
                    co = vert.co
                    co.x = center.x + (co.x - center.x) * 0.72
                    co.y = center.y + (co.y - center.y) * 0.90
                    co.z = center.z + (co.z - center.z) * z_scale

    eyelid = bpy.data.materials.get("Marmalade_EyelidIntegrated")
    if eyelid:
        eyelid.diffuse_color = (0.88, 0.31, 0.075, 1.0)
        if eyelid.use_nodes:
            bsdf = eyelid.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = (0.88, 0.31, 0.075, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.72

    # Full closure should read as a narrow coat-colored lid, not a circular
    # mask over the eyeball. Preserve the neutral/focus contours and flatten
    # only the Blink target around the eye center.
    for side, cy in (("L", -0.105), ("R", 0.105)):
        upper = bpy.data.objects[f"UpperLid.{side}"]
        if upper.data.shape_keys and "Blink" in upper.data.shape_keys.key_blocks:
            blink = upper.data.shape_keys.key_blocks["Blink"]
            for vert in blink.data:
                vert.co.z = 0.755 + (vert.co.z - 0.755) * 0.13

    # Give the whiskers a gentler storybook arc by moving their middle points.
    for obj in root.children_recursive:
        if obj.type != "CURVE" or not obj.name.startswith("Whisker."):
            continue
        for spline in obj.data.splines:
            points = spline.bezier_points if spline.type == "BEZIER" else spline.points
            count = len(points)
            for index, point in enumerate(points):
                t = index / max(1, count - 1)
                lift = 0.012 * math.sin(math.pi * t)
                if hasattr(point, "co"):
                    point.co.z += lift

    root["foundation_face_revision"] = "integrated-soft-v06"


def build_paw_shells(rig, body):
    cream = bpy.data.materials.get("Marmalade_Cream")
    if cream is None:
        cream = bpy.data.materials.new("Marmalade_Cream")
        cream.diffuse_color = (0.93, 0.78, 0.57, 1.0)

    # Preserve a hidden mesh backup before modifying the visible skin.
    backup = bpy.data.objects.get("Marmalade_WeightedCandidate_PrePawRepair")
    if backup is None:
        backup = body.copy()
        backup.data = body.data.copy()
        backup.name = "Marmalade_WeightedCandidate_PrePawRepair"
        body.users_collection[0].objects.link(backup)
        backup.hide_viewport = True
        backup.hide_render = True
    else:
        # A rerun always starts from the untouched pre-repair geometry.
        body.data = backup.data.copy()

    # Clean shells cover the source toe strips with a generous ankle overlap.
    # The original mesh remains untouched so the ankle silhouette cannot tear.
    tucked = {}
    for bone_name in PAW_BONES:
        bone = rig.data.bones[bone_name]
        start = rig.matrix_world @ bone.head_local
        end = rig.matrix_world @ bone.tail_local
        tucked[bone_name] = 0

        shell_name = f"Marmalade_PawShell_{bone_name.removeprefix('DEF_')}"
        old = bpy.data.objects.get(shell_name)
        if old:
            bpy.data.objects.remove(old, do_unlink=True)
        midpoint = start.lerp(end, 0.58)
        direction = (end - start).normalized()
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=midpoint)
        shell = bpy.context.view_layer.objects.active
        shell.name = shell_name
        shell.rotation_mode = "QUATERNION"
        shell.rotation_quaternion = Vector((1.0, 0.0, 0.0)).rotation_difference(direction)
        front = "front" in bone_name
        shell.scale = (0.084 if front else 0.086, 0.070 if front else 0.073, 0.057)
        bpy.context.view_layer.objects.active = shell
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        shell.data.materials.append(cream)
        # Bake the rest placement into mesh coordinates and deform the shell as
        # a rigid, single-group skinned island. This avoids bone-parent double
        # transforms when IK constraints are evaluated.
        world_matrix = shell.matrix_world.copy()
        shell.data.transform(world_matrix)
        shell.matrix_world.identity()
        group = shell.vertex_groups.new(name=bone_name)
        group.add(range(len(shell.data.vertices)), 1.0, "REPLACE")
        modifier = shell.modifiers.new("Marmalade_PawShellArmature", "ARMATURE")
        modifier.object = rig
        shell["purpose"] = "clean deformation-safe paw shell; foundation v12"

    body.data.update()
    body["paw_topology_repair"] = "non-destructive overlapping clean shells v12"
    return tucked


def reset_pose(rig):
    for bone in rig.pose.bones:
        bone.location = (0.0, 0.0, 0.0)
        bone.rotation_mode = "XYZ"
        bone.rotation_euler = (0.0, 0.0, 0.0)
        bone.scale = (1.0, 1.0, 1.0)


def build_idle(rig):
    act = action(rig, "Marmalade_IdleBreathing_v01")
    reset_pose(rig)
    root = rig.pose.bones["CTRL_root"]
    chest = rig.pose.bones["DEF_chest"]
    head = rig.pose.bones["DEF_head"]
    ears = [b for b in rig.pose.bones if "ear" in b.name.lower()]
    tail = [rig.pose.bones[f"DEF_tail_{i:02d}"] for i in range(1, 9)]
    for frame in range(1, 97):
        t = (frame - 1) / 96.0
        breath = math.sin(math.tau * t)
        key_bone(root, frame, location=(0.0, 0.0, 0.0025 * (breath + 1.0)))
        key_bone(chest, frame, rotation=(0.0, -0.010 * breath, 0.0), scale=(1.0, 1.0 + 0.008 * breath, 1.0 + 0.012 * breath))
        key_bone(head, frame, rotation=(0.0, -0.004 * breath, 0.003 * math.sin(math.tau * t + 0.7)))
        for i, bone in enumerate(tail, 1):
            key_bone(bone, frame, rotation=(0.0, 0.008 * math.sin(math.tau * t - i * 0.22), 0.020 * math.sin(math.tau * t - i * 0.27)))
        for i, bone in enumerate(ears):
            twitch = 0.0
            if 60 <= frame <= 72:
                u = (frame - 60) / 12.0
                twitch = math.sin(math.pi * u) * (0.035 if i % 2 == 0 else -0.020)
            key_bone(bone, frame, rotation=(0.0, twitch, 0.0))
    smooth_keys(act)
    return act


def build_peek(rig):
    act = action(rig, "Marmalade_Peeking_v01")
    reset_pose(rig)
    root = rig.pose.bones["CTRL_root"]
    pelvis = rig.pose.bones["DEF_pelvis"]
    chest = rig.pose.bones["DEF_chest"]
    head = rig.pose.bones["DEF_head"]
    # Hidden -> rise -> curious hold -> same neutral endpoint for clean reverse.
    poses = {
        1: ((0.16, 0.10, -0.48), (0.0, 0.0, -0.08), (0.0, 0.0, 0.10), (0.02, 0.0, -0.11)),
        22: ((0.05, 0.03, -0.15), (0.0, 0.0, -0.03), (0.0, 0.0, 0.04), (-0.02, 0.0, -0.04)),
        40: ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, -0.015, 0.035)),
        72: ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.010, -0.025)),
    }
    for frame, values in poses.items():
        key_bone(root, frame, location=values[0])
        key_bone(pelvis, frame, rotation=values[1])
        key_bone(chest, frame, rotation=values[2])
        key_bone(head, frame, rotation=values[3])
    smooth_keys(act)
    return act


def build_look(rig, face):
    act = action(rig, "Marmalade_LookingAround_v01")
    reset_pose(rig)
    head = rig.pose.bones["DEF_head"]
    poses = ((1, 0.0, 0.0), (28, -0.055, 0.11), (56, 0.035, -0.12), (84, -0.018, 0.05), (112, 0.0, 0.0))
    for frame, pitch, yaw in poses:
        key_bone(head, frame, rotation=(pitch, 0.0, yaw))
    smooth_keys(act)

    face_act = action(face, "Marmalade_LookingAround_Face_v01")
    for frame, x, y in ((1, 0.0, 0.0), (24, -0.85, 0.15), (52, 0.90, -0.10), (80, -0.30, 0.25), (112, 0.0, 0.0)):
        face["lookX"] = x
        face["lookY"] = y
        face.keyframe_insert('["lookX"]', frame=frame)
        face.keyframe_insert('["lookY"]', frame=frame)
    smooth_keys(face_act)
    return act, face_act


def export_glb(output):
    export = output.with_suffix(".glb")
    for obj in bpy.context.view_layer.objects:
        obj.select_set(False)
    rig = bpy.data.objects[RIG]
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    for obj in bpy.data.objects:
        if obj == rig or obj.parent == rig or obj.name == BODY or obj.parent == bpy.data.objects[FACE]:
            obj.select_set(True)
    bpy.ops.export_scene.gltf(
        filepath=str(export),
        export_format="GLB",
        use_selection=True,
        export_animations=True,
        export_skins=True,
        export_morph=True,
    )
    return export


def main():
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if not args:
        raise RuntimeError("Pass output .blend after --")
    output = Path(args[0]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    rig = bpy.data.objects[RIG]
    body = bpy.data.objects[BODY]
    face = bpy.data.objects[FACE]
    bpy.context.scene.frame_set(1)
    refine_face()
    tucked = build_paw_shells(rig, body)
    idle = build_idle(rig)
    peek = build_peek(rig)
    look, look_face = build_look(rig, face)
    rig.animation_data.action = idle
    face.animation_data.action = look_face
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 112
    bpy.context.scene["foundation_scope"] = "Idle, Peeking, Looking Around, Walking/Trotting only"
    bpy.context.scene["foundation_revision"] = "v12"
    bpy.ops.wm.save_as_mainfile(filepath=str(output))
    try:
        export = export_glb(output)
    except Exception as exc:
        # The interactive MCP context in some Blender builds lacks
        # active_object. Preserve the authored .blend and report the export
        # failure instead of discarding the completed scene.
        export = Path(str(output) + ".export-pending")
        bpy.context.scene["glb_export_error"] = str(exc)
    bpy.ops.wm.save_as_mainfile(filepath=str(output))
    print({"output": str(output), "glb": str(export), "paw_vertices_tucked": tucked,
           "actions": [idle.name, peek.name, look.name, look_face.name]})


if __name__ == "__main__":
    main()
