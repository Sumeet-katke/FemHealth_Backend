from django.db import models

# Create your models here.
# In your main app's models.py (FemHealth App)
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
# import uuid

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    age = models.PositiveIntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)  # in kilograms
    height = models.FloatField(blank=True, null=True)  # in meters

    BMI = models.FloatField(blank=True, null=True, editable=False)  # Calculated automatically

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.weight and self.height and self.height > 0:
            height_in_meters = self.height / 100  # convert cm to meters
            self.BMI = round(self.weight / (height_in_meters ** 2), 2)
        else:
            self.BMI = None
        super().save(*args, **kwargs)
    
# class PCOSPrediction(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # femhealth/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class CycleEntry(models.Model):
    """
    One row per user per date, logging flow/mood/symptoms.
    If `is_period_start` is True, we also snapshot MeanCycleLength
    so that we can feed it to the predictor just like your old PeriodLog.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cycle_entries'
    )
    date = models.DateField()
    
    # Daily diary fields
    flow = models.PositiveSmallIntegerField(default=0, help_text="1–5, or 0=no flow")
    mood = models.CharField(max_length=20, blank=True)
    symptoms = models.JSONField(default=list, help_text="e.g. ['Cramps','Bloating']")
    
    # “Period start” marker: when true, we treat this date as a new cycle
    is_period_start = models.BooleanField(default=False)
    # Only populated when is_period_start == True
    MeanCycleLength = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Avg cycle length on this start date"
    )
    ReproductiveCategory = models.CharField(
        max_length=50, blank=True, null=True
    )
    
    # snapshot of user at time of period start
    age = models.PositiveIntegerField(blank=True, null=True)
    BMI = models.FloatField(blank=True, null=True)
    Weight = models.FloatField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def save(self, *args, **kwargs):
        # Auto‐snapshot user stats when marking a period start
        if self.is_period_start:
            u = self.user
            self.age = u.age
            self.Weight = u.weight
            self.BMI = u.BMI
            # If you already have a history, you could recompute MeanCycleLength here,
            # or let the frontend pass it in via the serializer.
        super().save(*args, **kwargs)

    def __str__(self):
        tag = "Start" if self.is_period_start else "Entry"
        return f"{self.user.email} – {self.date} ({tag})"

# models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PCOSPredictionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    age = models.PositiveIntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    cycleType = models.CharField(max_length=1, choices=[('R', 'Regular'), ('I', 'Irregular')])
    cycleLength = models.PositiveIntegerField()
    marriedYears = models.PositiveIntegerField()
    pregnant = models.PositiveIntegerField()
    abortions = models.PositiveIntegerField()

    risk_level = models.FloatField()
    hormonal_imbalance = models.FloatField()
    cycle_irregularity = models.FloatField()
    
# femhealth/models.py
from django.db import models
from django.conf import settings

class PCOSDetectionLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pcos_detections'
    )
    image = models.ImageField(upload_to='pcos_detections/')
    score = models.FloatField(help_text="Probability score from the detector model")
    label = models.CharField(max_length=50, help_text="Predicted label, e.g. 'PCOS Detected' or 'No PCOS'")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.label} ({self.score:.2f}) on {self.created_at:%Y-%m-%d %H:%M}"
