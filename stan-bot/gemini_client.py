import os
import google.generativeai as genai

# Singleton for model
model = None
def get_model():
    global model
    key = os.getenv("GOOGLE_API_KEY", "")
    if not key:
        raise ValueError("Provide GOOGLE_API_KEY as env var.")
    genai.configure(api_key=key)
    if model is None:
        try:
            # Use gemini-1.5-flash or gemini-2.5-flash if you have access
            model_instance = genai.GenerativeModel('gemini-1.5-flash')
            model = model_instance
            return model_instance
        except Exception as e:
            raise RuntimeError("Failed to instantiate Gemini model: "+str(e))
    return model

def chat_with_gemini(model, prompt):
    response = model.generate_content(prompt)
    return getattr(response, "text", str(response))
