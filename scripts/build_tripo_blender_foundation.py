import bpy
import math
import os
import sys
from mathutils import Vector


source_blend, output_blend, output_glb = sys.argv[sys.argv.index("--") + 1 : sys.argv.index("--") + 4]
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(source_blend))

mesh = bpy.data.objects["Marmalade_Tripo20K"]
bpy.context.view_layer.objects.active = mesh
mesh.select_set(True)
# Tripo Studio compensates for its generated mesh axes in its own viewer. The
# downloaded GLB stores Marmalade sideways (Y-up). Convert to Blender Z-up
# before creating or binding any bones so the rest pose and web export agree.
mesh.rotation_euler = (0.0, math.radians(-90.0), 0.0)
# Its generated origin is also displaced from the visual volume. These measured
# offsets put the paw plane at Z=0 and center the head-to-tail span on the guide.
mesh.location = (0.0, 0.470360, 0.487915)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
coordinate_bounds = tuple(
    (min(vertex.co[axis] for vertex in mesh.data.vertices), max(vertex.co[axis] for vertex in mesh.data.vertices))
    for axis in range(3)
)
print(f"MESH_COORDINATE_BOUNDS={coordinate_bounds}")

armature_data = bpy.data.armatures.new("Marmalade_TripoRig_Armature")
armature = bpy.data.objects.new("Marmalade_TripoRig", armature_data)
bpy.context.collection.objects.link(armature)
armature.show_in_front = True
armature_data.display_type = "BBONE"

bpy.context.view_layer.objects.active = armature
armature.select_set(True)
mesh.select_set(False)
bpy.ops.object.mode_set(mode="EDIT")


def add_bone(name, head, tail, parent=None, deform=True, connected=False):
    bone = armature.data.edit_bones.new(name)
    bone.head = head
    bone.tail = tail
    bone.use_deform = deform
    radius = 0.15 if name in {"pelvis", "spine", "chest", "neck", "head"} else 0.085
    if name.startswith("tail"):
        radius = 0.075
    bone.head_radius = radius
    bone.tail_radius = radius * 0.85
    bone.envelope_distance = radius * 0.75
    if parent:
        bone.parent = armature.data.edit_bones[parent]
        bone.use_connect = connected
    return bone


add_bone("root", (0, 0, 0.03), (0, 0, 0.20), deform=False)
add_bone("pelvis", (0, 0.17, 0.42), (0, 0.04, 0.50), "root")
add_bone("spine", (0, 0.04, 0.50), (0, -0.13, 0.57), "pelvis", connected=True)
add_bone("chest", (0, -0.13, 0.57), (0, -0.25, 0.64), "spine", connected=True)
add_bone("neck", (0, -0.25, 0.64), (0, -0.30, 0.72), "chest", connected=True)
add_bone("head", (0, -0.30, 0.72), (0, -0.30, 0.88), "neck", connected=True)
add_bone("ear.L", (0.13, -0.30, 0.82), (0.18, -0.30, 0.96), "head")
add_bone("ear.R", (-0.13, -0.30, 0.82), (-0.18, -0.30, 0.96), "head")

for side, x in (("L", 0.16), ("R", -0.16)):
    add_bone(f"front_upper.{side}", (x, -0.20, 0.56), (x, -0.23, 0.34), "chest")
    add_bone(f"front_lower.{side}", (x, -0.23, 0.34), (x, -0.25, 0.13), f"front_upper.{side}", connected=True)
    add_bone(f"front_paw.{side}", (x, -0.25, 0.13), (x, -0.33, 0.06), f"front_lower.{side}", connected=True)
    add_bone(f"rear_upper.{side}", (x, 0.19, 0.50), (x, 0.27, 0.31), "pelvis")
    add_bone(f"rear_lower.{side}", (x, 0.27, 0.31), (x, 0.23, 0.13), f"rear_upper.{side}", connected=True)
    add_bone(f"rear_paw.{side}", (x, 0.23, 0.13), (x, 0.13, 0.06), f"rear_lower.{side}", connected=True)

