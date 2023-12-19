import openai
from flask import Flask, render_template, request, jsonify, session
import spacy
import sys
from modules.utils import speak, save_to_file, recognize_speech
from modules.reminders import handle_reminder_request
from modules.tasks import handle_task_request

# Set up the API key for OpenAI
openai.api_key = "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"

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "some_random_secret_key"  # Needed for session to work

# Define constants
INSTRUCTIONS = """
You are an empathetic, friendly, supportive assistant named IVA, for users with ADHD. Your role is to assist with tasks and offer engaging, varied conversation. It's crucial to maintain context, recall previous user inputs accurately, and provide coherent, contextually appropriate responses. Avoid repetitiveness and unnecessary greetings.
"""
TEMPERATURE = 0.5
MAX_TOKENS = 100
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
MAX_CONTEXT_QUESTIONS = 10

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Define a function to restart main loop
def restart_main():
    speak("Is there anything else I can help you with?")

stop_phrases = ["iva stop", "stop iva", "iva exit", "iva quit"]

def get_openai_response(previous_questions_and_answers):
    messages = [{"role": "system", "content": INSTRUCTIONS}]
    messages.extend({"role": role.lower(), "content": content} for role, content in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:])
    
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_iva():
    user_input = request.json.get('message')

    # Check if the session has a history, if not, initialize it
    if 'previous_questions_and_answers' not in session:
        session['previous_questions_and_answers'] = []

    # Add the user's input to the history
    session['previous_questions_and_answers'].append(("User", user_input))

    # Check for stop phrases
    if any(phrase in user_input.lower() for phrase in stop_phrases):
        save_to_file("iva", '\n'.join([f"{role}: {content}" for role, content in session['previous_questions_and_answers']]))
        return jsonify(response="Goodbye!")

    # Handle reminder and task requests
    reminder_response = handle_reminder_request(user_input, None)
    task_response = handle_task_request(user_input, None)
    if reminder_response:
        session['previous_questions_and_answers'].append(("Assistant", reminder_response))
        return jsonify(response=reminder_response)
    elif task_response:
        session['previous_questions_and_answers'].append(("Assistant", task_response))
        return jsonify(response=task_response)

    # Get response from OpenAI
    answer = get_openai_response(session['previous_questions_and_answers'])
    session['previous_questions_and_answers'].append(("Assistant", answer))

    return jsonify(response=answer)

def check_for_stop_command(user_input, previous_questions_and_answers):
    if any(phrase in user_input.lower() for phrase in stop_phrases):
        save_to_file("iva", '\n'.join([f"{role}: {content}" for role, content in previous_questions_and_answers]))
        speak("Goodbye!")
        sys.exit(0)  # This will terminate the program

if __name__ == '__main__':
    app.run(debug=True)