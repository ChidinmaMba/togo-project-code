import json
import os
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

REGION = 'us-east-1'
HOST = 'search-businesses-t3ncb2x2xqsltqorlegtclcz6i.us-east-1.es.amazonaws.com'
INDEX = 'businesses'

def lambda_handler(event, context):
    print("Event: " + json.dumps(event))
    print("Method: " + event['httpMethod'])

    email = event['queryStringParameters']['email']
    longitude = event['queryStringParameters']['longitude']
    latitude = event['queryStringParameters']['latitude']
    radius = event['queryStringParameters']['radius']
    results = query(email, longitude, latitude, radius)
    print(results)
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
        },
        'body': json.dumps(results)
    }

def query(email, longitude, latitude, radius):
    q = {'query': 
        {'multi_match': 
            {'query': term
                
            }
        }
    }
    if email == "":
        q = {
              "query": {
                "bool": {
                  "must": {
                    "match_all": {}
                  },
                  "filter": {
                    "geo_distance": {
                      "distance": radius,
                      "pin.location": {
                        "lat": float(latitude),
                        "lon": float(longitude)
                      }
                    }
                  }
                }
              }
            }
 
    print("Query body: " + json.dumps(q))
    client = OpenSearch(hosts=[{
        'host': HOST,
        'port': 443
    }],
                        http_auth=get_awsauth(REGION, 'es'),
                        use_ssl=True,
                        verify_certs=True,
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
