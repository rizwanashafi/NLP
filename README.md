# Urdu Voice Assistant ChatBot

A small Streamlit application that listens to a question in Urdu, sends it to Google's Gemini model through LangChain, and speaks the Urdu response aloud using Google Text-to-Speech.

This project is a good starting point for learning how speech recognition, generative AI, and text-to-speech work together in a simple browser-based app.

## Features

- 🎙️ Records voice directly from the browser
- 🇵🇰 Recognizes spoken Urdu using `streamlit-mic-recorder`
- 🤖 Generates a helpful Pure Urdu response with Gemini
- 🔊 Converts the generated response to Urdu audio with gTTS
- 💻 Runs locally through a clean Streamlit interface
- ⚡ Uses LangChain for the prompt and response pipeline

## How It Works

1. The app activates the browser microphone.
2. The recorded Urdu speech is converted into text.
3. LangChain sends the text to the Gemini model with an Urdu-only system prompt.
4. Gemini creates a response in Urdu.
5. gTTS saves the response as `output.mp3`.
6. Streamlit plays the audio back to the user.

```text
Microphone → Speech-to-Text → Gemini AI → Text Output → Urdu Audio
```

## Project Structure

```text
audio_urdu_chatbot/
├── audio_app.py       # Main Streamlit application
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## Requirements

- Windows 10 or 11
- Python 3.10 or newer
- A working microphone
- A modern browser such as Chrome, Edge, or Firefox
- A Google Gemini API key
- An internet connection

## Google Gemini API Key

Before running the app, add a valid Gemini API key in `audio_app.py`:

```python
api_key = "YOUR_GOOGLE_API_KEY"
```

You can create an API key from Google AI Studio:

https://aistudio.google.com/app/apikey

> **Security reminder:** Never commit a real API key or share it publicly. For a production app, store the key in an environment variable or Streamlit secrets instead of writing it directly in source code.

## Installation

Open PowerShell and move into the project folder:

```powershell
cd "C:\Users\new gen\Documents\audio_urdu_chatbot"
```

### 1. Create a virtual environment

```powershell
python -m venv .venv
```

### 2. Activate the virtual environment

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Command Prompt:

```powershell
.venv\Scripts\activate.bat
```

If PowerShell blocks script execution, allow scripts for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the App

Make sure the virtual environment is active, then run:

```powershell
streamlit run audio_app.py
```

Streamlit will print a local URL, normally:

```text
http://localhost:8501
```

Open that address in your browser. Allow microphone access when prompted, press the recording control, speak an Urdu question, and wait for the response.

## Example Usage

Try asking:

- "پاکستان کا دارالحکومت کیا ہے؟"
- "پانی کی اہمیت بیان کریں۔"
- "ایک مختصر کہانی سنائیں۔"
- "اردو میں صحت مند غذا کے فوائد لکھیں۔"

The model should return a response in Pure Urdu, and the app will also read it aloud.

## Configuration Notes

The app is currently configured for:

- **Recognition language:** Urdu (`ur`)
- **Output language:** Urdu (`ur`)
- **Gemini model:** `gemini-1.5-flash`
- **Audio output file:** `output.mp3`

Model names and API availability can change over time. If Gemini reports that a model is unavailable, replace `gemini-1.5-flash` with a currently supported model available to your Google account.

## Common Problems

### Microphone permission is not appearing

- Open the browser permission settings.
- Allow microphone access for `localhost`.
- Close and reopen the Streamlit page.

### The app says that speech could not be recognized

- Check that your microphone is connected and not muted.
- Speak clearly and relatively close to the microphone.
- Keep background noise low.
- Grant browser microphone permission.

### Authentication or API errors appear

- Confirm that `api_key` contains a valid Gemini API key.
- Confirm that Gemini API access is enabled for the key.
- Check that the selected model is supported by your account.
- Restart Streamlit after changing the API key.

### Audio does not play

- Confirm that `output.mp3` was created in the project folder.
- Check browser autoplay and audio settings.
- Make sure your system output device is working.

### Module not found errors

Reinstall dependencies inside the activated virtual environment:

```powershell
python -m pip install -r requirements.txt
```

## Security and Privacy

- Spoken text is sent to Google's AI service for processing.
- Generated text is sent to Google's text-to-speech service.
- Do not use the app with sensitive, confidential, or private information unless you understand the applicable API privacy and data policies.
- Add proper secret management before deploying the app publicly.

## Possible Improvements

- Store the API key using Streamlit secrets or environment variables
- Maintain chat history across multiple questions
- Add a text input option as a microphone fallback
- Add a language selector
- Let users choose a voice or playback speed
- Improve error handling and loading states
- Display a recording status indicator
- Add a download button for the generated audio
- Deploy securely with Streamlit Community Cloud or another host

## Technologies Used

- [Streamlit](https://streamlit.io/) - Web interface
- [LangChain](https://python.langchain.com/) - Prompt and model orchestration
- [Google Gemini](https://ai.google.dev/) - Generative AI response
- [streamlit-mic-recorder](https://github.com/B4PT0R/streamlit-mic-recorder) - Browser microphone recording
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) - Speech recognition support
- [gTTS](https://gtts.readthedocs.io/) - Google Text-to-Speech

## License

Add a license here if you plan to share or publish this project. For example, an MIT license allows others to use and modify the project with attribution.

## Acknowledgements

Built as a simple educational project to explore Urdu voice interaction, language models, and Streamlit. Small projects like this are a useful bridge between an idea and a working AI experience.
