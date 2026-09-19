"""Add separately controllable facial-production guides to Marmalade.

The Tripo source paints/fuses these features into one mesh. These clean objects
establish the production split and animation controls while the final eye
sockets and mouth loops are still being corrected on the quad base.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import bpy


COLLECTION = "15_FACE_PARTS"
ROOT = "Marmalade_FaceRoot"
AXIS_ROTATION = math.radians(39.997320722)


def material(name: str, rgba: tuple[float, float, float, float], roughness=0.55, metallic=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = rgba
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return mat


def move_to_collection(obj, collection):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)


def add_uv_sphere(name, location, scale, mat, collection, parent):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    obj.parent = parent
    move_to_collection(obj, collection)
    for poly in obj.data.polygons:
        poly.use_smooth = True
    return obj


def add_curve(name, points, bevel, mat, collection, parent, cyclic=False):
    curve = bpy.data.curves.new(name=f"{name}_Curve", type="CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 16
    curve.bevel_depth = bevel
    curve.bevel_resolution = 3
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(len(points) - 1)
    for point, co in zip(spline.bezier_points, points):
        point.co = co
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"
    spline.use_cyclic_u = cyclic
    obj = bpy.data.objects.new(name, curve)
    collection.objects.link(obj)
    obj.parent = parent
    obj.data.materials.append(mat)
    return obj


def add_triangular_nose(name, collection, parent, mat):
    front_x, back_x = -0.510, -0.492
    profile = [(-0.027, 0.693), (0.027, 0.693), (0.0, 0.662)]
    vertices = [(front_x, y, z) for y, z in profile] + [(back_x, y, z) for y, z in profile]
    faces = [
        (0, 1, 2),
        (5, 4, 3),
        (0, 3, 4, 1),
        (1, 4, 5, 2),
        (2, 5, 3, 0),
    ]
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.parent = parent
    obj.data.materials.append(mat)
    bevel = obj.modifiers.new("Soft_Nose_Edges", "BEVEL")
    bevel.width = 0.004
    bevel.segments = 3
    return obj


def driven(obj, data_path, index, expression, root, variables):
    fcurve = obj.driver_add(data_path, index)
    driver = fcurve.driver
    driver.type = "SCRIPTED"
    driver.expression = expression
    for variable_name, property_name in variables.items():
        variable = driver.variables.new()
        variable.name = variable_name
        variable.type = "SINGLE_PROP"
        target = variable.targets[0]
        target.id = root
        target.data_path = f'["{property_name}"]'
    return fcurve


def curve_shape_driver(obj, key_name, coordinates, root, property_name):
    if obj.data.shape_keys is None:
        obj.shape_key_add(name="Basis")
    key = obj.shape_key_add(name=key_name)
    for point, coordinate in zip(key.data, coordinates):
        point.co = coordinate
    fcurve = key.driver_add("value")
    variable = fcurve.driver.variables.new()
    variable.name = property_name
    variable.type = "SINGLE_PROP"
    variable.targets[0].id = root
    variable.targets[0].data_path = f'["{property_name}"]'
    fcurve.driver.expression = property_name
    return key


def main() -> None:
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if not args:
        raise RuntimeError("Pass output .blend path after --")
    output = Path(args[0]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    collection = bpy.data.collections.get(COLLECTION)
    if collection:
        for obj in list(collection.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
    else:
        collection = bpy.data.collections.new(COLLECTION)
        bpy.context.scene.collection.children.link(collection)

    root = bpy.data.objects.new(ROOT, None)
    collection.objects.link(root)
    root.rotation_euler.z = AXIS_ROTATION
    root["status"] = "production split guide; socket integration pending"
    for name, default, minimum, maximum in (
        ("lookX", 0.0, -1.0, 1.0),
        ("lookY", 0.0, -1.0, 1.0),
        ("blink", 0.0, 0.0, 1.0),
        ("focus", 0.0, 0.0, 1.0),
    ):
        root[name] = default
        ui = root.id_properties_ui(name)
        ui.update(min=minimum, max=maximum, soft_min=minimum, soft_max=maximum)

    cream = material("Marmalade_Cream", (0.93, 0.78, 0.57, 1.0), 0.75)
    amber = material("Marmalade_AmberIris", (0.96, 0.48, 0.035, 1.0), 0.28)
    pupil = material("Marmalade_Pupil", (0.025, 0.012, 0.007, 1.0), 0.24)
    catchlight = material("Marmalade_Catchlight", (1.0, 0.98, 0.92, 1.0), 0.15)
    lid = material("Marmalade_Eyelid", (0.88, 0.34, 0.12, 1.0), 0.68)
    pink = material("Marmalade_Pink", (0.94, 0.36, 0.36, 1.0), 0.58)
    mouth = material("Marmalade_MouthLine", (0.20, 0.055, 0.03, 1.0), 0.7)
    whisker = material("Marmalade_Whisker", (0.96, 0.88, 0.74, 1.0), 0.8)

    for side, y, mirror in (("L", -0.105, -1.0), ("R", 0.105, 1.0)):
        eye = add_uv_sphere(
            f"EyeWhite.{side}", (-0.426, y, 0.755), (0.059, 0.068, 0.078), cream, collection, root
        )
        eye["control"] = f"CTRL_eye.{side}"
        add_uv_sphere(
            f"Iris.{side}", (-0.480, y, 0.755), (0.012, 0.043, 0.055), amber, collection, root
        )
        add_uv_sphere(
            f"Pupil.{side}", (-0.490, y, 0.755), (0.009, 0.023, 0.040), pupil, collection, root
        )
        add_uv_sphere(
            f"Catchlight.{side}", (-0.499, y - 0.014 * mirror, 0.780), (0.006, 0.010, 0.010), catchlight, collection, root
        )

        # Upper and lower eyelids are independent curves for blink/focus tests.
        upper_lid = add_curve(
            f"UpperLid.{side}",
            [(-0.500, y - 0.055, 0.765), (-0.504, y, 0.815), (-0.500, y + 0.055, 0.765)],
            0.006,
            lid,
            collection,
            root,
        )
        lower_lid = add_curve(
            f"LowerLid.{side}",
            [(-0.500, y - 0.052, 0.748), (-0.503, y, 0.713), (-0.500, y + 0.052, 0.748)],
            0.005,
            lid,
            collection,
            root,
        )
        curve_shape_driver(
            upper_lid,
            "Blink",
            [(-0.500, y - 0.055, 0.752), (-0.504, y, 0.746), (-0.500, y + 0.055, 0.752)],
            root,
            "blink",
        )
        curve_shape_driver(
            lower_lid,
            "Blink",
            [(-0.500, y - 0.055, 0.752), (-0.504, y, 0.746), (-0.500, y + 0.055, 0.752)],
            root,
            "blink",
        )
        curve_shape_driver(
            upper_lid,
            "Focus",
            [(-0.500, y - 0.055, 0.760), (-0.504, y, 0.790), (-0.500, y + 0.055, 0.760)],
            root,
            "focus",
        )

    add_uv_sphere("Muzzle.L", (-0.478, -0.026, 0.650), (0.017, 0.035, 0.028), cream, collection, root)
    add_uv_sphere("Muzzle.R", (-0.478, 0.026, 0.650), (0.017, 0.035, 0.028), cream, collection, root)
    add_uv_sphere("Chin", (-0.466, 0.0, 0.620), (0.016, 0.036, 0.018), cream, collection, root)
    nose = add_triangular_nose("Nose", collection, root, pink)
    nose["control"] = "CTRL_nose"
    add_curve(
        "Mouth",
        [(-0.507, -0.045, 0.650), (-0.512, 0.0, 0.635), (-0.507, 0.045, 0.650)],
        0.003,
        mouth,
        collection,
        root,
    )

    for side, y_sign in (("L", -1.0), ("R", 1.0)):
        y0 = 0.045 * y_sign
        whisker_points = [
            [(-0.485, y0, 0.675), (-0.47, 0.13 * y_sign, 0.690), (-0.43, 0.23 * y_sign, 0.705)],
            [(-0.490, y0, 0.660), (-0.47, 0.14 * y_sign, 0.650), (-0.42, 0.24 * y_sign, 0.640)],
            [(-0.485, y0, 0.645), (-0.46, 0.13 * y_sign, 0.615), (-0.40, 0.22 * y_sign, 0.590)],
        ]
        for index, points in enumerate(whisker_points, start=1):
            add_curve(f"Whisker.{side}.{index:02d}", points, 0.0015, whisker, collection, root)

    hat_anchor = bpy.data.objects.new("Anchor_PartyHat", None)
    collection.objects.link(hat_anchor)
    hat_anchor.parent = root
    hat_anchor.location = (-0.34, 0.0, 0.945)
    hat_anchor.empty_display_type = "CIRCLE"
    hat_anchor.empty_display_size = 0.06

    party_blue = material("Marmalade_PartyBlue", (0.12, 0.36, 0.62, 1.0), 0.62)
    party_gold = material("Marmalade_PartyGold", (0.96, 0.63, 0.12, 1.0), 0.48, 0.08)
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.095, radius2=0.008, depth=0.22)
    party_hat = bpy.context.object
    party_hat.name = "PartyHat"
    party_hat.location = (-0.34, 0.0, 1.045)
    party_hat.parent = root
    party_hat.data.materials.append(party_blue)
    move_to_collection(party_hat, collection)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.095, minor_radius=0.008, major_segments=32, minor_segments=8)
    hat_brim = bpy.context.object
    hat_brim.name = "PartyHat_Brim"
    hat_brim.location = (-0.34, 0.0, 0.94)
    hat_brim.parent = root
    hat_brim.data.materials.append(party_gold)
    move_to_collection(hat_brim, collection)
    party_hat.hide_render = True
    hat_brim.hide_render = True
    party_hat.hide_viewport = True
    hat_brim.hide_viewport = True

    # Additive face inputs mirror the controls that the web character lab will
    # expose. Drivers keep pupils/catchlights inside the eye region.
    for side in ("L", "R"):
        for part in ("Iris", "Pupil", "Catchlight"):
            obj = bpy.data.objects[f"{part}.{side}"]
            base_y = obj.location.y
            base_z = obj.location.z
            driven(obj, "location", 1, f"{base_y:.8f} + lookX * 0.018", root, {"lookX": "lookX"})
            driven(obj, "location", 2, f"{base_z:.8f} + lookY * 0.015", root, {"lookY": "lookY"})
            driven(obj, "scale", 2, "1.0 - blink * 0.98", root, {"blink": "blink"})
        eye_white = bpy.data.objects[f"EyeWhite.{side}"]
        driven(eye_white, "scale", 2, "1.0 - blink * 0.98", root, {"blink": "blink"})
        catchlight_obj = bpy.data.objects[f"Catchlight.{side}"]
        driven(catchlight_obj, "scale", 1, "1.0 - blink * 0.98", root, {"blink": "blink"})
        pupil_obj = bpy.data.objects[f"Pupil.{side}"]
        driven(pupil_obj, "scale", 1, "1.0 - focus * 0.38", root, {"focus": "focus"})


    bpy.context.scene["marmalade_face_parts"] = "separate guides created"
    bpy.context.scene["marmalade_pipeline_stage"] = "face-control-checkpoint"
    bpy.context.scene["marmalade_next_gate"] = "integrate eye sockets and mouth loops into final quad topology"
    bpy.ops.wm.save_as_mainfile(filepath=str(output), check_existing=False)
    print(f"Saved separated Marmalade face guides: {output}")


if __name__ == "__main__":
    main()
