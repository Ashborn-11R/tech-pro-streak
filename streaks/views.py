from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import date

from .models import User, DailyMission, StreakHistory, MissionTemplate, MotivationalQuote
from .serializers import (
    UserRegistrationSerializer, UserSerializer, DailyMissionSerializer,
    StreakHistorySerializer, MissionTemplateSerializer, MotivationalQuoteSerializer
)
from .utils import (
    should_reset_streak, calculate_streak_stats, get_level_info,
    get_user_local_date, get_time_until_midnight
)


# ============= AUTHENTICATION VIEWS =============

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user and return JWT tokens"""
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """Get current authenticated user's profile"""
    user = request.user
    
    # Check if streak was reset by middleware
    streak_reset = getattr(request, 'streak_reset', False)
    
    return Response({
        'user': UserSerializer(user).data,
        'streak_reset': streak_reset,
        'days_missed': getattr(request, 'days_missed', 0)
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Update user profile (timezone, etc.)"""
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============= MISSION VIEWS =============

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_todays_missions(request):
    """Get or create today's missions for the user"""
    user = request.user
    user_today = get_user_local_date(user.timezone)
    
    # Get or create today's mission
    mission, created = DailyMission.objects.get_or_create(
        user=user,
        mission_date=user_today
    )
    
    # Get mission templates
    templates = MissionTemplate.objects.filter(active=True).order_by('mission_number')
    
    # Check if streak was reset
    streak_reset = getattr(request, 'streak_reset', False)
    
    return Response({
        'mission': DailyMissionSerializer(mission).data,
        'templates': MissionTemplateSerializer(templates, many=True).data,
        'is_new': created,
        'streak_reset': streak_reset,
        'time_until_midnight': get_time_until_midnight(user.timezone)
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_mission(request):
    """Mark a mission as complete"""
    user = request.user
    mission_number = request.data.get('mission_number')
    notes = request.data.get('notes', '')
    
    if mission_number not in [1, 2, 3]:
        return Response(
            {'error': 'Invalid mission number. Must be 1, 2, or 3.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get today's mission (in user's timezone)
    user_today = get_user_local_date(user.timezone)
    mission, created = DailyMission.objects.get_or_create(
        user=user,
        mission_date=user_today
    )
    
    # Complete the mission
    streak_increased = mission.complete_mission(mission_number, notes)
    
    # Refresh user data
    user.refresh_from_db()
    
    # Get level info
    level_info = get_level_info(user.current_streak)
    
    return Response({
        'mission': DailyMissionSerializer(mission).data,
        'user': UserSerializer(user).data,
        'streak_increased': streak_increased,
        'level_info': level_info,
        'message': f'Mission {mission_number} completed!' + 
                   (f' 🔥 Streak: {user.current_streak}!' if streak_increased else '')
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mission_history(request):
    """Get user's mission history (paginated)"""
    user = request.user
    missions = DailyMission.objects.filter(user=user).order_by('-mission_date')
    
    # Simple pagination
    limit = int(request.query_params.get('limit', 30))
    missions = missions[:limit]
    
    serializer = DailyMissionSerializer(missions, many=True)
    return Response(serializer.data)


# ============= STREAK VIEWS =============

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_streak_status(request):
    """Get user's current streak status with detailed info"""
    user = request.user
    
    # Get comprehensive streak stats
    stats = calculate_streak_stats(user)
    level_info = get_level_info(user.current_streak)
    
    return Response({
        **stats,
        'level_info': level_info
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_streak_history(request):
    """Get all past streaks"""
    user = request.user
    streaks = StreakHistory.objects.filter(user=user)
    serializer = StreakHistorySerializer(streaks, many=True)
    return Response(serializer.data)


# ============= DASHBOARD VIEW =============

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard(request):
    """Get all dashboard data in one request"""
    user = request.user
    user_today = get_user_local_date(user.timezone)
    
    # Get or create today's mission
    mission, created = DailyMission.objects.get_or_create(
        user=user,
        mission_date=user_today
    )
    
    # Get mission templates
    templates = MissionTemplate.objects.filter(active=True).order_by('mission_number')
    
    # Get random motivational quote
    quote = MotivationalQuote.get_random_quote()
    
    # Get streak stats
    streak_stats = calculate_streak_stats(user)
    level_info = get_level_info(user.current_streak)
    
    # Check if streak was reset
    streak_reset = getattr(request, 'streak_reset', False)
    
    return Response({
        'user': UserSerializer(user).data,
        'mission': DailyMissionSerializer(mission).data,
        'templates': MissionTemplateSerializer(templates, many=True).data,
        'quote': MotivationalQuoteSerializer(quote).data if quote else None,
        'streak_stats': streak_stats,
        'level_info': level_info,
        'streak_reset': streak_reset,
        'time_until_midnight': get_time_until_midnight(user.timezone)
    })