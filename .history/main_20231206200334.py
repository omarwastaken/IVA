import openai
import spacy
import sys
from modules.utils import speak, save_to_file, recognize_speech
from modules.reminders import handle_reminder_request
from modules.tasks import handle_task_request

# ======================== Constants ========================
OPENAI_API_KEY = "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" # Replace with your actual API key
INSTRUCTIONS = """
You are an empathetic, friendly, supportive assistant named IVA, for users with ADHD. 
Your role is to assist with tasks and offer engaging, varied conversation. 
It's crucial to maintain context, recall previous user inputs accurately, and provide coherent, contextually appropriate responses. 
Avoid repetitiveness and unnecessary greetings.
"""
TEMPERATURE = 0.5
MAX_TOKENS = 300
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
MAX_CONTEXT_QUESTIONS = 10
STOP_PHRASES = ["exit", "goodbye"]

# Setup
openai.api_key = OPENAI_API_KEY  
nlp = spacy.load("en_core_web_sm")

# Function to check for stop command from user and save conversation
def check_for_stop_command(user_input, previous_questions_and_answers):
    user_input_lower = user_input.lower().strip()
    if user_input_lower in STOP_PHRASES:
        save_to_file("iva_conversation", '\n'.join([f"{role}: {content}" for role, content in previous_questions_and_answers]))
        speak("Goodbye!")
        sys.exit(0)


# Function to get response from OpenAI
def get_openai_response(previous_questions_and_answers):
    messages = [{"role": "system", "content": INSTRUCTIONS}]
    messages.extend({"role": role.lower(), "content": content} for role, content in
                    previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:])

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            frequency_penalty=FREQUENCY_PENALTY,
            presence_penalty=PRESENCE_PENALTY,
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return "Sorry, I couldn't process that request right now."


# Function to manage conversation flow with IVA
def talk_iva():
    speak("How can I help you today?")
    previous_questions_and_answers = []  # Initialize the conversation history

    while True:
        user_input = recognize_speech()

        if check_for_stop_command(user_input, previous_questions_and_answers):
            break

        # Append user's input to conversation history
        previous_questions_and_answers.append(("User", user_input))

        # Handle specific requests (reminders or tasks)
        if handle_reminder_request(user_input, restart_main):
            continue
        if handle_task_request(user_input, restart_main):
            continue

        # Get general response from OpenAI
        answer = get_openai_response(previous_questions_and_answers)

        # Append IVA's response to conversation history
        previous_questions_and_answers.append(("Assistant", answer))

        speak(answer)


# Function to restart main loop (prompt for further help)
def restart_main():
    speak("Is there anything else I can help you with?")


# Main loop
if __name__ == "__main__":
    speak("Hello, please speak so that I can verify your microphone's functionality.")
    while True:
        command = recognize_speech()
        if command:
            talk_iva()
