import os
from unittest import mock

import pytest

from src.main.lambdas.iot_atlas_humidity_splitter import app


@pytest.fixture()
def valid_event():
    return {
        "address": 104,
        "name": "",
        "module": "HUM",
        "version": "1.0",
        "reading": {
            "value": "70.74,29.47,Dew,23.61",
            "timestamp": "2021-09-05 03:13:14.954163"
        }
    }


@mock.patch('botocore.client.BaseClient._make_api_call')
@mock.patch.dict(os.environ, {"IOT_MQTT_TOPIC": "my-test-topic"}, clear=True)
def test_lambda_handler(boto3, valid_event):
    response = app.lambda_handler(valid_event, "")
    assert "statusCode" in response
    assert "body" in response
    assert response['statusCode'] == 200
    assert response['body']['topic'] == 'my-test-topic'
