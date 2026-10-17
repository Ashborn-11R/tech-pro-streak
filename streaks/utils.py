from datetime import date, datetime, timedelta
import pytz
from django.utils import timezone


def get_user_local_date(user_timezone='UTC'):
    """
    Get current date in user's timezone
    """
    try:
        tz = pytz.timezone(user_timezone)
        return datetime.now(tz).date()
    except:
        # Fallback to UTC if timezone is invalid
        return datetime.now(pytz.UTC).date()


def get_user_local_datetime(user_timezone='UTC'):
    """
    Get current datetime in user's timezone
    """
    try:
        tz = pytz.timezone(user_timezone)
        return datetime.now(tz)
    except:
        return datetime.now(pytz.UTC)


def is_same_day(date1, date2):
    """Check if two dates are the same day"""
    if date1 is None or date2 is None:
        return False
    return date1 == date2


def is_yesterday(date_to_check, reference_date):
    """Check if date_to_check is exactly one day before reference_date"""
    if date_to_check is None or reference_date is None:
        return False
    return (reference_date - date_to_check).days == 1


def days_between(date1, date2):
    """Calculate days between two dates"""
    if date1 is None or date2 is None:
        return None
    return abs((date2 - date1).days)


def should_reset_streak(user):
    """
    Determine if user's streak should be reset
    
    Returns:
        (should_reset: bool, reason: str, days_missed: int)
    """
    if not user.last_completion_date:
        # User has never completed a day
        return False, "new_user", 0
    
    user_today = get_user_local_date(user.timezone)
    last_completion = user.last_completion_date
    
    # Case 1: Completed today already
    if is_same_day(last_completion, user_today):
        return False, "completed_today", 0
    
    # Case 2: Completed yesterday (streak continues)
    if is_yesterday(last_completion, user_today):
        return False, "streak_active", 0
    
    # Case 3: Missed 1+ days (RESET!)
    days_missed = days_between(last_completion, user_today) - 1
    return True, "missed_days", days_missed


def get_time_until_midnight(user_timezone='UTC'):
    """
    Calculate time remaining until midnight in user's timezone
    Returns: dict with hours, minutes, seconds
    """
    user_now = get_user_local_datetime(user_timezone)
    midnight = user_now.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    time_left = midnight - user_now
    
    hours = time_left.seconds // 3600
    minutes = (time_left.seconds % 3600) // 60
    seconds = time_left.seconds % 60
    
    return {
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'total_seconds': time_left.seconds,
        'formatted': f"{hours}h {minutes}m"
    }


def calculate_streak_stats(user):
    """
    Calculate all streak-related statistics
    """
    user_today = get_user_local_date(user.timezone)
    should_reset, reason, days_missed = should_reset_streak(user)
    
    return {
        'current_streak': user.current_streak,
        'longest_streak': user.longest_streak,
        'total_days_completed': user.total_days_completed,
        'level': user.level,
        'last_completion_date': user.last_completion_date,
        'should_reset': should_reset,
        'reset_reason': reason,
        'days_missed': days_missed,
        'user_today': user_today,
        'time_until_midnight': get_time_until_midnight(user.timezone)
    }


def get_level_info(current_streak):
    """
    Get level information based on streak
    """
    levels = [
        {'name': 'Beginner', 'min': 1, 'max': 7, 'icon': '🌱'},
        {'name': 'Builder', 'min': 8, 'max': 14, 'icon': '🔨'},
        {'name': 'Pro', 'min': 15, 'max': 21, 'icon': '⚡'},
        {'name': 'Elite', 'min': 22, 'max': 30, 'icon': '🔥'},
    ]
    
    current_level = None
    next_level = None
    progress = 0
    
    for i, level in enumerate(levels):
        if level['min'] <= current_streak <= level['max']:
            current_level = level
            if i + 1 < len(levels):
                next_level = levels[i + 1]
                # Calculate progress to next level
                range_size = current_level['max'] - current_level['min'] + 1
                progress_in_range = current_streak - current_level['min'] + 1
                progress = int((progress_in_range / range_size) * 100)
            else:
                # Max level reached
                progress = 100
            break
    
    if current_streak == 0:
        current_level = {'name': 'Beginner', 'min': 1, 'max': 7, 'icon': '🌱'}
        next_level = {'name': 'Builder', 'min': 8, 'max': 14, 'icon': '🔨'}
        progress = 0
    
    return {
        'current_level': current_level,
        'next_level': next_level,
        'progress_percentage': progress,
        'days_to_next_level': next_level['min'] - current_streak if next_level else 0
    }
def apply_streak_reset(user):
    """Reset the streak if days were missed. Returns (was_reset, days_missed)."""
    needs_reset, reason, days_missed = should_reset_streak(user)
    if needs_reset and user.current_streak > 0:
        user.reset_streak()
        return True, days_missed
    return False, 0