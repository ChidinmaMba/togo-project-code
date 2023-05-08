import json
import os
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

REGION = 'us-east-1'
HOST = 'search-reviews-kb4sj7gppw6sxsgw32n3cmmuiq.us-east-1.es.amazonaws.com'
INDEX = 'reviews'

def lambda_handler(event, context):
    print("Recieved event", event)
    body = json.loads(event['body'])
    print(body)
    data = {
        'user-email': body['user-email'],
        'business-email': body['business-email'],
        'rating': body['rating'],
        'review': body['review'],
        'business-reply': body['business-reply']
    }
    
    db = boto3.resource('dynamodb')
    table = db.Table('reviews')
    
    response = table.put_item(Item=data)
    
    print('response: ', response)
    
    review_id = data['user-email'] + '_' + data['business-email']
    search = get_opensearch()
    search.index(
        index=INDEX,
        id=review_id,
        body=data
    )
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
        },
        'body': json.dumps({})
    }

def get_opensearch():
    return OpenSearch(
        hosts=[{'host': HOST, 'port': 443}],
        http_auth=get_awsauth(REGION, 'es'),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

def get_awsauth(region, service):
    cred = boto3.Session().get_credentials()
    return AWS4Auth(cred.access_key,
                    cred.secret_key,
                    region,
                    service,
                    session_token=cred.token)
                    
        
