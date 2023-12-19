import datetime
import os.path
import re
import spacy
import parsedatetime as pdt
from dateutil import parser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from tzlocal import get_localzone

from modules.utils import speak, save_to_file, recognize_speech

# ======================== Constants ========================

TOKEN_PATH = os.path.join('config', 'token.json')
CREDENTIALS_PATH = os.path.join('config', 'credentials.json')
SCOPES = ['https://www.googleapis.com/auth/calendar']
CONFIRMATION_PHRASES = [
    "yes", "sure", "please do", "go ahead", "of course",
    "that's right", "correct", "affirmative"
]
DECLINING_PHRASES = [
    "no", "not now", "later", "don't", "cancel",
    "stop", "negative", "decline"
]
REMINDER_KEYWORDS = [
    "remind", "remember", "remind me", "set a reminder",
    "add to my reminders"
]

# ============ Google Calendar Functions ============

def get_calendar_service():
    """Returns a Google Calendar service object."""
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def insert_google_event(service, event):
    """Inserts an event into Google Calendar and returns the event link."""
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        return event.get('htmlLink')
    except Exception as e:
        if "The requested identifier already exists" in str(e):
            return "The reminder already exists in the calendar."
        else:
            # Log the error or handle specific exceptions here
            print(f"Error inserting Google event: {e}")
            return None

def set_google_reminder(date_str, time_str, reminder_content, is_recurring):
    """Sets a reminder in Google Calendar."""
    service = get_calendar_service()
    local_timezone = str(get_localzone())
    reminder_datetime_str = f"{date_str} {time_str}"
    reminder_datetime_obj = datetime.datetime.strptime(reminder_datetime_str, '%Y-%m-%d %I:%M %p')
    rfc_datetime = reminder_datetime_obj.isoformat()

    event = {
        'summary': reminder_content,
        'start': {'dateTime': rfc_datetime, 'timeZone': local_timezone},
        'end': {'dateTime': rfc_datetime, 'timeZone': local_timezone},
        'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}]},
    }

    if is_recurring:
        event['recurrence'] = ['RRULE:FREQ=DAILY']

    event_link = insert_google_event(service, event)
    print(f"Event created: {event_link}")

# ============ Reminder Handling Functions ============

def is_reminder_request(user_input):
    """Determines if the user_input indicates a reminder request."""
    user_input_lower = user_input.lower()

    # Clear intent patterns
    clear_intent_patterns = ["remind me to", "set a reminder to", "add to my reminders to"]

    # Inquiry patterns
    inquiry_patterns = ["can we set a reminder", "is it possible to set", "how do i set", "can you set reminders"]

    # Vague or incomplete commands
    vague_commands = ["let's set a reminder", "i need a reminder", "can you remind me something",
                      "can you set a reminder for"]

    return any(pattern in user_input_lower for pattern in clear_intent_patterns + inquiry_patterns + vague_commands)

def handle_reminder_request(user_input, restart_callback):
    """Handles a reminder request from user input."""
    if is_reminder_request(user_input):

        # If the user is making an inquiry or a vague command
        inquiry_patterns = ["can we set a reminder", "is it possible to set", "how do i set", "can you set reminders",
                            "let's set a reminder", "i need a reminder", "can you remind me something",
                            "can you set a reminder for"]
        if any(pattern in user_input.lower() for pattern in inquiry_patterns):
            speak(
                "Yes, you can set a reminder. Please provide the details of what you'd like to be reminded about and when.")
            return True

        # If the user provides a direct command
        else:
            create_reminder(user_input, restart_callback)
            return True
    return False

def confirm_and_save_reminder(reminder_content, date_str, time_str, is_recurring):
    """Asks the user for confirmation and saves the reminder if confirmed."""
    reminder_datetime_str = f"{date_str} {time_str}"
    reminder_datetime_obj = parser.parse(reminder_datetime_str)
    formatted_time = reminder_datetime_obj.strftime('%I:%M %p')
    formatted_date = reminder_datetime_obj.strftime('%Y-%m-%d')
    if is_recurring:
        reminder = f"Okay, I'll remind you every day at {formatted_time} to {reminder_content}."
    else:
        reminder = f"Okay, I'll remind you on {formatted_date} at {formatted_time} to {reminder_content}."
    speak(reminder)

    # Debugging: Print the reminder content, date, and time
    print(f"Reminder content: {reminder_content}")
    print(f"Date: {date_str}")
    print(f"Time: {time_str}")

    # Confirmation and saving
    speak("Do you want to save this reminder?")
    user_confirmation = recognize_speech().lower()

    if any(phrase in user_confirmation for phrase in CONFIRMATION_PHRASES):
        save_to_file("reminder", reminder)
        speak("Reminder saved successfully!")
        try:
            set_google_reminder(date_str, time_str, reminder_content, is_recurring)
        except Exception as e:
            print(f"Error setting Google reminder: {e}")
            speak("There was an error setting the reminder on Google Calendar.")
    elif any(phrase in user_confirmation for phrase in DECLINING_PHRASES):
        speak("Reminder not saved.")
    else:
        speak("I didn't understand your response. Please confirm again.")

