import sys
try:
    import bpy
except ImportError:
    print("Blender Python module 'bpy' not found.")
    sys.exit(1)
import json
import os
from metagpt.actions import Action

class AddObjectToBlender(Action):
    PROMPT_TEMPLATE: str = """
    Add a {object_type} to the Blender scene at location {location}.
    """

    name: str = "AddObjectToBlender"

    async def run(self, object_type: str, location: tuple):
        # Add the object to the Blender scene
        if object_type == "cube":
            bpy.ops.mesh.primitive_cube_add(size=2, location=location)
        elif object_type == "circle":
            bpy.ops.mesh.primitive_circle_add(radius=1, location=location)
        elif object_type == "uv_sphere":
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=location)
        else:
            raise ValueError("Unsupported object type")
        
        # Get the added object
        obj = bpy.context.object
        return obj.name

class VerifyBlenderScene(Action):
    PROMPT_TEMPLATE: str = """
    Verify the Blender scene by rendering an image and saving scene information.
    """

    name: str = "VerifyBlenderScene"

    async def run(self):
        output_directory = '/Users/yonghuizhu/Project/Blender/output'
        json_path = os.path.join(output_directory, 'scene_info.json')
        image_path = os.path.join(output_directory, 'rendered_image.png')

        # Ensure all objects are visible and included in the render layers
        for obj in bpy.data.objects:
            obj.hide_render = False
            obj.hide_viewport = False

        # Set the render settings and ensure the camera is set up correctly
        bpy.context.scene.camera = bpy.data.objects.get('Camera')
        bpy.context.scene.render.filepath = image_path
        bpy.context.scene.render.image_settings.file_format = 'PNG'

        # Gather scene information
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

        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)

        # Save scene information to a JSON file
        with open(json_path, 'w') as outfile:
            json.dump(scene_info, outfile, indent=4)

        print(f"Scene information saved to {json_path}")

        # Render the scene
        bpy.ops.render.render(write_still=True)

        print(f"Rendered image saved to {image_path}")

        return {
            "scene_info_path": json_path,
            "rendered_image_path": image_path
        }
