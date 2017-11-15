from __future__ import print_function
import boto3
import os
import sys
import uuid
from PIL import Image
import PIL.Image
     
s3_client = boto3.client('s3')
     
def resize_image(image_path, resized_path, width):
    with Image.open(image_path) as image:
        image.thumbnail(tuple(x / 4 for x in image.size))
        image.save(resized_path)
     
def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        #make key equal to the last string
        key = record['s3']['object']['key']
        download_key=key.split('/',2)[2].replace('/','__')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), download_key)
        upload_path = '/tmp/{}'.format(download_key)

        s3_client.download_file(bucket, key, download_path)
        for width in [200, 400, 600, 800]:
            resize_image(download_path, upload_path, width)
            s3_client.upload_file(upload_path, '{}'.format(bucket), 'images/thumbs/{}'.format(download_key.replace('__','/')))