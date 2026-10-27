import boto3

sm = boto3.client("secretsmanager", endpoint_url="http://172.172.72.97:4584", region_name="us-east-1",
                  aws_access_key_id="onprem-demo-jobs", aws_secret_access_key="Test@1234")
print(sm.get_secret_value(SecretId="kavion/dev")["SecretString"])