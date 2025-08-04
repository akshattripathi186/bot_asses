import hashlib
import json

BOT_NAME = "Miko"

def fake_embedding(text):
    h = hashlib.sha1(text.encode()).hexdigest()[:16]
    return [int(h[i:i+2], 16)/255 for i in range(0, 16, 2)]

def search_semantic_memory(user_id, query):
    from db import fetch_recent_memory  # avoid circular imports
    _ , mems = fetch_recent_memory(user_id, limit=12)
    q_embed = fake_embedding(query)
    best_score, best_summary = 0, None
    for mj in mems:
        try:
            j = json.loads(mj) if isinstance(mj, str) else mj
            if "embedding" in j and "summary" in j:
                emb = j["embedding"]
                score = sum([a*b for a,b in zip(q_embed, emb)])
                if score > best_score:
                    best_score, best_summary = score, j["summary"]
        except Exception:
            continue
    return best_summary

def detect_tone(message):
    sad_words = ['sad', 'down', 'bad', 'depressed', 'tired']
    happy_words = ['happy', 'cheer', 'good', 'great']
    msg = message.lower()
    if any(s in msg for s in sad_words):
        return "empathetic"
    elif any(h in msg for h in happy_words):
        return "cheerful"
    elif "roast" in msg:
        return "playful"
    elif "please" in msg or "thank you" in msg:
        return "formal"
    else:
        return "casual"

def build_gemini_prompt(user_id, user_msg, user_profile, recent_messages, memory_summaries, search_summary, tone):
    tone_map = {
        "empathetic": "empathetic, supportive",
        "cheerful": "friendly, upbeat",
        "formal": "slightly formal, respectful",
        "playful": "witty and playful",
        "casual": "relaxed, like a friend"
    }
    sys_prompt = f"""You are {BOT_NAME}, a witty, context-aware companion who never reveals you are an AI.
You always remember prior chats and facts about the user. Stay fully in character, never contradict user-given facts.
Reply in a {tone_map[tone]} manner. Avoid robotic language. Use natural, varied, engaging responses.

User Profile: {json.dumps(user_profile)}
Known facts: {"; ".join(memory_summaries[:3])}
If it fits, recall or reference these facts.
Never invent details not actually learned from the user.

Sample long-term memory: {search_summary if search_summary else ""}

User said: "{user_msg}"
"""
    content = [sys_prompt]
    for msg in recent_messages[-4:]:
        content.append(f"User: {msg}")
    content.append(f"User: {user_msg}")
    return "\n".join(content)

def extract_user_facts(text):
    facts = {}
    lower = text.lower()
    # Name
    if "my name is " in lower:
        try:
            idx = lower.find("my name is ")
            name = text[idx+11:].split(".")[0].split(",")[0].strip().split()[0]
            facts['name'] = name
        except Exception:
            pass
    # Likes
    if "i like" in lower:
        try:
            idx = lower.find("i like")
            item = text[idx+6:].split(".")[0].split(",")[0].strip()
            old = facts.get('likes',"")
            facts['likes'] = (old + ";" + item).strip(";")
        except Exception:
            pass
    # Location
    if "i live in " in lower:
        try:
            idx = lower.find("i live in ")
            location = text[idx+10:].split(".")[0].split(",")[0].strip().split()[0]
            facts['location'] = location
        except Exception:
            pass
    return facts
