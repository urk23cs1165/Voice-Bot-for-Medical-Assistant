from flask import Flask, request, jsonify, send_from_directory
import assistant
import os

app = Flask(__name__)

# Get the directory where app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home():
    # Explicitly serve from the current directory
    return send_from_directory(BASE_DIR, "index.html")

@app.route('/<path:filename>')
def serve_static(filename):
    # This ensures style.css and script.js are found in the root
    return send_from_directory(BASE_DIR, filename)

@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_text = assistant.recognize_speech()
        if not user_text.strip():
            return jsonify({"transcript": "No speech detected", "symptoms": [], "reply": "I didn't hear anything."})

        symptoms = assistant.detect_symptoms(user_text)
        advice = assistant.medical_response(user_text)

        return jsonify({
            "transcript": user_text,
            "symptoms": symptoms,
            "reply": advice
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)