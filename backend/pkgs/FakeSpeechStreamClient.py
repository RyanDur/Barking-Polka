import os
import time
from typing import Generator

import azure.cognitiveservices.speech as speech_sdk
from faker import Faker

speech_region = os.environ.get('SPEECH_REGION')
speech_key = os.environ.get('SPEECH_KEY')
speech_endpoint = f"https://{speech_region}.api.cognitive.microsoft.com"

class FakeSpeechStreamClient:
    def __init__(self):
        self.__fake = Faker()
        speech_config = speech_sdk.SpeechConfig(subscription=speech_key, endpoint=speech_endpoint)
        self.__synth = speech_sdk.speech.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    def speach_stream(self) -> Generator[bytes, None, None]:
        for i in range(10):
            sentence = self.__fake.sentence()
            result = self.__synth.speak_text_async(sentence).get()
            yield result.audio_data