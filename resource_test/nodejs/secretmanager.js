
const {
  SecretsManagerClient,
  GetSecretValueCommand,
} = require("@aws-sdk/client-secrets-manager");

const sm = new SecretsManagerClient({
  endpoint: "http://20.29.119.221:4584",
  region: "us-east-1",
  credentials: {
    accessKeyId: "onprem-demo-jobs",
    secretAccessKey: "Test@1234",
  },
});

async function getSecret() {
  try {
    const response = await sm.send(
      new GetSecretValueCommand({
        SecretId: "upadhi/dev",
      })
    );

    console.log(response.SecretString);
  } catch (error) {
    console.error("Failed to retrieve secret:", error.message);
  }
}

getSecret();
