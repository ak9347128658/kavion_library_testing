const { SQSClient, SendMessageCommand, ReceiveMessageCommand, DeleteMessageCommand } = require("@aws-sdk/client-sqs");

const sqs = new SQSClient({ region: "us-east-1", endpoint: "http://20.127.19.12:9324", credentials: { accessKeyId: "pskit", secretAccessKey: "pskit" }, maxAttempts: 1, requestHandler: { connectionTimeout: 5000 } });
const QUEUE = "http://20.127.19.12:9324/000000000000/jobs";

async function main() {
  // Add data
  await sqs.send(new SendMessageCommand({ QueueUrl: QUEUE, MessageBody: JSON.stringify({ orderId: 1 }) }));

  // Read and delete (only if no pskit trigger consumes this queue)
  const out = await sqs.send(new ReceiveMessageCommand({ QueueUrl: QUEUE, MaxNumberOfMessages: 10, WaitTimeSeconds: 2 }));
  for (const msg of out.Messages || []) {
    console.log("processing", msg.Body);
    await sqs.send(new DeleteMessageCommand({ QueueUrl: QUEUE, ReceiptHandle: msg.ReceiptHandle }));
  }
}

main();