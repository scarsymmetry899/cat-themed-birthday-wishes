import bpy
import json
import math
import os
import sys
from mathutils import Vector


blend_file, output_dir = sys.argv[sys.argv.index("--") + 1 : sys.argv.index("--") + 3]
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(blend_file))
obj = bpy.data.objects["Marmalade_Tripo20K"]
corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
mins = Vector((min(v.x for v in corners), min(v.y for v in corners), min(v.z for v in corners)))
maxs = Vector((max(v.x for v in corners), max(v.y for v in corners), max(v.z for v in corners)))
center = (mins + maxs) / 2


def point_at(item, target):
    item.rotation_euler = (Vector(target) - item.location).to_track_quat("-Z", "Y").to_euler()


world = bpy.context.scene.world or bpy.data.worlds.new("World")
bpy.context.scene.world = world
world.color = (0.035, 0.035, 0.045)

camera_data = bpy.data.cameras.new("QA_Camera")
camera = bpy.data.objects.new("QA_Camera", camera_data)
bpy.context.collection.objects.link(camera)
bpy.context.scene.camera = camera
camera.data.lens = 55

for name, location, energy, size in (
    ("Key", (2.5, -3.0, 3.0), 900, 3.0),
    ("Fill", (-2.0, -1.0, 2.2), 500, 2.5),
    ("Rim", (0.5, 2.5, 2.8), 700, 2.0),
):
    light_data = bpy.data.lights.new(name, "AREA")
    light_data.energy = energy
    light_data.shape = "DISK"
    light_data.size = size
    light = bpy.data.objects.new(name, light_data)
    bpy.context.collection.objects.link(light)
    light.location = location
    point_at(light, center)

output_dir = os.path.abspath(output_dir)
os.makedirs(output_dir, exist_ok=True)
scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.color_type = "TEXTURE"
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.render.resolution_x = 800
scene.render.resolution_y = 800
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"

views = {
    "front": (0.0, -2.6, 0.55),
    "three-quarter": (1.9, -2.2, 0.75),
    "side": (2.6, 0.0, 0.62),
}
for name, location in views.items():
    camera.location = location
    point_at(camera, center)
    scene.render.filepath = os.path.join(output_dir, f"{name}.png")
    bpy.ops.render.render(write_still=True)

print(
    "TRIPO_RECOVERY_RENDER="
    + json.dumps(
        {
            "bounds_min": list(mins),
            "bounds_max": list(maxs),
            "center": list(center),
            "renders": [os.path.join(output_dir, f"{name}.png") for name in views],
        }
    )
)
