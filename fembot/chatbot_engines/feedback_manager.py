import json, os

FEEDBACK_FILE = "chatbot_data/user_feedback.json"
PREFERENCES_FILE = "chatbot_data/user_preferences.json"
MOOD_FILE = "../femhealth/fembot/chatbot_data/mood_data.json" 


import os
import json

# Get the absolute path to the directory where the current script resides
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MOOD_FILE = os.path.join(BASE_DIR, "chatbot_data", "mood_data.json")
MOOD_FILE = os.path.join(BASE_DIR, "chatbot_data", "mood_data.json")

# Load the mood data
with open(MOOD_FILE, "r", encoding="utf-8") as f:
    mood_data = json.load(f)
    
def save_user_mood(user_id, mood):
    moods = load_json(MOOD_FILE)
    moods[user_id] = mood
    save_json(MOOD_FILE, moods)

def load_user_mood(user_id):
    moods = load_json(MOOD_FILE)
    return moods.get(user_id, None)

def load_json(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def update_feedback(diagnosis, item, liked=True):
    feedback = load_json(FEEDBACK_FILE)
    feedback.setdefault(diagnosis, {})
    feedback[diagnosis][item] = feedback[diagnosis].get(item, 0) + (1 if liked else -1)
    save_json(FEEDBACK_FILE, feedback)

def get_user_preferred_plan(diagnosis, plan_list):
    feedback = load_json(FEEDBACK_FILE)
    scores = feedback.get(diagnosis, {})
    return sorted(plan_list, key=lambda x: scores.get(x, 0), reverse=True)

def update_user_avoid_list(user_id, item):
    prefs = load_json(PREFERENCES_FILE)
    prefs.setdefault(user_id, [])
    if item not in prefs[user_id]:
        prefs[user_id].append(item)
    save_json(PREFERENCES_FILE, prefs)

def filter_avoided_items(user_id, plan):
    prefs = load_json(PREFERENCES_FILE)
    avoid = prefs.get(user_id, [])
    return [item for item in plan if item not in avoid]
