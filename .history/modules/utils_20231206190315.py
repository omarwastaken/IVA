import pyttsx3
import os
import datetime
import speech_recognition as sr
import requests  # Needed for ElevenLabs API request

# Choose the text-to-speech engine:
# (1 for pyttsx3, 2 for ElevenLabs)
TTS_ENGINE = 2

# Initialize the text-to-speech engine for pyttsx3
engine = pyttsx3.init() if TTS_ENGINE == 1 else None

# ElevenLabs API credentials and configuration
CHUNK_SIZE = 1024
ELEVENLABS_API_KEY = 'ba51100a1f87c3c2f1361d44d9b082d7'
ELEVENLABS_VOICE = 'Dorothy'


# Define a function to speak text aloud and print it as a subtitle
def speak(text):
    print(f"IVA: {text}")  # Print text as subtitle
    if TTS_ENGINE == 1 and engine is not None:
        engine.say(text)
        engine.runAndWait()
    elif TTS_ENGINE == 2:
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
            }
        }

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE}"

        response = requests.post(url, json=data, headers=headers)
        with open('output.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)

        if response.status_code == 200:
            # Handle the streaming audio content
            pass
        else:
            print(f"Error with ElevenLabs TTS: HTTP Status Code {response.status_code}, Response: {response.text}")


# Define a function to recognize speech
def recognize_speech():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Speak now...")
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You: {text}")  # Print user's speech
            return text
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please try again.")
        except Exception as e:
            print("Oops, something went wrong.")
            print(e)
            return None


# Define a function to generate file name
def generate_file_name(name):
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{name}_{now}.txt"


# Define a function to save text to file
def save_to_file(name, text):
    dir_path = os.path.abspath(os.path.dirname(__file__))

    # Create the directory if it does not exist
    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, generate_file_name(name))
    with open(file_path, 'w') as f:
        f.write(text)
