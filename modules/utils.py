import pyttsx3
import os
import datetime
import speech_recognition as sr
import pygame
import requests

# ======================== Constants ========================

# Input mode: (1 for typing, 2 for speech-to-text)
INPUT_MODE = 1

# Choose the text-to-speech engine: (1 for pyttsx3, 2 for ElevenLabs)
TTS_ENGINE = 2

# ElevenLabs API credentials and configuration
CHUNK_SIZE = 1024
ELEVENLABS_API_KEY = ''   # Replace with your actual API key
ELEVENLABS_VOICE = 'ThT5KcBeYPX3keUQqHPh' 

# Initialize the text-to-speech engine for pyttsx3
engine = pyttsx3.init() if TTS_ENGINE == 1 else None

def speak(text):
    """Function to speak text aloud and print"""
    print(f"IVA: {text}")
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
        if response.status_code == 200:
            audio_file = 'output.mp3'
            pygame.mixer.init()
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            with open(audio_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.quit()
        else:
            print(f"Error with ElevenLabs TTS: HTTP Status Code {response.status_code}, Response: {response.text}")

def recognize_speech():
    """Function to recognize speech"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
    try:
        text = r.recognize_google(audio)
        print(f"You: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please try again.")
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
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, generate_file_name(name))
    with open(file_path, 'w') as f:
        f.write(text)