tail_points = (
    (0, 0.29, 0.52),
    (0, 0.43, 0.59),
    (0, 0.52, 0.70),
    (0, 0.55, 0.82),
    (0, 0.51, 0.92),
    (0, 0.43, 0.96),
)
for index in range(len(tail_points) - 1):
    add_bone(
        f"tail.{index + 1:02d}",
        tail_points[index],
        tail_points[index + 1],
        "pelvis" if index == 0 else f"tail.{index:02d}",
        connected=index > 0,
    )

bpy.ops.object.mode_set(mode="OBJECT")

# The Tripo retopology is one fused fur shell. Blender's automatic heat solver
# rejects it and envelope binding previously left ~45% of the mesh on a pelvis
# fallback, which is why only one rear leg visibly moved in the browser. Build
# complete, deterministic weights from the authored guide instead. Every
# vertex receives a valid influence and every limb chain receives geometry.
mesh.parent = armature
mesh.matrix_parent_inverse = armature.matrix_world.inverted()
mesh.vertex_groups.clear()
for modifier in list(mesh.modifiers):
    if modifier.type == "ARMATURE":
        mesh.modifiers.remove(modifier)
armature_modifier = mesh.modifiers.new(name="Marmalade Tripo Rig", type="ARMATURE")
armature_modifier.object = armature
armature_modifier.use_deform_preserve_volume = True

deform_bones = {bone.name: bone for bone in armature.data.bones if bone.use_deform}
groups = {name: mesh.vertex_groups.new(name=name) for name in deform_bones}


def segment_distance(point, bone_name):
    bone = deform_bones[bone_name]
    start = bone.head_local
    end = bone.tail_local
    span = end - start
    amount = max(0.0, min(1.0, (point - start).dot(span) / max(span.length_squared, 1e-8)))
    return (point - (start + span * amount)).length


def assign_nearest(vertex, candidates, maximum=2, power=2.6):
    ranked = sorted((segment_distance(vertex.co, name), name) for name in candidates)[:maximum]
    weighted = [(1.0 / ((distance + 0.025) ** power), name) for distance, name in ranked]
    total = sum(weight for weight, _ in weighted)
    for weight, name in weighted:
        groups[name].add([vertex.index], weight / total, "REPLACE")


torso_chain = ("pelvis", "spine", "chest", "neck", "head")
tail_chain = tuple(f"tail.{index:02d}" for index in range(1, 6))
rigid_head_vertices = 0
for vertex in mesh.data.vertices:
    point = vertex.co
    # Preserve the painted eyes, muzzle and forehead as a single facial mass.
    if (point.y < -0.34 and point.z > 0.34) or (point.y < -0.20 and point.z > 0.60):
        groups["head"].add([vertex.index], 1.0, "REPLACE")
        rigid_head_vertices += 1
        continue

    # Ear tips can twitch without pulling the neighbouring eye surface.
    if point.y < -0.18 and point.z > 0.79 and abs(point.x) > 0.07:
        ear = "ear.L" if point.x >= 0 else "ear.R"
        assign_nearest(vertex, ("head", ear), maximum=2, power=3.2)
        continue

    # The raised tail is spatially distinct from the rump above this boundary.
    if point.y > 0.285 and point.z > 0.50:
        assign_nearest(vertex, tail_chain + ("pelvis",), maximum=2, power=3.0)
        continue

    # Split the four leg volumes by side and fore/aft position. Include the
    # relevant body anchor only at the shoulder/hip for a smooth fused-shell
    # transition; lower legs and paws remain strongly articulated.
    if point.z < 0.59 and abs(point.x) > 0.045:
        side = "L" if point.x >= 0 else "R"
        region = "front" if point.y < -0.035 else "rear"
        anchor = "chest" if region == "front" else "pelvis"
        limb = tuple(f"{region}_{part}.{side}" for part in ("upper", "lower", "paw"))
        if point.z < 0.19:
            candidates = (limb[2], limb[1])
        elif point.z < 0.37:
            candidates = (limb[1], limb[0])
        else:
            candidates = (limb[0], anchor)
        assign_nearest(vertex, candidates, maximum=2, power=3.1)
        continue

    assign_nearest(vertex, torso_chain, maximum=2, power=2.8)

