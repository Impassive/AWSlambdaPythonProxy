import json
from botocore.vendored import requests
import traceback

'''
Request JSON format for proxy integration
{
	"resource": "Resource path",
	"path": "Path parameter",
	"httpMethod": "Incoming request's method name"
	"headers": {Incoming request headers}
	"queryStringParameters": {query string parameters }
	"pathParameters":  {path parameters}
	"stageVariables": {Applicable stage variables}
	"requestContext": {Request context, including authorizer-returned key-value pairs}
	"body": "A JSON string of the request payload."
	"isBase64Encoded": "A boolean flag to indicate if the applicable request payload is Base64-encode"
}
Response JSON format
{
	"isBase64Encoded": true|false,
	"statusCode": httpStatusCode,
	"headers": { "headerName": "headerValue", ... },
	"body": "..."
}
'''


def response_proxy(data):
    response = {}
    response["isBase64Encoded"] = False
    response["statusCode"] = 200
    response["headers"] = {"Access-Control-Allow-Origin": "*"}
    if "headers" in data:
        response["headers"] = data["headers"]
    response["body"] = data
    print(response)
    return response


def request_proxy(data):
    link = str(data["stageVariables"]["albReferenceIngressAtcUi"])
    path = str(data["pathParameters"]["proxy"])
    method = str(data["requestContext"]["httpMethod"])
    params = '?'
    for key, value in data["queryStringParameters"].items():
        params += key + '=' + value + '&'
        
    print(json.dumps(data))
    if method == 'GET':
        print('Method is GET')
        r = requests.get(link + path + params)
    elif method == 'POST':
        print('Method is POST')
        post_data = str(data["body"])
        r = requests.post(link + path + params, post_data)
    elif method == 'PUT':
        print('Method is PUT')
        put_data = str(data["body"])
        r = requests.put(link + path + params, put_data)
    elif method == 'DELETE':
        print('Method is DELETE')
        delete_data = str(data["body"])
        r = requests.delete(link + path + params, delete_data)
    else:
        print('Unknown method specified')

    return r.text


def handler(event, context):
    try:
        response = request_proxy(event)
    except Exception as e:
        print('Event: ')
        print(json.dumps(event))
        traceback.print_exc()
        #response["statusCode"]=500
        response= '{ "error": "Lambda function internal error" }'	
   
    return response_proxy(response)