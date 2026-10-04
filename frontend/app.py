"""Frontend entry point for EchoVerse."""

import os
import sys

import streamlit as st

# Add project root to import backend modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.audio_generator import AudioGenerator
from backend.text_processor import TextProcessor
from backend.watson_service import WatsonService


def initialize_session_state():
    if "watson_service" not in st.session_state:
        st.session_state.watson_service = WatsonService()


def render_header():
    st.title("🎙️ EchoVerse - AI Powered Audiobook Creator")
    st.markdown("Transform your text into expressive, downloadable audio with AI-powered tone adaptation")


def render_input_section():
    st.header("📝 Input Text")
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
    text_input = st.text_area("Or paste your text here", height=150, placeholder="Enter your text here...")

    final_text = ""
    if uploaded_file is not None:
        try:
            final_text = uploaded_file.read().decode("utf-8")
        except Exception as exc:
            st.error(f"Error reading file: {exc}")
    elif text_input:
        final_text = text_input

    return final_text


def render_tone_and_voice_section(watson_available):
    col1, col2 = st.columns(2)

    with col1:
        tone = st.selectbox("🎵 Choose Tone", ["Neutral", "Suspenseful", "Inspiring"])

    with col2:
        if watson_available:
            voice = st.selectbox("🎤 Choose Voice", ["en-US_LisaV3Voice", "en-US_MichaelV3Voice", "en-US_AllisonV3Voice"])
        else:
            voice = st.selectbox("🎤 Voice Engine", ["Google TTS (Default)"])

    return tone, voice


def render_text_comparison(original_text, rewritten_text):
    st.header("📋 Text Comparison")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Text")
        st.text_area("Original", original_text, height=200, key="original", disabled=True)

    with col2:
        st.subheader("Rewritten Text")
        st.text_area("Rewritten", rewritten_text, height=200, key="rewritten", disabled=True)


def render_audio_output(audio_path):
    st.header("🎵 Audio Output")
    st.audio(audio_path)

    try:
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
            st.download_button("📥 Download MP3", audio_bytes, "audiobook.mp3", "audio/mp3")
    except Exception as exc:
        st.error(f"Error preparing download: {exc}")


def render_system_status(watson_available):
    st.sidebar.header("⚙️ System Status")
    if watson_available:
        st.sidebar.success("✅ IBM Watson TTS Connected")
        st.sidebar.info("Using premium IBM Watson voices")
    else:
        st.sidebar.warning("⚠️ Using Google TTS (Free)")
        st.sidebar.info("Configure IBM Watson for premium voices")


def render_setup_instructions():
    with st.sidebar.expander("🔧 Setup Instructions"):
        st.markdown(
            """
            ### For IBM Watson Premium Features:
            1. Create IBM Cloud account
            2. Enable Text-to-Speech service
            3. Get API key and URL
            4. Update `.streamlit/secrets.toml`
            ```
            TTS_API_KEY = "your_actual_api_key"
            TTS_URL = "your_service_url"
            ```
            """
        )


def render_features():
    with st.sidebar.expander("✨ Features"):
        st.markdown(
            """
            - 🎨 **Tone-Adaptive Text Rewriting**
            - 🎤 **Multiple Voices**
            - 🔊 **High-Quality Audio**
            - 📥 **Download MP3**
            - 📋 **Text Comparison**
            """
        )


def main():
    st.set_page_config(page_title="EchoVerse", page_icon="🎙️", layout="wide")
    initialize_session_state()
    render_header()

    final_text = render_input_section()
    watson_service = st.session_state.watson_service
    watson_available = watson_service.is_available()
    tone, voice = render_tone_and_voice_section(watson_available)

    if st.button("🚀 Generate Audiobook", type="primary", use_container_width=True):
        if not final_text.strip():
            st.warning("⚠️ Please enter or upload text first.")
        else:
            try:
                with st.spinner("🤖 Rewriting text with AI..."):
                    rewritten = TextProcessor.rewrite_text(final_text, tone)

                render_text_comparison(final_text, rewritten)

                with st.spinner("🎵 Generating audio..."):
                    audio_path = AudioGenerator.generate_audio(rewritten, voice if watson_available else None, watson_service)

                if audio_path:
                    render_audio_output(audio_path)
                    AudioGenerator.cleanup_audio(audio_path)
                    st.success("✅ Audiobook generated successfully!")
                else:
                    st.error("❌ Failed to generate audio. Please try again.")
            except Exception as exc:
                st.error(f"❌ An error occurred: {exc}")

    render_system_status(watson_available)
    render_setup_instructions()
    render_features()

    st.sidebar.markdown("---")
    st.sidebar.markdown("**EchoVerse** - AI Powered Audiobook Creator | Built with Streamlit & IBM Watson")


if __name__ == "__main__":
    main()
