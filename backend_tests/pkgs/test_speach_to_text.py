import unittest

from faker import Faker

from backend.pkgs.AzureTextClient import AzureTextClient
from backend.pkgs.FakeSpeechStreamClient import FakeSpeechStreamClient
from backend.pkgs.speach_to_text import SpeechToText


class TestSpeechToText(unittest.TestCase):
    def test_speech_to_text(self):
        Faker.seed(0)
        speach_to_text = SpeechToText(
            speech_client=FakeSpeechStreamClient(),
            text_client=AzureTextClient()
        )

        text = speach_to_text.conversation_stream()

        expected_text = "Serious inside else memory IF6 whose group through despite cause sense peace economy travel total financial role together range line beyond its policy daughter need kindness artist truth trouble rest human station property partner stock 4 region as true develop sound central language ball floor meet usually board necessary.Natural sport music White."
        self.assertEqual(expected_text, text)
