from django.core.management.base import BaseCommand
from datetime import datetime, time
from core.models import Schedule, Event


class Command(BaseCommand):
    help = 'Load sample schedule data for the festival'

    def handle(self, *args, **options):
        # Clear existing schedules
        Schedule.objects.all().delete()

        # Festival date (February 7, 2026)
        festival_date = datetime(2026, 2, 7).date()

        # Create schedule items
        schedule_data = [
            # Morning Session
            {
                'title': 'Inaugural Ceremony',
                'description': 'Opening ceremony with chief guest address and welcome speech',
                'start_time': time(9, 0),
                'end_time': time(10, 0),
                'date': festival_date,
                'is_break': False,
                'event': None,
                'order': 1,
            },
            {
                'title': 'Event Registrations & Brief',
                'description': 'Last minute registrations and event briefing for all participants',
                'start_time': time(10, 0),
                'end_time': time(10, 30),
                'date': festival_date,
                'is_break': False,
                'event': None,
                'order': 2,
            },
            {
                'title': 'Technical Events Round 1',
                'description': 'First round of coding and technical challenges',
                'start_time': time(10, 30),
                'end_time': time(12, 30),
                'date': festival_date,
                'is_break': False,
                'event': 'code-from-upside-down',
                'order': 3,
            },
            {
                'title': 'Lunch Break',
                'description': 'Enjoy refreshments and networking with fellow participants',
                'start_time': time(12, 30),
                'end_time': time(13, 30),
                'date': festival_date,
                'is_break': True,
                'event': None,
                'order': 4,
            },
            # Afternoon Session
            {
                'title': 'Non-Technical Events',
                'description': 'Games, quizzes, and creative activities for all participants',
                'start_time': time(13, 30),
                'end_time': time(15, 30),
                'date': festival_date,
                'is_break': False,
                'event': None,
                'order': 5,
            },
            {
                'title': 'Team Challenges & Dungeons & Dragons',
                'description': 'Interactive team-based games and adventure activities',
                'start_time': time(15, 30),
                'end_time': time(17, 0),
                'date': festival_date,
                'is_break': False,
                'event': 'dungeons-and-dragons',
                'order': 6,
            },
            {
                'title': 'Evening Break & Snacks',
                'description': 'Evening refreshments and informal networking',
                'start_time': time(17, 0),
                'end_time': time(17, 30),
                'date': festival_date,
                'is_break': True,
                'event': None,
                'order': 7,
            },
            # Evening Session
            {
                'title': 'Finals & Results Announcement',
                'description': 'Final rounds and announcement of winners',
                'start_time': time(17, 30),
                'end_time': time(19, 0),
                'date': festival_date,
                'is_break': False,
                'event': None,
                'order': 8,
            },
            {
                'title': 'Awards & Prize Distribution',
                'description': 'Honoring winners and presenting prizes and certificates',
                'start_time': time(19, 0),
                'end_time': time(20, 0),
                'date': festival_date,
                'is_break': False,
                'event': None,
                'order': 9,
            },
            {
                'title': 'Closing Ceremony & Dinner',
                'description': 'Closing remarks, cultural performances, and dinner reception',
                'start_time': time(20, 0),
                'end_time': time(22, 0),
                'date': festival_date,
                'is_break': False,
                'event': None,
                'order': 10,
            },
        ]

        # Create Schedule objects
        for item in schedule_data:
            event = None
            if item['event']:
                try:
                    event = Event.objects.get(slug=item['event'])
                except Event.DoesNotExist:
                    event = None

            Schedule.objects.create(
                title=item['title'],
                description=item['description'],
                start_time=item['start_time'],
                end_time=item['end_time'],
                date=item['date'],
                is_break=item['is_break'],
                event=event,
                order=item['order'],
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded 10 schedule items for the festival')
        )
