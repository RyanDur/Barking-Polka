import os
import unittest

from faker import Faker

from backend.pkgs.AzureTextClient import AzureTextClient
from backend.pkgs.FakeSpeechStreamClient import FakeSpeechStreamClient
from backend.pkgs.speach_to_text import SpeechToText

import azure.cognitiveservices.speech as speech_sdk
speech_key =  os.environ.get('SPEECH_KEY')
speech_endpoint = f"https://{os.environ.get('SPEECH_REGION')}.api.cognitive.microsoft.com"

class TestSpeechToText(unittest.TestCase):
    def test_speech_to_text(self):
        Faker.seed(0)
        text = ["hello", "how are you", "I am fine", "thank you", "goodbye"]
        speech_config = speech_sdk.SpeechConfig(subscription=speech_key, endpoint=speech_endpoint)
        speach_to_text = SpeechToText(
            speech_client=FakeSpeechStreamClient(speech_config, text),
            text_client=AzureTextClient(speech_config)
        )

        text = speach_to_text.conversation_stream()

        expected_text = "Hello. How are you? I am fine. Thank you. Goodbye."
        self.assertEqual(expected_text, text)
