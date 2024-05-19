import boto3
import json

from .prompts import SUMMARY_PROMPT_BEFORE, SUMMARY_PROMPT_AFTER

class AWSBedrockConnection:
    def __init__(self, region='us-east-1'):
        self.client = boto3.client(
            'bedrock-runtime'
        )
        
    def query_model(self, input_data, task='summary', modelId='amazon.titan-text-express-v1'):
        
        if task == 'summary':
            prompt_before = SUMMARY_PROMPT_BEFORE
            prompt_after = SUMMARY_PROMPT_AFTER
        else:
            raise Exception('Task not defined for using AWS Bedrock.')
        
        query = f"""{prompt_before}
                
            {input_data}
            
            {prompt_after}"""
        
        body = json.dumps({
            "inputText": query,
            "textGenerationConfig": {
                "maxTokenCount": 2048,
                "stopSequences": ["User:"],
                "temperature": 0,
                "topP": 0.9
            }
        })
        
        accept = 'application/json'
        content_type = 'application/json'
        
        response = self.client.invoke_model(body=body, modelId=modelId, accept=accept, contentType=content_type)
        response_body = json.loads(response.get('body').read().decode('utf-8'))['results'][0]['outputText']
        
        return {
            'task': task,
            'output': response_body
        }
    