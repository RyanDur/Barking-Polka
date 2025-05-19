from typing import Generator, List

import azure.cognitiveservices.speech as speech_sdk
from azure.cognitiveservices.speech import SpeechConfig


class FakeSpeechStreamClient:
    def __init__(self, config: SpeechConfig, text: List[str]):
        self.__text = text
        self.__synth = speech_sdk.speech.SpeechSynthesizer(speech_config=config, audio_config=None)

    def speach_stream(self) -> Generator[bytes, None, None]:
        for line in self.__text:
            result = self.__synth.speak_text_async(line).get()
            yield result.audio_data
