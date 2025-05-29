# import json
# import random
# import os
# from .feedback_manager import get_user_preferred_plan, update_user_avoid_list, filter_avoided_items
# from .pdf_generator import generate_plan_pdf
# import logging
# logger = logging.getLogger(__name__)

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# json_path = os.path.join(BASE_DIR, "chatbot_data", "diet_plans.json")

# with open(json_path, "r") as f:
#     diet_plans = json.load(f)

# # Load exercise_plans.json
# exercise_path = os.path.join(BASE_DIR, "chatbot_data", "exercise_plans.json")
# with open(exercise_path, "r", encoding="utf-8") as f:
#     exercise_plans = json.load(f)

# # Load substitutions.json
# substitutions_path = os.path.join(BASE_DIR, "chatbot_data", "substitutions.json")
# with open(substitutions_path, "r", encoding="utf-8") as f:
#     substitutions = {k.lower(): v for k, v in json.load(f).items()}

# chat_memory = {}
# mood_checkin = {}

# def format_plan_response(diet, exercise, mood="neutral"):
#     mood_tone = {
#         "happy": "You're doing great — let's maintain the momentum!",
#         "sad": "It's okay to feel down sometimes. Let's focus on small, supportive actions.",
#         "tired": "Rest matters. Even gentle activity can boost your energy.",
#         "anxious": "Deep breaths — steady progress is still progress.",
#         "depressed": "You're not alone. Let's take this step-by-step together.",
#         "angry": "Let’s channel that energy into something positive.",
#         "low": "Every bit of effort counts. You're doing better than you think.",
#         "good": "That's great! Let’s keep up the positive momentum."
#     }

#     tone = mood_tone.get(mood, "Let’s focus on consistent and healthy progress.")

#     # Format diet and exercise suggestions
#     diet_msg = "\n".join([f"-  {item}" for item in diet])
#     ex_msg = "\n".join([f"-  {item}" for item in exercise])

#     encouragements = [
#         "🔹 Progress is built on consistency — you're on the right path.",
#         "🔹 Each small step adds up — trust the process and keep going."
#     ]

#     return f"""
# ##  Your Personalized Wellness Plan

# ---

# ###  Diet Recommendations:
# {diet_msg}

# ---

# ###  Exercise Suggestions:
# {ex_msg}

# ---

# ###  Note:
# > {tone}

# {random.choice(encouragements)}

# ---

# ###  Need More Guidance?

# - 👉 [View Detailed Diet Plans](https://yourwebsite.com/diet-plans)  
# - 👉 [Explore More Exercise Routines](https://yourwebsite.com/exercise-plans)

# ---

# Would you like to **adjust** or **save** this plan? Let me know how you'd like to proceed.
# """.strip()


# def get_substitution(user_message):
#     user_message_lower = user_message.lower()
#     for key in substitutions:
#         if key in user_message_lower:
#             return f"If you'd like to substitute **{key}**, here are some alternatives: {', '.join(substitutions[key])}"
#     return None

# from .feedback_manager import get_user_preferred_plan, update_user_avoid_list, filter_avoided_items, save_user_mood, load_user_mood


# def get_bot_response(user_message, diagnosis, user_id="default"):
#     if diagnosis==None:
#         diagnosis['predicted'] = True
#         diagnosis['detected'] = True
#         diagnosis['depression'] = True

#     user_message_lower = user_message.lower()

#     # --- Mood Detection ---
#     mood_keywords = ["happy", "sad", "tired", "anxious", "good", "depressed", "angry", "low"]
#     for word in mood_keywords:
#         if word in user_message_lower:
#             prev_mood = mood_checkin.get(user_id)
#             mood_checkin[user_id] = word
#             save_user_mood(user_id, word)

