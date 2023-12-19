import datetime
from dateutil import parser
import parsedatetime as pdt
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Define a list of possible verbs and phrases related to setting a reminder
reminder_keywords = ["remind", "remember", "remind me", "set a reminder", "add to my reminders"]

def is_reminder_request(user_input):
    # Process the user input with spaCy
    doc = nlp(user_input)
    
    # Check if any of the tokens or phrases in the user input are related to setting a reminder
    for token in doc:
        if token.lemma_ in reminder_keywords:
            return True
    for phrase in reminder_keywords:
        if phrase in user_input.lower():
            return True
    return False

cal = pdt.Calendar()

def extract_datetime(user_input):
    # Use parsedatetime to extract date and time entities from user input
    time_struct, parse_status = cal.parse(user_input)
    datetime_obj = datetime.datetime(*time_struct[:6])
    
    date_str = datetime_obj.strftime('%Y-%m-%d') if parse_status else ""
    time_str = datetime_obj.strftime('%I:%M %p') if parse_status else ""
    
    return date_str, time_str

def create_reminder(user_input):
    # Process the user input with spaCy
    doc = nlp(user_input)
    
    # Initialize the reminder_text and reminder_time_input
    reminder_text = ""
    reminder_time_input = ""
    
    # Extract reminder content using dependency parsing
    for token in doc:
        if token.lemma_ in reminder_keywords:
            for child in token.children:
                if "obj" in child.dep_:
                    reminder_text = " ".join([w.text for w in child.subtree])
                    break
    
    # Refine the extracted reminder_text
    reminder_text = reminder_text[3:] if reminder_text.startswith("to ") else reminder_text
    
    # Extract date and time entities from user input
    date_str, time_str = extract_datetime(user_input)
    
    # Check if date or time is mentioned in the user input
    if date_str and not time_str:
        speak(f"You mentioned {date_str}. What time on {date_str} would you like to be reminded?")
        time_str = recognize_speech()
    elif time_str and not date_str:
        speak(f"You mentioned {time_str}. On which date would you like to be reminded at {time_str}?")
        date_str = recognize_speech()
    
    # Combine date and time input
    if date_str or time_str:
        reminder_time_input = f"{date_str} {time_str}"
    
    # If the reminder_text is not extracted, ask the user for it
    if not reminder_text:
        speak("What do you want me to remind you about?")
        reminder_text = recognize_speech()
    
    # If the reminder_time_input is not extracted, ask the user for it
    if not reminder_time_input:
        speak("When do you want to be reminded?")
        reminder_time_input = recognize_speech()
    
    if reminder_text and reminder_time_input:
        try:
            # Combine date and time strings and parse using dateutil parser
            reminder_datetime_obj = parser.parse(reminder_time_input)
            current_datetime_obj = datetime.datetime.now()
            if reminder_datetime_obj > current_datetime_obj:
                reminder = f"Okay, I'll remind you to {reminder_text} at {reminder_datetime_obj.strftime('%Y-%m-%d %I:%M %p')}"
                speak(reminder)
                
                # Use a for-loop for confirmation attempts
                for _ in range(3):
                    # Confirm the details of the reminder with the user
                    speak("Is this correct? Say 'yes' to confirm, 'no' to re-enter the time, or 'cancel' to cancel the reminder.")
                    confirmation = recognize_speech().lower()
                    if 'yes' in confirmation:
                        # Save only the reminder content and time in a structured format
                        reminder_data = {
                            "content": reminder_text,
                            "time": reminder_datetime_obj.strftime('%Y-%m-%d %I:%M %p')
                        }
                        save_to_file("reminder", str(reminder_data))
                        break
                    elif 'no' in confirmation:
                        speak("Please re-enter the details.")
                        return create_reminder(user_input)
                    elif any(keyword in confirmation for keyword in ['cancel', 'nevermind', 'stop']):
                        speak("Reminder cancelled.")
                        break
                    else:
                        speak("Sorry, I didn't catch that. Would you like to confirm the reminder?")
                else:
                    speak("Sorry, I couldn't confirm the reminder after several attempts. Please try again.")
            else:
                speak("Sorry, that time has already passed. Please enter a future time.")
        except ValueError:
            speak("Sorry, I didn't understand the time or date you said. Please say it again in a recognized format.")
    restart_main()
