import boto3  

client = boto3.client("bedrock-runtime", region_name="us-east-1")  

with open("README.md", "rb") as f: 
    doc_bytes = f.read()  

response = client.converse( 
    modelId="amazon.nova-pro-v1:0",
    messages=[{ 
        "role": "user", 
        "content": [ 
            { "document": { 
                  "format": "md", 
                  "name": "document", 
                  "source": {"bytes": doc_bytes} 
                } 
             }, 
             {"text": "Summarize this document."} 
         ] 
    }] 
)  
print(response["output"]["message"]["content"][0]["text"])
# print(response)