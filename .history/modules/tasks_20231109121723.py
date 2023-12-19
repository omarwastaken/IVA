import os.path
import re
import spacy

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from modules.utils import speak, save_to_file, recognize_speech

# ======================== Constants ========================
TOKEN_PATH = os.path.join('config', 'tasks_token.json')
CREDENTIALS_PATH = os.path.join('config', 'tasks_credentials.json')
SCOPES = ['https://www.googleapis.com/auth/tasks']

TASK_KEYWORDS = [
    r"\badd (?:to my tasks|to my to-do list)\b",
    r"\bcreate (?:a task|a to-do)\b",
    r"\bmake (?:a task|a to-do)\b",
    r"\bset (?:a task|a to-do)\b"
]

CONFIRMATION_PHRASES = ["yes", "sure", "please do", "go ahead", "of course", "that's right", "correct", "affirmative"]
DECLINING_PHRASES = ["no", "not now", "later", "don't", "cancel", "stop", "negative", "decline"]

# Load the spaCy NLP model
NLP = spacy.load("en_core_web_sm")


# ============ Google Tasks Functions ============

def get_tasks_service():
    """Returns a Google Tasks service object."""
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    else:
        creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())

    return build('tasks', 'v1', credentials=creds)


def insert_google_task(service, task_title, due_date=None, notes=None):
    """Inserts a task into Google Tasks."""
    task_body = {'title': task_title}
    if due_date:
        task_body['due'] = due_date
    if notes:
        task_body['notes'] = notes

    try:
        task = service.tasks().insert(tasklist='@default', body=task_body).execute()
        return task.get('id')
    except Exception as e:
        print(f"Error inserting Google task: {e}")
        return None


def set_google_task(task_title, due_date=None, notes=None):
    """Sets a task in Google Tasks."""
    service = get_tasks_service()
    task_id = insert_google_task(service, task_title, due_date, notes)
    if task_id:
        print(f"Task created with ID: {task_id}")


# ============ Task Handling Functions ============

def is_task_request(user_input):
    """Checks if the user input indicates a task request."""
    user_input_lower = user_input.lower()
    return any(re.search(pattern, user_input_lower) for pattern in TASK_KEYWORDS)


def handle_task_request(user_input, restart_callback):
    """Handles user input for tasks. Returns True if a task was created."""
    if is_task_request(user_input):
        create_task(user_input, restart_callback)
        return True
    return False


def extract_task_content(user_input):
    """Extracts the task content and due date from user input."""
    doc = NLP(user_input)
    task_content = ' '.join([token.text for token in doc])

    # Extract due date using Spacy's NER
    due_date = None
    for ent in doc.ents:
        if ent.label_ == "DATE":
            due_date = ent.text
            task_content = task_content.replace(due_date, "").strip()

    return task_content, due_date


def confirm_and_save_task(task_content, due_date=None):
    """Asks the user for confirmation and saves the task if confirmed."""
    speak(f"Do you want to save this task: {task_content}?")
    user_confirmation = recognize_speech().lower()

    if any(phrase in user_confirmation for phrase in CONFIRMATION_PHRASES):
        save_to_file("task", task_content)
        speak("Task saved successfully!")
        try:
            set_google_task(task_content, due_date)
        except Exception as e:
            speak("There was an error setting the task in Google Tasks.")
            print(f"Error setting Google task: {e}")
    elif any(phrase in user_confirmation for phrase in DECLINING_PHRASES):
        speak("Task not saved.")
    else:
        speak("I didn't understand your response. Please confirm again.")


def create_task(user_input, restart_callback):
    """Creates a task based on user input."""
    task_content, due_date = extract_task_content(user_input)
    if task_content:
        try:
            confirm_and_save_task(task_content, due_date)
        except ValueError:
            speak("Sorry, I didn't understand the task you said. Please say it again.")
    restart_callback()
