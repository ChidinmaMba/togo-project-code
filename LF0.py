import json
import boto3

client = boto3.client('dynamodb')

table_name = "businesses"


business_object = {
  "name": {
    "S": ""
  },
  "owner": {
    "M": {
      "firstname": {
        "S": ""
      },
      "lastname": {
        "S": ""
      }
    }
  },
  "cuisine": {
    "SS": [""]
  },
  "email": {
    "S": ""
  },
  "location": {
    "M":{
      "longitude": {
        "S": ""
      },
      "latitude": {
        "S": ""
      }
    }
  },
  "menu": {
    "L":[
          {
            "M":{
              "food-title": {
                "S": ""
              },
              "price": {
                "N": "0"
              },
              "description": {
                "S": ""
              }
            }
          }
    ]
  },
  "operational-hours": {
    "M":{    
      "sunday": {
        "M":{
            "is-open": {
                "BOOL": True
            },
            "open-time": {
                "S": ""
            },
            "close-time": {
                "S": ""
            }
        }
      },
      "monday": {
        "M":{
            "is-open": {
                "BOOL": True
            },
            "open-time": {
                "S": ""
            },
            "close-time": {
                "S": ""
            }
        }
      },
      "tuesady": {
        "M":{
            "is-open": {
                "BOOL": True
            },
            "open-time": {
                "S": ""
            },
            "close-time": {
                "S": ""
            }
        }
      },
      "wednesday": {
        "M":{
            "is-open": {
                "BOOL": True
            },
            "open-time": {
                "S": ""
            },
            "close-time": {
                "S": ""
            }
        }
      },
      "thursday": {
        "M":{
            "is-open": {
                "BOOL": True
            },
            "open-time": {
                "S": ""
            },
            "close-time": {
                "S": ""
            }
        }
      },
      "friday": {
        "M":{
            "is-open": {
                "BOOL": True
            },
            "open-time": {
                "S": ""
            },
            "close-time": {
                "S": ""
            }
        }
      },
      "saturday": {
        "M":{
            "is-open": {
                "BOOL": True
            },
            "open-time": {
                "S": ""
            },
            "close-time": {
                "S": ""
            }
        }
      }
    }
  }
}

def lambda_handler(event, context):
    # TODO implement
    print("event", event)
    if event["request"]["userAttributes"]["email_verified"] == "true":
        print("email verified")
        # add user email to users dynamodb
        business_object["email"] = {
          "S": event["request"]["userAttributes"]["email"]
        }

        data = client.put_item(
            TableName=table_name,
            Item=business_object 
        )
        
    return event
