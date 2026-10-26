const { SQSClient, GetQueueUrlCommand, SendMessageCommand } = require("@aws-sdk/client-sqs");

const sqs = new SQSClient({ endpoint:"http://20.127.9.130:8080", region: "us-east-1",
  credentials: { accessKeyId: "pskit", secretAccessKey: "pskit" } });

async function main() {
  const { QueueUrl } = await sqs.send(new GetQueueUrlCommand({ QueueName: "sqs-fun-test-jobs" }));
  await sqs.send(new SendMessageCommand({ QueueUrl, MessageBody: JSON.stringify({ orderId: 1 }) }));
}

main();