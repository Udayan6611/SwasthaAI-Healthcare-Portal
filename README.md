# SwasthaAI: AI-Powered Healthcare Portal

**SwasthaAI** is a smart, multilingual healthcare portal designed to provide reliable, AI-driven medical guidance to underserved and rural communities.

---

## 🚑 The Problem

In many rural areas, access to timely medical advice is limited. This often leads to harmful self-medication or avoidable hospital visits due to language barriers and a lack of reliable information.

**SwasthaAI** aims to bridge this gap by providing an accessible first point of contact for health-related queries.

---

## 💡 Our Solution

This application features a dual-AI system that combines a fast, locally-trained model for initial diagnosis with the power of the Google Gemini API for detailed, multilingual advice.

The portal includes a symptom checker and an AI health assistant to make the guidance immediately actionable.

---

## 🔍 Key Features

- **Hybrid AI System**  
  Uses a local Scikit-learn model for instant predictions and the Google Gemini API for nuanced, detailed advice.

- **Multilingual Support**  
  The user interface and all AI-generated responses are available in English, Marathi, and Hindi.

- **Intelligent Symptom Analysis**  
  Gathers user symptoms to provide a data-driven preliminary analysis.

---

## 🛠️ Tech Stack (Hackathon Version)

| Category          | Technology                       | Purpose                                      |
|-------------------|-----------------------------------|----------------------------------------------|
| **Frontend**       | HTML, CSS, Vanilla JavaScript     | User Interface & Experience                  |
| **Gateway Backend**| Node.js, Express.js               | Manages web traffic and API routing          |
| **AI Backend**     | Python, Flask                     | Handles all AI processing and model serving  |
| **ML Model**       | Scikit-learn (RandomForestClassifier) | Instant symptom-to-disease prediction  |
| **LLM & NLP**      | Google Gemini API                 | Detailed advice generation & real-time translation |
| **Architecture**   | Full-Stack, Microservice          | Separates UI logic from intensive AI tasks   |

---

## 🧱 Project Structure

The project uses a two-server architecture to separate concerns between web traffic management and AI processing.

```
Swasthaai/
├── AI/                     # The Python AI Backend
│   ├── ai_server.py
│   ├── train_model.py
│   ├── symptom_data.csv
│   └── .env
│
├── backend_swasthaai/      # The Node.js Gateway Backend
│   ├── controllers/
│   ├── routes/
│   ├── app.js
│   └── package.json
│
└── index.html              # The main frontend file
```

---

## ⚙️ Setup and Installation

To run this project locally, follow these steps:

### ✅ Prerequisites

- Node.js (v16 or newer)
- Python (v3.8 or newer) and `pip`

---

### 1️⃣ AI Backend Setup (Python)

First, set up the AI "brain" of the application.

```bash
cd AI
```

Create a `requirements.txt` file with the following contents:

```
Flask
flask-cors
pandas
scikit-learn
joblib
python-dotenv
requests
```

Install the Python packages:

```bash
pip install -r requirements.txt
```

Get a Gemini API key from **Google AI Studio**. Then create a `.env` file in the `AI` folder:

```
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

Train the local model by running:

```bash
python train_model.py
```

---

### 2️⃣ Gateway Backend Setup (Node.js)

Next, set up the server that connects the user to the AI backend.

```bash
cd backend_swasthaai
```

Install the required Node.js packages:

```bash
npm install express cors axios dotenv
```

---

## 🚀 Running the Application

Both servers must be running simultaneously.

### Start the Python AI Server:

In your first terminal:

```bash
cd AI
python ai_server.py
```

Wait for the message indicating it's running on **port 5001**.

---

### Start the Node.js Gateway Server:

In your second terminal:

```bash
cd backend_swasthaai
node app.js
```

Wait for the message indicating it's running on **port 5000**.

---

### Launch the Frontend:

Simply open the `index.html` file in your web browser.

Your AI-powered multilingual health portal is now **ready to use** 

---

## 🙌 Contributing

Want to contribute? Found a bug or idea? Please feel free to raise an issue or submit a pull request!

---

## ✨ Acknowledgements

- Google AI Studio (Gemini API)
- Flask & Express Communities
- scikit-learn Developers
