import sys
from modules.utils import speak, save_to_file, recognize_speech
from modules.reminders import handle_reminder_request
from modules.tasks import handle_task_request
from modules.ai import get_openai_response

STOP_PHRASES = ["exit", "goodbye"]

def check_for_stop_command(user_input, previous_questions_and_answers):
    """
    Check user_input for a stop keyword.
    """
    user_input_lower = user_input.lower().strip()
    if user_input_lower in STOP_PHRASES:
        save_to_file("iva_conversation", '\n'.join([f"{role}: {content}" for role, content in previous_questions_and_answers]))
        print("Goodbye!")
        sys.exit(0)
    return False

def process_input(user_input, previous_questions_and_answers, context_data):
    """
    Process the user input and return the AI assistant's response.
    """
    if check_for_stop_command(user_input, previous_questions_and_answers):
        return "Goodbye!"
    previous_questions_and_answers.append(("User", user_input))

    # Handle Reminder Requests
    if context_data.get("awaiting_reminder_confirmation"):
        response = handle_reminder_confirmation(user_input, context_data)
        if response:
            return response

    if is_reminder_request(user_input):
        reminder_response = handle_reminder_request(user_input, restart_main)
        if reminder_response:
            context_data["awaiting_reminder_confirmation"] = True
            return reminder_response
    answer = get_openai_response(previous_questions_and_answers)
    previous_questions_and_answers.append(("Assistant", answer))
    return answer

def handle_input(input_text=None, is_voice_input=False):
    """
    Process either text or voice input and return the AI assistant's response.
    """
    previous_questions_and_answers = []
    if is_voice_input:
        input_text = recognize_speech()
    if input_text:
        response = process_input(input_text, previous_questions_and_answers)
        if response:
            speak(response)
        return response
    return ""

def restart_main():
    return "Is there anything else I can help you with?"

if __name__ == "__main__":
    print("Welcome to Iva.")
    handle_input()