# Use the Conversation API to send a text message to Mistral.

import boto3
from botocore.exceptions import ClientError

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Mistral Large.
model_id = "mistral.mistral-large-2402-v1:0"

# Start a multi-turn conversation loop
conversation = []

print("Chat with Mistral (type 'exit' to quit)\n")

while True:
    # Get user message
    user_message = input("You: ").strip()
    
    # Check for exit command
    if user_message.lower() == "exit":
        print("Goodbye!")
        break
    
    # Skip empty messages
    if not user_message:
        continue
    
    # Add user message to conversation
    conversation.append({
        "role": "user",
        "content": [{"text": user_message}],
    })
    
    try:
        # Send the message to the model, using a basic inference configuration.
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        print(f"Mistral AI: {response_text}\n")
        
        # Add assistant response to conversation
        conversation.append({
            "role": "assistant",
            "content": [{"text": response_text}],
        })

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}\n")


