# Main Flask server for AI logic. Handles local model prediction and calls to the Gemini API.
import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from dotenv import load_dotenv

#Server Setup
load_dotenv()
app = Flask(__name__)
CORS(app)

#Load Local Model
#Load local scikit-learn model and columns on startup.
try:
    model = joblib.load('disease_prediction_model.joblib')
    model_columns = joblib.load('model_columns.joblib')
    print("AI Model loaded successfully.")
except FileNotFoundError:
    print("ERROR: Model files not found. Run train_model.py first.")
    model = None

#Get API key from the .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("CRITICAL ERROR: GEMINI_API_KEY not found in .env file.")

#Gemini API Function
#This is a general function to call Gemini with a given prompt.
def call_gemini(prompt):
    if not GEMINI_API_KEY:
        return None

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        
        raw_text = response.json()['candidates'][0]['content']['parts'][0]['text']
        return raw_text
    except requests.exceptions.RequestException as e:
        print(f"Gemini API request failed: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Failed to parse Gemini's response: {e}")
        return None

#API Endpoints
@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({"error": "AI model not loaded."}), 500

    data = request.get_json()
    symptom_names = list(data.get('symptoms', {}).keys())
    age = data.get('ageGroup', 'adult')
    #Get language from the request
    language = data.get('language', 'en')
    lang_map = {'en': 'English', 'mr': 'Marathi', 'hi': 'Hindi'}
    target_language = lang_map.get(language, 'English')
    
    #Local Prediction
    query_df = pd.DataFrame(columns=model_columns)
    query_df.loc[0] = 0
    for symptom in symptom_names:
        if symptom in model_columns:
            query_df.loc[0, symptom] = 1
    
    predicted_disease = model.predict(query_df)[0]
    
    #Enrich with Gemini
    predict_prompt = f"""
    As an AI health assistant, your role is to provide a helpful, safe, and informative summary. You are not a doctor.
    The local model predicted the condition: '{predicted_disease}' for a patient in the '{age}' age group.

    Generate a JSON object with the following structure.
    IMPORTANT: You MUST translate the CONTENT of the 'specialist', 'advice', and 'priority' fields into the {target_language} language.

    {{
        "specialist": "The medical specialist for this condition.",
        "advice": "Provide 2-3 clear, actionable next steps. The final sentence must be: 'For a proper diagnosis, please consult a healthcare professional.'",
        "priority": "One word only: Urgent, Moderate, or Routine"
    }}
    
    Respond only with the JSON object.
    """
    
    gemini_response_text = call_gemini(predict_prompt)

    if not gemini_response_text:
        return jsonify({"error": "AI Health Assistant is currently unavailable."}), 503

    try:
        cleaned_json_text = gemini_response_text.strip().replace("```json", "").replace("```", "").strip()
        gemini_result = json.loads(cleaned_json_text)
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to understand AI response."}), 500

    #Combine results
    final_response = {
        "predicted_disease": str(predicted_disease),
        "specialist": gemini_result.get('specialist', 'General Physician'),
        "advice": gemini_result.get('advice', 'Please consult a doctor for advice.'),
        "priority": gemini_result.get('priority', 'Moderate')
    }

    return jsonify(final_response)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_query = request.get_json().get('query')
    language = data.get('language', 'en')
    lang_map = {'en': 'English', 'mr': 'Marathi', 'hi': 'Hindi'}
    target_language = lang_map.get(language, 'English')
    if not user_query:
        return jsonify({"error": "No query provided."}), 400

    #A different prompt, designed for conversation.
    chat_prompt = f"""
    You are SwasthaAI, a helpful AI health assistant. Your role is to provide general health information. You are not a doctor and must not provide a diagnosis.
    Respond to the user's question in the {target_language} language.
    Keep your answer concise.
    
    User's question: "{user_query}"
    """
    
    response_text = call_gemini(chat_prompt)
    
    if not response_text:
        return jsonify({"response": "I am having trouble connecting right now. Please try again later."})
        
    return jsonify({"response": response_text})


#Main Entry Point
if __name__ == '__main__':
    print("Starting Python AI server with Gemini integration on http://127.0.0.1:5001")
    app.run(port=5001, debug=True)