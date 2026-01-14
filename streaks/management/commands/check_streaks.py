from django.core.management.base import BaseCommand
from django.utils import timezone
from streaks.models import User, DailyMission
from streaks.utils import should_reset_streak, get_user_local_date
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Check all users streaks and reset if they missed yesterday'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be reset without actually resetting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        self.stdout.write(self.style.WARNING(
            f'Running streak check at {timezone.now()}'
        ))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        users = User.objects.filter(is_active=True)
        total_users = users.count()
        
        reset_count = 0
        maintained_count = 0
        new_users = 0
        
        for user in users:
            user_today = get_user_local_date(user.timezone)
            needs_reset, reason, days_missed = should_reset_streak(user)
            
            if reason == "new_user":
                new_users += 1
                self.stdout.write(f"  ⚪ {user.username}: New user (no streak yet)")
                continue
            
            if needs_reset:
                if user.current_streak > 0:
                    self.stdout.write(self.style.ERROR(
                        f"  ❌ {user.username}: Missed {days_missed} day(s) - "
                        f"Streak {user.current_streak} → 0"
                    ))
                    
                    if not dry_run:
                        user.reset_streak()
                    
                    reset_count += 1
                else:
                    self.stdout.write(f"  ⚪ {user.username}: No active streak")
            else:
                if user.current_streak > 0:
                    self.stdout.write(self.style.SUCCESS(
                        f"  ✅ {user.username}: Streak maintained - Day {user.current_streak} 🔥"
                    ))
                    maintained_count += 1
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('SUMMARY:'))
        self.stdout.write(f"  Total users checked: {total_users}")
        self.stdout.write(self.style.SUCCESS(f"  ✅ Streaks maintained: {maintained_count}"))
        self.stdout.write(self.style.ERROR(f"  ❌ Streaks reset: {reset_count}"))
        self.stdout.write(f"  ⚪ New users: {new_users}")
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\nDRY RUN - No actual changes made'))
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ Streak check complete!'))