group_counts = {
    group.name: sum(
        1
        for vertex in mesh.data.vertices
        if any(item.group == group.index and item.weight > 0.01 for item in vertex.groups)
    )
    for group in mesh.vertex_groups
}
print(f"RIGID_HEAD_VERTICES={rigid_head_vertices}")
print("WEIGHT_GROUP_COUNTS=" + ",".join(f"{name}:{count}" for name, count in group_counts.items()))


def reset_pose():
    for pose_bone in armature.pose.bones:
        pose_bone.rotation_mode = "XYZ"
        pose_bone.location = (0, 0, 0)
        pose_bone.rotation_euler = (0, 0, 0)
        pose_bone.scale = (1, 1, 1)


def key_pose(frame, transforms):
    bpy.context.scene.frame_set(frame)
    reset_pose()
    for name, values in transforms.items():
        pose_bone = armature.pose.bones[name]
        if "location" in values:
            pose_bone.location = values["location"]
        if "rotation" in values:
            pose_bone.rotation_euler = values["rotation"]
        if "scale" in values:
            pose_bone.scale = values["scale"]
    for pose_bone in armature.pose.bones:
        pose_bone.keyframe_insert("location", frame=frame, group=pose_bone.name)
        pose_bone.keyframe_insert("rotation_euler", frame=frame, group=pose_bone.name)
        pose_bone.keyframe_insert("scale", frame=frame, group=pose_bone.name)


def new_action(name, end_frame):
    reset_pose()
    action = bpy.data.actions.new(name)
    armature.animation_data_create()
    armature.animation_data.action = action
    action.frame_start = 1
    action.frame_end = end_frame
    return action


new_action("Marmalade_IdleBreathing_Tripo", 120)
for frame, lift, chest_pitch, head_pitch, tail in (
    (1, 0.000, 0.000, 0.000, 0.00),
    (30, 0.014, -0.040, 0.018, 0.11),
    (60, 0.000, 0.000, 0.000, 0.00),
    (90, 0.014, -0.040, 0.018, -0.11),
    (120, 0.000, 0.000, 0.000, 0.00),
):
    key_pose(frame, {
        "root": {"location": (0, 0, lift)},
        "chest": {"rotation": (chest_pitch, 0, 0)},
        "head": {"rotation": (head_pitch, 0, 0)},
        "tail.01": {"rotation": (0, tail, 0)},
        "tail.02": {"rotation": (0, tail * 0.7, 0)},
        "tail.03": {"rotation": (0, tail * 0.45, 0)},
    })

new_action("Marmalade_Peeking_Tripo", 72)
for frame, x, z, pitch, roll in (
    (1, -0.54, -0.34, 0.10, -0.08),
    (12, -0.46, -0.28, 0.08, -0.07),
    (28, -0.18, -0.08, -0.06, 0.04),
    (42, 0.02, 0.00, -0.02, 0.02),
    (72, 0.02, 0.00, 0.00, 0.00),
):
    key_pose(frame, {
        "root": {"location": (x, 0, z), "rotation": (0, 0, roll)},
        "head": {"rotation": (pitch, 0, -roll * 0.4)},
        "ear.L": {"rotation": (0, 0.05, 0)},
        "ear.R": {"rotation": (0, -0.05, 0)},
    })

