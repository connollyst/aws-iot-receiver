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


@mock.patch('botocore.client.BaseClient._make_api_call')
@mock.patch.dict(os.environ, {"IOT_MQTT_TOPIC": "my-test-topic"}, clear=True)
def test_lambda_handler(motor_driver_event):
    response = app.lambda_handler(motor_driver_event, "")
    assert "statusCode" in response
    assert "body" in response
    assert response['statusCode'] == 200
    assert response['body']['topic'] == 'my-test-topic'
