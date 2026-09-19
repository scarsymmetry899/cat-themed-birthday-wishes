"""Author deformation-safe Marmalade colors as a point-domain color attribute."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


OBJECT = "Marmalade_WeightedCandidate_v01"
ATTRIBUTE = "MarmaladeColor"
MATERIAL = "Marmalade_ProductionCoat_v01"
ANGLE = math.radians(39.997320722)
FORWARD = Vector((-math.cos(ANGLE), -math.sin(ANGLE), 0.0))
SIDE = Vector((-math.sin(ANGLE), math.cos(ANGLE), 0.0))

ORANGE = Vector((0.72, 0.180, 0.018))
DARK = Vector((0.205, 0.018, 0.004))
CREAM = Vector((0.88, 0.61, 0.31))
PINK = Vector((0.72, 0.22, 0.18))


def clamp01(value):
    return max(0.0, min(1.0, value))


def smoothstep(edge0, edge1, value):
    if edge0 == edge1:
        return float(value >= edge1)
    t = clamp01((value - edge0) / (edge1 - edge0))
    return t * t * (3.0 - 2.0 * t)


def band(value, center, half_width, feather):
    return 1.0 - smoothstep(half_width, half_width + feather, abs(value - center))


def mix(a, b, factor):
    return a.lerp(b, clamp01(factor))


def anatomical_position(obj, vertex):
    point = obj.matrix_world @ vertex.co
    return point.dot(FORWARD), point.dot(SIDE), point.z


def coat_color(f, s, z):
    color = ORANGE.copy()

    # Cream paw tips, central chest, belly, and rounded muzzle.
    paw = 1.0 - smoothstep(0.105, 0.145, z)
    chest_center = 1.0 - smoothstep(0.075, 0.155, abs(s))
    chest_height = smoothstep(0.17, 0.23, z) * (1.0 - smoothstep(0.54, 0.61, z))
    chest_front = smoothstep(-0.02, 0.12, f)
    chest = chest_center * chest_height * chest_front
    belly = (
        (1.0 - smoothstep(0.30, 0.39, z))
        * smoothstep(-0.36, -0.22, f)
        * (1.0 - smoothstep(0.06, 0.16, f))
        * (1.0 - smoothstep(0.15, 0.23, abs(s)))
    )
    muzzle = (
        smoothstep(0.39, 0.455, f)
        * smoothstep(0.50, 0.58, z)
        * (1.0 - smoothstep(0.73, 0.78, z))
        * (1.0 - smoothstep(0.10, 0.18, abs(s)))
    )
    cream_mask = max(paw, chest, belly, muzzle)
    color = mix(color, CREAM, cream_mask)

    # Four dorsal bars, kept away from the cream underside.
    dorsal = 0.0
    for center in (-0.29, -0.16, -0.03, 0.10):
        dorsal = max(dorsal, band(f, center, 0.018, 0.035))
    dorsal *= smoothstep(0.40, 0.52, z) * (1.0 - smoothstep(0.73, 0.83, z))
    dorsal *= 1.0 - smoothstep(0.19, 0.27, abs(s))

    # Two readable bands on each leg.
    leg_region = max(smoothstep(0.08, 0.18, f), smoothstep(-0.18, -0.30, f))
    leg_region *= 1.0 - smoothstep(0.18, 0.27, abs(s))
    legs = max(band(z, 0.225, 0.017, 0.025), band(z, 0.325, 0.019, 0.028)) * leg_region

    # Three cheek accents per side.
    cheek = max(band(z, 0.575, 0.012, 0.022), band(z, 0.625, 0.012, 0.022), band(z, 0.675, 0.012, 0.022))
    cheek *= smoothstep(0.29, 0.365, f) * (1.0 - smoothstep(0.445, 0.50, f))
    cheek *= smoothstep(0.09, 0.15, abs(s))
    cheek *= 1.0 - smoothstep(0.25, 0.31, abs(s))

    # Forehead M: central taper plus two outward tapered strokes.
    forehead_region = smoothstep(0.22, 0.34, f) * smoothstep(0.675, 0.72, z) * (1.0 - smoothstep(0.91, 0.95, z))
    taper = clamp01((z - 0.69) / 0.23)
    outer_center = 0.025 + 0.072 * taper
    forehead = max(
        band(s, 0.0, 0.012, 0.018),
        band(abs(s), outer_center, 0.010, 0.018),
    ) * forehead_region

    # Tail markings are added from tail-bone weights below; this prevents the
    # bands from sliding or flipping on the curled silhouette.
    stripe_mask = max(dorsal, legs, cheek, forehead) * (1.0 - cream_mask * 0.75)
    color = mix(color, DARK, stripe_mask)

    # Soft pink inside the tall ear zones; intentionally restrained so the
    # outer orange rim remains visible.
    inner_ear = smoothstep(0.80, 0.86, z) * smoothstep(0.17, 0.26, abs(s)) * smoothstep(0.02, 0.18, f)
    inner_ear *= 1.0 - smoothstep(0.93, 0.97, z)
    color = mix(color, PINK, inner_ear * 0.72)
    return color


def tail_pattern_weight(obj, vertex):
    tail_indices = {
        obj.vertex_groups[f"DEF_tail_{index:02d}"].index: index
        for index in range(1, 9)
        if obj.vertex_groups.get(f"DEF_tail_{index:02d}")
    }
    weights = {index: 0.0 for index in range(1, 9)}
    for assignment in vertex.groups:
        index = tail_indices.get(assignment.group)
        if index is not None:
            weights[index] = assignment.weight
    total = sum(weights.values())
    dark = max(weights[2], weights[4], weights[6], weights[8])
    return dark, total


def build_material():
    material = bpy.data.materials.get(MATERIAL) or bpy.data.materials.new(MATERIAL)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    shader = nodes.new("ShaderNodeBsdfPrincipled")
    attribute = nodes.new("ShaderNodeAttribute")
    attribute.attribute_name = ATTRIBUTE
    shader.inputs["Roughness"].default_value = 0.62
    shader.inputs["IOR"].default_value = 1.42
    if "Coat Weight" in shader.inputs:
        shader.inputs["Coat Weight"].default_value = 0.08
    links.new(attribute.outputs["Color"], shader.inputs["Base Color"])
    links.new(shader.outputs["BSDF"], output.inputs["Surface"])
    return material


def main():
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if not args:
        raise RuntimeError("Pass output blend after --")
    output = Path(args[0]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    obj = bpy.data.objects.get(OBJECT)
    if obj is None or obj.type != "MESH":
        raise RuntimeError(f"Missing mesh: {OBJECT}")
    mesh = obj.data
    old = mesh.color_attributes.get(ATTRIBUTE)
    if old:
        mesh.color_attributes.remove(old)
    layer = mesh.color_attributes.new(name=ATTRIBUTE, type="FLOAT_COLOR", domain="POINT")
    for vertex in mesh.vertices:
        f, s, z = anatomical_position(obj, vertex)
        rgb = coat_color(f, s, z)
        tail_dark, tail_weight = tail_pattern_weight(obj, vertex)
        if tail_weight > 0.18:
            ring_mask = smoothstep(0.10, 0.62, tail_dark)
            rgb = mix(rgb, DARK, ring_mask * smoothstep(0.18, 0.55, tail_weight))
        layer.data[vertex.index].color = (*rgb, 1.0)

    material = build_material()
    obj.data.materials.clear()
    obj.data.materials.append(material)
    obj["marking_source"] = "deformation-safe procedural point colors"
    obj["marking_attribute"] = ATTRIBUTE
    obj["marking_status"] = "validation candidate; requires painted-master comparison"
    bpy.ops.wm.save_as_mainfile(filepath=str(output))
    print({"output": str(output), "attribute": ATTRIBUTE, "vertices": len(mesh.vertices)})


if __name__ == "__main__":
    main()
