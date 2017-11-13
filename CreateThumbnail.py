from __future__ import print_function
import boto3
import os
import sys
import uuid
from PIL import Image, ImageOps
     
s3_client = boto3.client('s3')
     
def resize_image(image_path, resized_path, new_size):
    with Image.open(image_path) as image:
        dimg = ImageOps.fit(image,
            size=(new_size, new_size),
            centering=(0.5, 0.5))
        dimg.save(resized_path)

def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        #make key equal to the last string
        key = record['s3']['object']['key']
        download_key=key.split('/',2)[2].replace('/','__')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), download_key)
        upload_path = '/tmp/{}'.format(download_key)

        #Copy the image to the "hi_res" folder
        #copy_source = {
        #    'Bucket': bucket,
        #    'Key': key
        #}
        #s3.meta.client.copy(copy_source, bucket, 'hi_res/{}'.format(download_key)) 
        s3_client.download_file(bucket, key, download_path)
        for i in [240, 480, 960]:
            resize_image(download_path, upload_path, i)
            s3_client.upload_file(upload_path, '{}'.format(bucket), 'images/{}/{}'.format(i, download_key.replace('__','/')))
