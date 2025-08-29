# EchoVerse - AI Powered Audiobook Creator

EchoVerse is a generative AI-based audiobook creation system that transforms user-provided text into expressive, downloadable audio content. Designed for accessibility, convenience, and content reusability.

## Features

- **Tone-Adaptive Text Rewriting**: Rewrites input text into Neutral, Suspenseful, or Inspiring tones using AI
- **High-Quality Voice Narration**: Converts rewritten text into natural-sounding audio using IBM Watson Text-to-Speech
- **Multiple Voice Options**: Choose from Lisa, Michael, or Allison voices
- **Downloadable Audio**: Download the final narration in .mp3 format for offline use
- **Side-by-Side Text Comparison**: Displays original and tone-adapted text together for easy verification

## Setup Instructions

### 1. Install Dependencies

```bash
pip install streamlit ibm-watson ibm-cloud-sdk-core
```

### 2. IBM Watson Configuration

1. Create an IBM Cloud account at [https://cloud.ibm.com](https://cloud.ibm.com)
2. Enable the following services:
   - **Watsonx AI** (for text rewriting)
   - **Text to Speech** (for audio generation)
3. Get your API keys and service URLs from each service

### 3. Configure Credentials

Edit `.streamlit/secrets.toml` with your actual IBM Watson credentials:

```toml
# Watsonx LLM Service
WATSONX_API_KEY = "your_actual_watsonx_api_key"
WATSONX_URL = "your_actual_watsonx_service_url"

# Watson Text-to-Speech Service
TTS_API_KEY = "your_actual_tts_api_key"
TTS_URL = "your_actual_tts_service_url"
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Usage

1. **Input Text**: Either upload a .txt file or paste text directly
2. **Select Tone**: Choose from Neutral, Suspenseful, or Inspiring
3. **Choose Voice**: Select from Lisa, Michael, or Allison voices
4. **Generate**: Click "Generate Audiobook" to process your text
5. **Download**: Listen to the audio and download the MP3 file

## Technology Stack

- **Frontend**: Streamlit
- **AI Services**: IBM Watsonx (LLM), IBM Watson Text-to-Speech
- **Programming Language**: Python

## File Structure

```
echoverse/
├── app.py                 # Main Streamlit application
├── .streamlit/
│   └── secrets.toml      # Configuration file for credentials
└── README.md             # This file
```

## Note

The current implementation includes a placeholder function for text rewriting. To enable full IBM Watsonx LLM integration, you'll need to:

1. Replace the `rewrite_text_with_watson` function in `app.py` with actual Watsonx API calls
2. Ensure your Watsonx service is properly configured with the appropriate model

## License

This project is for educational/demonstration purposes.
