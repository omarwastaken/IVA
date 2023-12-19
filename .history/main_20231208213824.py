import sys
import threading
import keyboard
from modules.utils import speak, save_to_file, recognize_speech
from modules.reminders import handle_reminder_request
from modules.tasks import handle_task_request
from modules.ai import get_openai_response

STOP_PHRASES = ["exit", "goodbye"]

# Global variable to keep track of the current input mode
input_mode = 'voice'

def on_ctrl_m_press():
    global input_mode
    input_mode = 'text' if input_mode == 'voice' else 'voice'
    print(f"Switched to {input_mode} mode")

# Function to manage mode switching
def listen_for_mode_switch():
    keyboard.add_hotkey('ctrl+m', on_ctrl_m_press)
    keyboard.wait()

def get_user_input():
    if input_mode == 'voice':
        return recognize_speech()
    else:
        return input("Type your request: ")

def check_for_stop_command(user_input, previous_questions_and_answers):
    user_input_lower = user_input.lower().strip()
    if user_input_lower in STOP_PHRASES:
        save_to_file("iva_conversation", '\n'.join([f"{role}: {content}" for role, content in previous_questions_and_answers]))
        speak("Goodbye!")
        sys.exit(0)

def talk_iva():
    global input_mode
    speak("How can I help you today?")
    previous_questions_and_answers = []

    while True:
        user_input = get_user_input()

        if check_for_stop_command(user_input, previous_questions_and_answers):
            break

        previous_questions_and_answers.append(("User", user_input))

        if handle_reminder_request(user_input, restart_main):
            continue
        if handle_task_request(user_input, restart_main):
            continue

        answer = get_openai_response(previous_questions_and_answers)
        previous_questions_and_answers.append(("Assistant", answer))
        speak(answer)

def restart_main():
    speak("Is there anything else I can help you with?")

if __name__ == "__main__":
    speak("Welcome to the AI Assistant. Press Ctrl+M at any time to switch between voice and text mode.")
    mode_switch_thread = threading.Thread(target=listen_for_mode_switch, daemon=True)
    mode_switch_thread.start()
    talk_iva()