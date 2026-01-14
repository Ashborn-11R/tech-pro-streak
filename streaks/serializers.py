from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, DailyMission, StreakHistory, MissionTemplate, MotivationalQuote


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'timezone']
        extra_kwargs = {
            'email': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            timezone=validated_data.get('timezone', 'UTC')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'timezone',
            'current_streak', 'longest_streak', 'total_days_completed',
            'last_completion_date', 'level'
        ]
        read_only_fields = [
            'current_streak', 'longest_streak', 'total_days_completed',
            'last_completion_date', 'level'
        ]


class MissionTemplateSerializer(serializers.ModelSerializer):
    """Serializer for mission templates"""
    class Meta:
        model = MissionTemplate
        fields = ['id', 'mission_number', 'title', 'description']


class DailyMissionSerializer(serializers.ModelSerializer):
    """Serializer for daily missions"""
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = DailyMission
        fields = [
            'id', 'user', 'mission_date',
            'mission_1_completed', 'mission_1_notes', 'mission_1_completed_at',
            'mission_2_completed', 'mission_2_notes', 'mission_2_completed_at',
            'mission_3_completed', 'mission_3_notes', 'mission_3_completed_at',
            'all_completed', 'completed_at'
        ]
        read_only_fields = [
            'user', 'all_completed', 'completed_at',
            'mission_1_completed_at', 'mission_2_completed_at', 'mission_3_completed_at'
        ]


class StreakHistorySerializer(serializers.ModelSerializer):
    """Serializer for streak history"""
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = StreakHistory
        fields = ['id', 'user', 'streak_count', 'started_at', 'ended_at', 'is_active']


class MotivationalQuoteSerializer(serializers.ModelSerializer):
    """Serializer for motivational quotes"""
    class Meta:
        model = MotivationalQuote
        fields = ['id', 'quote', 'author']