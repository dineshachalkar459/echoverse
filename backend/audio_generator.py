"""Audio generation utilities."""

import os
import tempfile

import streamlit as st
from gtts import gTTS


class AudioGenerator:
    """Generates MP3 audio using Watson or gTTS fallback."""

    @staticmethod
    def generate_audio(text, voice_name=None, watson_service=None):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                if watson_service and watson_service.is_available():
                    try:
                        audio_content = watson_service.synthesize(text, voice_name)
                        tmp_file.write(audio_content)
                    except Exception as exc:
                        st.warning(f"Watson synthesis failed, falling back to gTTS: {exc}")
                        AudioGenerator._use_gtts(text, tmp_file)
                else:
                    AudioGenerator._use_gtts(text, tmp_file)
                return tmp_file.name
        except Exception as exc:
            st.error(f"Error generating audio: {exc}")
            return None

    @staticmethod
    def _use_gtts(text, tmp_file):
        tts = gTTS(text)
        tts.save(tmp_file.name)

    @staticmethod
    def cleanup_audio(audio_path):
        try:
            if audio_path and os.path.exists(audio_path):
                os.unlink(audio_path)
        except Exception as exc:
            st.warning(f"Could not clean up audio file: {exc}")
