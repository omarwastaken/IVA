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
from modules.utils import save_to_file

# ======================== Google Calendar API Constants ========================

# Define constants for Google Calendar API
TOKEN_PATH = os.path.join('config', 'token.json')  # Path to store access token
CREDENTIALS_PATH = os.path.join('config', 'credentials.json')  # Path to store API credentials
SCOPES = ['https://www.googleapis.com/auth/calendar']  # Required scopes for Google Calendar access

# ======================== User Interaction Phrases ========================
# Define phrases for interaction with the user

# Phrases for user confirmation
CONFIRMATION_PHRASES = [
    "yes", "sure", "please do", "go ahead", "of course",
    "that's right", "correct", "affirmative"
]
# Phrases for user declining
DECLINING_PHRASES = [
    "no", "not now", "later", "don't", "cancel",
    "stop", "negative", "decline"
]
# Keywords that trigger reminder creation
REMINDER_PHRASES = [
    "remind", "remember", "remind me", "set a reminder",
    "add to my reminders"
]
# Patterns indicating a clear intent to set a reminder
CLEAR_INTENT_PHRASES = [
    "remind me to", "set a reminder to", "add to my reminders to"
]
# Patterns indicating a question or inquiry about setting a reminder
INQUIRY_PHRASES = [
    "can we set a reminder", "is it possible to set",
    "how do i set", "can you set reminders",
    "let's set a reminder", "i need a reminder",
    "can you remind me something", "can you set a reminder for"
]
# Less specific commands that imply a reminder is needed
VAGUE_PHRASES = [
    "let's set a reminder", "i need a reminder",
    "can you remind me something", "can you set a reminder for"
]
# Phrases to be removed when parsing reminder content
REMOVAL_PHRASES = (
    r"\b(?:could you|can you|can we|let's|remind me to|set a reminder to|"
    r"add to my reminders to|remind me|set a reminder|add to my reminders|"
    r"please|I need a reminder to|I have a|I need to|set a reminder for|"
    r"set a reminder called|on the|at|every day)\b"
)

# ============ Google Calendar Functions ============

def get_calendar_service():
    """Authenticates and returns a service object to interact with Google Calendar"""
    creds = None
    # Check if token file exists to reuse credentials
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    # Refresh or create new credentials if not valid    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request()) # Refresh existing credentials
        else:
            # Initiate new authentication flow if no valid credentials
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            # Save new credentials to file
            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def insert_google_event(service, event):
    """Inserts an event into Google Calendar and handles potential exceptions"""
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        return event.get('htmlLink') # Return the link to the created event
    except Exception as e:
        if "The requested identifier already exists" in str(e):
            return "The reminder already exists in the calendar."
        else:
            print(f"Error inserting Google event: {e}")
            return None

def set_google_reminder(date_str, time_str, reminder_content, is_recurring):
    """Creates a Google Calendar event based on provided reminder details"""
    service = get_calendar_service()
    local_timezone = str(get_localzone()) # Get the local timezone
    reminder_datetime_str = f"{date_str} {time_str}"
    reminder_datetime_obj = datetime.datetime.strptime(reminder_datetime_str, '%Y-%m-%d %I:%M %p')
    rfc_datetime = reminder_datetime_obj.isoformat() # Convert to RFC3339 format
    event = {
        'summary': reminder_content,
        'start': {'dateTime': rfc_datetime, 'timeZone': local_timezone},
        'end': {'dateTime': rfc_datetime, 'timeZone': local_timezone},
        'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}]},
    }
    if is_recurring:
        event['recurrence'] = ['RRULE:FREQ=DAILY'] # Set recurrence for daily reminders
    event_link = insert_google_event(service, event)
    print(f"Event created: {event_link}")

# ============ Reminder Handling Functions ============

def is_reminder_request(user_input):
    """Determines if the user input is a request to set a reminder"""
    user_input_lower = user_input.lower()
    return any(pattern in user_input_lower for pattern in CLEAR_INTENT_PHRASES + INQUIRY_PHRASES + VAGUE_PHRASES)

def handle_reminder_request(user_input):
    """Processes a user input to handle a reminder request"""
    response_messages = []
    if is_reminder_request(user_input):
        if any(pattern in user_input.lower() for pattern in INQUIRY_PHRASES):
            response_messages.append(
                "Yes, you can set a reminder. Please provide the details.")
            return response_messages
        else:
            response_from_create = create_reminder(user_input)
            response_messages.extend(response_from_create)
            return response_messages
    return False