def create_reminder(user_input, restart_callback):
    """Creates a reminder based on user input."""
    date_str, time_str, is_recurring = get_reminder_datetime(user_input)
    reminder_content = get_reminder_content(user_input, date_str, time_str)
    if reminder_content and time_str:
        try:
            confirm_and_save_reminder(reminder_content, date_str, time_str, is_recurring)
        except ValueError:
            speak("Sorry, I didn't understand the time or date you said. Please say it again in a recognized format.")
    restart_callback()

# ============ Utility and Extraction Functions ============

def generate_time_formats(time_str):
    """Generate multiple formats for a given time string."""
    base_time = time_str.lstrip('0').lower()
    # Convert "06:00 AM" to "6:00 a.m."
    time_alternate = base_time.replace(' ', '.').replace('am', 'a.m.').replace('pm', 'p.m.')
    # Convert "06:00 AM" to "6 a.m."
    time_short = base_time.split(':')[0].replace('am', 'a.m.').replace('pm', 'p.m.')
    return [time_str, time_alternate, time_short]

def extract_datetime(user_input):
    """Extracts date and time from user input."""
    cal = pdt.Calendar()
    time_struct, parse_status = cal.parse(user_input)
    datetime_obj = datetime.datetime(*time_struct[:6])

    # If the parsed date is in the past, assume next month
    today = datetime.datetime.today()
    if datetime_obj.date() < today.date():
        datetime_obj = datetime_obj.replace(month=datetime_obj.month % 12 + 1)

    # If the day is mentioned but not the month, and the parsed day is the 1st, adjust to the mentioned day
    if "on the" in user_input and datetime_obj.day == 1:
        match = re.search(r"on the (\d+)(st|nd|rd|th)", user_input)
        if match:
            mentioned_day = int(match.group(1))
            datetime_obj = datetime_obj.replace(day=mentioned_day)

    # Adjust time based on common phrases
    time_adjustments = {
        "morning": 7,
        "afternoon": 13,
        "evening": 19,
        "night": 21
    }
    if datetime_obj.time() == datetime.time(0, 0):
        for phrase, hour in time_adjustments.items():
            if phrase in user_input:
                datetime_obj = datetime_obj.replace(hour=hour)
                break

    date_str = datetime_obj.strftime('%Y-%m-%d')
    time_str = datetime_obj.strftime('%I:%M %p')
    is_recurring = "every day" in user_input or "everyday" in user_input
    return date_str, time_str, is_recurring

def extract_reminder_content(user_input, date_str, time_str):
    """Extracts the reminder content from user input."""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(user_input)

    # Remove date and time entities identified by spaCy
    content_tokens = [token.text for token in doc if token.ent_type_ not in ['DATE', 'TIME', 'ORDINAL']]

    # If the word "at" is followed by a time entity, remove it
    for i, token in enumerate(doc[:-1]):
        if token.text.lower() == "at" and doc[i + 1].ent_type_ == 'TIME':
            content_tokens.remove(token.text)

    # Define a list of phrases that should be removed entirely from the reminder content
    removal_phrases = r"\b(?:could you|can you|can we|let's|remind me to|set a reminder to|add to my reminders to|remind me|set a reminder|add to my reminders|please|I need a reminder to|I have a|I need to|set a reminder for|set a reminder called|on the|at|every day)\b"

    # Remove these phrases from the content using regex
    content = ' '.join(content_tokens)
    content = re.sub(removal_phrases, '', content).strip()

    # Use regular expressions to remove date and time patterns
    date_pattern = re.compile(r'\b' + re.escape(date_str) + r'\b')
    content = date_pattern.sub('', content)
    time_formats = generate_time_formats(time_str)
    for time_format in time_formats:
        time_pattern = re.compile(r'\b' + re.escape(time_format) + r'\b')
        content = time_pattern.sub('', content)
    content = content.replace("  ", " ")
    content = content.strip(":")

    return content

def get_reminder_content(user_input, date_str, time_str):
    """Extracts or asks the user for the reminder content."""
    reminder_content = extract_reminder_content(user_input, date_str, time_str)
    if not reminder_content:
        speak("What do you want me to remind you about?")
        reminder_content = recognize_speech()
    return reminder_content

def get_reminder_datetime(user_input):
    """Extracts or asks the user for the reminder date and time."""
    date_str, time_str, is_recurring = extract_datetime(user_input)
    if not date_str or not time_str:
        speak("When do you want to be reminded?")
        reminder_time_input = recognize_speech()
        date_str, time_str, _ = extract_datetime(reminder_time_input)
    return date_str, time_str, is_recurring