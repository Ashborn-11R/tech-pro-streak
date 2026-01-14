from .utils import should_reset_streak


class StreakCheckMiddleware:
    """
    Middleware that checks if user's streak needs to be reset on every request
    This ensures streaks are checked whenever user visits the app
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check streak before processing request
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
            
            # Check if streak should be reset
            needs_reset, reason, days_missed = should_reset_streak(user)
            
            if needs_reset and user.current_streak > 0:
                # Reset the streak
                user.reset_streak()
                
                # Add info to request so views can notify user
                request.streak_reset = True
                request.days_missed = days_missed
            else:
                request.streak_reset = False
        
        response = self.get_response(request)
        return response