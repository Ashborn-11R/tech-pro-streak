from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import DailyMission, StreakHistory, MissionTemplate, MotivationalQuote
from .serializers import (
    UserRegistrationSerializer, UserSerializer, DailyMissionSerializer,
    StreakHistorySerializer, MissionTemplateSerializer, MotivationalQuoteSerializer,AdminMissionTemplateSerializer, AdminQuoteSerializer
)
from .utils import (
    apply_streak_reset, calculate_streak_stats, get_level_info,
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
    streak_reset, days_missed = apply_streak_reset(user)

    return Response({
        'user': UserSerializer(user).data,
        'streak_reset': streak_reset,
        'days_missed': days_missed
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
    streak_reset, days_missed = apply_streak_reset(user)
    user_today = get_user_local_date(user.timezone)

    mission, created = DailyMission.objects.get_or_create(
        user=user,
        mission_date=user_today
    )

    templates = MissionTemplate.objects.filter(active=True).order_by('mission_number')

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
    streak_reset, days_missed = apply_streak_reset(user)
    mission_number = request.data.get('mission_number')
    notes = request.data.get('notes', '')

    if mission_number not in [1, 2, 3]:
        return Response(
            {'error': 'Invalid mission number. Must be 1, 2, or 3.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user_today = get_user_local_date(user.timezone)
    mission, created = DailyMission.objects.get_or_create(
        user=user,
        mission_date=user_today
    )

    streak_increased = mission.complete_mission(mission_number, notes)

    user.refresh_from_db()
    level_info = get_level_info(user.current_streak)

    return Response({
        'mission': DailyMissionSerializer(mission).data,
        'user': UserSerializer(user).data,
        'streak_increased': streak_increased,
        'streak_reset': streak_reset,
        'level_info': level_info,
        'message': f'Mission {mission_number} completed!' +
                   (f' 🔥 Streak: {user.current_streak}!' if streak_increased else '')
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def undo_mission(request):
    """Untick a mission for today (rolls the streak back if the day was complete)"""
    user = request.user
    mission_number = request.data.get('mission_number')

    if mission_number not in [1, 2, 3]:
        return Response(
            {'error': 'Invalid mission number. Must be 1, 2, or 3.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user_today = get_user_local_date(user.timezone)
    try:
        mission = DailyMission.objects.get(user=user, mission_date=user_today)
    except DailyMission.DoesNotExist:
        return Response({'error': 'No missions for today.'}, status=status.HTTP_404_NOT_FOUND)

    streak_rolled_back = mission.undo_mission(mission_number)

    user.refresh_from_db()

    return Response({
        'mission': DailyMissionSerializer(mission).data,
        'user': UserSerializer(user).data,
        'streak_rolled_back': streak_rolled_back,
        'level_info': get_level_info(user.current_streak),
        'message': f'Mission {mission_number} unticked.'
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mission_history(request):
    """Get user's mission history"""
    user = request.user
    missions = DailyMission.objects.filter(user=user).order_by('-mission_date')

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
    streak_reset, days_missed = apply_streak_reset(user)

    stats = calculate_streak_stats(user)
    level_info = get_level_info(user.current_streak)

    return Response({
        **stats,
        'streak_reset': streak_reset,
        'level_info': level_info
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_streak_history(request):
    """Get all past streaks"""
    streaks = StreakHistory.objects.filter(user=request.user)
    serializer = StreakHistorySerializer(streaks, many=True)
    return Response(serializer.data)


# ============= DASHBOARD VIEW =============

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard(request):
    """Get all dashboard data in one request"""
    user = request.user
    streak_reset, days_missed = apply_streak_reset(user)
    user_today = get_user_local_date(user.timezone)

    mission, created = DailyMission.objects.get_or_create(
        user=user,
        mission_date=user_today
    )

    templates = MissionTemplate.objects.filter(active=True).order_by('mission_number')
    quote = MotivationalQuote.get_random_quote()

    streak_stats = calculate_streak_stats(user)
    level_info = get_level_info(user.current_streak)

    return Response({
        'user': UserSerializer(user).data,
        'mission': DailyMissionSerializer(mission).data,
        'templates': MissionTemplateSerializer(templates, many=True).data,
        'quote': MotivationalQuoteSerializer(quote).data if quote else None,
        'streak_stats': streak_stats,
        'level_info': level_info,
        'streak_reset': streak_reset,
        'days_missed': days_missed,
        'time_until_midnight': get_time_until_midnight(user.timezone)
    })

# ============= ADMIN (staff only) =============

class AdminMissionList(generics.ListAPIView):
    queryset = MissionTemplate.objects.all().order_by('mission_number', 'id')
    serializer_class = AdminMissionTemplateSerializer
    permission_classes = [IsAdminUser]


class AdminMissionDetail(generics.RetrieveUpdateAPIView):
    queryset = MissionTemplate.objects.all()
    serializer_class = AdminMissionTemplateSerializer
    permission_classes = [IsAdminUser]


class AdminQuoteList(generics.ListCreateAPIView):
    queryset = MotivationalQuote.objects.all().order_by('-id')
    serializer_class = AdminQuoteSerializer
    permission_classes = [IsAdminUser]


class AdminQuoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MotivationalQuote.objects.all()
    serializer_class = AdminQuoteSerializer
    permission_classes = [IsAdminUser]