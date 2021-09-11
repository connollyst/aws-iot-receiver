import copy
import json
import os

import boto3


def publish_message(client, topic, message):
    try:
        client.publish(topic=topic, payload=json.dumps(message, default=str))
    except Exception as e:
        print(e)
        raise e


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    print(event)
    module = event['module']
    value = event['reading']['value']
    if module == 'RTD':
        type = 'temperature'
        value = float(value)
    elif module == 'Relay':
        type = 'switch'
        if value == 'ON':
            value = 1  # True
        elif value == 'OFF':
            value = 0  # False
        else:
            print('Unsupported switch value: {}'.format(value))
    else:
        type = 'other'
    message = copy.deepcopy(event)
    message['reading']['type'] = type
    message['reading']['value'] = value
    client = boto3.client('iot-data')
    topic = os.environ['IOT_MQTT_TOPIC']
    publish_message(client, topic, message)
    return {
        'statusCode': 200,
        'body': {
            'topic': topic,
            'messages': {
                type: message
            }
        }
    }
