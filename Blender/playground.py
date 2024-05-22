import bpy
import os
import json

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

# Function to center the camera to include all objects
def set_camera_view():
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        obj.select_set(True)
    bpy.ops.view3d.camera_to_view_selected()

# Ensure all objects are visible and included in the render layers
for obj in bpy.data.objects:
    obj.hide_render = False
    obj.hide_viewport = False


# Define paths for the JSON file and rendered image
output_directory = '/Users/yonghuizhu/Project/Blender/output'
json_path = os.path.join(output_directory, 'scene_info.json')
image_path = os.path.join(output_directory, 'rendered_image.png')

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Set the render settings
bpy.context.scene.camera = bpy.data.objects.get('Camera')
bpy.context.scene.render.filepath = image_path
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Add a cube to the scene
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.object
cube.name = "NewCube"
print("Cube added to the scene")

# Modify cube's location
cube.location.x += 3
cube.location.y += 2
cube.location.z += 1
print("Cube moved to a new location")

# Create a new material
mat = bpy.data.materials.new(name="NewMaterial")
mat.diffuse_color = (1, 0, 0, 1)  # Red color


# Assign the material to the cube
cube.data.materials.append(mat)
print("Red material assigned to the cube")

# Set keyframes for animation
cube.location = (0, 0, 0)
cube.keyframe_insert(data_path="location", frame=1)

cube.location = (5, 5, 5)
cube.keyframe_insert(data_path="location", frame=50)
print("Animation keyframes set for the cube")


# Gather scene information
scene_info = get_scene_info()

# Center the camera to include all objects
set_camera_view()

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
