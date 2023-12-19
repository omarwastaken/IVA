from flask import Flask, render_template, request, jsonify
import main  # Importing the main module

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_iva():
    user_input = request.json.get('query')
    
    # Here, process the user_input with your existing logic
    # For the sake of this example, we'll just return the user_input
    # You will integrate your actual logic from main.py
    
    response = f"Your question was: {user_input}"  # Replace this with actual logic
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
