import requests
import json
# ElevenLabs API credentials and configuration
CHUNK_SIZE = 1024
ELEVENLABS_API_KEY = 'ba51100a1f87c3c2f1361d44d9b082d7' # Replace with your actual API key
ELEVENLABS_VOICE = 'ThT5KcBeYPX3keUQqHPh'               # You can Find voices using EL_Voices.py
XI_API_KEY = "ba51100a1f87c3c2f1361d44d9b082d7"  # Replace with your actual API key

url = "https://api.elevenlabs.io/v1/voices"
headers = {
    "Accept": "application/json",
    "xi-api-key": XI_API_KEY,
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
data = response.json()

for voice in data['voices']:
    print(f"{voice['name']}; {voice['voice_id']}")
