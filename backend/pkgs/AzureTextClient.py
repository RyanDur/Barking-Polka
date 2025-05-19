import time
from typing import Generator, Callable

import azure.cognitiveservices.speech as speech_sdk
from azure.cognitiveservices.speech import SpeechConfig


class AzureTextClient:

    def __init__(self, config: SpeechConfig):
        self.__channels = 1
        self.__bits_per_sample = 16
        self.__samples_per_second = 16000
        self.__speech_config = config

    def to_text(self, stream: Generator[bytes, None, None], on_transcribed: Callable[[str], None]):
        done = False
        def stop_cb(_):
            nonlocal done
            done = True

        form = speech_sdk.audio.AudioStreamFormat(self.__samples_per_second, self.__bits_per_sample, self.__channels)
        push_stream = speech_sdk.audio.PushAudioInputStream(stream_format=form)
        transcriber = self.__create_transcriber(push_stream)

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

    def __create_transcriber(self, push_stream):
        audio_config = speech_sdk.audio.AudioConfig(stream=push_stream)
        transcriber = speech_sdk.transcription.ConversationTranscriber(self.__speech_config, audio_config)

        transcriber.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        transcriber.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        transcriber.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

        return transcriber