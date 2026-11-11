import os

import boto3
from botocore.config import Config

s3 = boto3.client(
    "s3",
    endpoint_url="http://52.182.190.250:9000",            # http://52.182.190.250:9000
    region_name="us-east-1",
    aws_access_key_id="myuser",
    aws_secret_access_key="TEst@1234",
    config=Config(s3={"addressing_style": "path"}),
)
# s3.put_object(Bucket="mybucket", Key="reports/today.txt", Body=b"hello", ContentType="text/plain")
# print(s3.get_object(Bucket="mybucket", Key="reports/today.txt")["Body"].read())
# s3.upload_file("big.iso", "mybucket", "isos/big.iso")          # multipart for large files
url = s3.generate_presigned_url("get_object", Params={"Bucket": "mybucket", "Key": "reports/today.txt"}, ExpiresIn=60)
print("my usl : ",url)