import datetime
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from tzlocal import get_localzone

# Constants
TOKEN_PATH = 'path/to/your/token.json'  # Adjust the path to your token.json
CREDENTIALS_PATH = 'path/to/your/credentials.json'  # Adjust the path to your credentials.json
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Function to get Google Calendar service
def get_calendar_service():
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

# Function to get reminders for today
def get_reminders_for_today():
    service = get_calendar_service()
    tz = get_localzone()
    now = datetime.datetime.now(tz)
    time_min = now.isoformat()
    time_max = (now + datetime.timedelta(days=1)).isoformat()

    events_result = service.events().list(calendarId='primary', timeMin=time_min,
                                          timeMax=time_max, singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result.get('items', [])

# Main
if __name__ == "__main__":
    reminders_today = get_reminders_for_today()
    if reminders_today:
        print("Reminders for Today:")
        for event in reminders_today:
            print(f"- {event['summary']} at {event['start']['dateTime']}")
    else:
        print("No reminders for today.")
