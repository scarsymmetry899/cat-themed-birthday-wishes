"""Build a non-destructive topology proxy for Marmalade.

The voxel/decimate result is a silhouette and deformation-planning aid. It is
not treated as final animation topology; the shoulder, hip, face, paw, and tail
loops must be reviewed and corrected before skinning.
"""

from __future__ import annotations

import json
from pathlib import Path

import bpy
import bmesh


REPO_ROOT = Path(__file__).resolve().parents[2]
WORK_BLEND = (
    REPO_ROOT
    / "assets"
    / "character"
    / "3d"
    / "blender"
    / "marmalade-production-v01.blend"
)
OUTPUT_BLEND = (
    REPO_ROOT
    / "assets"
    / "character"
    / "3d"
    / "blender"
    / "marmalade-retopo-proxy-v01.blend"
)
TARGET_TRIANGLES = 40_000
VOXEL_SIZE_METERS = 0.003


def ensure_collection(name: str) -> bpy.types.Collection:
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    return collection


def move_exclusively(obj: bpy.types.Object, collection: bpy.types.Collection) -> None:
    if collection.objects.get(obj.name) is None:
        collection.objects.link(obj)
    for existing in list(obj.users_collection):
        if existing != collection:
            existing.objects.unlink(obj)


def main() -> None:
    if Path(bpy.data.filepath).resolve() != WORK_BLEND.resolve():
        bpy.ops.wm.open_mainfile(filepath=str(WORK_BLEND))

    scene = bpy.context.scene
    scene.name = "Marmalade_Production"
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    source_collection = ensure_collection("00_SOURCE_HIGHRES")
    retopo_collection = ensure_collection("10_RETOPOLOGY")
    ensure_collection("20_RIG")
    ensure_collection("30_EXPORT")
    ensure_collection("90_REFERENCE")

    source = bpy.data.objects.get("Marmalade_HighRes_Source")
    if source is None or source.type != "MESH":
        raise RuntimeError("Marmalade_HighRes_Source mesh was not found")
    move_exclusively(source, source_collection)
    source["source_role"] = "immutable_tripo_reference"
    source["tripo_task_id"] = "23f922b4-df98-4927-a1f6-631f75c6deb7"

    prior = bpy.data.objects.get("Marmalade_Retopo_Proxy")
    if prior is not None:
        bpy.data.objects.remove(prior, do_unlink=True)

    proxy = source.copy()
    proxy.data = source.data.copy()
    proxy.name = "Marmalade_Retopo_Proxy"
    proxy.data.name = "Marmalade_Retopo_Proxy_Mesh"
    retopo_collection.objects.link(proxy)

    bpy.ops.object.select_all(action="DESELECT")
    proxy.select_set(True)
    bpy.context.view_layer.objects.active = proxy
    proxy.data.remesh_voxel_size = VOXEL_SIZE_METERS
    proxy.data.remesh_voxel_adaptivity = 0.0
    proxy.data.use_remesh_fix_poles = True
    proxy.data.use_remesh_preserve_volume = True
    proxy.data.use_remesh_preserve_attributes = False
    bpy.ops.object.voxel_remesh()
    voxel_vertices = len(proxy.data.vertices)
    voxel_faces = len(proxy.data.polygons)

    # QuadriFlow rejects the detached shells that can survive around painted
    # whiskers and facial cards. Keep the main watertight body shell and rebuild
    # eyes/whiskers later as dedicated animation components.
    bm = bmesh.new()
    bm.from_mesh(proxy.data)
    remaining = set(bm.verts)
    components: list[list[bmesh.types.BMVert]] = []
    while remaining:
        seed_vertex = remaining.pop()
        component = [seed_vertex]
        stack = [seed_vertex]
        while stack:
            vertex = stack.pop()
            for edge in vertex.link_edges:
                neighbor = edge.other_vert(vertex)
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    component.append(neighbor)
                    stack.append(neighbor)
        components.append(component)
    components.sort(key=len, reverse=True)
    removed_component_vertices = sum(len(component) for component in components[1:])
    if len(components) > 1:
        bmesh.ops.delete(
            bm,
            geom=[vertex for component in components[1:] for vertex in component],
            context="VERTS",
        )
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(proxy.data)
    bm.free()
    proxy.data.update()

    proxy.data.calc_loop_triangles()
    voxel_triangles = len(proxy.data.loop_triangles)
    modifier = proxy.modifiers.new(name="Planning_Decimate", type="DECIMATE")
    modifier.decimate_type = "COLLAPSE"
    modifier.ratio = min(1.0, TARGET_TRIANGLES / max(1, voxel_triangles))
    modifier.use_collapse_triangulate = True
    bpy.ops.object.modifier_apply(modifier=modifier.name)

    if source.data.materials and not proxy.data.materials:
        proxy.data.materials.append(source.data.materials[0])

    proxy["topology_role"] = "planning_proxy_not_final_rig_mesh"
    proxy["target_triangles"] = TARGET_TRIANGLES
    proxy["proxy_method"] = "voxel_then_decimate"
    source.hide_set(True)
    source.hide_render = True

    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT_BLEND))
    result = {
        "blend_file": str(OUTPUT_BLEND),
        "source_vertices": len(source.data.vertices),
        "source_faces": len(source.data.polygons),
        "voxel_size_meters": VOXEL_SIZE_METERS,
        "voxel_vertices": voxel_vertices,
        "voxel_faces": voxel_faces,
        "voxel_triangles": voxel_triangles,
        "voxel_components": len(components),
        "removed_component_vertices": removed_component_vertices,
        "proxy_vertices": len(proxy.data.vertices),
        "proxy_edges": len(proxy.data.edges),
        "proxy_faces": len(proxy.data.polygons),
        "proxy_uv_layers": [layer.name for layer in proxy.data.uv_layers],
        "collections": sorted(collection.name for collection in bpy.data.collections),
    }
    print("MARMALADE_RETOPO_PROXY=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
