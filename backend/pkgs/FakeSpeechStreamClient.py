from typing import Generator

import azure.cognitiveservices.speech as speech_sdk
from azure.cognitiveservices.speech import SpeechConfig
from faker import Faker


class FakeSpeechStreamClient:
    def __init__(self, config: SpeechConfig):
        self.__fake = Faker()
        self.__synth = speech_sdk.speech.SpeechSynthesizer(speech_config=config, audio_config=None)

    def speach_stream(self) -> Generator[bytes, None, None]:
        for i in range(10):
            sentence = self.__fake.sentence()
            result = self.__synth.speak_text_async(sentence).get()
            yield result.audio_data