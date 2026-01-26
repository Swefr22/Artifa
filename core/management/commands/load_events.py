"""
Management command to load sample events data
"""
from django.core.management.base import BaseCommand
from core.models import Event
from datetime import datetime

class Command(BaseCommand):
    help = 'Load sample competition events into the database'

    def handle(self, *args, **options):
        # Sample events data
        events_data = [
            {
                "name": "Suzie's Never Ending Story",
                "slug": "suzies-never-ending-story",
                "description": "Build something extraordinary in a marathon coding session. Like Suzie and Dustin, your code should tell a never-ending story of innovation.",
                "event_type": "technical",
                "is_team_event": True,
                "min_team_size": 1,
                "max_team_size": 3,
                "icon_class": "fas fa-laptop-code"
            },
            {
                "name": "No.8's Vision Forge",
                "slug": "no8s-vision-forge",
                "description": "Channel your inner Eleven and forge visions with AI. Master the art of prompt engineering in this battle of creativity.",
                "event_type": "technical",
                "is_team_event": False,
                "min_team_size": 1,
                "max_team_size": 1,
                "icon_class": "fas fa-robot"
            },
            {
                "name": "Code from the Upside Down",
                "slug": "code-from-the-upside-down",
                "description": "Navigate through algorithmic puzzles that would make even the Demogorgon confused. Think fast, code faster.",
                "event_type": "technical",
                "is_team_event": False,
                "min_team_size": 1,
                "max_team_size": 1,
                "icon_class": "fas fa-code"
            },
            {
                "name": "Hawkins Data Files",
                "slug": "hawkins-data-files",
                "description": "Uncover patterns hidden in data like investigating Hawkins Lab files. Turn raw data into compelling insights.",
                "event_type": "technical",
                "is_team_event": False,
                "min_team_size": 1,
                "max_team_size": 1,
                "icon_class": "fas fa-chart-bar"
            },
            {
                "name": "Dungeons & Dragons",
                "slug": "dungeons-dragons",
                "description": "Roll the dice and embark on an adventure. Just like the Hellfire Club, strategy and teamwork are your weapons.",
                "event_type": "non-technical",
                "is_team_event": True,
                "min_team_size": 2,
                "max_team_size": 2,
                "icon_class": "fas fa-dice-d20"
            },
            {
                "name": "Make Your Hellfire Club",
                "slug": "make-your-hellfire-club",
                "description": "Build your dream team in this thrilling auction. Manage your budget and draft the ultimate squad.",
                "event_type": "non-technical",
                "is_team_event": True,
                "min_team_size": 5,
                "max_team_size": 5,
                "icon_class": "fas fa-users"
            },
            {
                "name": "Eleven's Reality Check",
                "slug": "elevens-reality-check",
                "description": "Can you distinguish AI-generated content from reality? Test your perception in this mind-bending challenge.",
                "event_type": "non-technical",
                "is_team_event": True,
                "min_team_size": 2,
                "max_team_size": 2,
                "icon_class": "fas fa-eye"
            }
        ]

        created_count = 0
        for event_data in events_data:
            # Check if event already exists
            if not Event.objects.filter(slug=event_data['slug']).exists():
                Event.objects.create(**event_data)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {event_data["name"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Already exists: {event_data["name"]}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully created {created_count} events!')
        )
