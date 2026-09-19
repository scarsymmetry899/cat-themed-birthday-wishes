"""Create Marmalade's non-deforming production rig guide.

The guide establishes naming, hierarchy, pivots, and tail/limb joint counts. It
does not bind the proxy: final skinning must wait for deformation-friendly quad
topology and separate facial geometry.
"""

from __future__ import annotations

import sys
import math
from pathlib import Path

import bpy


RIG_NAME = "Marmalade_RigGuide"


def add_bone(arm, name, head, tail, parent=None, connected=False):
    bone = arm.edit_bones.new(name)
    bone.head = head
    bone.tail = tail
    bone.parent = parent
    bone.use_connect = bool(parent and connected)
    return bone


def main() -> None:
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if not args:
        raise RuntimeError("Pass output .blend path after --")
    output = Path(args[0]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    old = bpy.data.objects.get(RIG_NAME)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)

    rig_collection = bpy.data.collections.get("20_RIG")
    if rig_collection is None:
        rig_collection = bpy.data.collections.new("20_RIG")
        bpy.context.scene.collection.children.link(rig_collection)

    armature = bpy.data.armatures.new(f"{RIG_NAME}_Armature")
    rig = bpy.data.objects.new(RIG_NAME, armature)
    rig_collection.objects.link(rig)
    rig.show_in_front = True
    rig.display_type = "WIRE"
    # The Tripo source is posed diagonally in world XY; PCA of the proxy gives
    # a 39.997-degree longitudinal axis. Keep guide coordinates anatomical and
    # rotate the guide object to match that source orientation.
    rig.rotation_euler.z = math.radians(39.997320722)
    rig["purpose"] = "non-deforming joint and naming guide"
    rig["bind_status"] = "UNBOUND - final quad topology required"
    rig["foundation_scope"] = "Idle, Peeking, Looking, Walking/Trotting only"

    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")

    root = add_bone(armature, "CTRL_root", (0.02, 0.0, 0.03), (0.02, 0.0, 0.18))
    pelvis = add_bone(armature, "DEF_pelvis", (0.17, 0.0, 0.38), (0.09, 0.0, 0.48), root)
    spine_01 = add_bone(armature, "DEF_spine_01", (0.09, 0.0, 0.48), (-0.04, 0.0, 0.50), pelvis, True)
    spine_02 = add_bone(armature, "DEF_spine_02", (-0.04, 0.0, 0.50), (-0.18, 0.0, 0.54), spine_01, True)
    chest = add_bone(armature, "DEF_chest", (-0.18, 0.0, 0.54), (-0.27, 0.0, 0.61), spine_02, True)
    neck = add_bone(armature, "DEF_neck", (-0.27, 0.0, 0.61), (-0.34, 0.0, 0.69), chest, True)
    head = add_bone(armature, "DEF_head", (-0.34, 0.0, 0.69), (-0.38, 0.0, 0.84), neck, True)
    add_bone(armature, "DEF_jaw", (-0.40, 0.0, 0.69), (-0.48, 0.0, 0.66), head)

    # Independent facial controls: the generated source has these painted/fused,
    # but the production redraw will use separate eye globes and eyelid shells.
    for side, y in (("L", -0.105), ("R", 0.105)):
        add_bone(armature, f"CTRL_eye.{side}", (-0.425, y, 0.765), (-0.485, y, 0.765), head)
        add_bone(armature, f"CTRL_ear.{side}", (-0.34, y, 0.84), (-0.33, y * 1.22, 0.955), head)

    # Front legs use three deforming segments plus a non-deforming paw control.
    for side, y in (("L", -0.115), ("R", 0.115)):
        upper = add_bone(armature, f"DEF_front_upper.{side}", (-0.20, y, 0.52), (-0.23, y, 0.31), chest)
        lower = add_bone(armature, f"DEF_front_lower.{side}", (-0.23, y, 0.31), (-0.25, y, 0.11), upper, True)
        add_bone(armature, f"DEF_front_paw.{side}", (-0.25, y, 0.11), (-0.33, y, 0.055), lower, True)

        thigh = add_bone(armature, f"DEF_rear_thigh.{side}", (0.17, y, 0.43), (0.26, y, 0.29), pelvis)
        shin = add_bone(armature, f"DEF_rear_lower.{side}", (0.26, y, 0.29), (0.20, y, 0.13), thigh, True)
        add_bone(armature, f"DEF_rear_paw.{side}", (0.20, y, 0.13), (0.12, y, 0.055), shin, True)

    tail_points = [
        (0.25, 0.0, 0.46),
        (0.34, 0.0, 0.49),
        (0.42, 0.0, 0.55),
        (0.47, 0.0, 0.64),
        (0.47, 0.0, 0.74),
        (0.43, 0.0, 0.83),
        (0.36, 0.0, 0.88),
        (0.29, 0.0, 0.86),
        (0.25, 0.0, 0.80),
    ]
    parent = pelvis
    for index, (a, b) in enumerate(zip(tail_points, tail_points[1:]), start=1):
        parent = add_bone(armature, f"DEF_tail_{index:02d}", a, b, parent, index > 1)

    bpy.ops.object.mode_set(mode="OBJECT")
    armature.display_type = "OCTAHEDRAL"
    bpy.context.scene["marmalade_pipeline_stage"] = "rig-guide"
    bpy.context.scene["marmalade_next_gate"] = "final quad retopology and separated facial geometry"
    bpy.ops.wm.save_as_mainfile(filepath=str(output), check_existing=False)
    print(f"Saved Marmalade rig guide: {output}")


if __name__ == "__main__":
    main()
