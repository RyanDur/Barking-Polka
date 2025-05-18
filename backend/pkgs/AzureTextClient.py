import time
from typing import Generator, Callable
import os

import azure.cognitiveservices.speech as speech_sdk


class AzureTextClient:

    def __init__(self):
        channels = 1
        bits_per_sample = 16
        samples_per_second = 16000
        self.done = False
        self.__wave_format = speech_sdk.audio.AudioStreamFormat(samples_per_second, bits_per_sample, channels)
        self.__speech_config = speech_sdk.SpeechConfig(
            subscription=os.environ.get('SPEECH_KEY'),
            region=os.environ.get('SPEECH_REGION'))

    def to_text(self, stream: Generator[bytes, None, None], on_transcribed: Callable[[str], None]):
        push_stream, transcriber = self.__create_stream(on_transcribed)

        for chunk in stream:
            push_stream.write(chunk)

        push_stream.close()

        while not self.done:
            time.sleep(.5)

        transcriber.stop_transcribing_async()

    def __create_stream(self, on_transcribed: Callable[[str], None]):
        push_stream = speech_sdk.audio.PushAudioInputStream(stream_format=self.__wave_format)
        audio_config = speech_sdk.audio.AudioConfig(stream=push_stream)

        transcriber = speech_sdk.transcription.ConversationTranscriber(self.__speech_config, audio_config)
        transcriber.transcribed.connect(lambda evt: on_transcribed(evt.result.text))
        transcriber.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        transcriber.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        transcriber.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
        transcriber.session_stopped.connect(self.__stop_cb)
        transcriber.canceled.connect(self.__stop_cb)
        transcriber.start_transcribing_async()

        return (push_stream, transcriber)

    def __stop_cb(self):
        self.done = True