#             if word in ["sad", "low", "depressed","anxious","angry"]:
#                 cheer_up_jokes = [
#                        "Why don't scientists trust atoms? Because they make up everything!",
#                         "How does a penguin build its house? Igloos it together.",
#                         "What do you call a bear with no teeth? A gummy bear!",
#                         "Why did the bicycle fall over? It was two-tired.",
#                         "I'm reading a book on anti-gravity... it's impossible to put down!",
#                         "Why did the scarecrow win an award? Because he was outstanding in his field.",
#                         "What do you call fake spaghetti? An impasta.",
#                         "Why did the golfer bring two pairs of pants? In case he got a hole in one.",
#                         "I told my computer I needed a break, and now it won’t stop sending me vacation ads.",
#                         "What do you get when you cross a snowman and a dog? Frostbite!",
#                         "Why can't your nose be 12 inches long? Because then it would be a foot.",
#                         "I’m on a seafood diet… I see food and I eat it!",
#                         "Why did the tomato blush? Because it saw the salad dressing!",
#                         "How do you organize a space party? You planet.",
#                         "Did you hear about the cheese factory that exploded? There was nothing left but de-brie.",
#                         "Why did the cookie go to the hospital? Because it felt crummy.",
#                         "Parallel lines have so much in common… it’s a shame they’ll never meet.",
#                         "Why did the math book look sad? It had too many problems.",
#                         "Why don't eggs tell jokes? They’d crack each other up.",
#                         "I made a pencil with two erasers… it was pointless.",
#                         "Why couldn’t the leopard play hide and seek? Because he was always spotted.",
#                         "What's orange and sounds like a parrot? A carrot!",
#                         "What do you call a sleeping bull? A bulldozer.",
#                         "Why did the banana go to the doctor? It wasn’t peeling well.",
#                         "What do you call a group of musical whales? An orca-stra.",
#                         "Why did the computer go to art school? Because it had a lot of bytes of creativity.",
#                         "What kind of shoes do ninjas wear? Sneakers!",
#                         "Why did the gym close down? It just didn’t work out.",
#                         "Did you hear about the guy who invented Lifesavers? He made a mint.",
#                         "Why are ghosts such bad liars? Because they are too transparent.",
#                         "Why don't skeletons fight each other? They don’t have the guts.",
#                         "What do you call a fish with no eyes? Fsh.",
#                         "Why don’t seagulls fly over the bay? Because then they’d be bagels.",
#                         "How do cows stay up to date? They read the mooo-spaper.",
#                         "Why did the musician bring a ladder? To reach the high notes.",
#                         "How do you make a tissue dance? You put a little boogie in it.",
#                         "What kind of music do mummies listen to? Wrap music.",
#                         "Why was the broom late? It swept in!",
#                         "What did one wall say to the other wall? I'll meet you at the corner.",
#                         "What did the big flower say to the little flower? Hey bud!"
#                 ]
#                 fun_activities = [
#                     "Try painting or doodling something silly",
#                     "Listen to a happy playlist (or I can recommend one!)",
#                     "Watch a light comedy or cute animal videos",
#                     "Do 5 minutes of gentle breathing or stretching",
#                     "Have a solo dance party to your favorite song!",
#                     "Write down 3 things you're grateful for today",
#                     "Take a funny selfie or record a goofy video",
#                     "Blow bubbles — yes, like the ones from childhood!",
#                     "Read a feel-good short story or comic strip",
#                     "Play or cuddle with a pet (or watch cute pet videos)",
#                     "Scroll through old photos or create a mood board",
#                     "Step outside for a few minutes of fresh air",
#                     "Talk to your plants",
#                     "Bake something simple and sweet",
#                     "Call or voice message a close friend",
#                     "Make a little photo collage of happy memories",
#                     "Try adult coloring books or mandalas",
#                     "Hug a stuffed animal (seriously—it works)",
#                     "Write a kind note to yourself or someone else",
#                     "Pretend you're hosting a talk show and narrate your day",
#                     "Wear your softest, coziest socks and just vibe",
#                     "Clean or organize a small space (satisfying, trust me)",
#                     "Rewatch your favorite childhood cartoon or movie",
#                     "Play a cozy or silly game (even a mobile one!)"
#                 ]

