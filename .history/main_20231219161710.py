import sys
from modules.utils import speak, save_to_file, recognize_speech
from modules.reminders import handle_reminder_request
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

def process_input(user_input, previous_questions_and_answers):
    if check_for_stop_command(user_input, previous_questions_and_answers):
        return "Goodbye!"
    previous_questions_and_answers.append(("User", user_input))
    # Updated to pass only one argument
    response_messages = handle_reminder_request(user_input)
    if response_messages:
        return " ".join(response_messages)
    answer = get_openai_response(previous_questions_and_answers)
    previous_questions_and_answers.append(("Assistant", answer))
    return answer