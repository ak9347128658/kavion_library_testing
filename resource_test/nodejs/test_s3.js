const { S3Client, PutObjectCommand, ListObjectsV2Command, GetObjectCommand } = require("@aws-sdk/client-s3");

const s3 = new S3Client({
  endpoint: "http://172.190.151.19:9000", region: "us-east-1", forcePathStyle: true, maxAttempts: 1, requestHandler: { connectionTimeout: 5000 },
  credentials: { accessKeyId: "onprem-demo-jobs", secretAccessKey:"Test@123" },
});

async function main() {
  // Add data (pskit storage triggers see it on their next poll)
  await s3.send(new PutObjectCommand({ Bucket: "files", Key: "in/hello.txt", Body: "hello" }));

  // List 50 at a time
  const page = await s3.send(new ListObjectsV2Command({ Bucket: "files", MaxKeys: 50 }));
  for (const obj of page.Contents || []) console.log(obj.Key, obj.Size);

  // Read
  const out = await s3.send(new GetObjectCommand({ Bucket: "files", Key: "in/hello.txt" }));
  console.log(await out.Body.transformToString());
}

main();