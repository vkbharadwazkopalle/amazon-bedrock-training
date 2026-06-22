# Paramater Tuning for Bedrock Models
'''
Parameter Tuning: Adjust the model's parameters to optimize its performance for specific tasks or datasets.
'''

import json
import boto3

client = boto3.client('bedrock-runtime', region_name='us-east-1')

prompt = "What are the latest advancements in LLM floating point operations?"

model_id_1 = 'mistral.mistral-large-2402-v1:0'
model_id_2 = 'google.gemma-3-12b-it'

response1 = client.converse(
    modelId=model_id_2,
    messages=[{"role": "user", "content": [{"text": prompt}]}],
    inferenceConfig={"maxTokens": 200, "temperature": 0.2, "topP": 0.9},
)

response2 = client.converse(
    modelId=model_id_2,
    messages=[{"role": "user", "content": [{"text": prompt}]}],
    inferenceConfig={"maxTokens": 200, "temperature": 0.9, "topP": 0.9},
)

print("Response with temperature 0.2:")
print(response1["output"]["message"]["content"][0]["text"])

print("\nResponse with temperature 0.9:")
print(response2["output"]["message"]["content"][0]["text"])