"""Integrate Marmalade face parts with surface eyelids and the head bone."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import bpy


ROOT = "Marmalade_FaceRoot"
RIG = "Marmalade_ProductionRig_v01"
COLLECTION = "15_FACE_PARTS"


def material(name, rgba, roughness=0.58):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.diffuse_color = rgba
    shader = mat.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = rgba
    shader.inputs["Roughness"].default_value = roughness
    return mat


def shape_driver(key, root, property_name):
    curve = key.driver_add("value")
    variable = curve.driver.variables.new()
    variable.name = property_name
    variable.type = "SINGLE_PROP"
    variable.targets[0].id = root
    variable.targets[0].data_path = f'["{property_name}"]'
    curve.driver.expression = property_name


def build_lid(name, center_y, upper, collection, root, lid_material):
    old = bpy.data.objects.get(name)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)

    columns = 18
    rows = 5 if upper else 3
    vertices = []
    for row in range(rows):
        t = row / (rows - 1)
        for index in range(columns):
            u = -1.0 + 2.0 * index / (columns - 1)
            arch = math.sqrt(max(0.0, 1.0 - u * u))
            y = center_y + u * 0.057
            if upper:
                arc = 0.758 + arch * 0.055
                top = arc + 0.030
                bottom = arc - 0.003
            else:
                arc = 0.746 - arch * 0.039
                top = arc - 0.004
                bottom = arc + 0.002
            z = top + (bottom - top) * t
            x = -0.497 - 0.014 * arch - 0.005 * math.sin(math.pi * t)
            vertices.append((x, y, z))
    faces = []
    for row in range(rows - 1):
        start = row * columns
        next_start = (row + 1) * columns
        for index in range(columns - 1):
            faces.append((start + index, start + index + 1, next_start + index + 1, next_start + index))

    mesh = bpy.data.meshes.new(f"{name}_SurfaceMesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.parent = root
    obj.data.materials.append(lid_material)
    for polygon in obj.data.polygons:
        polygon.use_smooth = True

    basis = obj.shape_key_add(name="Basis")
    blink = obj.shape_key_add(name="Blink")
    focus = obj.shape_key_add(name="Focus") if upper else None
    for row in range(rows):
        t = row / (rows - 1)
        for index in range(columns):
            u = -1.0 + 2.0 * index / (columns - 1)
            arch = math.sqrt(max(0.0, 1.0 - u * u))
            vertex_index = row * columns + index
            if upper:
                open_arc = 0.758 + arch * 0.055
                top = open_arc + 0.030
                closed_bottom = 0.746 - arch * 0.039
                blink.data[vertex_index].co.z = top + (closed_bottom - top) * t
                blink.data[vertex_index].co.x = -0.497 - 0.014 * arch - 0.012 * math.sin(math.pi * t)
                if focus:
                    focus_bottom = 0.747 + arch * 0.025
                    focus.data[vertex_index].co.z = top + (focus_bottom - top) * t
    shape_driver(blink, root, "blink")
    if focus:
        shape_driver(focus, root, "focus")

    subdivision = obj.modifiers.new("Eyelid_SmoothSurface", "SUBSURF")
    subdivision.levels = 2
    subdivision.render_levels = 2
    solidify = obj.modifiers.new("Eyelid_Thickness", "SOLIDIFY")
    solidify.thickness = 0.0015 if upper else 0.0006
    solidify.offset = 0.0
    bevel = obj.modifiers.new("Eyelid_Soften", "BEVEL")
    bevel.width = 0.0012 if upper else 0.0006
    bevel.segments = 2
    obj["component"] = "integrated eyelid surface"
    return obj


def main():
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if not args:
        raise RuntimeError("Pass output .blend after --")
    output = Path(args[0]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    scene = bpy.context.scene
    scene.frame_set(1)
    root = bpy.data.objects.get(ROOT)
    rig = bpy.data.objects.get(RIG)
    collection = bpy.data.collections.get(COLLECTION)
    if not root or not rig or not collection:
        raise RuntimeError("Face root, production rig, or face collection is missing")

    # Keep the assembled face attached to head motion without changing its
    # existing neutral placement.
    world = root.matrix_world.copy()
    root.parent = rig
    root.parent_type = "BONE"
    root.parent_bone = "DEF_head"
    root.matrix_world = world
    root["status"] = "head-bone attached; surface eyelids v01"

    lid_material = material("Marmalade_EyelidIntegrated", (0.72, 0.18, 0.018, 1.0), 0.64)
    for side, center_y in (("L", -0.105), ("R", 0.105)):
        build_lid(f"UpperLid.{side}", center_y, True, collection, root, lid_material)
        build_lid(f"LowerLid.{side}", center_y, False, collection, root, lid_material)

    # Refine the face palette and visibility for the assembled checkpoint.
    palette = {
        "EyeWhite": material("Marmalade_EyeWhiteIntegrated", (0.92, 0.75, 0.48, 1.0), 0.46),
        "Iris": material("Marmalade_AmberIrisIntegrated", (0.95, 0.36, 0.018, 1.0), 0.28),
        "Pupil": material("Marmalade_PupilIntegrated", (0.012, 0.004, 0.002, 1.0), 0.22),
        "Catchlight": material("Marmalade_CatchlightIntegrated", (1.0, 0.96, 0.82, 1.0), 0.16),
    }
    eye_x = {"EyeWhite": -0.432, "Iris": -0.486, "Pupil": -0.496, "Catchlight": -0.505}
    for obj in collection.objects:
        if obj.name.startswith(("PartyHat", "Anchor_PartyHat")):
            obj.hide_render = True
            obj.hide_viewport = True
            continue
        if obj.name.startswith(("Muzzle.", "Chin")):
            obj.hide_render = True
            obj.hide_viewport = True
            continue
        obj.hide_render = False
        obj.hide_viewport = False
        for prefix, mat in palette.items():
            if obj.name.startswith(prefix) and obj.type == "MESH":
                obj.data.materials.clear()
                obj.data.materials.append(mat)
                obj.location.x = eye_x[prefix]
                if not obj.get("identity_eye_refine_v01"):
                    if prefix == "Iris":
                        for vertex in obj.data.vertices:
                            vertex.co.y *= 1.16
                            vertex.co.z *= 1.08
                    elif prefix == "Pupil":
                        for vertex in obj.data.vertices:
                            vertex.co.y *= 0.82
                    obj["identity_eye_refine_v01"] = True

    root["blink_surface_version"] = 1
    scene["marmalade_pipeline_stage"] = "integrated-face-checkpoint"
    scene["marmalade_next_gate"] = "validate neutral gaze blink focus and head attachment"
    bpy.ops.wm.save_as_mainfile(filepath=str(output), check_existing=False)
    print({"output": str(output), "parent_bone": root.parent_bone, "lid_objects": 4})


if __name__ == "__main__":
    main()
