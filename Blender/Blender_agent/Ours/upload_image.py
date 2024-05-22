import boto3
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv

from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
# AWS credentials (replace with your actual credentials)
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')
BUCKET_NAME = 'blenderproject'

def upload_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket"""
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

# File to upload
file_name = '/Users/yonghuizhu/Project/Blender/output/rendered_image.png'
object_name = 'rendered_image.png'  # The name of the object in S3

# Upload the file to S3 and get the URL
image_url = upload_to_s3(file_name, BUCKET_NAME, object_name)

if image_url:
    print("Image URL:", image_url)
    MODEL = "gpt-4o"

    client = OpenAI(
       api_key=openai_api_key)

    task = "cube 0 0 0"
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
        {"role": "system", "content": "You are a helpful assistant that responds in Markdown. Help me verify the blender scene!"},
        {"role": "user", "content": [{"type": "text", "text": f"Is the {task} completed? Here is the image"}, 
                                     {"type": "image_url", "image_url":{"url":f"{image_url}"}}]}
        ],
        temperature=0.5,
    )

print(response.choices[0].message.content)