#                 mood_lifting_meals = random.sample([
#                     "Banana and peanut butter smoothie",
#                     "A square of dark chocolate with almonds",
#                     "Warm veggie soup with whole grain toast",
#                     "Greek yogurt with berries and honey",
#                     "Baby carrots with hummus",
#                     "Apple slices with almond or peanut butter",
#                     "A handful of mixed nuts and raisins",
#                     "Cheese cubes with whole grain crackers",
#                     "Banana topped with sunflower seeds",
#                     "Frozen grapes (so refreshing!)",
#                     "Whole grain toast with cottage cheese and honey",
#                     "Sliced cucumber with a sprinkle of sea salt and lemon juice",
#                     "Guacamole with baked tortilla chips",
#                     "Baked sweet potato chips",
#                     "A cup of chamomile tea with a dash of honey",
#                     "Hot cocoa made with almond milk and dark chocolate",
#                     "Herbal coffee with cinnamon and oat milk",
#                     "Green tea with lemon slices",
#                     "Warm turmeric milk (golden milk) with a hint of vanilla",
#                     "Warm apple cider with cinnamon",
#                     "Peppermint tea – soothing and refreshing",
#                     "Coconut milk hot chocolate",
#                     "Warm ginger tea with mint leaves",
#                     "Warm lemon water with honey and a pinch of cayenne",
#                     "Strawberries dipped in dark chocolate",
#                     "Chia pudding with coconut milk and berries",
#                     "A soft oatmeal raisin cookie",
#                     "Frozen yogurt with a sprinkle of granola",
#                     "Greek yogurt parfait with honey and crushed walnuts",
#                     "Banana ice cream (just blend frozen bananas!)",
#                     "Coconut macaroons (light and chewy)",
#                     "Sweet potato brownie bites",
#                     "Medjool dates stuffed with almond butter",
#                     "A couple of pieces of 70% dark chocolate"
#                 ], 4)

#                 return f"""
# I'm really sorry you're feeling {word}. You're not alone, and I’m here to support you 

# Here are some things that might help lift your spirits:

#  **Try This Fun Activity:** {random.choice(fun_activities)}
#  **Mood-Lifting Snack:** {random.choice(mood_lifting_meals)}
#  **Here's a Joke to Make You Smile:** {random.choice(cheer_up_jokes)}

# If you need a friendly plan to feel better today, just say "plan" and I’ll whip one up! 
# """.strip(), {}
            
#             if prev_mood and prev_mood != word:
#                 return f"Thanks for the update! I've noted you're feeling **{word}** now. ", {}
#             elif not prev_mood:
#                 return f"Thanks for sharing. I've noted you're feeling **{word}** ", {}

#     # --- Load Saved Mood if Not Available ---
#     if user_id not in mood_checkin:
#         saved_mood = load_user_mood(user_id)
#         if saved_mood:
#             mood_checkin[user_id] = saved_mood
#         else:
#             return "Before we begin, how are you feeling today?  (e.g., happy, anxious, tired)", {}
        
#     # --- Redirect if user asks about PCOS or depression ---
#     if any(keyword in user_message_lower for keyword in ["pcos", "pcod", "depression", "symptoms", "mental health"]):
#         return (
#             "It sounds like you want to learn more about PCOS or depression.  "
#             "You can explore symptoms, detection, and get support here: [Visit our website](https://your-pcos-website.com) ",
#             {}
#         )
    
#     # --- Substitution Check ---
#     sub_msg = get_substitution(user_message)
#     if sub_msg:
#         return sub_msg, {}

#     # --- Avoidance Handling ---
#     if any(phrase in user_message_lower for phrase in ["avoid", "don’t like", "no "]):
#         for item in substitutions:
#             if item in user_message_lower:
#                 update_user_avoid_list(user_id, item)
#                 return f"Got it! I’ll remember to avoid {item} in your future plans.", {}

#     # --- Chat Memory ---
#     if user_id not in chat_memory:
#         chat_memory[user_id] = []
#     chat_memory[user_id].append(user_message)
#     if "save" in user_message_lower and "pln" in user_message_lower:
#     # Reverse-search for the most recent valid plan
#         for entry in reversed(chat_memory.get(user_id, [])):
#             if all(k in entry for k in ["diet", "exercise", "diagnosis", "mood"]):
#                 # Fix dicts if present
#                 diagnosis = entry["diagnosis"]
#                 mood = entry["mood"]

