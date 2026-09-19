"""Build IK-planted walk and trot proof actions for Marmalade."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


RIG_NAME = "Marmalade_ProductionRig_v01"
COLLECTION = "25_GAIT_CONTROLS"
PAWS = {
    "front.L": "DEF_front_lower.L",
    "front.R": "DEF_front_lower.R",
    "rear.L": "DEF_rear_lower.L",
    "rear.R": "DEF_rear_lower.R",
}
PAW_ORIENTATION_BONES = {
    "front.L": "DEF_front_paw.L",
    "front.R": "DEF_front_paw.R",
    "rear.L": "DEF_rear_paw.L",
    "rear.R": "DEF_rear_paw.R",
}


def smooth01(value):
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def point_segment_distance(point, start, end):
    segment = end - start
    length_squared = segment.length_squared
    if length_squared <= 1.0e-10:
        return (point - start).length
    t = max(0.0, min(1.0, (point - start).dot(segment) / length_squared))
    return (point - (start + segment * t)).length


def rigidify_paw_weights(rig):
    body = bpy.data.objects.get("Marmalade_WeightedCandidate_v01")
    if body is None:
        raise RuntimeError("Missing weighted Marmalade body")
    paw_names = tuple(PAW_ORIENTATION_BONES.values())
    deform_groups = [group for group in body.vertex_groups if group.name.startswith("DEF_")]
    paw_segments = {}
    for name in paw_names:
        bone = rig.data.bones[name]
        paw_segments[name] = (rig.matrix_world @ bone.head_local, rig.matrix_world @ bone.tail_local)

    assignments = {name: [] for name in paw_names}
    for vertex in body.data.vertices:
        point = body.matrix_world @ vertex.co
        if point.z > 0.175:
            continue
        nearest_name = None
        nearest_distance = 1.0e9
        for name, (start, end) in paw_segments.items():
            distance = point_segment_distance(point, start, end)
            if distance < nearest_distance:
                nearest_name = name
                nearest_distance = distance
        if nearest_name and nearest_distance < 0.082:
            for group in deform_groups:
                group.remove([vertex.index])
            assignments[nearest_name].append(vertex.index)
    for name, indices in assignments.items():
        if indices:
            body.vertex_groups[name].add(indices, 1.0, "REPLACE")
    body["paw_weight_strategy"] = "rigid islands below ankle; v01"
    return {name: len(indices) for name, indices in assignments.items()}


def animation_action(owner, name):
    owner.animation_data_create()
    old = bpy.data.actions.get(name)
    if old:
        if owner.animation_data.action == old:
            owner.animation_data.action = None
        bpy.data.actions.remove(old)
    action = bpy.data.actions.new(name)
    owner.animation_data.action = action
    return action


def clear_action(action):
    # Actions are recreated for each build, so no in-place channel deletion is
    # needed. This also works with Blender's layered Action API.
    return None


def set_linear(action):
    curves = []
    if hasattr(action, "fcurves"):
        curves.extend(action.fcurves)
    else:
        for layer in action.layers:
            for strip in layer.strips:
                for slot in action.slots:
                    bag = strip.channelbag(slot, ensure=False)
                    if bag:
                        curves.extend(bag.fcurves)
    for curve in curves:
        for point in curve.keyframe_points:
            point.interpolation = "LINEAR"


def get_or_create_controls(rig):
    collection = bpy.data.collections.get(COLLECTION)
    if collection is None:
        collection = bpy.data.collections.new(COLLECTION)
        bpy.context.scene.collection.children.link(collection)
    controls = {}
    # Remove the earlier three-bone proof constraints before installing the
    # volume-preserving two-bone chains.
    for name in ("DEF_front_paw.L", "DEF_front_paw.R", "DEF_rear_paw.L", "DEF_rear_paw.R"):
        old = rig.pose.bones[name].constraints.get("Marmalade_PawPlant_IK")
        if old:
            rig.pose.bones[name].constraints.remove(old)
    for label, bone_name in PAWS.items():
        name = f"CTRL_paw_ik.{label}"
        control = bpy.data.objects.get(name)
        if control is None:
            control = bpy.data.objects.new(name, None)
            collection.objects.link(control)
        control.empty_display_type = "SPHERE"
        control.empty_display_size = 0.026
        rest_tip = rig.matrix_world @ rig.data.bones[bone_name].tail_local
        control.location = rest_tip
        rest_paw_matrix = rig.matrix_world @ rig.data.bones[PAW_ORIENTATION_BONES[label]].matrix_local
        control.rotation_mode = "QUATERNION"
        control.rotation_quaternion = rest_paw_matrix.to_quaternion()
        control["paw"] = label
        controls[label] = control

        pose_bone = rig.pose.bones[bone_name]
        constraint = pose_bone.constraints.get("Marmalade_PawPlant_IK")
        if constraint is None:
            constraint = pose_bone.constraints.new("IK")
            constraint.name = "Marmalade_PawPlant_IK"
        constraint.target = control
        constraint.chain_count = 2
        constraint.use_stretch = False
        constraint.influence = 1.0

        paw_pose = rig.pose.bones[PAW_ORIENTATION_BONES[label]]
        orient = paw_pose.constraints.get("Marmalade_PawWorldOrientation")
        if orient is None:
            orient = paw_pose.constraints.new("COPY_ROTATION")
            orient.name = "Marmalade_PawWorldOrientation"
        orient.target = control
        orient.owner_space = "WORLD"
        orient.target_space = "WORLD"
        orient.mix_mode = "REPLACE"
        orient.influence = 1.0
    return controls


def paw_position(base, forward_world, t, phase_offset, stride, stance_ratio, lift):
    cycle = t + phase_offset
    step = math.floor(cycle)
    phase = cycle - step
    if phase < stance_ratio:
        progress = 0.0
        height = 0.0
    else:
        swing = (phase - stance_ratio) / (1.0 - stance_ratio)
        progress = smooth01(swing)
        height = lift * math.sin(math.pi * swing)
    position = base + forward_world * ((step + progress) * stride)
    position.z = base.z + height
    return position


def key_bone(bone, frame, location=None, rotation=None):
    bone.rotation_mode = "XYZ"
    if location is not None:
        bone.location = location
        bone.keyframe_insert("location", frame=frame)
    if rotation is not None:
        bone.rotation_euler = rotation
        bone.keyframe_insert("rotation_euler", frame=frame)


def build_gait(rig, controls, gait, frame_count, stride, stance_ratio, lift, phases, trot=False):
    rig_action = animation_action(rig, f"Marmalade_{gait}_Body_v01")
    clear_action(rig_action)
    target_actions = {}
    bases = {
        label: rig.matrix_world @ rig.data.bones[PAWS[label]].tail_local
        for label in controls
    }
    forward_world = (rig.matrix_world.to_3x3() @ Vector((-1.0, 0.0, 0.0))).normalized()
    for label, control in controls.items():
        action = animation_action(control, f"Marmalade_{gait}_Paw_{label}_v01")
        clear_action(action)
        target_actions[label] = action

    # Restore the rig action after creating the target actions.
    rig.animation_data.action = rig_action
    root = rig.pose.bones["CTRL_root"]
    pelvis = rig.pose.bones["DEF_pelvis"]
    chest = rig.pose.bones["DEF_chest"]
    head = rig.pose.bones["DEF_head"]
    tail_bones = [rig.pose.bones[f"DEF_tail_{index:02d}"] for index in range(1, 9)]

    for frame in range(1, frame_count + 2):
        t = (frame - 1) / frame_count
        cadence = 2.0 if trot else 1.0
        motion_scale = 0.55 if trot else 1.0
        wave = math.sin(math.tau * cadence * t)
        double_wave = math.sin(math.tau * 2.0 * cadence * t)
        root_location = Vector((-stride * t, 0.0, (0.003 if trot else 0.0035) * (1.0 - math.cos(math.tau * 2.0 * t))))
        key_bone(root, frame, location=root_location, rotation=(0.0, 0.0, 0.0))
        key_bone(pelvis, frame, rotation=(0.018 * wave * motion_scale, 0.040 * double_wave * motion_scale, 0.024 * wave * motion_scale))
        key_bone(chest, frame, rotation=(-0.012 * wave * motion_scale, -0.030 * double_wave * motion_scale, -0.018 * wave * motion_scale))
        key_bone(head, frame, rotation=(0.0, -0.012 * double_wave * motion_scale, 0.006 * wave * motion_scale))
        for index, bone in enumerate(tail_bones, start=1):
            falloff = 0.55 + index * 0.075
            key_bone(
                bone,
                frame,
                rotation=(0.0, -0.016 * double_wave * falloff, -0.035 * math.sin(math.tau * t - index * 0.18) * falloff),
            )

        for label, control in controls.items():
            control.animation_data.action = target_actions[label]
            control.location = paw_position(bases[label], forward_world, t, phases[label], stride, stance_ratio, lift)
            control.keyframe_insert("location", frame=frame)
        rig.animation_data.action = rig_action

    set_linear(rig_action)
    for action in target_actions.values():
        set_linear(action)
    return rig_action, target_actions


def main():
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if not args:
        raise RuntimeError("Pass output .blend after --")
    output = Path(args[0]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    scene = bpy.context.scene
    scene.frame_set(1)
    rig = bpy.data.objects.get(RIG_NAME)
    if rig is None:
        raise RuntimeError(f"Missing rig: {RIG_NAME}")
    paw_weight_counts = rigidify_paw_weights(rig)
    controls = get_or_create_controls(rig)

    walk_phases = {"rear.L": 0.00, "front.L": 0.25, "rear.R": 0.50, "front.R": 0.75}
    trot_phases = {"rear.L": 0.00, "front.R": 0.00, "rear.R": 0.50, "front.L": 0.50}
    walk_action, walk_targets = build_gait(rig, controls, "WalkContact", 32, 0.11, 0.62, 0.038, walk_phases)
    build_gait(rig, controls, "TrotContact", 24, 0.11, 0.52, 0.042, trot_phases, trot=True)

    # Leave the walk proof active and store the gait contract on the rig.
    rig.animation_data.action = walk_action
    for label, control in controls.items():
        control.animation_data.action = walk_targets[label]
    rig["gait_active"] = "WalkContact"
    rig["gait_walk_frames"] = 32
    rig["gait_trot_frames"] = 24
    rig["gait_contact_system"] = "world-space paw IK; no stretch"
    scene.frame_start = 1
    scene.frame_end = 33
    scene.frame_set(1)
    scene["marmalade_pipeline_stage"] = "contact-gait-proof"
    scene["marmalade_next_gate"] = "render contact sheet and measure stance drift"
    bpy.ops.wm.save_as_mainfile(filepath=str(output), check_existing=False)
    print({"output": str(output), "walk": walk_action.name, "controls": list(controls), "rigid_paw_vertices": paw_weight_counts})


if __name__ == "__main__":
    main()
