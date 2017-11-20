from __future__ import print_function
import boto3
import os
import sys
import uuid
from PIL import Image, ImageOps
     
s3_client = boto3.client('s3')

def thumbnail_image(image, resized_path, width):
    divisor = (image.width // width)
    image.thumbnail(tuple(x / divisor for x in image.size))
    image.save(resized_path, progressive=True, optimize=True, quality=80)
            
def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        #make key equal to the last string, and change switch / to __
        #this fixes an issue where lambda wasn't able to see the file
        key = record['s3']['object']['key']
        download_key=key.split('/',2)[2].replace('/','__')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), download_key)
        upload_path = '/tmp/{}'.format(download_key)
        s3_client.download_file(bucket, key, download_path)
        
        #work on the image
        new_width = 1000
        with Image.open(download_path) as image:
            #Is the W:H ratio > 4:3? If so, it's a panorama and we should crop
            if ((image.width / image.height) > (4/3)):
                pan_height = image.height
                pan_width = (image.height//0.75)
                image = ImageOps.fit(image, (pan_width, pan_height))

            thumbnail_image(image.copy(), upload_path, new_width)
            s3_client.upload_file(upload_path, 
                '{}'.format(bucket), 
                'images/thumbs/{}'.format(download_key.replace('__','/')))