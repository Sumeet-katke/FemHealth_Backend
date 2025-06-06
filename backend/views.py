from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser as User
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from .serializers import RegisterUserSerializer
from django.conf import settings
import os 


class RegisterUserAPIView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        
        try:
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                userData = {
                    "email": user.email,
                    "phone": user.phone,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "age": user.age,
                    "weight": user.weight
                }
                return Response({
                    "message": "User registered successfully.",
                    "user": userData,
                    "refresh_token": str(refresh),
                    "access_token": str(refresh.access_token)
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "message": "Validation failed.",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({
                "message": "Validation error occurred.",
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": "An unexpected error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class LoginUserAPIView(APIView):
    def post(self, request): 
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"error": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        userData = {
            "email": user.email,
            "phone": user.phone,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "weight": user.weight
        }
        # You can also include other user data in the response if needed
        return Response({
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
            "user": userData
        }, status=status.HTTP_200_OK)
    def get(self, request):
        return Response({"message": "GET request received."}, status=status.HTTP_200_OK)
    def put(self, request):
        return Response({"message": "PUT request received."}, status=status.HTTP_200_OK)
    

    
#PCOS Prediction
# views.py
import numpy as np
import joblib
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import PCOSPredictionLog
from .serializers import PCOSPredictionSerializer

model_path = os.path.join(settings.BASE_DIR, 'femhealth', 'Models', 'pcos_xgboost_model.pkl')
scaler_file = os.path.join(settings.BASE_DIR, 'femhealth', 'Models', 'scaler.pkl')


# Load model and scaler only once
model = joblib.load(model_path)
scaler, feature_columns = joblib.load(scaler_file)


# 2) Blood‐group dropdown → numeric mapping
BLOOD_GROUP_MAP = {
    'A+': 11, 'A-': 12,
    'B+': 13, 'B-': 14,
    'O+': 15, 'O-': 16,
    'AB+':17, 'AB-':18
}

# 3) Default fallback for all 44 features (keys must exactly match feature_columns)
DEFAULTS = {
    'Age_yrs': 26,
    'Weight_Kg': 70,
    'HeightCm': 160,
    'BMI': 27,
    'Blood_Group': 11,
    'Pulse_ratebpm': 78,
    'RR_breaths/min': 18,
    'Hbg/dl': 12,
    'CycleR/I': 1,
    'Cycle_lengthdays': 30,
    'Marraige_Status_Yrs': 0,
    'PregnantY/N': 0,
    'No._of_aborptions': 0,
    'I___beta-HCGmIU/mL': 2,
    'II____beta-HCGmIU/mL': 2,
    'FSHmIU/mL': 6.5,
    'LHmIU/mL': 7.2,
    'FSH/LH': 0.9,
    'Hipinch': 36,
    'Waistinch': 32,
    'Waist:Hip_Ratio': 0.88,
    'TSH_mIU/L': 2.5,
    'AMHng/mL': 3,
    'PRLng/mL': 12,
    'Vit_D3_ng/mL': 22,
    'PRGng/mL': 0.5,
    'RBSmg/dl': 95,
    'Weight_gainY/N': 0,
    'hair_growthY/N': 0,
    'Skin_darkening_Y/N': 0,
    'Hair_lossY/N': 0,
    'PimplesY/N': 0,
    'Fast_food_Y/N': 1,
    'Reg.ExerciseY/N': 1,
    'BP__Systolic_mmHg': 120,
    'BP__Diastolic_mmHg': 80,
    'Follicle_No._L': 10,
    'Follicle_No._R': 10,
    'Avg._F_size_L_mm': 3.5,
    'Avg._F_size_R_mm': 3.5,
    'Endometrium_mm': 8,
    'I___beta-HCGmIU/mL_dup': 2,
    'II____beta-HCGmIU/mL_dup': 2,
    'AMHng/mL_dup': 3
}

class PCOSPredictView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """
        Return the latest prediction in the same { predictions: [...] } format.
        """
        try:
            last = (
                PCOSPredictionLog.objects
                .filter(user=request.user)
                .latest('created_at')
            )
        except PCOSPredictionLog.DoesNotExist:
            return Response(
                {"detail": "No predictions found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            "predictions": [
                { "label": "Risk Level",         "value": round(last.risk_level, 2) },
                { "label": "Hormonal Imbalance", "value": round(last.hormonal_imbalance, 2) },
                { "label": "Cycle Irregularity", "value": round(last.cycle_irregularity, 2) },
            ]
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            data = request.data

            # --- 1) Parse & clean user inputs ---
            age            = int(data.get('age', DEFAULTS['Age_yrs']))
            weight         = float(data.get('weight', DEFAULTS['Weight_Kg']))
            height         = float(data.get('height', DEFAULTS['HeightCm']))
            bmi            = round(weight / ((height/100)**2), 2)
            cycle_flag     = 1 if data.get('cycleType','R') == 'I' else 0
            cycle_length   = int(data.get('cycleLength', DEFAULTS['Cycle_lengthdays']))
            married_years  = int(data.get('marriedYears', DEFAULTS['Marraige_Status_Yrs']))
            pregnant_flag  = 1 if data.get('pregnant','No') == 'Yes' else 0
            abortions      = int(data.get('abortions', DEFAULTS['No._of_aborptions']))

            # Booleans from selects:
            weight_gain    = 1 if data.get('weightGain','No') == 'Yes' else 0
            hair_growth    = 1 if data.get('hairGrowth','No') == 'Yes' else 0
            skin_darkening = 1 if data.get('skinDarkening','No') == 'Yes' else 0
            hair_loss      = 1 if data.get('hairLoss','No') == 'Yes' else 0
            pimples        = 1 if data.get('pimples','No') == 'Yes' else 0
            fast_food      = 1 if data.get('fastFood','No') == 'Yes' else 0
            exercise       = 1 if data.get('exercise','No') == 'Yes' else 0

            # Map blood group
            bg_code = BLOOD_GROUP_MAP.get(data.get('bloodGroup'), DEFAULTS['Blood_Group'])

            # --- 2) Build full 44-length feature map ---
            feature_map = {}
            feature_map.update({
                'Age_yrs': age,
                'Weight_Kg': weight,
                'HeightCm': height,
                'BMI': bmi,
                'Blood_Group': bg_code,
                'CycleR/I': cycle_flag,
                'Cycle_lengthdays': cycle_length,
                'Marraige_Status_Yrs': married_years,
                'PregnantY/N': pregnant_flag,
                'No._of_aborptions': abortions,
                'Weight_gainY/N': weight_gain,
                'hair_growthY/N': hair_growth,
                'Skin_darkening_Y/N': skin_darkening,
                'Hair_lossY/N': hair_loss,
                'PimplesY/N': pimples,
                'Fast_food_Y/N': fast_food,
                'Reg.ExerciseY/N': exercise
            })

            # --- 3) Assemble into array, scale & predict ---
            X        = [feature_map[f] for f in feature_columns]
            X_scaled = scaler.transform([X])
            pred     = model.predict(X_scaled)[0]
            prob     = model.predict_proba(X_scaled)[0][1]

            # Sub‐scores
            risk_level         = round(prob * 100, 2)
            hormonal_imbalance = round(risk_level * 0.75, 2)
            cycle_irregularity = round(risk_level * 0.85, 2)

            # --- 4) Save log ---
            PCOSPredictionLog.objects.create(
                user=request.user,
                age=age,
                weight=weight,
                height=height,
                cycleType='I' if cycle_flag else 'R',
                cycleLength=cycle_length,
                marriedYears=married_years,
                pregnant=pregnant_flag,
                abortions=abortions,
                risk_level=risk_level,
                hormonal_imbalance=hormonal_imbalance,
                cycle_irregularity=cycle_irregularity
            )

            # --- 5) Return response ---
            return Response({
                "predictions": [
                    { "label": "Risk Level",         "value": round(risk_level, 2) },
                    { "label": "Hormonal Imbalance", "value": round(hormonal_imbalance, 2) },
                    { "label": "Cycle Irregularity", "value": round(cycle_irregularity, 2) },
                ]
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# femhealth/views.py
import datetime
import pandas as pd
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from .models import CycleEntry
from .serializers import CycleEntrySerializer

# assume `model` is already imported & instantiated above

class CycleEntryListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return only the current cycle’s contiguous daily entries,
        starting from the last period start up through today.
        """
        today = timezone.localdate()

        # 1) find the last period start on or before today
        last_start = (
            CycleEntry.objects
            .filter(user=request.user, is_period_start=True, date__lte=today)
            .order_by('-date')
            .first()
        )
        if not last_start:
            return Response(
                {"detail": "No period start found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2) pull all entries from that date up to today (inclusive)
        entries_qs = CycleEntry.objects.filter(
            user=request.user,
            date__gte=last_start.date,
            date__lte=today
        ).order_by('date')

        # 3) build a date→entry map for quick lookup
        entry_map = {entry.date: entry for entry in entries_qs}

        # 4) walk day-by-day from start until a missing day
        continuous = []
        cur = last_start.date
        while cur <= today:
            if cur in entry_map:
                continuous.append(entry_map[cur])
            else:
                break
            cur += timedelta(days=1)

        # 5) serialize and return
        serializer = CycleEntrySerializer(continuous, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def post(self, request):
        """
        Accepts { entries: [ { date, flow, mood, symptoms,
                               is_period_start?, MeanCycleLength?, ReproductiveCategory? }, … ] }
        and upserts each one, auto-marking new period starts if >2 days since last start.
        """
        entries = request.data.get('entries')
        if not isinstance(entries, list):
            return Response(
                {"detail": "`entries` must be a list."},
                status=status.HTTP_400_BAD_REQUEST
            )

        saved, errors = [], []
        # Fetch last period-start up front
        last_start = (
            CycleEntry.objects
            .filter(user=request.user, is_period_start=True)
            .order_by('-date')
            .first()
        )

        for idx, entry in enumerate(entries):
            serializer = CycleEntrySerializer(data=entry)
            if not serializer.is_valid():
                errors.append({idx: serializer.errors})
                continue

            data = serializer.validated_data

            # Auto-detect new period start if not explicitly set
            is_start = data.get('is_period_start', False)
            entry_date = data['date']
            if not is_start:
                if (not last_start) or ((entry_date - last_start.date) >= timedelta(days=3)):
                    data['is_period_start'] = True
                    # update last_start so subsequent entries in this batch use the new start
                    last_start = type(last_start)(
                        user=request.user,
                        date=entry_date,
                        is_period_start=True
                    )
                else:
                    data['is_period_start'] = False

            # Upsert the entry
            obj, _ = CycleEntry.objects.update_or_create(
                user=request.user,
                date=data['date'],
                defaults=data
            )
            saved.append(CycleEntrySerializer(obj).data)

        status_code = (status.HTTP_207_MULTI_STATUS if errors else status.HTTP_201_CREATED)
        response_payload = {"saved": saved}
        if errors:
            response_payload["errors"] = errors

        return Response(response_payload, status=status_code)


# femhealth/views.py
# femhealth/views.py

import datetime
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import CycleEntry

import pickle

# --- 1) load the period model once at top ---
period_model_path = os.path.join(settings.BASE_DIR, 'femhealth', 'Models','period_prediction_model_2.pkl')

with open(period_model_path, 'rb') as f:
    period_model = pickle.load(f)

import datetime
import pandas as pd
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import CycleEntry
from .serializers import CycleEntrySerializer
# assume `model` is already imported & instantiated

class PredictPeriod(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # 1) fetch the last period-start on or before today
        today = timezone.localdate()
        try:
            last_start = (
                CycleEntry.objects
                .filter(user=request.user, is_period_start=True, date__lte=today)
                .latest('date')
            )
        except CycleEntry.DoesNotExist:
            return Response(
                {"detail": "No period data available."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2) collect entries since that date to compute menses stats
        entries = CycleEntry.objects.filter(
            user=request.user,
            date__gte=last_start.date,
            date__lte=today
        ).order_by('date')

        # 3) compute menses length & total score
        menses_flows = []
        for e in entries:
            if e.flow and e.flow > 0:
                menses_flows.append(e.flow)
            else:
                break
        length_of_menses = len(menses_flows)
        total_menses_score = sum(menses_flows)
        mean_bleeding_intensity = (
            total_menses_score / length_of_menses
            if length_of_menses else 0.0
        )

        # 4) determine cycle length fallback if missing
        default_cycle = 28
        cycle_length = last_start.MeanCycleLength if last_start.MeanCycleLength else default_cycle

        # 5) assemble features dict in exact model order
        luteal_phase_length = 14  # fixed or tracked value
        feature_dict = {
            'LengthofCycle':          cycle_length,
            'MeanCycleLength':        cycle_length,
            'EstimatedDayofOvulation': cycle_length - luteal_phase_length,
            'LengthofLutealPhase':    luteal_phase_length,
            'LengthofMenses':         length_of_menses,
            'TotalMensesScore':       total_menses_score,
            'MeanBleedingIntensity':  mean_bleeding_intensity,
            'BMI':                    last_start.BMI or 0.0,
        }

        # 6) force DataFrame columns in the exact order
        columns_order = [
            'LengthofCycle',
            'MeanCycleLength',
            'EstimatedDayofOvulation',
            'LengthofLutealPhase',
            'LengthofMenses',
            'TotalMensesScore',
            'MeanBleedingIntensity',
            'BMI'
        ]
        X = pd.DataFrame([feature_dict], columns=columns_order)

        # 7) predict
        try:
            pred_len = int(period_model.predict(X)[0])
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 8) compute additional outputs
        # days since period start (1-based)
        day_of_period = (today - last_start.date).days + 1
        next_date = last_start.date + datetime.timedelta(days=pred_len)
        next_in = (next_date - today).days
        cycle_type = (
            "Regular"
            if abs(pred_len - cycle_length) <= 2
            else "Irregular"
        )
        latest = CycleEntry.objects.filter(user=request.user).order_by('-date').first()
        latest_mood = latest.mood if latest else ""
        latest_symptoms = latest.symptoms if latest else []

        return Response({
            "day_of_period":              day_of_period,
            "cycle_type":                 cycle_type,
            "next_period_in_days":        next_in,
            "predicted_cycle_length":     pred_len,
            "predicted_next_period_date": next_date.strftime('%Y-%m-%d'),
            "latest_mood":                latest_mood,
            "latest_symptoms":            latest_symptoms
        })

    
# femhealth/backend/views.py
import os, pickle

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
# ... other imports ...

from .pcosdetector_model_wrapper import PCOSDetector
from .models     import PCOSDetectionLog
from .serializers import PCOSDetectionSerializer

# Build the correct path
DETECTOR_PATH = os.path.join(
    settings.BASE_DIR,
    'femhealth', 'Models', 'pcos_detector.onnx'
)

# Instantiate once at import-time
detector = PCOSDetector(str(DETECTOR_PATH))

class PCOSDetectView(APIView):
    parser_classes     = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Return the latest PCOS detection result for this user.
        """
        try:
            latest = PCOSDetectionLog.objects.filter(user=request.user) \
                                             .latest('created_at')
        except PCOSDetectionLog.DoesNotExist:
            return Response(
                {"detail": "No detection results found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PCOSDetectionSerializer(latest)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        img_file = request.FILES.get('image')
        if not img_file:
            return Response({"detail":"Provide an 'image' file."}, status=400)

        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp:
            for chunk in img_file.chunks():
                tmp.write(chunk)
            tmp.flush()

            result = detector.predict(detector.preprocess_image(tmp.name))

        # Save to DB
        log = PCOSDetectionLog.objects.create(
            user   = request.user,
            image  = img_file,
            score  = result['score'],
            label  = result['label']
        )
        return Response(PCOSDetectionSerializer(log).data, status=201)