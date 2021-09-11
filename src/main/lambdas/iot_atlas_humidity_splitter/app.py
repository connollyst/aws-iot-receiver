import copy
import json
import os

import boto3


def split(reading):
    readings = reading.split(',')
    humidity_reading = float(readings.pop(0))
    temp_reading = None
    dew_reading = None
    if 'Dew' in readings:
        dew_index = readings.index('Dew')
        dew_label = readings.pop(dew_index)
        dew_reading = float(readings.pop(dew_index))
    if (len(readings)):
        temp_reading = float(readings.pop())
    if (len(readings)):
        raise Error('Unexpected reading: {}'.format(readings))
    print('Humidity: {}'.format(humidity_reading))
    print('Temperature: {}'.format(temp_reading))
    print('Dew Point: {}'.format(dew_reading))
    return humidity_reading, temp_reading, dew_reading


def construct(event, humidity_reading, temp_reading, dew_reading):
    humidity_message = construct_message(event, 'humidity', humidity_reading)
    temp_message = construct_message(event, 'temperature', temp_reading)
    dew_message = construct_message(event, 'dew', dew_reading)
    return humidity_message, temp_message, dew_message


def construct_message(event, label, reading):
    if reading:
        message = copy.deepcopy(event)
        message['reading']['type'] = label
        message['reading']['value'] = reading
        return message
    else:
        return None


def publish(client, topic, humidity_message, temp_message, dew_message):
    if humidity_message:
        publish_message(client, topic, humidity_message)
    if temp_message:
        publish_message(client, topic, temp_message)
    if dew_message:
        publish_message(client, topic, dew_message)


def publish_message(client, topic, message):
    try:
        client.publish(topic=topic, payload=json.dumps(message))
    except Exception as e:
        print(e)
        raise e


def lambda_handler(event, context):
    reading = event['reading']['value']
    if reading == 'Err':
        return {
            'statusCode': 400,
            'body': 'Invalid raw humidity sensor reading: Err'
        }
    humidity_reading, temp_reading, dew_reading = split(reading)
    humidity_message, temp_message, dew_message = construct(event, humidity_reading, temp_reading, dew_reading)
    client = boto3.client('iot-data')
    topic = os.environ['IOT_MQTT_TOPIC']
    publish(client, topic, humidity_message, temp_message, dew_message)
    return {
        'statusCode': 200,
        'body': {
            'topic': topic,
            'messages': {
                'humidity': humidity_message,
                'temp': temp_message,
                'dew': dew_message
            }
        }
    }