new_action("Marmalade_LookingAround_Tripo", 120)
for frame, yaw, pitch in ((1, 0.0, 0.0), (25, 0.32, 0.02), (50, 0.32, 0.02), (75, -0.32, -0.02), (100, -0.32, -0.02), (120, 0.0, 0.0)):
    key_pose(frame, {
        # The fused Tripo face cannot safely take differential facial weights.
        # Turn the full hierarchy as one solid character for this checkpoint.
        "root": {"rotation": (0, yaw * 0.90, 0)},
        "head": {"rotation": (pitch, yaw * 0.16, 0)},
        "ear.L": {"rotation": (0, yaw * 0.09, 0)},
        "ear.R": {"rotation": (0, -yaw * 0.09, 0)},
        "tail.01": {"rotation": (0, -yaw * 0.34, 0)},
        "tail.02": {"rotation": (0, -yaw * 0.18, 0)},
    })

new_action("Marmalade_Walking_Tripo", 32)
walk_frames = (
    (1, 0.000, 0.50),
    (9, 0.020, 0.0),
    (17, 0.000, -0.50),
    (25, 0.020, 0.0),
    (32, 0.000, 0.50),
)
for frame, lift, swing in walk_frames:
    key_pose(frame, {
        "root": {"location": (0, 0, lift)},
        "pelvis": {"rotation": (0, -swing * 0.15, swing * 0.04)},
        "chest": {"rotation": (0, swing * 0.13, -swing * 0.03)},
        "head": {"rotation": (-abs(swing) * 0.035, -swing * 0.045, 0)},
        "front_upper.L": {"rotation": (swing, 0, 0)},
        "front_lower.L": {"rotation": (-max(swing, 0) * 0.72, 0, 0)},
        "front_paw.L": {"rotation": (max(swing, 0) * 0.22, 0, 0)},
        "front_upper.R": {"rotation": (-swing, 0, 0)},
        "front_lower.R": {"rotation": (min(swing, 0) * 0.72, 0, 0)},
        "front_paw.R": {"rotation": (-min(swing, 0) * 0.22, 0, 0)},
        "rear_upper.L": {"rotation": (-swing, 0, 0)},
        "rear_lower.L": {"rotation": (min(swing, 0) * 0.78, 0, 0)},
        "rear_paw.L": {"rotation": (-min(swing, 0) * 0.26, 0, 0)},
        "rear_upper.R": {"rotation": (swing, 0, 0)},
        "rear_lower.R": {"rotation": (-max(swing, 0) * 0.78, 0, 0)},
        "rear_paw.R": {"rotation": (max(swing, 0) * 0.26, 0, 0)},
        "tail.01": {"rotation": (0, -swing * 0.34, 0)},
        "tail.02": {"rotation": (0, -swing * 0.24, 0)},
        "tail.03": {"rotation": (0, -swing * 0.14, 0)},
    })

# Preserve all actions for glTF export and leave Idle active in Blender.
armature.animation_data.action = bpy.data.actions["Marmalade_IdleBreathing_Tripo"]
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 120
bpy.context.scene.frame_set(1)

mesh["identity_source"] = "Tripo 20K retopology"
mesh["rig_source"] = "Blender recovery quadruped"
armature["foundation_states"] = "Idle, Peeking, LookingAround, Walking"

output_blend = os.path.abspath(output_blend)
output_glb = os.path.abspath(output_glb)
os.makedirs(os.path.dirname(output_blend), exist_ok=True)
os.makedirs(os.path.dirname(output_glb), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=output_blend)

bpy.ops.object.select_all(action="DESELECT")
mesh.select_set(True)
armature.select_set(True)
bpy.context.view_layer.objects.active = armature
bpy.ops.export_scene.gltf(
    filepath=output_glb,
    export_format="GLB",
    use_selection=True,
    export_animations=True,
    export_animation_mode="ACTIONS",
    export_force_sampling=True,
    export_frame_step=1,
    export_skins=True,
    export_all_influences=False,
    export_image_format="AUTO",
    export_yup=True,
)

print(f"FOUNDATION_BLEND={output_blend}")
print(f"FOUNDATION_GLB={output_glb}")
