import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .chatbot_engine import chatbot  # relative import
from fembot.models import ChatHistory  # Using ChatHistory model
from backend.models import PCOSDetectionLog, PCOSPredictionLog

from rest_framework_simplejwt.tokens import AccessToken

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class ChatBotConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chatbot = chatbot

    async def connect(self):
        self.user = self.scope['user']
        await self.accept()
        logger.info("WebSocket connection established.")
        await self.send_welcome_message()

    async def disconnect(self, code):
        logger.info(f"WebSocket connection closed with close code {code}.")

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            logger.warning("Received no text data.")
            return

        try:
            data = self.parse_message(text_data)
            user_input = data.get('message')
            logger.info(f"User: {self.user}, Authenticated: {self.user.is_authenticated}, User ID: {self.user.id}")
            logger.info(f"Received message: {user_input}")

            if self.user.is_authenticated and self.user.id:
                bot_reply = await self.get_bot_reply(user_input)
                await self.save_chat_to_db(self.user.id, user_input, bot_reply)
                await self.send_message(bot_reply)
            else:
                logger.warning("Unauthenticated user interaction blocked.")
                await self.send_error_message()
        except Exception as e:
            logger.error(f"Error while processing the message: {e}")
            await self.send_error_message()

    async def send_welcome_message(self):
        welcome_message = {"message": "Hello from FemHealth ChatBot!"}
        await self.send(text_data=json.dumps(welcome_message))

    async def send_message(self, message):
        await self.send(text_data=json.dumps({'message': message}))

    async def send_error_message(self):
        error_message = {'message': 'Sorry, there was an error processing your request.'}
        await self.send(text_data=json.dumps(error_message))

    def parse_message(self, text_data):
        return json.loads(text_data)

    async def get_bot_reply(self, user_input):
        # fetch latest prediction and detection logs via sync_to_async
        pred = await sync_to_async(
            lambda: PCOSPredictionLog.objects.filter(user=self.user).order_by('-created_at').first()
        )()
        detected_log = await sync_to_async(
            lambda: PCOSDetectionLog.objects.filter(user=self.user).order_by('-created_at').first()
        )()

        predicted = False
        detected = False
        depression = False

        if pred:
            predicted = pred.risk_level >= 75
            depression = pred.cycle_irregularity >= 75
        if detected_log:
            detected = detected_log.label == "PCOS Detected"

        diagnosis = {
            'predicted': predicted,
            'detected': detected,
            'depression': depression
        }

        # get bot response synchronously or asynchronously as needed
        response = await sync_to_async(self.chatbot.get_bot_response)(user_input, diagnosis=diagnosis)
        return response

    async def save_chat_to_db(self, user_id, user_input, bot_reply):
        try:
            chat_log = ChatHistory(
                user_id=user_id,
                message=user_input,
                bot_response=bot_reply
            )
            await sync_to_async(chat_log.save)()
            logger.info("Chat log saved to the database.")
        except Exception as e:
            logger.error(f"Error saving chat log to the database: {e}")
