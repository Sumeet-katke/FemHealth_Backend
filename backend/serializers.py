from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser as User

# Serializer for User Registration
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'phone', 'first_name', 'last_name', 'age', 'weight', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)
    
# serializers.py
from rest_framework import serializers
from .models import PCOSPredictionLog

class PCOSPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCOSPredictionLog
        fields = [
            'id', 'user', 'created_at', 'age', 'weight', 'height', 'cycleType',
            'cycleLength', 'marriedYears', 'pregnant', 'abortions',
            'risk_level', 'hormonal_imbalance', 'cycle_irregularity'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'risk_level', 'hormonal_imbalance', 'cycle_irregularity']

from rest_framework import serializers
# from .models import PeriodLog
from rest_framework import serializers
from .models import CycleEntry

class CycleEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for CycleEntry, handling both daily logs and period-start snapshots.
    """
    class Meta:
        model = CycleEntry
        fields = [
            'id',
            'date',
            'flow',
            'mood',
            'symptoms',
            'is_period_start',
            'MeanCycleLength',
            'ReproductiveCategory',
            'age',
            'BMI',
            'Weight',
            'created_at'
        ]
        read_only_fields = [
            'id',
            'age',
            'BMI',
            'Weight',
            'created_at'
        ]


# femhealth/serializers.py

from rest_framework import serializers
from .models import PCOSDetectionLog

class PCOSDetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCOSDetectionLog
        fields = [
            'id',
            'user',
            'image',
            'score',
            'label',
            'created_at'
        ]
        read_only_fields = [
            'id',
            'user',
            'score',
            'label',
            'created_at'
        ]