from django.core.management.base import BaseCommand
from streaks.models import MissionTemplate, MotivationalQuote


class Command(BaseCommand):
    help = 'Seeds database with mission templates and quotes'

    def handle(self, *args, **kwargs):
        # Clear existing data
        MissionTemplate.objects.all().delete()
        MotivationalQuote.objects.all().delete()
        
        # Mission Templates
        missions = [
            {
                'mission_number': 1,
                'title': 'Communicate & Learn',
                'description': 'Explain a tech concept to someone (or write it down) + Learn for 10 minutes'
            },
            {
                'mission_number': 2,
                'title': 'Build & Think',
                'description': 'Work on a real project for 30+ minutes + Write a dev log about what you learned'
            },
            {
                'mission_number': 3,
                'title': 'Reflect & Connect',
                'description': 'Journal about your emotions/progress + Reach out to someone (mentor, peer, or community)'
            }
        ]
        
        for mission in missions:
            MissionTemplate.objects.create(**mission)
        
        # Motivational Quotes
        quotes = [
            {'quote': 'The only way to do great work is to love what you do.', 'author': 'Steve Jobs'},
            {'quote': 'Code is like humor. When you have to explain it, it\'s bad.', 'author': 'Cory House'},
            {'quote': 'First, solve the problem. Then, write the code.', 'author': 'John Johnson'},
            {'quote': 'Consistency beats intensity every single time.', 'author': 'Anonymous'},
            {'quote': 'A journey of a thousand miles begins with a single step.', 'author': 'Lao Tzu'},
            {'quote': 'The best way to predict the future is to implement it.', 'author': 'David Heinemeier Hansson'},
            {'quote': 'Every expert was once a beginner. Every master started with baby steps.', 'author': 'Robin Sharma'},
            {'quote': 'Discipline is choosing between what you want now and what you want most.', 'author': 'Abraham Lincoln'},
        ]
        
        for quote in quotes:
            MotivationalQuote.objects.create(**quote)
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
        self.stdout.write(f'Created {len(missions)} mission templates')
        self.stdout.write(f'Created {len(quotes)} motivational quotes')