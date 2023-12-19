import pyttsx3
import os
import datetime

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Define a function to speak text aloud and print it as a subtitle
def speak(text):
    print(f"IVA: {text}")  # Print text as subtitle
    engine.say(text)
    engine.runAndWait()

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
