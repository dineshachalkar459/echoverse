"""
Watson service integration for EchoVerse.
"""

import streamlit as st
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def is_watson_configured():
    """Return True when IBM Watson TTS credentials are configured."""
    tts_api_key = st.secrets.get("TTS_API_KEY", "your_tts_api_key_here")
    tts_url = st.secrets.get("TTS_URL", "your_tts_url_here")
    return tts_api_key != "your_tts_api_key_here" and tts_url != "your_tts_url_here"


class WatsonService:
    """Wrapper for IBM Watson Text-to-Speech service."""

    def __init__(self):
        self.api_key = st.secrets.get("TTS_API_KEY", "your_tts_api_key_here")
        self.url = st.secrets.get("TTS_URL", "your_tts_url_here")
        self.service = None

        if is_watson_configured():
            self._initialize_service()

    def _initialize_service(self):
        try:
            authenticator = IAMAuthenticator(self.api_key)
            self.service = TextToSpeechV1(authenticator=authenticator)
            self.service.set_service_url(self.url)
        except Exception as exc:
            st.error(f"Error initializing Watson services: {exc}")
            self.service = None

    def is_available(self):
        return self.service is not None

    def synthesize(self, text, voice):
        if not self.is_available():
            raise Exception("Watson service not available")

        response = self.service.synthesize(text, voice=voice, accept="audio/mp3").get_result()
        return response.content
