import os
import boto3
import json
import openai
import bpy
import asyncio
import typer
from botocore.exceptions import NoCredentialsError


# Set your AWS and OpenAI credentials
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Function to upload a file to S3
def upload_to_s3(file_name, bucket, object_name=None):
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    try:
        s3_client.upload_file(file_name, bucket, object_name or file_name)
        print(f"File uploaded to https://{bucket}.s3.amazonaws.com/{object_name or file_name}")
        return f"https://{bucket}.s3.amazonaws.com/{object_name or file_name}"
    except FileNotFoundError:
        print("The file was not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None

# Function to interact with OpenAI API
def interact_with_openai(image_url, task):
    openai.api_key = OPENAI_API_KEY
    MODEL = "gpt-4"

    client = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that responds in Markdown. Help me verify the blender scene!"},
            {"role": "user", "content": [{"type": "text", "text": f"Is the {task} completed? Here is the image"}, 
                                     {"type": "image_url", "image_url":{"url":f"{image_url}"}}]}   
            ],
        temperature=0.5,
    )

    return client['choices'][0]['message']['content']

# Function to add an object to Blender
def add_object_to_blender(object_type: str, location: tuple):
    if object_type == "cube":
        bpy.ops.mesh.primitive_cube_add(size=2, location=location)
    elif object_type == "circle":
        bpy.ops.mesh.primitive_circle_add(radius=1, location=location)
    elif object_type == "uv_sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=location)
    else:
        raise ValueError("Unsupported object type")
    obj = bpy.context.object
    return obj.name

# Function to render the Blender scene and save the image
def render_blender_scene(output_directory):
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

    return image_path, json_path

# Main function using Typer
app = typer.Typer()

@app.command()
def main(
    object_type: str = typer.Argument(default="cube", help="Type of object to add (cube, circle, uv_sphere)"),
    location: str = typer.Argument(default="0,0,0", help="Location to place the object, format: 'x,y,z'"),
):
    location_tuple = tuple(map(float, location.split(',')))

    # Add object to Blender
    obj_name = add_object_to_blender(object_type, location_tuple)
    print(f"Added {object_type} named {obj_name} at location {location_tuple}")

    # Render Blender scene and save the image
    output_directory = '/Users/yonghuizhu/Project/Blender/output'
    image_path, json_path = render_blender_scene(output_directory)

    # Upload the rendered image to S3
    object_name = 'rendered_image.png'
    image_url = upload_to_s3(image_path, BUCKET_NAME, object_name)

    if image_url:
        print("Image URL:", image_url)
        task = f"{object_type} at {location}"
        response = interact_with_openai(image_url, task)
        print(response)

if __name__ == '__main__':
    app()
