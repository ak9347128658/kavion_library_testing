import json

import boto3
from botocore.config import Config

# Fail in seconds when the port is closed, instead of retrying for minutes
quick = Config(connect_timeout=5, read_timeout=25, retries={"total_max_attempts": 1, "mode": "standard"})
sqs = boto3.client("sqs", region_name="us-east-1", endpoint_url="http://13.72.87.80:9324", aws_access_key_id="pskit", aws_secret_access_key="pskit", config=quick)
QUEUE = "http://13.72.87.80:9324/000000000000/jobs"

# Add data
sqs.send_message(QueueUrl=QUEUE, MessageBody=json.dumps({"order_id": 143}))

# How many are waiting
print(sqs.get_queue_attributes(QueueUrl=QUEUE, AttributeNames=["ApproximateNumberOfMessages"]))

# Read and delete (only if no pskit trigger consumes this queue)
for msg in sqs.receive_message(QueueUrl=QUEUE, MaxNumberOfMessages=10, WaitTimeSeconds=2).get("Messages", []):
    print("processing", msg["Body"])
    sqs.delete_message(QueueUrl=QUEUE, ReceiptHandle=msg["ReceiptHandle"])