#                 if isinstance(diagnosis, dict):
#                     diagnosis = diagnosis.get("label", "Unknown")
#                 if isinstance(mood, dict):
#                     mood = mood.get("description", "Unknown")

#                 pdf_path = generate_plan_pdf(
#                     user_id,
#                     diagnosis,
#                     entry["diet"],
#                     entry["exercise"],
#                     mood
#                 )
#                 return (
#                     f" Your personalized wellness plan has been saved successfully!\n\n"
#                     f" [Click here to download your plan]({pdf_path})",
#                     {
#                         "pdf_path": pdf_path,
#                         **entry
#                     }
#                 )
#         return " Hmm, I couldn't find a recent plan to save. Try generating a new one first!", {}

#     # --- Plan Request Handling ---
#     if "plan" in user_message_lower:
#         status = "default"
#         logger.info(f"Received diagnosis: {diagnosis}")
#         if diagnosis.get("predicted") and not diagnosis.get("detected"):
#             status = "predicted"
#         elif diagnosis.get("predicted") and diagnosis.get("detected") and not diagnosis.get("depression"):
#             status = "confirmed"
#         elif diagnosis.get("depression"):
#             status = "depression"

#         mood = mood_checkin.get(user_id, "neutral")

#         # Mood-aware fallbacks
#         diet_raw = diet_plans.get(mood, diet_plans.get(status, diet_plans["default"]))
#         exercise_raw = exercise_plans.get(mood, exercise_plans.get(status, exercise_plans["default"]))

#         # Apply avoid list
#         diet_filtered = filter_avoided_items(user_id, diet_raw)
#         exercise_filtered = filter_avoided_items(user_id, exercise_raw)

#         # Feedback-based sorting
#         diet = get_user_preferred_plan(status, diet_filtered)
#         exercise = get_user_preferred_plan(status, exercise_filtered)

#         # Save for re-use
#         plan_result = {
#             "diagnosis": status,
#             "diet": diet,
#             "exercise": exercise,
#             "mood": mood
#         }

#         chat_memory[user_id].append({
#                 "diet": diet,
#                 "exercise": exercise,
#                 "diagnosis": diagnosis,
#                 "mood": mood,
#                 # "timestamp": datetime.now().isoformat()  # optional, for latest tracking
#             })

#         return format_plan_response(diet, exercise, mood), plan_result

#     # --- PDF Save Handling ---

#     # --- Default Response ---
#     return "Hi there! Let me know if you'd like a diet or exercise plan, or need a substitution!"


# import json
# import random
# import os
# import logging
# from .feedback_manager import (
#     get_user_preferred_plan,
#     update_user_avoid_list,
#     filter_avoided_items,
#     save_user_mood,
#     load_user_mood,
# )
# from .pdf_generator import generate_plan_pdf

# logger = logging.getLogger(__name__)

# class ChatbotEngine:
#     def __init__(self, base_dir):
#         self.base_dir = base_dir
#         self.chat_memory = {}
#         self.mood_checkin = {}
#         self.diet_plans = self._load_json("chatbot_data/diet_plans.json")
#         self.exercise_plans = self._load_json("chatbot_data/exercise_plans.json")
#         self.substitutions = self._load_json("chatbot_data/substitutions.json", lower_keys=True)

#     def _load_json(self, relative_path, lower_keys=False):
#         path = os.path.join(self.base_dir, relative_path)
#         with open(path, "r", encoding="utf-8") as f:
#             data = json.load(f)
#             if lower_keys:
#                 return {k.lower(): v for k, v in data.items()}
#             return data

#     def get_mood_tone(self, mood):
#         mood_tones = {
#             "happy": "You're doing great — let's maintain the momentum!",
#             "sad": "It's okay to feel down sometimes. Let's focus on small, supportive actions.",
#             "tired": "Rest matters. Even gentle activity can boost your energy.",
#             "anxious": "Deep breaths — steady progress is still progress.",
#             "depressed": "You're not alone. Let's take this step-by-step together.",
#             "angry": "Let’s channel that energy into something positive.",
#             "low": "Every bit of effort counts. You're doing better than you think.",
#             "good": "That's great! Let’s keep up the positive momentum.",
#         }
#         return mood_tones.get(mood, "Let’s focus on consistent and healthy progress.")

