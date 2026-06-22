# one-shot prompt example
'''
One-shot: Provide the model with a single example of the desired output, and then ask it to generate a similar output for a new input.
'''

import json
import boto3


client = boto3.client('bedrock-runtime', region_name='us-east-1')

model_id = 'google.gemma-3-12b-it'

messages = [
    {"role": "system", "content": "You are a helpful assistant that translates English to French."},
    {"role": "user", "content": "Example:\nEnglish: How are you?\nFrench:"},
    {"role": "assistant", "content": "Comment ça va?"},
    {"role": "user", "content": "Now translate the following sentence:\nEnglish: What is the capital of France?\nFrench:"},
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