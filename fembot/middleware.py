from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import TokenError, ExpiredTokenError
import logging
import json

User = get_user_model()

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class JWTAuthMiddleware(BaseMiddleware):
    """
    Middleware to extract and validate JWT from cookies or query string, then set the user in the scope.
    """
    async def __call__(self, scope, receive, send):
        # Log the incoming scope to debug
        logger.info(f"Scope data: {scope}")
        
        # Extract token from query parameters
        token = None
        query_string = scope.get("query_string", b"").decode()
        logger.info(f"Query string: {query_string}")  # Log the query string

        qs = parse_qs(query_string)
        token = qs.get('token', [None])[0]

        if not token:
            logger.warning("No token found in query string.")
            await send_error_message(send, "No token provided.")
            return  # Exit early if there's no token

        # Default to anonymous user if no token
        scope["user"] = AnonymousUser()

        if token:
            try:
                logger.info(f"Attempting to validate token: {token}")
                validated_token = UntypedToken(token)
                logger.info(f"Validated token: {validated_token}")

                user_id = validated_token["user_id"]
                logger.info(f"User ID from token: {user_id}")

                user = await database_sync_to_async(User.objects.get)(id=user_id)
                logger.info(f"Authenticated user: {user}")

                # Set the user in scope
                scope["user"] = user

            except ExpiredTokenError as e:
                logger.error("Token has expired.")
                await send_error_message(send, "Token expired. Please log in again.")
                return  # Exit early if token is expired
            except TokenError as e:
                logger.error(f"Token error: {e}")
                await send_error_message(send, "Token is invalid. Please log in again.")
                return  # Exit early if token is invalid

        return await super().__call__(scope, receive, send)


async def send_error_message(send, message):
    # This function ensures that we only send an error message after the socket is accepted
    try:
        await send({
            'type': 'websocket.send',
            'text': json.dumps({'message': message})
        })
    except ValueError as e:
        logger.error(f"Error sending message: {e}")