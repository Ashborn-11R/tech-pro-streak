from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', views.get_current_user, name='current_user'),
    path('auth/profile/', views.update_profile, name='update_profile'),
    
    # Missions
    path('missions/today/', views.get_todays_missions, name='todays_missions'),
    path('missions/complete/', views.complete_mission, name='complete_mission'),
    path('missions/history/', views.get_mission_history, name='mission_history'),
    path('missions/undo/', views.undo_mission, name='undo_mission'),

    # Streak
    path('streak/status/', views.get_streak_status, name='streak_status'),
    path('streak/history/', views.get_streak_history, name='streak_history'),
    
    # Dashboard
    path('dashboard/', views.get_dashboard, name='dashboard'),
]