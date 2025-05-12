import json
import unittest
from unittest.mock import patch

from faker import Faker
from starlette.testclient import TestClient

from backend.app.main import app, ServerEvent


class TestChatEvents(unittest.TestCase):

    @patch('time.sleep', return_value=None)
    def test_chat_events(self, sleep_mock):
        Faker.seed(0)
        client = TestClient(app)

        response = client.get("/api/events")

        self.assertEqual(response.status_code, 200)

        expected = "".join([
            str(ServerEvent(event="chat", data=json.dumps({
                "voice": "friend 2",
                "message": "American whole magazine truth stop whose.",
                "id": 0,
            }))),
            str(ServerEvent(event="chat", data=json.dumps({
                "voice": "friend 2",
                "message": "Through despite cause cause believe son would mouth.",
                "id": 1,
            }))),
            str(ServerEvent(event="chat", data=json.dumps({
                "voice": "friend 1",
                "message": "Better available sure form nice.",
                "id": 2,
            }))),
            str(ServerEvent(event="chat", data=json.dumps({
                "voice": "friend 2",
                "message": "First policy daughter need kind miss.",
                "id": 3,
            }))),
            str(ServerEvent(event="chat", data=json.dumps({
                "voice": "friend 1",
                "message": "Trouble behavior style report size personal partner.",
                "id": 4,
            })))
        ])

        self.assertEqual(expected, response.text)
        self.assertEqual(5, sleep_mock.call_count)
