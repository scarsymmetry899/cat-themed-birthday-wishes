import bpy
import os
import sys


source, destination = sys.argv[sys.argv.index("--") + 1 : sys.argv.index("--") + 3]
source = os.path.abspath(source)
destination = os.path.abspath(destination)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=source)

meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
character = max(meshes, key=lambda obj: len(obj.data.polygons))

for obj in list(bpy.context.scene.objects):
    if obj != character:
        bpy.data.objects.remove(obj, do_unlink=True)

character.name = "Marmalade_Tripo20K"
character.data.name = "Marmalade_Tripo20K_Mesh"
character.parent = None
character.matrix_parent_inverse.identity()
character.animation_data_clear()
character.vertex_groups.clear()
for modifier in list(character.modifiers):
    character.modifiers.remove(modifier)

bpy.context.view_layer.objects.active = character
character.select_set(True)
bpy.ops.object.shade_smooth_by_angle()

scene = bpy.context.scene
scene.name = "Marmalade_TripoRecovery"
scene.unit_settings.system = "METRIC"
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1024
scene.render.resolution_y = 1024
scene.render.resolution_percentage = 100

scene["source_asset"] = "Tripo retopology, 19,105 triangles"
scene["recovery_status"] = "Original Tripo mesh preserved; faulty one-bone export rig removed"

os.makedirs(os.path.dirname(destination), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=destination)
print(f"RECOVERY_BLEND={destination}")