#     def format_plan_response(self, diet, exercise, mood="neutral"):
#         tone = self.get_mood_tone(mood)
#         diet_msg = "\n".join([f"-  {item}" for item in diet])
#         ex_msg = "\n".join([f"-  {item}" for item in exercise])
#         encouragements = [
#             "🔹 Progress is built on consistency — you're on the right path.",
#             "🔹 Each small step adds up — trust the process and keep going.",
#         ]
#         return f"""
# ##  Your Personalized Wellness Plan

# ---

# ###  Diet Recommendations:
# {diet_msg}

# ---

# ###  Exercise Suggestions:
# {ex_msg}

# ---

# ###  Note:
# > {tone}

# {random.choice(encouragements)}

# ---

# ###  Need More Guidance?

# - 👉 [View Detailed Diet Plans](https://yourwebsite.com/diet-plans)  
# - 👉 [Explore More Exercise Routines](https://yourwebsite.com/exercise-plans)

# ---

# Would you like to **adjust** or **save** this plan? Let me know how you'd like to proceed.
# """.strip()

#     def get_substitution(self, user_message):
#         user_message_lower = user_message.lower()
#         for key in self.substitutions:
#             if key in user_message_lower:
#                 return f"If you'd like to substitute **{key}**, here are some alternatives: {', '.join(self.substitutions[key])}"
#         return None

#     def handle_mood_detection(self, user_message, user_id):
#         mood_keywords = ["happy", "sad", "tired", "anxious", "good", "depressed", "angry", "low"]
#         for word in mood_keywords:
#             if word in user_message.lower():
#                 prev_mood = self.mood_checkin.get(user_id)
#                 self.mood_checkin[user_id] = word
#                 save_user_mood(user_id, word)
#                 if prev_mood and prev_mood != word:
#                     return f"Thanks for the update! I've noted you're feeling **{word}** now."
#                 return f"Thanks for sharing. I've noted you're feeling **{word}**."
#         return None

#     def generate_plan(self, diagnosis, user_id):
#         status = self._get_diagnosis_status(diagnosis)
#         mood = self.mood_checkin.get(user_id, "neutral")
#         diet_raw = self.diet_plans.get(mood, self.diet_plans.get(status, self.diet_plans["default"]))
#         exercise_raw = self.exercise_plans.get(mood, self.exercise_plans.get(status, self.exercise_plans["default"]))
#         diet_filtered = filter_avoided_items(user_id, diet_raw)
#         exercise_filtered = filter_avoided_items(user_id, exercise_raw)
#         diet = get_user_preferred_plan(status, diet_filtered)
#         exercise = get_user_preferred_plan(status, exercise_filtered)
#         return self.format_plan_response(diet, exercise, mood), {"diet": diet, "exercise": exercise, "mood": mood}

#     def _get_diagnosis_status(self, diagnosis):
#         if diagnosis.get("predicted") and not diagnosis.get("detected"):
#             return "predicted"
#         elif diagnosis.get("predicted") and diagnosis.get("detected") and not diagnosis.get("depression"):
#             return "confirmed"
#         elif diagnosis.get("depression"):
#             return "depression"
#         return "default"

#     def get_bot_response(self, user_message, diagnosis, user_id="default"):
#         if not diagnosis:
#             diagnosis = {"predicted": True, "detected": True, "depression": True}

#         mood_response = self.handle_mood_detection(user_message, user_id)
#         if mood_response:
#             return mood_response, {}

#         if user_id not in self.mood_checkin:
#             saved_mood = load_user_mood(user_id)
#             if saved_mood:
#                 self.mood_checkin[user_id] = saved_mood
#             else:
#                 return "Before we begin, how are you feeling today? (e.g., happy, anxious, tired)", {}

#         if "plan" in user_message.lower():
#             return self.generate_plan(diagnosis, user_id)

#         substitution_response = self.get_substitution(user_message)
#         if substitution_response:
#             return substitution_response, {}

#         if any(phrase in user_message.lower() for phrase in ["avoid", "don’t like", "no "]):
#             for item in self.substitutions:
#                 if item in user_message.lower():
#                     update_user_avoid_list(user_id, item)
#                     return f"Got it! I’ll remember to avoid {item} in your future plans.", {}

