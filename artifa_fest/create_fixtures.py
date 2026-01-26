import json
from datetime import date, time

# Events data
events = [
    {
        "model": "core.event",
        "pk": 1,
        "fields": {
            "name": "Suzie's Never Ending Story",
            "slug": "suzies-never-ending-story",
            "description": "Build something extraordinary in a marathon coding session. Like Suzie and Dustin, your code should tell a never-ending story of innovation.",
            "event_type": "technical",
            "is_team_event": True,
            "min_team_size": 1,
            "max_team_size": 3,
            "icon_class": "fas fa-laptop-code"
        }
    },
    {
        "model": "core.event",
        "pk": 2,
        "fields": {
            "name": "No.8's Vision Forge",
            "slug": "no8s-vision-forge",
            "description": "Channel your inner Eleven and forge visions with AI. Master the art of prompt engineering in this battle of creativity.",
            "event_type": "technical",
            "is_team_event": False,
            "min_team_size": 1,
            "max_team_size": 1,
            "icon_class": "fas fa-robot"
        }
    },
    {
        "model": "core.event",
        "pk": 3,
        "fields": {
            "name": "Code from the Upside Down",
            "slug": "code-from-the-upside-down",
            "description": "Navigate through algorithmic puzzles that would make even the Demogorgon confused. Think fast, code faster.",
            "event_type": "technical",
            "is_team_event": False,
            "min_team_size": 1,
            "max_team_size": 1,
            "icon_class": "fas fa-code"
        }
    },
    {
        "model": "core.event",
        "pk": 4,
        "fields": {
            "name": "Hawkins Data Files",
            "slug": "hawkins-data-files",
            "description": "Uncover patterns hidden in data like investigating Hawkins Lab files. Turn raw data into compelling insights.",
            "event_type": "technical",
            "is_team_event": False,
            "min_team_size": 1,
            "max_team_size": 1,
            "icon_class": "fas fa-chart-bar"
        }
    },
    {
        "model": "core.event",
        "pk": 5,
        "fields": {
            "name": "Dungeons & Dragons",
            "slug": "dungeons-dragons",
            "description": "Roll the dice and embark on an adventure. Just like the Hellfire Club, strategy and teamwork are your weapons.",
            "event_type": "non-technical",
            "is_team_event": True,
            "min_team_size": 2,
            "max_team_size": 2,
            "icon_class": "fas fa-dice-d20"
        }
    },
    {
        "model": "core.event",
        "pk": 6,
        "fields": {
            "name": "Make Your Hellfire Club",
            "slug": "make-your-hellfire-club",
            "description": "Build your dream team in this thrilling auction. Manage your budget and draft the ultimate squad.",
            "event_type": "non-technical",
            "is_team_event": True,
            "min_team_size": 5,
            "max_team_size": 5,
            "icon_class": "fas fa-users"
        }
    },
    {
        "model": "core.event",
        "pk": 7,
        "fields": {
            "name": "Eleven's Reality Check",
            "slug": "elevens-reality-check",
            "description": "Can you distinguish AI-generated content from reality? Test your perception in this mind-bending challenge.",
            "event_type": "non-technical",
            "is_team_event": True,
            "min_team_size": 2,
            "max_team_size": 2,
            "icon_class": "fas fa-eye"
        }
    }
]

# Schedule data
schedule = [
    {
        "model": "core.schedule",
        "pk": 1,
        "fields": {
            "title": "Inaugural Ceremony",
            "description": "Opening the gates to the Upside Down",
            "start_time": "09:30:00",
            "end_time": "10:30:00",
            "date": "2026-02-07",
            "is_break": False,
            "order": 1
        }
    },
    {
        "model": "core.schedule",
        "pk": 2,
        "fields": {
            "title": "Break",
            "description": "Refuel for the journey ahead",
            "start_time": "10:30:00",
            "end_time": "10:45:00",
            "date": "2026-02-07",
            "is_break": True,
            "order": 2
        }
    },
    {
        "model": "core.schedule",
        "pk": 3,
        "fields": {
            "event": 1,
            "title": "Hackathon Begins",
            "description": "Suzie's Never Ending Story begins",
            "start_time": "10:30:00",
            "end_time": "16:00:00",
            "date": "2026-02-07",
            "is_break": False,
            "order": 3
        }
    },
    {
        "model": "core.schedule",
        "pk": 4,
        "fields": {
            "title": "Technical Events",
            "description": "AI Prompt War, Coding Challenge, Data Analysis",
            "start_time": "10:45:00",
            "end_time": "13:00:00",
            "date": "2026-02-07",
            "is_break": False,
            "order": 4
        }
    },
    {
        "model": "core.schedule",
        "pk": 5,
        "fields": {
            "title": "Lunch Break",
            "description": "Eggos and more",
            "start_time": "13:00:00",
            "end_time": "14:00:00",
            "date": "2026-02-07",
            "is_break": True,
            "order": 5
        }
    },
    {
        "model": "core.schedule",
        "pk": 6,
        "fields": {
            "title": "Non-Technical Events",
            "description": "D&D, IPL Auction, AI or Real?",
            "start_time": "14:00:00",
            "end_time": "16:30:00",
            "date": "2026-02-07",
            "is_break": False,
            "order": 6
        }
    },
    {
        "model": "core.schedule",
        "pk": 7,
        "fields": {
            "title": "Prize Distribution",
            "description": "Crowning the champions",
            "start_time": "16:30:00",
            "end_time": "17:15:00",
            "date": "2026-02-07",
            "is_break": False,
            "order": 7
        }
    }
]

# Save to fixtures
with open('events_fixture.json', 'w') as f:
    json.dump(events, f, indent=2)

with open('schedule_fixture.json', 'w') as f:
    json.dump(schedule, f, indent=2)

print("Fixtures created successfully!")