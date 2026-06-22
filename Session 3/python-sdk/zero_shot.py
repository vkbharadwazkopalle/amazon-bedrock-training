# zero-shot prompt example

'''
Zero-shot: Give the model an instruction without examples, 
relying on its pre-trained knowledge and reasoning abilities to generate a response.
'''
import json
import boto3

client = boto3.client('bedrock-runtime', region_name='us-east-1')

model_id = 'google.gemma-3-12b-it'

messages = [
    {"role": "system", "content": "You are a helpful assistant that translates English to Swahili."},
    {"role": "user", "content": "Translate the following sentence:\nEnglish: I would like a cup of coffee.\nSwahili:"},
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
