import sounddevice as sd
import vosk
import queue
import json
import datetime
from pymongo import MongoClient

# ------------------ MongoDB Setup ------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["voice_medical_db"]
collection = db["records"]

# ------------------ Vosk Model ------------------
# Ensure this folder name matches your exact directory
model = vosk.Model("vosk-model-small-en-us-0.15")

# ------------------ Speak Function ------------------
def speak(text):
    print("Assistant:", text)

# ------------------ Symptom Detection ------------------
def detect_symptoms(text):
    text = text.lower()
    symptoms = []
    if "fever" in text: symptoms.append("fever")
    if "cold" in text: symptoms.append("cold")
    if "cough" in text: symptoms.append("cough")
    if "headache" in text: symptoms.append("headache")
    if "stomach" in text: symptoms.append("stomach pain")
    return symptoms

# ------------------ Medical Response & DB Save ------------------
def medical_response(text):
    symptoms = detect_symptoms(text)
    if not symptoms:
        return "No clear symptoms detected."

    advice = ""
    if "fever" in symptoms and "cough" in symptoms:
        advice = "Possible infection. Monitor temperature and consult doctor."
    elif "fever" in symptoms:
        advice = "Take rest and drink plenty of fluids."
    elif "cold" in symptoms or "cough" in symptoms:
        advice = "Avoid cold food and drink warm water."
    elif "headache" in symptoms:
        advice = "Take rest and avoid screen exposure."
    elif "stomach pain" in symptoms:
        advice = "Eat light food and stay hydrated."

    # Save to MongoDB
    data = {
        "timestamp": datetime.datetime.now(),
        "speech_text": text,
        "detected_symptoms": symptoms,
        "advice_given": advice
    }
    collection.insert_one(data)
    return advice

# ------------------ Audio Logic ------------------
def record_audio():
    fs = 16000
    duration = 5  # seconds
    print("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    return audio

def recognize_speech():
    audio_data = record_audio()
    rec = vosk.KaldiRecognizer(model, 16000)
    rec.AcceptWaveform(audio_data.tobytes())
    result = json.loads(rec.Result())
    return result.get("text", "")