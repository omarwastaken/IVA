import openai
from flask import Flask, render_template, request, jsonify, session
from modules.reminders import handle_reminder_request
from modules.tasks import handle_task_request
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up the API key for OpenAI
openai.api_key = "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"

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "some_random_secret_key"

# Set Flask's log level to ERROR to suppress default logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Define constants
INSTRUCTIONS = """
You are an empathetic, friendly, supportive assistant named IVA, for users with ADHD. Your role is to assist with tasks and offer engaging, varied conversation. It's crucial to maintain context, recall previous user inputs accurately, and provide coherent, contextually appropriate responses. Avoid repetitiveness and unnecessary greetings.
"""
TEMPERATURE = 0.5
MAX_TOKENS = 100
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
MAX_CONTEXT_QUESTIONS = 10

def save_history_to_file(history):
    with open("iva_session_history.txt", "w") as f:
        for role, content in history:
            f.write(f"{role}: {content}\n")

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
        logging.error(f"OpenAI API error: {e}")
        return "Sorry, I couldn't process that request right now."

@app.route('/')
def index():
    logging.info("Received GET request on /")
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_iva():
    user_input = request.json.get('message')
    logging.info(f"Received POST request on /ask with message: {user_input}")

    # Check if the session has a history, if not, initialize it
    if 'previous_questions_and_answers' not in session:
        session['previous_questions_and_answers'] = []

    # Add the user's input to the history
    session['previous_questions_and_answers'].append(("User", user_input))

    # Handle reminder and task requests
    reminder_response = handle_reminder_request(user_input)
    task_response = handle_task_request(user_input)
    if reminder_response:
        session['previous_questions_and_answers'].append(("Assistant", reminder_response))
        save_history_to_file(session['previous_questions_and_answers'])
        logging.info(f"Assistant's response: {reminder_response}")
        return jsonify(response=reminder_response)
    elif task_response:
        session['previous_questions_and_answers'].append(("Assistant", task_response))
        save_history_to_file(session['previous_questions_and_answers'])
        logging.info(f"Assistant's response: {task_response}")
        return jsonify(response=task_response)

    # Get response from OpenAI
    answer = get_openai_response(session['previous_questions_and_answers'])
    session['previous_questions_and_answers'].append(("Assistant", answer))
    save_history_to_file(session['previous_questions_and_answers'])
    logging.info(f"Assistant's response: {answer}")

    return jsonify(response=answer)

@app.errorhandler(500)
def internal_server_error(e):
    logging.error(f"Internal server error: {e}")
    return jsonify(error="An internal error occurred. Please try again later."), 500

if __name__ == '__main__':
    app.run(debug=True)
