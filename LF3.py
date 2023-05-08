import json
import os
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

REGION = 'us-east-1'
HOST = 'search-reviews-kb4sj7gppw6sxsgw32n3cmmuiq.us-east-1.es.amazonaws.com'
INDEX = 'reviews'

def lambda_handler(event, context):
    print('Received event: ' + json.dumps(event))
    
    user_email = ""
    business_email = ""
    if 'useremail' in event['queryStringParameters']:
        user_email = event['queryStringParameters']['useremail']
    if 'businessemail' in event['queryStringParameters']:
        business_email = event['queryStringParameters']['businessemail']
        
    if user_email == "":
        reviews = query(business_email, False)
    else:
        reviews = query(user_email, True)
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
        },
        'body': json.dumps({'reviews': reviews})
    }

def query(term, by_user):
    if by_user:
        q = {"query": {"match_phrase": {"user-email": term}}}
    else:
        q = {"query": {"match_phrase": {"business-email": term}}}
    
    print(q)
    
    client = OpenSearch(hosts=[{'host': HOST, 'port': 443}],
    http_auth=get_awsauth(REGION, 'es'),
    use_ssl=True,
    vertify_certs=True,
    connection_class=RequestsHttpConnection)
    
    res = client.search(index=INDEX, body=q)
    print(res)
    
    hits = res['hits']['hits']
    results = []
    for hit in hits:
        results.append(hit['_source'])
    
    return results

def get_awsauth(region, service):
    cred = boto3.Session().get_credentials()
    return AWS4Auth(cred.access_key,
                    cred.secret_key,
                    region,
                    service,
                    session_token=cred.token)

