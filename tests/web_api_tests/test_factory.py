from tests.web_api_tests._tests_fixtures import client, app

from web.api import create_app
from flask import json


def test_config():
    """ Tests that changing config value applies correctly """
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_hello(client):
    """ Tests that the hello route correctly returns the expected message """
    response = client.get('/api/v1/general/hello/world')
    decoder = json.JSONDecoder()
    responseObject = decoder.decode(str(response.data, 'utf-8'))
    assert responseObject['message'] == 'Hello, world!'