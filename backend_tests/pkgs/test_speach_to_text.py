import os
import unittest

import azure.cognitiveservices.speech as speech_sdk

from backend.pkgs.AzureTextClient import AzureTextClient
from backend.pkgs.FakeSpeechStreamClient import FakeSpeechStreamClient
from backend.pkgs.speach_to_text import SpeechToText

speech_key =  os.environ.get('SPEECH_KEY')
speech_region = os.environ.get('SPEECH_REGION')

class TestSpeechToText(unittest.TestCase):
    def test_speech_to_text(self):
        text = ["hello", "how are you", "I am fine", "thank you", "goodbye"]
        speech_config = speech_sdk.SpeechConfig(subscription=speech_key, region=speech_region)
        speach_to_text = SpeechToText(
            speech_client=FakeSpeechStreamClient(speech_config, text),
            text_client=AzureTextClient(speech_config)
        )

        text = speach_to_text.conversation_stream()

        expected_text = "Hello. How are you? I am fine. Thank you. Goodbye."
        self.assertEqual(expected_text, text)
