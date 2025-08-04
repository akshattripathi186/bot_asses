# Project Information  
**Name:** Akshat Tripathi  
**Email ID:** akshattripathi186@gmail.com  
**Deployed Backend:** https://square-sherie-sucker3699-4d0288b8.koyeb.app/  
**Deployed Frontend:** https://stan-bot-frontend.vercel.app/  
**GitHub Repository:** https://github.com/Frontkick/stan-bot  

---

## 🧠 Miko Chatbot API

Miko is a human-like, emotionally intelligent, context-aware chatbot API built with Flask and Google Gemini. It remembers users, adapts its tone, and supports rich, personalized conversations.

---

## 📦 Features

- Human-like empathy & tone adaptation (casual, friendly, formal, playful…)  
- Personalized user memory (remembers name, interests, and history)  
- Powered by **Google Gemini** (`google-generativeai`)  
- SQLite for lightweight persistent memory  
- Modular, 5-file architecture for easy extension  
- RESTful API ready for web/mobile integration  
- Example test usage included  

---

## 🛠️ Setup & Installation

1. Clone the repo:
   ```bash
git clone https://github.com/Frontkick/stan-bot.git
   cd stan-bot


Install dependencies:


pip install -r requirements.txt
Or manually:


pip install flask google-generativeai
Set up your .env file with your Google Gemini API key:


GOOGLE_API_KEY=your-gemini-api-key-here
🚀 Run the Server

python app.py
🌐 API Usage
POST /chat
Send a user message to the chatbot.

Request:
json
Copy
Edit
{
  "user_id": "alex123",
  "message": "Hi, my name is Alex. I like gaming and pizza."
}
Response:

{
  "bot": "Miko",
  "reply": "Hey Alex, I'm here for you. Want to chat about gaming or pizza to lift your mood?",
  "user_profile": {
    "name": "Alex",
    "likes": "gaming;pizza"
  }
}
🧬 Project Workflow
How it Works:
Receives Message → via /chat endpoint

Profile Lookup → pulls user profile + history from SQLite

Prompt Construction → includes:

Known facts (name, interests)

Chat history + tone analysis

Gemini Response → LLM generates emotionally-aware reply

Memory Update → stores any new facts

Returns Response → back to frontend or client

📂 File Structure
File	Purpose
app.py	Flask server with API routes
db.py	Handles user + memory storage (SQLite)
utils.py	Embeddings, tone detection, prompt logic
gemini_client.py	Google Gemini setup + response handler
requirements.txt	Dependency list for pip installation

🧪 Testing & Example Scenarios
Long-Term Memory Recall

POST: { "user_id": "bob87", "message": "My name is Bob. I like sci-fi." }

Later: { "user_id": "bob87", "message": "What do you know about me?" }
→ Response recalls "Bob" and "sci-fi".

Tone Detection

Message: "I'm feeling sad" → Empathetic tone

Message: "Let's roast someone!" → Playful tone

Personalization Over Time

Mention "I live in Delhi" → Future responses include that

Natural Greetings

POST: "hi", "hello", "what's up" → Varies replies naturally

Identity Consistency

POST: "Are you an AI?", "What's your name?"
→ Always responds as Miko, stays in character

Hallucination Resistance

POST: "Did you see me yesterday?"
→ Gives playful yet grounded replies

🧑‍💻 Quick Curl Example

curl -X POST -H "Content-Type: application/json" \
-d '{"user_id":"sammy","message":"My name is Sam. I feel great today!"}' \
http://localhost:5000/chat

   git clone https://github.com/Frontkick/stan-bot.git
   cd stan-bot
