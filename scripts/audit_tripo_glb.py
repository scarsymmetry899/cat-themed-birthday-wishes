import bpy
import json
import sys


source = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=source)

meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
armatures = [obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"]
report = {
    "objects": len(bpy.context.scene.objects),
    "meshes": len(meshes),
    "vertices": sum(len(obj.data.vertices) for obj in meshes),
    "polygons": sum(len(obj.data.polygons) for obj in meshes),
    "materials": sorted({slot.material.name for obj in meshes for slot in obj.material_slots if slot.material}),
    "images": [
        {
            "name": image.name,
            "size": list(image.size),
            "packed": bool(image.packed_file),
            "filepath": image.filepath,
        }
        for image in bpy.data.images
    ],
    "armatures": [obj.name for obj in armatures],
    "actions": [
        {
            "name": action.name,
            "frame_range": list(action.frame_range),
            "slots": [slot.name_display for slot in action.slots],
        }
        for action in bpy.data.actions
    ],
    "animation_data": {
        obj.name: {
            "action": obj.animation_data.action.name if obj.animation_data and obj.animation_data.action else None,
            "nla_tracks": [
                {
                    "name": track.name,
                    "strips": [strip.name for strip in track.strips],
                }
                for track in obj.animation_data.nla_tracks
            ] if obj.animation_data else [],
        }
        for obj in bpy.context.scene.objects
        if obj.animation_data
    },
    "bones": {
        obj.name: [
            {
                "name": bone.name,
                "parent": bone.parent.name if bone.parent else None,
                "head": [round(v, 4) for v in bone.head_local],
                "tail": [round(v, 4) for v in bone.tail_local],
            }
            for bone in obj.data.bones
        ]
        for obj in armatures
    },
    "pose_bones": {
        obj.name: [
            {
                "name": bone.name,
                "location": [round(v, 4) for v in bone.location],
                "matrix_translation": [round(v, 4) for v in bone.matrix.translation],
            }
            for bone in obj.pose.bones
        ]
        for obj in armatures
    },
    "shape_keys": {
        obj.name: [key.name for key in obj.data.shape_keys.key_blocks]
        for obj in meshes
        if obj.data.shape_keys
    },
    "weight_centers": {
        obj.name: {
            group.name: {
                "count": len(items),
                "weight": round(sum(weight for _, weight in items), 4),
                "center": [
                    round(sum(obj.data.vertices[index].co[axis] * weight for index, weight in items) / max(sum(weight for _, weight in items), 1e-8), 4)
                    for axis in range(3)
                ],
            }
            for group in obj.vertex_groups
            if (items := [
                (vertex.index, membership.weight)
                for vertex in obj.data.vertices
                for membership in vertex.groups
                if membership.group == group.index and membership.weight > 0.01
            ])
        }
        for obj in meshes
        if obj.vertex_groups
    },
    "bounds": {
        obj.name: {
            "dimensions": [round(v, 4) for v in obj.dimensions],
            "location": [round(v, 4) for v in obj.location],
        }
        for obj in meshes
    },
}
print("TRIPO_AUDIT=" + json.dumps(report))
