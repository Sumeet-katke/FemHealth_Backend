from django.db import models

# Create your models here.
from django.db import models
# from django.contrib.auth.models import settings.AUTH_USER_MODEL
from django.conf import settings

# Mood Model - Tracks the mood of users for personalized responses
class Mood(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mood = models.CharField(max_length=50, choices=[
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('tired', 'Tired'),
        ('anxious', 'Anxious'),
        ('depressed', 'Depressed'),
        ('angry', 'Angry'),
        ('low', 'Low'),
        ('good', 'Good'),
        ('neutral', 'Neutral'),
    ], default='neutral')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.mood}'

# settings.AUTH_USER_MODEL Preferences Model - Stores individual preferences like avoid list, preferred plans, etc.
class UserPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avoid_list = models.JSONField(default=list)  # A list of foods, exercises to avoid
    preferred_diet = models.CharField(max_length=100, blank=True, null=True)
    preferred_exercise = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Preferences'

# Chat History Model - Stores user's chat history for the chatbot, useful for understanding context
class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chat with {self.user.username} - {self.timestamp}'

# Plan Model - Stores the personalized plans like diet and exercise
class Plan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    diet_plan = models.JSONField()  # JSON data storing diet recommendations
    exercise_plan = models.JSONField()  # JSON data storing exercise recommendations
    mood = models.CharField(max_length=50, choices=[
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('tired', 'Tired'),
        ('anxious', 'Anxious'),
        ('depressed', 'Depressed'),
        ('angry', 'Angry'),
        ('low', 'Low'),
        ('good', 'Good'),
        ('neutral', 'Neutral'),
    ], default='neutral')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Plan for {self.user.username} - {self.created_at}'

# Substitution Model - Tracks substitutions for foods, activities, etc.
class Substitution(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_to_avoid = models.CharField(max_length=100)  # The item user wants to avoid
    substitution_items = models.JSONField()  # List of items that can replace the item_to_avoid

    def __str__(self):
        return f'{self.user.username} - Avoiding {self.item_to_avoid}'

# Bot Feedback Model - Stores feedback about the bot's responses
class BotFeedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    feedback = models.TextField()  # Textual feedback from the user about the chatbot
    rating = models.IntegerField(choices=[(1, 'Very Bad'), (2, 'Bad'), (3, 'Neutral'), (4, 'Good'), (5, 'Excellent')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback from {self.user.username} - Rating {self.rating}'