def save_reminder(reminder_content, date_str, time_str, is_recurring):
    """Saves reminder details and creates a Google Calendar event"""
    response_messages = []
    reminder_datetime_str = f"{date_str} {time_str}"
    reminder_datetime_obj = parser.parse(reminder_datetime_str)
    formatted_time = reminder_datetime_obj.strftime('%I:%M %p')
    formatted_date = reminder_datetime_obj.strftime('%Y-%m-%d')
    if is_recurring:
        reminder = f"Okay, I'll remind you every day at {formatted_time} to {reminder_content}."
    else:
        reminder = f"Okay, I'll remind you on {formatted_date} at {formatted_time} to {reminder_content}."
    try:
        save_to_file("reminder", reminder)
        response_messages.append("Reminder saved successfully.")
        set_google_reminder(date_str, time_str, reminder_content, is_recurring)
    except Exception as e:
        print(f"Error setting Google reminder: {e}")
        response_messages.append("There was an error setting the reminder on Google Calendar.")
    return response_messages

def create_reminder(user_input):
    """Main function to create a reminder from user input"""
    response_messages = []
    date_str, time_str, is_recurring = get_reminder_datetime(user_input)
    reminder_content = get_reminder_content(user_input, date_str, time_str)
    if reminder_content and time_str:
        try:
            response_from_save = save_reminder(reminder_content, date_str, time_str, is_recurring)
            response_messages.extend(response_from_save)
        except ValueError:
            response_messages.append("Couldn't understand the time or date. Please re-enter.")
    return response_messages

def get_reminders_for_period(period):
    """Retrieves reminders from Google Calendar for a given time period (day or week)"""
    service = get_calendar_service()
    tz = get_localzone()
    now = datetime.datetime.now(tz)
    time_min = now.isoformat()
    if period == 'day':
        time_max = (now + datetime.timedelta(days=1)).isoformat()
    elif period == 'week':
        time_max = (now + datetime.timedelta(weeks=1)).isoformat()
    else:
        raise ValueError("Invalid period specified. Choose 'day' or 'week'.")
    events_result = service.events().list(calendarId='primary', timeMin=time_min, timeMax=time_max, singleEvents=True, orderBy='startTime').execute()
    print("Debug - Raw API Response:", events_result)

    events = events_result.get('items', [])
    formatted_events = []
    for event in events:
        if 'dateTime' in event['start']:
            start_time = datetime.datetime.fromisoformat(event['start']['dateTime'])
            formatted_start = start_time.strftime('%H:%M%p')
        elif 'date' in event['start']:
            formatted_start = "All Day"
        else:
            formatted_start = "No Time"
        formatted_events.append({'summary': event.get('summary', 'No Title'), 'time': formatted_start, 'id': event.get('id')})
    return formatted_events

def mark_reminder_as_done(event_id):
    """Marks a reminder in Google Calendar as completed"""
    service = get_calendar_service()
    try:
        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        event['status'] = 'cancelled'
        updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    except Exception as e:
        print(f"Error updating reminder status: {e}")
        raise

# ============ Utility and Extraction Functions ============

def generate_time_formats(time_str):
    """Generates different time formats for string comparison"""
    base_time = time_str.lstrip('0').lower()
    time_alternate = base_time.replace(' ', '.').replace('am', 'a.m.').replace('pm', 'p.m.')
    time_short = base_time.split(':')[0].replace('am', 'a.m.').replace('pm', 'p.m.')
    return [time_str, time_alternate, time_short]

def extract_datetime(user_input):
    """Extracts date and time information from user input"""
    cal = pdt.Calendar()
    # Use parsedatetime to parse natural language date and time
    time_struct, parse_status = cal.parse(user_input)
    datetime_obj = datetime.datetime(*time_struct[:6])
    # Adjust for dates set in the past
    today = datetime.datetime.today()
    if datetime_obj.date() < today.date():
        datetime_obj = datetime_obj.replace(month=datetime_obj.month % 12 + 1)
    # Adjust for 'on the XXth' phrases in user input
    if "on the" in user_input and datetime_obj.day == 1:
        match = re.search(r"on the (\d+)(st|nd|rd|th)", user_input)
        if match:
            mentioned_day = int(match.group(1))
            datetime_obj = datetime_obj.replace(day=mentioned_day)
    # Adjust for general time phrases like 'morning', 'evening'
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
    """Extracts the main content of the reminder from user input"""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(user_input)
    content_tokens = [token.text for token in doc if token.ent_type_ not in ['DATE', 'TIME', 'ORDINAL']]
    for i, token in enumerate(doc[:-1]):
        if token.text.lower() == "at" and doc[i + 1].ent_type_ == 'TIME':
            content_tokens.remove(token.text)
    content = ' '.join(content_tokens)
    content = re.sub(REMOVAL_PHRASES, '', content).strip()
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
    """Wrapper function to extract reminder content"""
    reminder_content = extract_reminder_content(user_input, date_str, time_str)
    if not reminder_content:
        return None
    return reminder_content

def get_reminder_datetime(user_input):
    """Extracts both the date and time for a reminder from user input"""
    date_str, time_str, is_recurring = extract_datetime(user_input)
    if not date_str or not time_str:
        return None, None, None
    return date_str, time_str, is_recurring