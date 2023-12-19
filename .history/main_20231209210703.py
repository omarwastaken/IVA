import sys
from modules.utils import speak, save_to_file, recognize_speech
from modules.reminders import handle_reminder_request
from modules.tasks import handle_task_request
from modules.ai import get_openai_response

STOP_PHRASES = ["exit", "goodbye"]

def check_for_stop_command(user_input, previous_questions_and_answers):
    user_input_lower = user_input.lower().strip()
    if user_input_lower in STOP_PHRASES:
        save_to_file("iva_conversation", '\n'.join([f"{role}: {content}" for role, content in previous_questions_and_answers]))
        print("Goodbye!")
        sys.exit(0)
    return False



def talk_iva():
    print("How can I help you today?")
    previous_questions_and_answers = []

    while True:
        user_input = recognize_speech()
        response = process_input(user_input, previous_questions_and_answers)
        if response:
            speak(response)
            if response == "Goodbye!":
                break

def restart_main():
    print("Is there anything else I can help you with?")

if __name__ == "__main__":
    print("Welcome to Iva.")
    talk_iva()
