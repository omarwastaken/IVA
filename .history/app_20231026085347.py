import openai
from modules.utils import speak, save_to_file, recognize_speech
from modules.reminders import handle_reminder_request
from modules.tasks import handle_task_request

# Set up the API key for OpenAI
openai.api_key = "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"

# Define constants
INSTRUCTIONS = """Your instructions here."""
TEMPERATURE = 0.5
MAX_TOKENS = 100
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
MAX_CONTEXT_QUESTIONS = 10



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


from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json['message']
    iva_response = get_openai_response([("User", user_message)])
    return jsonify(response=iva_response)

if __name__ == '__main__':
    app.run(debug=True)