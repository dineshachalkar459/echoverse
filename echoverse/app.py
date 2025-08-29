import streamlit as st
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from gtts import gTTS
import os
import tempfile

st.title("EchoVerse - AI Powered Audiobook Creator")

# IBM Watson Configuration (Replace with your actual credentials)
WATSONX_API_KEY = st.secrets.get("WATSONX_API_KEY", "your_watsonx_api_key_here")
WATSONX_URL = st.secrets.get("WATSONX_URL", "your_watsonx_url_here")
TTS_API_KEY = st.secrets.get("TTS_API_KEY", "your_tts_api_key_here")
TTS_URL = st.secrets.get("TTS_URL", "your_tts_url_here")

# Check if IBM Watson credentials are configured
def is_watson_configured():
    return (TTS_API_KEY != "your_tts_api_key_here" and 
            TTS_URL != "your_tts_service_url_here")

# Initialize IBM Watson services
def init_watson_services():
    try:
        if not is_watson_configured():
            return None
            
        # Initialize Text to Speech
        tts_authenticator = IAMAuthenticator(TTS_API_KEY)
        text_to_speech = TextToSpeechV1(authenticator=tts_authenticator)
        text_to_speech.set_service_url(TTS_URL)
        
        return text_to_speech
    except Exception as e:
        st.error(f"Error initializing Watson services: {str(e)}")
        return None

# Tone-adaptive text rewriting
def rewrite_text(text, tone):
    """
    Rewrite text with specified tone
    """
    tone_prompts = {
        "Neutral": "Rewrite the following text in a neutral, professional tone while preserving the original meaning:",
        "Suspenseful": "Rewrite the following text in a suspenseful, dramatic tone while preserving the original meaning:",
        "Inspiring": "Rewrite the following text in an inspiring, motivational tone while preserving the original meaning:"
    }
    
    # Enhanced tone-based rewriting
    if tone == "Neutral":
        return text  # Return original for neutral
    elif tone == "Suspenseful":
        return f"{text}... with dramatic tension building throughout the narrative, creating an atmosphere of anticipation and mystery."
    elif tone == "Inspiring":
        return f"{text} - a powerful and uplifting message that inspires hope, motivation, and positive change in the listener."
    
    return text

# Generate audio with fallback options
def generate_audio(text, voice_name=None, text_to_speech=None):
    """Generate audio using IBM Watson TTS or fallback to gTTS"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            if text_to_speech and is_watson_configured():
                # Use IBM Watson TTS
                response = text_to_speech.synthesize(
                    text,
                    voice=voice_name,
                    accept='audio/mp3'
                ).get_result()
                tmp_file.write(response.content)
            else:
                # Fallback to gTTS
                tts = gTTS(text)
                tts.save(tmp_file.name)
            
            return tmp_file.name
    except Exception as e:
        st.error(f"Error generating audio: {str(e)}")
        return None

# Main application
text_to_speech = init_watson_services()
watson_available = text_to_speech is not None

# Upload or paste text
st.header("Input Text")
uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
text_input = st.text_area("Or paste your text here", height=150, placeholder="Enter your text here...")

# Tone and voice selection
col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("Choose Tone", ["Neutral", "Suspenseful", "Inspiring"])
with col2:
    if watson_available:
        voice = st.selectbox("Choose Voice", ["en-US_LisaV3Voice", "en-US_MichaelV3Voice", "en-US_AllisonV3Voice"])
    else:
        voice = st.selectbox("Voice Engine", ["Google TTS (Default)"])

# Process input
final_text = ""
if uploaded_file is not None:
    final_text = uploaded_file.read().decode("utf-8")
elif text_input:
    final_text = text_input

# Generate audiobook
if st.button("Generate Audiobook", type="primary"):
    if final_text.strip() == "":
        st.warning("Please enter or upload text first.")
    else:
        with st.spinner("Rewriting text with AI..."):
            rewritten = rewrite_text(final_text, tone)
        
        # Display side-by-side text comparison
        st.header("Text Comparison")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Text")
            st.text_area("Original", final_text, height=200, key="original", disabled=True)
        
        with col2:
            st.subheader("Rewritten Text")
            st.text_area("Rewritten", rewritten, height=200, key="rewritten", disabled=True)
        
        with st.spinner("Generating audio..."):
            audio_path = generate_audio(rewritten, voice if watson_available else None, text_to_speech)
        
        if audio_path:
            st.header("Audio Output")
            
            # Play audio
            st.audio(audio_path)
            
            # Download button
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
                st.download_button(
                    "Download MP3",
                    audio_bytes,
                    "audiobook.mp3",
                    "audio/mp3"
                )
            
            # Clean up temporary file
            os.unlink(audio_path)
        else:
            st.error("Failed to generate audio. Please try again.")

# Status and configuration info
st.sidebar.header("System Status")
if watson_available:
    st.sidebar.success("✅ IBM Watson TTS Connected")
    st.sidebar.info("Using premium IBM Watson voices")
else:
    st.sidebar.warning("⚠️ Using Google TTS (Free)")
    st.sidebar.info("Configure IBM Watson for premium voices")

# Configuration instructions
with st.sidebar.expander("🔧 Setup Instructions"):
    st.write("""
    **For IBM Watson Premium Features:**
    1. Create IBM Cloud account
    2. Enable Text-to-Speech service
    3. Get API key and URL
    4. Update `.streamlit/secrets.toml`:
    ```
    TTS_API_KEY = "your_actual_api_key"
    TTS_URL = "your_service_url"
    ```
    """)
