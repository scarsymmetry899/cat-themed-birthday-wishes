"""Build Marmalade's first region-aware corrective rig and weight pass.

The previous audit proved that bone heat and unconstrained proximity weighting
collapse the fused Tripo shoulder/belly and miss the tail tip. This script uses
anatomical-space masks plus local bone distances, and moves the tail chain onto
the actual curled-tail volume. It remains an audited candidate, not final skin.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector


SOURCE_MESH = "Marmalade_QuadBase_Candidate"
GUIDE_RIG = "Marmalade_RigGuide"
RIG_NAME = "Marmalade_ProductionRig_v01"
SKIN_NAME = "Marmalade_WeightedCandidate_v01"
ANGLE = math.radians(39.997320722)


TAIL_POINTS = [
    (0.285, 0.015, 0.455),
    (0.375, 0.005, 0.485),
    (0.470, 0.000, 0.540),
    (0.555, 0.000, 0.630),
    (0.600, 0.005, 0.735),
    (0.570, 0.010, 0.825),
    (0.500, 0.012, 0.855),
    (0.435, 0.012, 0.820),
    (0.405, 0.010, 0.750),
]


def clamp(value, minimum=0.0, maximum=1.0):
    return max(minimum, min(maximum, value))


def smoothstep(edge0, edge1, value):
    if edge0 == edge1:
        return float(value >= edge1)
    t = clamp((value - edge0) / (edge1 - edge0))
    return t * t * (3.0 - 2.0 * t)


def point_segment_distance(point, start, end):
    segment = end - start
    if segment.length_squared == 0.0:
        return (point - start).length
    factor = clamp((point - start).dot(segment) / segment.length_squared)
    return (point - (start + factor * segment)).length


def distance_weights(point, segments, count=3, exponent=4.0):
    nearest = sorted(
        ((point_segment_distance(point, start, end), name) for name, start, end in segments),
        key=lambda item: item[0],
    )[:count]
    raw = [(1.0 / max(distance, 0.010) ** exponent, name) for distance, name in nearest]
    total = sum(weight for weight, _ in raw)
    return {name: weight / total for weight, name in raw}


def mix_weights(target, source, factor):
    for name, weight in source.items():
        target[name] = target.get(name, 0.0) + weight * factor


def normalized(weights):
    cleaned = {name: max(0.0, weight) for name, weight in weights.items() if weight > 0.00001}
    total = sum(cleaned.values())
    return {name: weight / total for name, weight in cleaned.items()} if total else {}


def key_rotation(pose_bone, frame, xyz):
    pose_bone.rotation_mode = "XYZ"
    pose_bone.rotation_euler = xyz
    pose_bone.keyframe_insert("rotation_euler", frame=frame)


def main():
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if not args:
        raise RuntimeError("Pass output .blend path after --")
    output = Path(args[0]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    source = bpy.data.objects[SOURCE_MESH]
    guide = bpy.data.objects[GUIDE_RIG]
    old_rig = bpy.data.objects.get(RIG_NAME)
    if old_rig:
        bpy.data.objects.remove(old_rig, do_unlink=True)
    old_skin = bpy.data.objects.get(SKIN_NAME)
    if old_skin:
        bpy.data.objects.remove(old_skin, do_unlink=True)

    rig = guide.copy()
    rig.data = guide.data.copy()
    rig.name = RIG_NAME
    rig.data.name = f"{RIG_NAME}_Armature"
    rig["status"] = "region-aware corrective rig candidate"
    bpy.data.collections["20_RIG"].objects.link(rig)
    guide.hide_viewport = True
    guide.hide_render = True

    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    for index, (start, end) in enumerate(zip(TAIL_POINTS, TAIL_POINTS[1:]), start=1):
        bone = rig.data.edit_bones[f"DEF_tail_{index:02d}"]
        bone.head = start
        bone.tail = end
    bpy.ops.object.mode_set(mode="OBJECT")
    for bone in rig.data.bones:
        bone.use_deform = bone.name.startswith("DEF_")

    skin = source.copy()
    skin.data = source.data.copy()
    skin.name = SKIN_NAME
    skin.data.name = f"{SKIN_NAME}_Mesh"
    skin["status"] = "corrective weighting candidate; deformation acceptance required"
    bpy.data.collections["30_EXPORT"].objects.link(skin)
    source.hide_viewport = True
    source.hide_render = True

    skin.parent = rig
    skin.matrix_parent_inverse = rig.matrix_world.inverted()
    modifier = skin.modifiers.new("Marmalade_Armature", "ARMATURE")
    modifier.object = rig
    modifier.use_deform_preserve_volume = True

    groups = {
        bone.name: skin.vertex_groups.new(name=bone.name)
        for bone in rig.data.bones
        if bone.use_deform
    }
    bone_segments = {
        bone.name: (Vector(bone.head_local), Vector(bone.tail_local))
        for bone in rig.data.bones
        if bone.use_deform
    }
    body_names = ["DEF_pelvis", "DEF_spine_01", "DEF_spine_02", "DEF_chest", "DEF_neck"]
    head_names = ["DEF_neck", "DEF_head", "DEF_jaw"]
    tail_names = [f"DEF_tail_{index:02d}" for index in range(1, 9)]
    inverse_axis = Matrix.Rotation(-ANGLE, 4, "Z")

    for vertex in skin.data.vertices:
        world = skin.matrix_world @ vertex.co
        point = inverse_axis @ world
        weights = {}

        tail_mask = smoothstep(0.31, 0.41, point.x) * smoothstep(0.31, 0.43, point.z)
        tail_mask *= 1.0 - 0.65 * smoothstep(0.11, 0.19, abs(point.y))

        head_mask = (1.0 - smoothstep(-0.31, -0.22, point.x)) * smoothstep(0.48, 0.61, point.z)

        front_region = 1.0 - smoothstep(-0.16, -0.08, point.x)
        front_vertical = 1.0 - smoothstep(0.29, 0.49, point.z)
        front_leg_mask = front_region * front_vertical * (1.0 - head_mask)

        rear_region = smoothstep(0.09, 0.17, point.x) * (1.0 - smoothstep(0.34, 0.43, point.x))
        rear_vertical = 1.0 - smoothstep(0.27, 0.46, point.z)
        rear_leg_mask = rear_region * rear_vertical

        side = "L" if point.y < 0.0 else "R"
        front_names = [f"DEF_front_upper.{side}", f"DEF_front_lower.{side}", f"DEF_front_paw.{side}"]
        rear_names = [f"DEF_rear_thigh.{side}", f"DEF_rear_lower.{side}", f"DEF_rear_paw.{side}"]

        body_factor = max(0.0, 1.0 - max(tail_mask, head_mask, front_leg_mask, rear_leg_mask))
        if body_factor > 0.0:
            segments = [(name, *bone_segments[name]) for name in body_names]
            mix_weights(weights, distance_weights(point, segments, count=2), body_factor)
        if head_mask > 0.0:
            segments = [(name, *bone_segments[name]) for name in head_names]
            mix_weights(weights, distance_weights(point, segments, count=2), head_mask)
        if front_leg_mask > 0.0:
            segments = [(name, *bone_segments[name]) for name in front_names]
            mix_weights(weights, distance_weights(point, segments, count=2), front_leg_mask)
        if rear_leg_mask > 0.0:
            segments = [(name, *bone_segments[name]) for name in rear_names]
            mix_weights(weights, distance_weights(point, segments, count=2), rear_leg_mask)
        if tail_mask > 0.0:
            segments = [(name, *bone_segments[name]) for name in tail_names]
            mix_weights(weights, distance_weights(point, segments, count=3), tail_mask)

        weights = normalized(weights)
        for name, weight in weights.items():
            groups[name].add([vertex.index], weight, "REPLACE")

    action = bpy.data.actions.new("AUDIT_CorrectiveJointRange")
    rig.animation_data_create()
    rig.animation_data.action = action
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 60
    animated = [
        "DEF_front_upper.L", "DEF_front_upper.R", "DEF_front_lower.L", "DEF_front_lower.R",
        "DEF_rear_thigh.L", "DEF_rear_thigh.R", "DEF_rear_lower.L", "DEF_rear_lower.R",
        "DEF_neck", "DEF_head",
    ] + tail_names
    for name in animated:
        key_rotation(rig.pose.bones[name], 1, (0.0, 0.0, 0.0))
        key_rotation(rig.pose.bones[name], 60, (0.0, 0.0, 0.0))

    key_rotation(rig.pose.bones["DEF_front_upper.L"], 12, (0.0, math.radians(13), 0.0))
    key_rotation(rig.pose.bones["DEF_front_upper.R"], 12, (0.0, math.radians(-13), 0.0))
    key_rotation(rig.pose.bones["DEF_front_lower.L"], 12, (0.0, math.radians(-17), 0.0))
    key_rotation(rig.pose.bones["DEF_front_lower.R"], 12, (0.0, math.radians(17), 0.0))
    key_rotation(rig.pose.bones["DEF_rear_thigh.L"], 24, (0.0, math.radians(-15), 0.0))
    key_rotation(rig.pose.bones["DEF_rear_thigh.R"], 24, (0.0, math.radians(15), 0.0))
    key_rotation(rig.pose.bones["DEF_rear_lower.L"], 24, (0.0, math.radians(19), 0.0))
    key_rotation(rig.pose.bones["DEF_rear_lower.R"], 24, (0.0, math.radians(-19), 0.0))
    key_rotation(rig.pose.bones["DEF_neck"], 36, (math.radians(5), math.radians(-6), math.radians(4)))
    key_rotation(rig.pose.bones["DEF_head"], 36, (math.radians(-4), math.radians(8), math.radians(-5)))
    for index, name in enumerate(tail_names, start=1):
        amount = math.radians(4.5 * math.sin(index * 0.9))
        key_rotation(rig.pose.bones[name], 48, (amount * 0.25, amount, amount * 0.18))

    group_counts = {name: 0 for name in groups}
    index_to_name = {group.index: group.name for group in skin.vertex_groups}
    for vertex in skin.data.vertices:
        for assignment in vertex.groups:
            if assignment.weight > 0.0001:
                group_counts[index_to_name[assignment.group]] += 1
    empty = [name for name, count in group_counts.items() if count == 0]
    skin["empty_weight_groups"] = ", ".join(empty)
    scene.frame_set(1)
    scene["marmalade_pipeline_stage"] = "corrective-rig-audit-v01"
    scene["marmalade_next_gate"] = "visual deformation review and manual loop/weight correction"
    bpy.ops.wm.save_as_mainfile(filepath=str(output), check_existing=False)
    print({"output": str(output), "empty_weight_groups": empty, "tail_points": TAIL_POINTS})


if __name__ == "__main__":
    main()
