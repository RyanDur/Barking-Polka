import unittest
import uuid
from typing import List
from unittest.mock import patch

from async_asgi_testclient import TestClient
from faker import Faker

from backend.app.main import app


async def collect_events_data(response) -> List[str]:
    events = []
    async for event in response.iter_content(None):
        message_content: str = event.strip().decode()
        events.append(message_content)
    return events


class TestChatEvents(unittest.IsolatedAsyncioTestCase):

    @patch('uuid.uuid4', return_value=uuid.UUID('123e4567-e89b-12d3-a456-426614174000'))
    async def test_chat_events(self, uuid_mock):
        Faker.seed(0)
        client = TestClient(app)

        response = await client.get("/api/events", stream=True)

        line = await anext(response.iter_content(None))
        self.assertEqual(
            line,
            b'event:chat\ndata:{"voice": "friend 2", "message": "American whole magazine truth stop whose.", "id": "123e4567e89b12d3a456426614174000"}\n\n'
        )
        response.close()
        self.assertEqual(response.status_code, 200)
        uuid_mock.assert_called_once()
