from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DailyMission, StreakHistory, MissionTemplate, MotivationalQuote


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom user admin with streak fields"""
    list_display = ['username', 'email', 'current_streak', 'longest_streak', 'level', 'is_staff']
    list_filter = ['level', 'is_staff', 'is_active']
    
    # Add streak fields to the admin form
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Streak Info', {
            'fields': ('timezone', 'current_streak', 'longest_streak', 
                      'total_days_completed', 'last_completion_date', 'level')
        }),
    )
    
    readonly_fields = ['current_streak', 'longest_streak', 'total_days_completed', 
                      'last_completion_date', 'level']


@admin.register(DailyMission)
class DailyMissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'mission_date', 'mission_1_completed', 
                   'mission_2_completed', 'mission_3_completed', 'all_completed']
    list_filter = ['mission_date', 'all_completed']
    search_fields = ['user__username']
    date_hierarchy = 'mission_date'
    
    readonly_fields = ['completed_at', 'mission_1_completed_at', 
                      'mission_2_completed_at', 'mission_3_completed_at']


@admin.register(StreakHistory)
class StreakHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'streak_count', 'started_at', 'ended_at', 'is_active']
    list_filter = ['is_active', 'started_at']
    search_fields = ['user__username']
    date_hierarchy = 'started_at'


@admin.register(MissionTemplate)
class MissionTemplateAdmin(admin.ModelAdmin):
    list_display = ['mission_number', 'title', 'active', 'created_at']
    list_filter = ['mission_number', 'active']
    search_fields = ['title', 'description']


@admin.register(MotivationalQuote)
class MotivationalQuoteAdmin(admin.ModelAdmin):
    list_display = ['quote_preview', 'author', 'active', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['quote', 'author']
    
    def quote_preview(self, obj):
        return obj.quote[:50] + "..." if len(obj.quote) > 50 else obj.quote
    quote_preview.short_description = 'Quote'