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
mesh.location = (0.092586, 0.470360, 0.487915)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

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

# Bind the preserved Tripo mesh to the new deform skeleton.
bpy.ops.object.select_all(action="DESELECT")
mesh.select_set(True)
armature.select_set(True)
bpy.context.view_layer.objects.active = armature
bpy.ops.object.parent_set(type="ARMATURE_AUTO")

armature_modifiers = [modifier for modifier in mesh.modifiers if modifier.type == "ARMATURE"]
weighted_memberships = sum(len(vertex.groups) for vertex in mesh.data.vertices)
if not armature_modifiers or weighted_memberships == 0:
    mesh.parent = None
    mesh.vertex_groups.clear()
    for modifier in list(mesh.modifiers):
        if modifier.type == "ARMATURE":
            mesh.modifiers.remove(modifier)
    bpy.ops.object.select_all(action="DESELECT")
    mesh.select_set(True)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.parent_set(type="ARMATURE_ENVELOPE")

# Envelope binding can leave isolated fur-shell vertices without any group.
# Those vertices visibly stay behind during whole-character moves (notably the
# peek). Give only the genuinely unweighted remainder a pelvis fallback; the
# authored limb/head/tail envelope weights remain untouched.
pelvis_group = mesh.vertex_groups.get("pelvis") or mesh.vertex_groups.new(name="pelvis")
unweighted_vertices = [
    vertex.index
    for vertex in mesh.data.vertices
    if not any(group.weight > 1e-6 for group in vertex.groups)
]
if unweighted_vertices:
    pelvis_group.add(unweighted_vertices, 1.0, "REPLACE")
print(f"UNWEIGHTED_FALLBACK={len(unweighted_vertices)}")

# The Tripo face is a fused, pre-painted volume rather than separable eyes and
# lids. Mixed heat weights visibly shear the eyes/muzzle when the head turns.
# Keep the whole facial mass rigid on the head bone so identity is preserved.
head_vertices = [
    vertex.index
    for vertex in mesh.data.vertices
    if (vertex.co.y < -0.34 and vertex.co.z > 0.34)
    or (vertex.co.y < -0.20 and vertex.co.z > 0.58)
]
for group in mesh.vertex_groups:
    group.remove(head_vertices)
head_group = mesh.vertex_groups.get("head") or mesh.vertex_groups.new(name="head")
head_group.add(head_vertices, 1.0, "REPLACE")
print(f"RIGID_HEAD_VERTICES={len(head_vertices)}")


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
    (30, 0.008, -0.025, 0.012, 0.08),
    (60, 0.000, 0.000, 0.000, 0.00),
    (90, 0.008, -0.025, 0.012, -0.08),
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

new_action("Marmalade_Peeking_Tripo", 80)
for frame, z, pitch in ((1, -0.52, 0.12), (18, -0.38, 0.08), (38, -0.08, -0.04), (52, 0.0, 0.0), (80, 0.0, 0.0)):
    key_pose(frame, {
        "root": {"location": (0, 0, z)},
        "head": {"rotation": (pitch, 0, 0)},
        "ear.L": {"rotation": (0, 0.05, 0)},
        "ear.R": {"rotation": (0, -0.05, 0)},
    })

new_action("Marmalade_LookingAround_Tripo", 120)
for frame, yaw, pitch in ((1, 0.0, 0.0), (25, 0.32, 0.02), (50, 0.32, 0.02), (75, -0.32, -0.02), (100, -0.32, -0.02), (120, 0.0, 0.0)):
    key_pose(frame, {
        # The fused Tripo face cannot safely take differential facial weights.
        # Turn the full hierarchy as one solid character for this checkpoint.
        "root": {"rotation": (0, yaw * 0.38, 0)},
        "tail.01": {"rotation": (0, -yaw * 0.18, 0)},
    })

new_action("Marmalade_Walking_Tripo", 32)
walk_frames = (
    (1, 0.0, 0.34),
    (9, 0.010, 0.0),
    (17, 0.0, -0.34),
    (25, 0.010, 0.0),
    (32, 0.0, 0.34),
)
for frame, lift, swing in walk_frames:
    key_pose(frame, {
        "root": {"location": (0, 0, lift)},
        "pelvis": {"rotation": (0, -swing * 0.08, 0)},
        "chest": {"rotation": (0, swing * 0.07, 0)},
        "head": {"rotation": (-abs(swing) * 0.025, -swing * 0.025, 0)},
        "front_upper.L": {"rotation": (swing, 0, 0)},
        "front_lower.L": {"rotation": (-max(swing, 0) * 0.50, 0, 0)},
        "front_upper.R": {"rotation": (-swing, 0, 0)},
        "front_lower.R": {"rotation": (min(swing, 0) * 0.50, 0, 0)},
        "rear_upper.L": {"rotation": (-swing, 0, 0)},
        "rear_lower.L": {"rotation": (min(swing, 0) * 0.58, 0, 0)},
        "rear_upper.R": {"rotation": (swing, 0, 0)},
        "rear_lower.R": {"rotation": (-max(swing, 0) * 0.58, 0, 0)},
        "tail.01": {"rotation": (0, -swing * 0.25, 0)},
        "tail.02": {"rotation": (0, -swing * 0.18, 0)},
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
