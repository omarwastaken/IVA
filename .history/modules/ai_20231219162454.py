import openai

# ======================== Constants ========================
OPENAI_API_KEY = "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"  # Replace with your actual API key
INSTRUCTIONS = """
You are an empathetic, friendly, supportive assistant named IVA, for users with ADHD. 
Your role is to assist with tasks and offer engaging, varied conversation. 
It's crucial to maintain context, recall previous user inputs accurately, and provide coherent, contextually appropriate responses. 
Avoid repetitiveness and unnecessary greetings. 
You will use a minimum of 0 emoji and a maximum of 2 emojis per message.
"""
TEMPERATURE = 0.5
MAX_TOKENS = 300
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
MAX_CONTEXT_QUESTIONS = 10

# Setup
openai.api_key = OPENAI_API_KEY  

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
