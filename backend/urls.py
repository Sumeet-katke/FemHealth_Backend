# urls.py
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (RegisterUserAPIView,
                    LoginUserAPIView
                    )
from django.urls import path
from .views import  PredictPeriod, PCOSPredictView, CycleEntryListCreate, PCOSDetectView

urlpatterns = [
    # Your other paths...
    
    # JWT Token paths
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('predict-period/', PredictPeriod.as_view(), name='predict_period'),  # For prediction
    path('predict-pcos/', PCOSPredictView.as_view(), name='predict-pcos'),
    path('daily-entry/', CycleEntryListCreate.as_view(), name='daily_entry'),  # For daily entries
    path('pcos-detect/', PCOSDetectView.as_view(), name='pcos_detect'),  # For PCOS detection
]

# urls.py

