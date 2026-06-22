# chain of thought example using the Mistral model in the Amazon Bedrock Python SDK.

'''
Chain of Thought: Prompt the model to generate a step-by-step explanation or reasoning process before providing the final answer, 
which can help improve performance on complex tasks.
'''

import json
import boto3

client = boto3.client('bedrock-runtime', region_name='us-east-1')

model_id = 'google.gemma-3-12b-it'

messages = [
    {"role": "system", "content": "You are a helpful assistant that explains your reasoning step by step."},
    {"role": "user", "content": "how do you build tiktokenizer app?"},
]

# Send a properly formatted JSON payload expected by many Bedrock models
response = client.invoke_model(
    modelId=model_id,
    contentType='application/json',
    accept='application/json',
    body=json.dumps({"messages": messages}).encode('utf-8'),
)

# Some SDKs return `outputText` directly; others stream bytes under `body`.
if isinstance(response, dict) and 'outputText' in response:
    print('outputText')
    print(response['outputText']['content'])
elif isinstance(response, dict) and 'body' in response:
    print('body')
    print(json.loads(response['body'].read().decode('utf-8')).get('choices', [{}])[0].get('message', {}).get('content', 'No content found'))
else:
    print('Unknown response format')
    print(response)