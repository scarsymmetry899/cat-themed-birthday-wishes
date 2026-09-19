"""Bind a disposable copy of the quad candidate for deformation auditing.

This file is never the production skin. It exposes weighting and joint-loop
failures before the final mesh is approved.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


MESH_SOURCE = "Marmalade_QuadBase_Candidate"
RIG_NAME = "Marmalade_RigGuide"
AUDIT_MESH = "Marmalade_DeformAudit"


def key_rotation(pose_bone, frame, xyz):
    pose_bone.rotation_mode = "XYZ"
    pose_bone.rotation_euler = xyz
    pose_bone.keyframe_insert("rotation_euler", frame=frame)


def point_segment_distance(point: Vector, start: Vector, end: Vector) -> float:
    segment = end - start
    denominator = segment.length_squared
    if denominator == 0.0:
        return (point - start).length
    factor = max(0.0, min(1.0, (point - start).dot(segment) / denominator))
    return (point - (start + factor * segment)).length


def assign_proximity_weights(mesh_obj, rig):
    """Deterministic fallback when Blender bone heat cannot solve the source."""
    for group in list(mesh_obj.vertex_groups):
        mesh_obj.vertex_groups.remove(group)
    bones = [bone for bone in rig.data.bones if bone.use_deform]
    groups = {bone.name: mesh_obj.vertex_groups.new(name=bone.name) for bone in bones}
    segments = [
        (bone.name, rig.matrix_world @ bone.head_local, rig.matrix_world @ bone.tail_local)
        for bone in bones
    ]
    for vertex in mesh_obj.data.vertices:
        point = mesh_obj.matrix_world @ vertex.co
        distances = sorted(
            ((point_segment_distance(point, start, end), name) for name, start, end in segments),
            key=lambda item: item[0],
        )[:4]
        raw = [(1.0 / max(distance, 0.008) ** 4, name) for distance, name in distances]
        total = sum(weight for weight, _ in raw)
        for weight, name in raw:
            groups[name].add([vertex.index], weight / total, "REPLACE")


def main():
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if not args:
        raise RuntimeError("Pass output .blend path after --")
    output = Path(args[0]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    source = bpy.data.objects[MESH_SOURCE]
    rig = bpy.data.objects[RIG_NAME]
    for bone in rig.data.bones:
        bone.use_deform = bone.name.startswith("DEF_")

    old = bpy.data.objects.get(AUDIT_MESH)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    audit = source.copy()
    audit.data = source.data.copy()
    audit.name = AUDIT_MESH
    audit.data.name = f"{AUDIT_MESH}_Mesh"
    audit["status"] = "DISPOSABLE deformation audit; not production skin"
    bpy.data.collections["30_EXPORT"].objects.link(audit)

    source.hide_viewport = True
    source.hide_render = True
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    audit.select_set(True)
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.parent_set(type="ARMATURE_AUTO", keep_transform=True)
    # The Tripo-derived surface regularly defeats bone heat because its limbs
    # and torso are fused in a posed stance. Use an explicit deterministic
    # proximity fallback for this audit file; final weights remain hand-tuned.
    assign_proximity_weights(audit, rig)

    action = bpy.data.actions.new("AUDIT_JointRange")
    rig.animation_data_create()
    rig.animation_data.action = action
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 60

    animated = [
        "DEF_front_upper.L", "DEF_front_upper.R", "DEF_front_lower.L", "DEF_front_lower.R",
        "DEF_rear_thigh.L", "DEF_rear_thigh.R", "DEF_rear_lower.L", "DEF_rear_lower.R",
        "DEF_neck", "DEF_head",
    ] + [f"DEF_tail_{index:02d}" for index in range(1, 9)]
    for name in animated:
        key_rotation(rig.pose.bones[name], 1, (0.0, 0.0, 0.0))
        key_rotation(rig.pose.bones[name], 60, (0.0, 0.0, 0.0))

    key_rotation(rig.pose.bones["DEF_front_upper.L"], 12, (0.0, math.radians(18), 0.0))
    key_rotation(rig.pose.bones["DEF_front_upper.R"], 12, (0.0, math.radians(-18), 0.0))
    key_rotation(rig.pose.bones["DEF_front_lower.L"], 12, (0.0, math.radians(-22), 0.0))
    key_rotation(rig.pose.bones["DEF_front_lower.R"], 12, (0.0, math.radians(22), 0.0))

    key_rotation(rig.pose.bones["DEF_rear_thigh.L"], 24, (0.0, math.radians(-20), 0.0))
    key_rotation(rig.pose.bones["DEF_rear_thigh.R"], 24, (0.0, math.radians(20), 0.0))
    key_rotation(rig.pose.bones["DEF_rear_lower.L"], 24, (0.0, math.radians(25), 0.0))
    key_rotation(rig.pose.bones["DEF_rear_lower.R"], 24, (0.0, math.radians(-25), 0.0))

    key_rotation(rig.pose.bones["DEF_neck"], 36, (math.radians(7), math.radians(-8), math.radians(5)))
    key_rotation(rig.pose.bones["DEF_head"], 36, (math.radians(-5), math.radians(10), math.radians(-6)))
    for index in range(1, 9):
        angle = math.radians(7 if index % 2 else -7)
        key_rotation(rig.pose.bones[f"DEF_tail_{index:02d}"], 48, (angle * 0.35, angle, 0.0))

    scene.frame_set(1)
    scene["marmalade_pipeline_stage"] = "deformation-audit"
    scene["marmalade_audit_frames"] = "1 neutral; 12 front legs; 24 rear legs; 36 neck/head; 48 tail"
    group_weights = {group.name: 0 for group in audit.vertex_groups}
    index_to_name = {group.index: group.name for group in audit.vertex_groups}
    for vertex in audit.data.vertices:
        for assignment in vertex.groups:
            if assignment.weight > 0.0001:
                group_weights[index_to_name[assignment.group]] += 1
    empty_groups = [name for name, count in group_weights.items() if count == 0]
    audit["audit_empty_weight_groups"] = ", ".join(empty_groups)
    bpy.ops.wm.save_as_mainfile(filepath=str(output), check_existing=False)
    print({
        "output": str(output),
        "vertex_groups": len(audit.vertex_groups),
        "empty_weight_groups": empty_groups,
        "action": action.name,
    })


if __name__ == "__main__":
    main()
