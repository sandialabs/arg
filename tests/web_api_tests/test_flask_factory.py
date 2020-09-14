from web.api import create_app
from flask import json
from unittest import TestCase


class TestFlaskFactory(TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        print('setUp')
        TestFlaskFactory.app = create_app({
            'TESTING': True
        })
        TestFlaskFactory.client = TestFlaskFactory.app.test_client()
        TestFlaskFactory.runner = TestFlaskFactory.app.test_cli_runner()

    def test_config(self):
        """ Tests that changing config value applies correctly """
        self.assertFalse(create_app({'TESTING': False}).testing)
        self.assertTrue(create_app({'TESTING': True}).testing)

    def test_hello(self):
        """ Tests that the hello route correctly returns the expected message """
        response = self.client.get('/api/v1/server/hello/world')
        decoder = json.JSONDecoder()
        responseObject = decoder.decode(str(response.data, 'utf-8'))
        self.assertEqual(responseObject['message'], 'Hello, world!')
