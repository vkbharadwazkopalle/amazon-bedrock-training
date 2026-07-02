import boto3
import dotenv
import os


dotenv.load_dotenv()

bedrock_client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

self_mng_kb_id = os.getenv('SELF_MNG_KB_ID')
mng_kb_id = os.getenv('MNG_KB_ID')
model_arn = os.getenv('MODEL_ARN')


def query_self_managed_kb(query: str) -> str:
    """Query a self-managed knowledge base and let Bedrock generate an answer."""
    response = bedrock_client.retrieve_and_generate(
        input={'text': query},
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': self_mng_kb_id,
                # on-demand models only
                'modelArn': model_arn
            }
        }
    )

    return response['output']['text']


def query_managed_kb(query: str) -> str:
    """Query an AWS-managed knowledge base and return the retrieved passages."""
    response = bedrock_client.retrieve(
        retrievalQuery={'text': query},
        knowledgeBaseId=mng_kb_id,
        retrievalConfiguration={
            "managedSearchConfiguration": {
                "numberOfResults": 2
            }
        }
    )

    results = sorted(response.get('retrievalResults', []), key=lambda r: r.get('score', 0), reverse=True)
    passages = [r.get('content', {}).get('text', '') for r in results]

    scores = [r.get('score', 0) for r in results]
    print(f"Retrieved {len(passages)} passages with scores: {scores}")
    return "\n\n---\n\n".join(passages)
