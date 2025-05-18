import os
import time

import azure.cognitiveservices.speech as speechsdk

speech_key = os.environ.get('SPEECH_KEY')
region = os.environ.get('SPEECH_REGION')
speech_endpoint="https://eastus.api.cognitive.microsoft.com"
filename = "output_16kHz_mono.wav"

def speech_recognition():
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, endpoint=speech_endpoint)

    channels = 1
    bits_per_sample = 16
    samples_per_second = 16000

    synth = speechsdk.speech.SpeechSynthesizer(speech_config=speech_config, audio_config=None)


    # Create audio configuration using the push stream
    wave_format = speechsdk.audio.AudioStreamFormat(samples_per_second, bits_per_sample, channels)
    stream = speechsdk.audio.PushAudioInputStream(stream_format=wave_format)
    audio_config = speechsdk.audio.AudioConfig(stream=stream)

    transcriber = speechsdk.transcription.ConversationTranscriber(speech_config, audio_config)

    done = False

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous transcription upon receiving an event `evt`"""
        print('CLOSING {}'.format(evt))
        nonlocal done
        done = True

    # Subscribe to the events fired by the conversation transcriber
    transcriber.transcribed.connect(lambda evt: print('TRANSCRIBED: {}'.format(evt)))
    transcriber.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    transcriber.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    transcriber.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    # stop continuous transcription on either session stopped or canceled events
    transcriber.session_stopped.connect(stop_cb)
    transcriber.canceled.connect(stop_cb)

    transcriber.start_transcribing_async()
    text = ["hello", "how are you", "I am fine", "thank you", "goodbye"]
    # Read the whole wave files at once and stream it to sdk

    for line in text:
        print(line)
        foo = synth.speak_text_async(line)
        result = foo.get()
        stream.write(result.audio_data)

    stream.close()
    stream.close()
    while not done:
        time.sleep(.5)

    transcriber.stop_transcribing_async()

speech_recognition()