import bpy
import json
import os

# Function to gather scene information
def get_scene_info():
    scene_info = []
    for obj in bpy.data.objects:
        obj_info = {
            'name': obj.name,
            'type': obj.type,
            'location': {
                'x': obj.location.x,
                'y': obj.location.y,
                'z': obj.location.z
            }
        }
        scene_info.append(obj_info)
    return scene_info

# Ensure all objects are visible and included in the render layers
for obj in bpy.data.objects:
    obj.hide_render = False
    obj.hide_viewport = False

# Function to add more objects to the scene
def add_objects():
    # Add a cube
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    cube = bpy.context.object
    cube.name = "NewCube"
    
    # Add a circle
    bpy.ops.mesh.primitive_circle_add(radius=1, location=(3, 3, 0))
    circle = bpy.context.object
    circle.name = "NewCircle"
    
    # Add a UV sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(-3, -3, 0))
    sphere = bpy.context.object
    sphere.name = "NewSphere"

# Add objects to the scene
add_objects()

# Set the render settings and ensure the camera is set up correctly
bpy.context.scene.camera = bpy.data.objects.get('Camera')
bpy.context.scene.render.filepath = '/Users/yonghuizhu/Project/Blender/output/rendered_image.png'
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Function to center the camera to include all objects
def set_camera_view():
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        obj.select_set(True)
    bpy.ops.view3d.camera_to_view_selected()

# Center the camera to include all objects
set_camera_view()

# Save the scene before rendering (optional but good practice)
bpy.ops.wm.save_as_mainfile(filepath='/Users/yonghuizhu/Project/Blender/output/scene.blend')

# Define paths for the JSON file and rendered image
output_directory = '/Users/yonghuizhu/Project/Blender/output'
json_path = os.path.join(output_directory, 'scene_info.json')
image_path = os.path.join(output_directory, 'rendered_image.png')

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Gather scene information
scene_info = get_scene_info()

# Save scene information to a JSON file
with open(json_path, 'w') as outfile:
    json.dump(scene_info, outfile, indent=4)

print(f"Scene information saved to {json_path}")

# Render the scene
bpy.ops.render.render(write_still=True)

print(f"Rendered image saved to {image_path}")

# Print all objects in the scene to the console
print("Objects in the scene:")
for obj in bpy.data.objects:
    print(obj.name)
