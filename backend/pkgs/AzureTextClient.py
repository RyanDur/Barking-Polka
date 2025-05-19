import time
from typing import Generator, Callable

import azure.cognitiveservices.speech as speech_sdk
from azure.cognitiveservices.speech import SpeechConfig


class AzureTextClient:

    def __init__(self, config: SpeechConfig):
        channels = 1
        bits_per_sample = 16
        samples_per_second = 16000
        self.__speech_config = config
        self.__format = speech_sdk.audio.AudioStreamFormat(samples_per_second, bits_per_sample, channels)

    def to_text(self, stream: Generator[bytes, None, None], on_transcribed: Callable[[str], None]):
        done = False

        def stop_cb(_):
            nonlocal done
            done = True

        push_stream = speech_sdk.audio.PushAudioInputStream(stream_format=self.__format)
        audio_config = speech_sdk.audio.AudioConfig(stream=push_stream)
        transcriber = speech_sdk.transcription.ConversationTranscriber(self.__speech_config, audio_config)

        transcriber.transcribed.connect(lambda evt: on_transcribed(evt.result.text))
        transcriber.session_stopped.connect(stop_cb)
        transcriber.canceled.connect(stop_cb)

        transcriber.start_transcribing_async()

        for chunk in stream:
            push_stream.write(chunk)

        push_stream.close()
        while not done:
            time.sleep(.5)

        transcriber.stop_transcribing_async()
