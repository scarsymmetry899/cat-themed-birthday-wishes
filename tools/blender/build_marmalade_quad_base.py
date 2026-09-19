"""Create a quad retopology candidate from the repaired Marmalade proxy.

This is a topology *candidate*, not an automatically approved deforming mesh.
It remains unbound until shoulder, hip, face, paw, and tail-base loops pass the
deformation audit.
"""

from __future__ import annotations

import sys
from pathlib import Path

import bmesh
import bpy


SOURCE = "Marmalade_Retopo_Proxy"
OUTPUT = "Marmalade_QuadBase_Candidate"


def topology_stats(obj: bpy.types.Object) -> dict[str, int]:
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    stats = {
        "vertices": len(bm.verts),
        "edges": len(bm.edges),
        "faces": len(bm.faces),
        "triangles": sum(1 for face in bm.faces if len(face.verts) == 3),
        "quads": sum(1 for face in bm.faces if len(face.verts) == 4),
        "ngons": sum(1 for face in bm.faces if len(face.verts) > 4),
        "boundary_edges": sum(1 for edge in bm.edges if edge.is_boundary),
        "nonmanifold_edges": sum(1 for edge in bm.edges if not edge.is_manifold),
    }
    bm.free()
    return stats


def patch_triangular_holes_with_quads(obj: bpy.types.Object) -> int:
    """Close tiny three-edge QuadriFlow openings for visual/deform auditing.

    These four caps remain explicitly tracked triangles and must be converted
    into hand-authored quad patches before the production mesh is approved.
    """
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.edges.ensure_lookup_table()
    boundary = [edge for edge in bm.edges if edge.is_boundary]
    seen = set()
    components = []
    for edge in boundary:
        if edge in seen:
            continue
        stack = [edge]
        seen.add(edge)
        edges = []
        vertices = set()
        while stack:
            current = stack.pop()
            edges.append(current)
            for vertex in current.verts:
                vertices.add(vertex)
                for linked in vertex.link_edges:
                    if linked.is_boundary and linked not in seen:
                        seen.add(linked)
                        stack.append(linked)
        components.append((edges, list(vertices)))

    triangular_components = [
        (edges, vertices) for edges, vertices in components if len(edges) == 3 and len(vertices) == 3
    ]
    patched = 0
    for _, vertices in triangular_components:
        try:
            bm.faces.new(vertices)
            patched += 1
        except ValueError:
            pass

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
    return patched


def main() -> None:
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if not args:
        raise RuntimeError("Pass output .blend path after --")
    output_path = Path(args[0]).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    source = bpy.data.objects.get(SOURCE)
    if source is None:
        raise RuntimeError(f"Missing required source object: {SOURCE}")

    old = bpy.data.objects.get(OUTPUT)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)

    candidate = source.copy()
    candidate.data = source.data.copy()
    candidate.name = OUTPUT
    candidate.data.name = f"{OUTPUT}_Mesh"
    candidate.hide_viewport = False
    candidate.hide_render = False
    candidate["status"] = "CANDIDATE - deformation audit required"
    candidate["source_object"] = SOURCE

    retopo_collection = bpy.data.collections.get("10_RETOPOLOGY")
    if retopo_collection is None:
        retopo_collection = bpy.data.collections.new("10_RETOPOLOGY")
        bpy.context.scene.collection.children.link(retopo_collection)
    retopo_collection.objects.link(candidate)

    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    candidate.select_set(True)
    bpy.context.view_layer.objects.active = candidate

    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode="OBJECT")

    result = bpy.ops.object.quadriflow_remesh(
        use_mesh_symmetry=False,
        use_preserve_sharp=True,
        use_preserve_boundary=False,
        preserve_attributes=False,
        smooth_normals=True,
        mode="FACES",
        target_faces=12000,
        seed=7,
    )
    if "FINISHED" not in result:
        raise RuntimeError(f"QuadriFlow did not finish: {result}")

    patched_holes = patch_triangular_holes_with_quads(candidate)
    stats = topology_stats(candidate)
    for key, value in stats.items():
        candidate[f"topology_{key}"] = value
    candidate["topology_target_faces"] = 12000
    candidate["topology_method"] = "QuadriFlow from repaired manifold proxy"
    candidate["topology_temporary_triangle_caps"] = patched_holes

    source.hide_viewport = True
    source.hide_render = True
    bpy.context.scene["marmalade_pipeline_stage"] = "quad-base-candidate"
    bpy.context.scene["marmalade_next_gate"] = "deformation-loop audit and facial separation"
    bpy.ops.wm.save_as_mainfile(filepath=str(output_path), check_existing=False)
    print({"output": str(output_path), "stats": stats})


if __name__ == "__main__":
    main()
