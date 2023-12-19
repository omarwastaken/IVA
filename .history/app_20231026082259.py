from flask import Flask, render_template, request, jsonify

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to the IVA chat app!"

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form.get("input")
    # For now, simply echo the user input as the AI's response
    # We will integrate the AI's logic later
    return jsonify({"response": user_input})