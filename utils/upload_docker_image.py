import os, sys
import boto3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--region', help='S3 exist region')
parser.add_argument('--bucket', help='target S3 bucket')
parser.add_argument('--file_path', help='target file path')
args = parser.parse_args()

client = boto3.client('s3', region_name=args.region)

response = client.upload_file(args.file_path, args.bucket, 'docker_images/' + args.file_path.split(os.sep)[-1])

print (response)