#         return "Hi there! Let me know if you'd like a diet or exercise plan, or need a substitution!", {}


# # Usage
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# chatbot = ChatbotEngine(BASE_DIR)


import os
import json
import random
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
        self.jokes = self._load_json("chatbot_data/jokes.json")
        self.affirmations = self._load_json("chatbot_data/affirmations.json")
        # self.jokes = self.jokes.get("jokes", [])
        # self.affirmations = self.affirmations.get("affirmations", [])

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
        diet_msg = "\n".join([f"- {item}" for item in diet])
        ex_msg = "\n".join([f"- {item}" for item in exercise])
        encouragement = random.choice(self.affirmations) if self.affirmations else "You're doing great!"

        return f"""
## 🧘‍♀️ Your Personalized Wellness Plan

---

### 🥗 Diet Recommendations:
{diet_msg}

---

### 🏃‍♀️ Exercise Suggestions:
{ex_msg}

---

### 🧠 Note:
> {tone}

💡 {encouragement}

Would you like to **adjust**, **save as PDF**, or get a new plan?
"""

    def get_substitution(self, user_message):
        user_message_lower = user_message.lower()
        for key in self.substitutions:
            if key in user_message_lower:
                alternatives = ", ".join(self.substitutions[key])
                return f"Looking to substitute **{key}**? Try: {alternatives}"
        return None

    def handle_mood_detection(self, user_message, user_id):
        mood_keywords = ["happy", "sad", "tired", "anxious", "good", "depressed", "angry", "low"]
        for word in mood_keywords:
            if word in user_message.lower():
                prev_mood = self.mood_checkin.get(user_id)
                self.mood_checkin[user_id] = word
                save_user_mood(user_id, word)
                if prev_mood and prev_mood != word:
                    return f"Thanks for the update! You're now feeling **{word}**."
                return f"Thanks for sharing. You're feeling **{word}**."
        return None

    def generate_plan(self, diagnosis, user_id):
        status = self._get_diagnosis_status(diagnosis)
        mood = self.mood_checkin.get(user_id, "neutral")

        # Load and filter plans
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

    def get_bot_response(self, user_message, diagnosis=None, user_id="default"):
        if diagnosis is None:
            diagnosis = {"predicted": False, "detected": False, "depression": False}

        # Mood check/update
        mood_response = self.handle_mood_detection(user_message, user_id)
        if mood_response:
            return mood_response, {}

        # Ask for mood if not provided
        if user_id not in self.mood_checkin:
            saved_mood = load_user_mood(user_id)
            if saved_mood:
                self.mood_checkin[user_id] = saved_mood
            elif saved_mood is None:
                return "Before we begin, how are you feeling today? (happy, tired, anxious, etc.)", {}

        # Plan generation
        if "plan" in user_message.lower():
            return self.generate_plan(diagnosis, user_id)

        # Save plan
        if "save as pdf" in user_message.lower() or "pdf" in user_message.lower():
            plan_text, data = self.generate_plan(diagnosis, user_id)
            filename = generate_plan_pdf(user_id=user_id, diet=data["diet"], exercise=data["exercise"], mood=data["mood"])
            return f"Your plan has been saved as a PDF! 📄 You can download it here: `/media/plans/{filename}`", {}

        # Substitution
        substitution_response = self.get_substitution(user_message)
        if substitution_response:
            return substitution_response, {}

        # Avoid list
        if any(keyword in user_message.lower() for keyword in ["avoid", "don’t like", "no "]):
            for item in self.substitutions:
                if item in user_message.lower():
                    update_user_avoid_list(user_id, item)
                    return f"Understood! I’ll avoid **{item}** in your future plans.", {}

        # Joke
        if "joke" in user_message.lower():
            return random.choice(self.jokes), {}

        # Default response
        return (
            "Hi! 👋 I can help with diet or exercise plans, substitutions, or even tell you a joke! Just type what you need 😊",
            {}
        )


# Initialize the chatbot engine
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
chatbot = ChatbotEngine(BASE_DIR)