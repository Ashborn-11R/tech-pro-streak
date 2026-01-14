from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date, timedelta


class User(AbstractUser):
    """
    Extended User model with streak tracking
    """
    # Timezone for accurate day calculations
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Streak stats
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    total_days_completed = models.IntegerField(default=0)
    
    # Track when user last completed all missions
    last_completion_date = models.DateField(null=True, blank=True)
    
    # Level system
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),    # Day 1-7
        ('Builder', 'Builder'),       # Day 8-14
        ('Pro', 'Pro'),               # Day 15-21
        ('Elite', 'Elite'),           # Day 22-30
    ]
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='Beginner')
    
    def __str__(self):
        return f"{self.username} - Day {self.current_streak}"
    
    def update_level(self):
        """Update user level based on current streak"""
        if self.current_streak >= 22:
            self.level = 'Elite'
        elif self.current_streak >= 15:
            self.level = 'Pro'
        elif self.current_streak >= 8:
            self.level = 'Builder'
        else:
            self.level = 'Beginner'
        self.save()
    
    def increment_streak(self):
        """Increment streak by 1 and update stats"""
        self.current_streak += 1
        self.total_days_completed += 1
        
        # Update longest streak if needed
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        
        self.last_completion_date = date.today()
        self.update_level()
        self.save()
    
    def reset_streak(self):
        """Reset streak to 0 (when user misses a day)"""
        # Save to history before resetting
        if self.current_streak > 0:
            StreakHistory.objects.create(
                user=self,
                streak_count=self.current_streak,
                started_at=date.today() - timedelta(days=self.current_streak),
                ended_at=date.today() - timedelta(days=1),
                is_active=False
            )
        
        self.current_streak = 0
        self.level = 'Beginner'
        self.save()


class MissionTemplate(models.Model):
    """
    Admin-customizable mission templates
    """
    mission_number = models.IntegerField(
        choices=[(1, 'Mission 1'), (2, 'Mission 2'), (3, 'Mission 3')]
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['mission_number']
    
    def __str__(self):
        return f"Mission {self.mission_number}: {self.title}"


class DailyMission(models.Model):
    """
    Tracks user's daily mission completion
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_missions')
    mission_date = models.DateField(default=date.today)
    
    # Mission 1: Communicate & Learn
    mission_1_completed = models.BooleanField(default=False)
    mission_1_notes = models.TextField(blank=True, null=True)
    mission_1_completed_at = models.DateTimeField(null=True, blank=True)
    
    # Mission 2: Build & Think
    mission_2_completed = models.BooleanField(default=False)
    mission_2_notes = models.TextField(blank=True, null=True)
    mission_2_completed_at = models.DateTimeField(null=True, blank=True)
    
    # Mission 3: Reflect & Connect
    mission_3_completed = models.BooleanField(default=False)
    mission_3_notes = models.TextField(blank=True, null=True)
    mission_3_completed_at = models.DateTimeField(null=True, blank=True)
    
    # Overall completion
    all_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'mission_date']
        ordering = ['-mission_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.mission_date} - {'✅' if self.all_completed else '⏳'}"
    
    def check_all_completed(self):
        """Check if all 3 missions are done"""
        if self.mission_1_completed and self.mission_2_completed and self.mission_3_completed:
            if not self.all_completed:  # Only increment streak once
                self.all_completed = True
                self.completed_at = timezone.now()
                self.save()
                
                # Increment user's streak
                self.user.increment_streak()
                return True
        return False
    
    def complete_mission(self, mission_number, notes=None):
        """Complete a specific mission"""
        if mission_number == 1:
            self.mission_1_completed = True
            self.mission_1_completed_at = timezone.now()
            if notes:
                self.mission_1_notes = notes
        elif mission_number == 2:
            self.mission_2_completed = True
            self.mission_2_completed_at = timezone.now()
            if notes:
                self.mission_2_notes = notes
        elif mission_number == 3:
            self.mission_3_completed = True
            self.mission_3_completed_at = timezone.now()
            if notes:
                self.mission_3_notes = notes
        
        self.save()
        return self.check_all_completed()


class StreakHistory(models.Model):
    """
    Records all past streaks (for history page)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='streak_history')
    streak_count = models.IntegerField()
    started_at = models.DateField()
    ended_at = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Streak histories'
    
    def __str__(self):
        status = "Active" if self.is_active else "Ended"
        return f"{self.user.username} - {self.streak_count} days ({status})"


class MotivationalQuote(models.Model):
    """
    Quotes shown on dashboard (admin customizable)
    """
    quote = models.TextField()
    author = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quote[:50]}... - {self.author}"
    
    @classmethod
    def get_random_quote(cls):
        """Get a random active quote"""
        return cls.objects.filter(active=True).order_by('?').first()