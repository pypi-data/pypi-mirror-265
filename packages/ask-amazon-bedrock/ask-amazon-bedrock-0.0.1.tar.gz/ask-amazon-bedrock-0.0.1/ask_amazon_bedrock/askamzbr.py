import boto3
import json
import argparse

import logging
import sys
from colorlog import ColoredFormatter
from botocore.exceptions import ClientError

logger = logging.getLogger("ask_amazon_bedrock")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s: %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'white',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red',
    }
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def parse_list_param(param) -> list:
    """
    Parse a comma-separated list parameter into a list.

    :param param: Comma-separated list parameter
    :type param: str
    :return: List of items in the comma-separated list
    """
    if not param:
        return []
    if ',' not in param:
        return [param]
    return param.split(',')


def get_bedrock_insights(bedrock_model, bedrock_region, bedrock_query):
    """
    Get the query as an input and leverage specified Bedrock model and region

    :param bedrock_model: Bedrock Model used to get insights
    :type bedrock_model: str
    :param bedrock_region: Region where Bedrock Model will be invoked
    :type bedrock_region: str
    :param bedrock_query: Query to ask Bedrock model
    :type bedrock_query: str
    
    :return: Bedrock response as text output
    """
    
    model = bedrock_model
    
    bedrock_client = boto3.client('bedrock-runtime', region_name=bedrock_region)
    body = {"messages":[{"role":"user",
                         "content":[{"type":"text","text":bedrock_query}]
                        }],
            "anthropic_version":"bedrock-2023-05-31",
            "max_tokens":4000}
    accept = 'application/json'
    contentType = 'application/json'
    response = bedrock_client.invoke_model(
        body=json.dumps(body), 
        modelId=model, 
        accept=accept, 
        contentType=contentType
    )
    response_body = json.loads(response.get('body').read())
    return response_body.get('content')[0]['text']

def main(bedrock_region, bedrock_model, bedrock_query):

    bedRockInsights = get_bedrock_insights(bedrock_model, bedrock_region, bedrock_query)
    print(bedRockInsights)

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Example script with command-line arguments")
    parser.add_argument('--query', '-q', dest='bedrock_query', type=str,
                        help="Query that you want to post to Amazon Bedrock.", required=True)
    parser.add_argument('--bedrock-region', '-b', dest='bedrock_region', type=str,
                        help="Region where Bedrock Model will be invoked.", default='us-west-2')
    parser.add_argument('--bedrock-model', '-m', dest='bedrock_model', type=str,
                        help="Bedrock Model used to get insights.", default='anthropic.claude-3-sonnet-20240229-v1:0')
    parser.add_argument('--debug', '-d', dest='debug', action='store_true', help="Enable debug mode.",
                        default=False)

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    main(args.bedrock_region,
         args.bedrock_model,
         args.bedrock_query)
