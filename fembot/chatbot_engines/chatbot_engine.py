import json
import random
import os
import logging
from .feedback_manager import (
    get_user_preferred_plan,
    update_user_avoid_list,
    filter_avoided_items,
    save_user_mood,
    load_user_mood,
)
from .pdf_generator import generate_plan_pdf

logger = logging.getLogger(__name__)

class ChatbotEngine:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.chat_memory = {}
        self.mood_checkin = {}
        self.diet_plans = self._load_json("chatbot_data/diet_plans.json")
        self.exercise_plans = self._load_json("chatbot_data/exercise_plans.json")
        self.substitutions = self._load_json("chatbot_data/substitutions.json", lower_keys=True)

    def _load_json(self, relative_path, lower_keys=False):
        path = os.path.join(self.base_dir, relative_path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if lower_keys:
                return {k.lower(): v for k, v in data.items()}
            return data

    def get_mood_tone(self, mood):
        mood_tones = {
            "happy": "You're doing great — let's maintain the momentum!",
            "sad": "It's okay to feel down sometimes. Let's focus on small, supportive actions.",
            "tired": "Rest matters. Even gentle activity can boost your energy.",
            "anxious": "Deep breaths — steady progress is still progress.",
            "depressed": "You're not alone. Let's take this step-by-step together.",
            "angry": "Let’s channel that energy into something positive.",
            "low": "Every bit of effort counts. You're doing better than you think.",
            "good": "That's great! Let’s keep up the positive momentum.",
        }
        return mood_tones.get(mood, "Let’s focus on consistent and healthy progress.")

    def format_plan_response(self, diet, exercise, mood="neutral"):
        tone = self.get_mood_tone(mood)
        diet_msg = "\n".join([f"-  {item}" for item in diet])
        ex_msg = "\n".join([f"-  {item}" for item in exercise])
        encouragements = [
            "🔹 Progress is built on consistency — you're on the right path.",
            "🔹 Each small step adds up — trust the process and keep going.",
        ]
        return f"""
##  Your Personalized Wellness Plan

---

###  Diet Recommendations:
{diet_msg}

---

###  Exercise Suggestions:
{ex_msg}

---

###  Note:
> {tone}

{random.choice(encouragements)}

---

###  Need More Guidance?

- 👉 [View Detailed Diet Plans](https://yourwebsite.com/diet-plans)  
- 👉 [Explore More Exercise Routines](https://yourwebsite.com/exercise-plans)

---

Would you like to **adjust** or **save** this plan? Let me know how you'd like to proceed.
""".strip()

    def get_substitution(self, user_message):
        user_message_lower = user_message.lower()
        for key in self.substitutions:
            if key in user_message_lower:
                return f"If you'd like to substitute **{key}**, here are some alternatives: {', '.join(self.substitutions[key])}"
        return None

    def handle_mood_detection(self, user_message, user_id):
        mood_keywords = ["happy", "sad", "tired", "anxious", "good", "depressed", "angry", "low"]
        for word in mood_keywords:
            if word in user_message.lower():
                prev_mood = self.mood_checkin.get(user_id)
                self.mood_checkin[user_id] = word
                save_user_mood(user_id, word)
                if prev_mood and prev_mood != word:
                    return f"Thanks for the update! I've noted you're feeling **{word}** now."
                return f"Thanks for sharing. I've noted you're feeling **{word}**."
        return None

    def generate_plan(self, diagnosis, user_id):
        status = self._get_diagnosis_status(diagnosis)
        mood = self.mood_checkin.get(user_id, "neutral")
        diet_raw = self.diet_plans.get(mood, self.diet_plans.get(status, self.diet_plans["default"]))
        exercise_raw = self.exercise_plans.get(mood, self.exercise_plans.get(status, self.exercise_plans["default"]))
        diet_filtered = filter_avoided_items(user_id, diet_raw)
        exercise_filtered = filter_avoided_items(user_id, exercise_raw)
        diet = get_user_preferred_plan(status, diet_filtered)
        exercise = get_user_preferred_plan(status, exercise_filtered)
        return self.format_plan_response(diet, exercise, mood), {"diet": diet, "exercise": exercise, "mood": mood}

    def _get_diagnosis_status(self, diagnosis):
        if diagnosis.get("predicted") and not diagnosis.get("detected"):
            return "predicted"
        elif diagnosis.get("predicted") and diagnosis.get("detected") and not diagnosis.get("depression"):
            return "confirmed"
        elif diagnosis.get("depression"):
            return "depression"
        return "default"

    def get_bot_response(self, user_message, diagnosis, user_id="default"):
        if not diagnosis:
            diagnosis = {"predicted": True, "detected": True, "depression": True}

        mood_response = self.handle_mood_detection(user_message, user_id)
        if mood_response:
            return mood_response, {}

        if user_id not in self.mood_checkin:
            saved_mood = load_user_mood(user_id)
            if saved_mood:
                self.mood_checkin[user_id] = saved_mood
            else:
                return "Before we begin, how are you feeling today? (e.g., happy, anxious, tired)", {}

        if "plan" in user_message.lower():
            return self.generate_plan(diagnosis, user_id)

        substitution_response = self.get_substitution(user_message)
        if substitution_response:
            return substitution_response, {}

        if any(phrase in user_message.lower() for phrase in ["avoid", "don’t like", "no "]):
            for item in self.substitutions:
                if item in user_message.lower():
                    update_user_avoid_list(user_id, item)
                    return f"Got it! I’ll remember to avoid {item} in your future plans.", {}

        return "Hi there! Let me know if you'd like a diet or exercise plan, or need a substitution!", {}


# Usage
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
chatbot = ChatbotEngine(BASE_DIR)
