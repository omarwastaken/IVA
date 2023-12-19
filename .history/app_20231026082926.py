from flask import Flask, render_template, request, jsonify

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return html_template

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form.get("input")
    return jsonify({"response": user_input})

"Flask app reinitialized and updated to serve the chat interface."