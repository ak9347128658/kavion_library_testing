import boto3

ses = boto3.client(
    "sesv2",
    endpoint_url="http://172.173.102.50:4579",
    region_name="us-east-1",
    aws_access_key_id="myuser",
    aws_secret_access_key="Test@1234",
)
out = ses.send_email(
    FromEmailAddress="sender@asifkhanofficial.in",
    Destination={"ToAddresses": ["ak2311581@gmail.com","Asif.Khan@Kavion.ai"]},
    Content={"Simple": {"Subject": {"Data": "Hello from SES"}, "Body": {"Text": {"Data": "It works."}}}},
)
print(out["MessageId"])