import os
from unittest import mock

import pytest

from src.main.lambdas.iot_atlas_misc import app


@pytest.fixture()
def motor_driver_event():
    return {
        "address": "N/A",
        "addressType": "N/A",
        "name": "",
        "module": "Motor Driver",
        "version": "0.1",
        "reading": {
            "value": 20,
            "timestamp": 1631054894.9632235
        }
    }


@pytest.fixture()
def etape_event():
    return {
        "name": "rpi-ads1115-etape",
        "module": "eTape",
        "version": "0.2",
        "host": "25ee3924b3fd1ae1280c4442862eb844",
        "addressType": "I2C",
        "address": 72,
        "reading": {
            "type": "level",
            "value": 11483,
            "timestamp": 1633232725.3501136
        }
    }


@mock.patch('botocore.client.BaseClient._make_api_call')
@mock.patch.dict(os.environ, {"MQTT_TOPIC": "my-test-topic", "MQTT_ENDPOINT": "localhost"}, clear=True)
def test_lambda_handler(motor_driver_event):
    response = app.lambda_handler(motor_driver_event, "")
    assert "statusCode" in response
    assert "body" in response
    assert response['statusCode'] == 200
    assert response['body']['topic'] == 'my-test-topic'


@mock.patch('botocore.client.BaseClient._make_api_call')
@mock.patch.dict(os.environ, {"MQTT_TOPIC": "my-test-topic", "MQTT_ENDPOINT": "localhost"}, clear=True)
def test_lambda_handler2(etape_event):
    response = app.lambda_handler(etape_event, "")
    assert "statusCode" in response
    assert "body" in response
    assert response['statusCode'] == 200
    assert response['body']['topic'] == 'my-test-topic'
