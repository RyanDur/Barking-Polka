from backend.pkgs import AzureTextClient, FakeSpeechStreamClient


class SpeechToText:
    __text_client: AzureTextClient
    __speech_client: FakeSpeechStreamClient

    def __init__(self, speech_client, text_client):
        self.__speech_client = speech_client
        self.__text_client = text_client

    def conversation_stream(self):
        ongoing_text = ""

        def on_transcribed(text: str):
            nonlocal ongoing_text
            ongoing_text += text

        self.__text_client.to_text(self.__speech_client.speach_stream(), on_transcribed)
        return ongoing_text
