"""
Dataset Expansion Script - Timeline & Event Details
Adds comprehensive Q&A pairs about festival timeline and event names/details
Target: ~100 new pairs covering events and timeline information
"""

import os
import sys
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artifa_fest.settings')
sys.path.insert(0, r'c:\Users\Mano Sathiyamoorthi\Downloads\ARTIFA FEST')
django.setup()

from core.models import ChatbotTraining

# Timeline and Event Details Q&A pairs
timeline_event_data = [
    # Event Names and Basic Info
    {
        'question': "What are all the events at ARTIFA FEST?",
        'answer': '''<h3>ARTIFA FEST Events</h3>
<p><strong>Technical Events:</strong></p>
<ul>
<li><strong>Suzie's Never Ending Story</strong> - Hackathon (Team: 1-3 members)</li>
<li><strong>No.8's Vision Forge</strong> - AI & Prompt Engineering (Solo)</li>
<li><strong>Code from the Upside Down</strong> - Algorithmic Challenges (Solo)</li>
<li><strong>Hawkins Data Files</strong> - Data Science & Analytics (Solo)</li>
</ul>
<p><strong>Non-Technical Events:</strong></p>
<ul>
<li><strong>Dungeons & Dragons</strong> - Strategy Game (Team: 2 members)</li>
<li><strong>Make Your Hellfire Club</strong> - Auction Event (Team: 5 members)</li>
<li><strong>Eleven's Reality Check</strong> - AI Content Detection (Team: 2 members)</li>
</ul>''',
        'intent': 'event_info',
        'keywords': 'events, list, all, names, technical, non-technical'
    },
    
    # Individual Event Details
    {
        'question': "Tell me about Suzie's Never Ending Story event",
        'answer': '''<h3>Suzie's Never Ending Story - Hackathon</h3>
<p><strong>Type:</strong> Technical Event</p>
<p><strong>Format:</strong> Team Hackathon (1-3 members per team)</p>
<p><strong>Description:</strong> Build something extraordinary in a marathon coding session. Like Suzie and Dustin, your code should tell a never-ending story of innovation.</p>
<p><strong>Skills Required:</strong> Programming, Problem-solving, Innovation, Teamwork</p>
<p><strong>Duration:</strong> Approximately 5.5 hours</p>''',
        'intent': 'event_info',
        'keywords': 'suzie, never ending story, hackathon, coding, team event'
    },
    
    {
        'question': "What is No.8's Vision Forge event?",
        'answer': '''<h3>No.8's Vision Forge - AI Challenge</h3>
<p><strong>Type:</strong> Technical Event</p>
<p><strong>Format:</strong> Solo Challenge</p>
<p><strong>Description:</strong> Channel your inner Eleven and forge visions with AI. Master the art of prompt engineering in this battle of creativity.</p>
<p><strong>Key Skills:</strong> Prompt Engineering, Artificial Intelligence, Creativity, ChatGPT/LLM Usage</p>
<p><strong>Focus:</strong> Advanced AI prompt crafting and understanding language models</p>''',
        'intent': 'event_info',
        'keywords': 'no.8, vision forge, ai, prompt engineering, solo'
    },
    
    {
        'question': "Tell me about Code from the Upside Down",
        'answer': '''<h3>Code from the Upside Down - Algorithmic Challenge</h3>
<p><strong>Type:</strong> Technical Event</p>
<p><strong>Format:</strong> Solo Coding Challenge</p>
<p><strong>Description:</strong> Navigate through algorithmic puzzles that would make even the Demogorgon confused. Think fast, code faster.</p>
<p><strong>Requirements:</strong> Strong algorithmic thinking, Problem-solving, Quick coding</p>
<p><strong>Topics Covered:</strong> Data structures, Algorithms, Optimization, Edge cases</p>''',
        'intent': 'event_info',
        'keywords': 'code, upside down, algorithmic, puzzle, challenge'
    },
    
    {
        'question': "What is Hawkins Data Files event?",
        'answer': '''<h3>Hawkins Data Files - Data Science Challenge</h3>
<p><strong>Type:</strong> Technical Event</p>
<p><strong>Format:</strong> Solo Competition</p>
<p><strong>Description:</strong> Uncover patterns hidden in data like investigating Hawkins Lab files. Turn raw data into compelling insights.</p>
<p><strong>Skills Required:</strong> Data Analysis, Statistics, Machine Learning basics, Data Visualization, Python/SQL</p>
<p><strong>Objective:</strong> Extract meaningful insights from provided datasets and present findings</p>''',
        'intent': 'event_info',
        'keywords': 'hawkins, data files, data science, analysis, challenge'
    },
    
    {
        'question': "Tell me about Dungeons & Dragons event",
        'answer': '''<h3>Dungeons & Dragons - Strategy Game</h3>
<p><strong>Type:</strong> Non-Technical Event</p>
<p><strong>Format:</strong> Team Competition (2 members per team)</p>
<p><strong>Description:</strong> Roll the dice and embark on an adventure. Just like the Hellfire Club, strategy and teamwork are your weapons.</p>
<p><strong>Requirements:</strong> Strategic thinking, Teamwork, Quick decision-making, Adventure spirit</p>
<p><strong>What You Need:</strong> No prior D&D experience needed - open to beginners and veterans</p>''',
        'intent': 'event_info',
        'keywords': 'dungeons, dragons, d&d, strategy, game, team'
    },
    
    {
        'question': "What is Make Your Hellfire Club event?",
        'answer': '''<h3>Make Your Hellfire Club - Auction Event</h3>
<p><strong>Type:</strong> Non-Technical Event</p>
<p><strong>Format:</strong> Team Event (Exactly 5 members per team)</p>
<p><strong>Description:</strong> Build your dream team in this thrilling auction. Manage your budget and draft the ultimate squad.</p>
<p><strong>Skills Required:</strong> Budget management, Strategic planning, Negotiation, Teamwork</p>
<p><strong>Objective:</strong> Auction and team building with limited resources</p>
<p><strong>Team Size:</strong> Exactly 5 members required</p>''',
        'intent': 'event_info',
        'keywords': 'hellfire club, auction, team building, budget, five members'
    },
    
    {
        'question': "Tell me about Eleven's Reality Check event",
        'answer': '''<h3>Eleven's Reality Check - AI Content Detection</h3>
<p><strong>Type:</strong> Non-Technical Event</p>
<p><strong>Format:</strong> Team Challenge (2 members per team)</p>
<p><strong>Description:</strong> Can you distinguish AI-generated content from reality? Test your perception in this mind-bending challenge.</p>
<p><strong>Challenge:</strong> Identify whether content is AI-generated or human-created</p>
<p><strong>Topics:</strong> AI detection, Content analysis, Critical thinking</p>
<p><strong>Team Size:</strong> 2 members per team</p>''',
        'intent': 'event_info',
        'keywords': 'eleven, reality check, ai detection, perception, team'
    },
    
    # Timeline Information
    {
        'question': "When is ARTIFA FEST happening?",
        'answer': '''<h3>ARTIFA FEST 2026 Schedule</h3>
<p><strong>Festival Date:</strong> February 7, 2026</p>
<p><strong>Main Festival Day:</strong> Saturday, February 7, 2026</p>
<p><strong>Event Duration:</strong> Full day event from morning to evening</p>
<p><strong>Timeline Highlights:</strong></p>
<ul>
<li>8:00 AM - Portal Registration Opens</li>
<li>9:00 AM - Opening Ceremony</li>
<li>Throughout the day - Various events running in parallel</li>
<li>Evening - Awards Ceremony and Closing</li>
</ul>''',
        'intent': 'artifa_info',
        'keywords': 'date, when, festival, 2026, february, schedule'
    },
    
    {
        'question': "What time does ARTIFA FEST start?",
        'answer': '''<h3>ARTIFA FEST Start Time</h3>
<p><strong>Registration Opens:</strong> 8:00 AM</p>
<p><strong>Opening Ceremony:</strong> 9:00 AM - 9:30 AM</p>
<p><strong>Events Begin:</strong> 9:30 AM onwards</p>
<p><strong>Note:</strong> Arrive early to complete registration and get your goodie bags!</p>''',
        'intent': 'artifa_info',
        'keywords': 'start time, when, begin, morning, 8am, 9am'
    },
    
    {
        'question': "What is the complete festival timeline?",
        'answer': '''<h3>Complete ARTIFA FEST Timeline - February 7, 2026</h3>
<p><strong>8:00 AM - 8:45 AM:</strong> Portal Registration Opens</p>
<p><strong>9:00 AM - 9:30 AM:</strong> Opening Ceremony</p>
<p><strong>9:30 AM - 1:00 PM:</strong> Morning Events & Hackathon</p>
<p><strong>1:00 PM - 2:00 PM:</strong> Lunch Break</p>
<p><strong>2:00 PM - 5:00 PM:</strong> Afternoon Events Continue</p>
<p><strong>5:00 PM - 5:30 PM:</strong> Break</p>
<p><strong>5:30 PM - 6:30 PM:</strong> Final Events</p>
<p><strong>6:30 PM - 7:30 PM:</strong> Awards Ceremony</p>
<p><strong>7:30 PM:</strong> Closing & Celebration</p>''',
        'intent': 'artifa_info',
        'keywords': 'timeline, complete, schedule, hours, all events'
    },
    
    # Event Timing Details
    {
        'question': "What time does Suzie's Never Ending Story event run?",
        'answer': '''<h3>Suzie's Never Ending Story - Hackathon Schedule</h3>
<p><strong>Start Time:</strong> 9:30 AM</p>
<p><strong>End Time:</strong> 3:00 PM (1:00 PM registration closing)</p>
<p><strong>Duration:</strong> Approximately 5.5 hours</p>
<p><strong>Note:</strong> This is a continuous hackathon session. Plan your lunch break accordingly or arrange team food delivery.</p>''',
        'intent': 'event_info',
        'keywords': 'suzie, time, start, end, schedule, duration'
    },
    
    {
        'question': "When do the Solo technical events happen?",
        'answer': '''<h3>Solo Technical Events Schedule</h3>
<p><strong>No.8's Vision Forge:</strong> 2:00 PM - 4:00 PM</p>
<p><strong>Code from the Upside Down:</strong> 2:00 PM - 4:00 PM (parallel)</p>
<p><strong>Hawkins Data Files:</strong> 2:00 PM - 4:00 PM (parallel)</p>
<p><strong>Note:</strong> All solo events run in parallel. Choose only one to participate in.</p>''',
        'intent': 'event_info',
        'keywords': 'solo, technical, time, schedule, when'
    },
    
    {
        'question': "What time are non-technical events?",
        'answer': '''<h3>Non-Technical Events Schedule</h3>
<p><strong>Dungeons & Dragons:</strong> 2:00 PM - 4:30 PM</p>
<p><strong>Make Your Hellfire Club:</strong> 4:30 PM - 5:30 PM</p>
<p><strong>Eleven's Reality Check:</strong> 2:00 PM - 4:00 PM (parallel)</p>
<p><strong>Awards Ceremony:</strong> 6:30 PM - 7:30 PM</p>''',
        'intent': 'event_info',
        'keywords': 'non-technical, time, schedule, when, events'
    },
    
    # Event Categories/Types
    {
        'question': "How many technical events are there?",
        'answer': '''<h3>Technical Events Count</h3>
<p><strong>Total Technical Events:</strong> 4</p>
<p><strong>List of Technical Events:</strong></p>
<ul>
<li>1. Suzie's Never Ending Story (Hackathon)</li>
<li>2. No.8's Vision Forge (AI/Prompt Engineering)</li>
<li>3. Code from the Upside Down (Algorithms)</li>
<li>4. Hawkins Data Files (Data Science)</li>
</ul>''',
        'intent': 'event_info',
        'keywords': 'technical, events, count, how many'
    },
    
    {
        'question': "How many non-technical events are there?",
        'answer': '''<h3>Non-Technical Events Count</h3>
<p><strong>Total Non-Technical Events:</strong> 3</p>
<p><strong>List of Non-Technical Events:</strong></p>
<ul>
<li>1. Dungeons & Dragons (Strategy Game)</li>
<li>2. Make Your Hellfire Club (Auction/Team Building)</li>
<li>3. Eleven's Reality Check (AI Detection)</li>
</ul>''',
        'intent': 'event_info',
        'keywords': 'non-technical, events, count, how many'
    },
    
    # Team Size Information
    {
        'question': "Which events are team events?",
        'answer': '''<h3>Team Events at ARTIFA FEST</h3>
<p><strong>Team Events:</strong></p>
<ul>
<li><strong>Suzie's Never Ending Story</strong> - 1-3 members per team</li>
<li><strong>Dungeons & Dragons</strong> - 2 members per team</li>
<li><strong>Make Your Hellfire Club</strong> - Exactly 5 members per team</li>
<li><strong>Eleven's Reality Check</strong> - 2 members per team</li>
</ul>
<p><strong>Solo Events:</strong></p>
<ul>
<li>No.8's Vision Forge</li>
<li>Code from the Upside Down</li>
<li>Hawkins Data Files</li>
</ul>''',
        'intent': 'event_info',
        'keywords': 'team events, group, members, solo'
    },
    
    {
        'question': "Which events are solo challenges?",
        'answer': '''<h3>Solo Challenge Events</h3>
<p><strong>Solo Events (1 member each):</strong></p>
<ul>
<li><strong>No.8's Vision Forge</strong> - AI & Prompt Engineering</li>
<li><strong>Code from the Upside Down</strong> - Algorithmic Challenge</li>
<li><strong>Hawkins Data Files</strong> - Data Science Challenge</li>
</ul>
<p><strong>Advantages of Solo Events:</strong></p>
<ul>
<li>Showcase individual skills</li>
<li>No coordination needed</li>
<li>Direct competition</li>
<li>Individual recognition</li>
</ul>''',
        'intent': 'event_info',
        'keywords': 'solo, individual, one member, single'
    },
    
    # Event Complexity/Difficulty
    {
        'question': "What are the easiest events for beginners?",
        'answer': '''<h3>Beginner-Friendly Events</h3>
<p><strong>Non-Technical Events (Good for everyone):</strong></p>
<ul>
<li><strong>Dungeons & Dragons</strong> - Strategy game, no experience needed</li>
<li><strong>Eleven's Reality Check</strong> - No coding/technical background required</li>
<li><strong>Make Your Hellfire Club</strong> - Fun team auction, minimal prerequisites</li>
</ul>
<p><strong>Technical Events for Beginners:</strong></p>
<ul>
<li><strong>No.8's Vision Forge</strong> - AI prompt engineering (accessible with ChatGPT)</li>
</ul>
<p><strong>Tip:</strong> Start with events matching your comfort level and skill set!</p>''',
        'intent': 'event_info',
        'keywords': 'beginner, easy, easy, simple, no experience, new'
    },
    
    # Event Requirements/Difficulty
    {
        'question': "What events require programming skills?",
        'answer': '''<h3>Events Requiring Programming</h3>
<p><strong>Strong Programming Required:</strong></p>
<ul>
<li><strong>Suzie's Never Ending Story</strong> - Hackathon (Full coding marathon)</li>
<li><strong>Code from the Upside Down</strong> - Complex algorithmic puzzles</li>
</ul>
<p><strong>Programming Knowledge Helpful:</strong></p>
<ul>
<li><strong>Hawkins Data Files</strong> - Python/SQL for data analysis</li>
</ul>
<p><strong>No Programming Required:</strong></p>
<ul>
<li>Dungeons & Dragons</li>
<li>Make Your Hellfire Club</li>
<li>Eleven's Reality Check</li>
<li>No.8's Vision Forge (AI/LLM focused)</li>
</ul>''',
        'intent': 'event_info',
        'keywords': 'programming, coding, skills, required, technical'
    },
    
    # Parallel Events
    {
        'question': "Which events run at the same time?",
        'answer': '''<h3>Parallel Events Schedule</h3>
<p><strong>2:00 PM - 4:00 PM (Parallel Round):</strong></p>
<ul>
<li>No.8's Vision Forge (AI challenge)</li>
<li>Code from the Upside Down (Algorithm challenge)</li>
<li>Hawkins Data Files (Data Science)</li>
<li>Eleven's Reality Check (AI detection)</li>
</ul>
<p><strong>Note:</strong> You can only participate in ONE event during this slot. Choose wisely based on your strengths!</p>''',
        'intent': 'event_info',
        'keywords': 'parallel, same time, concurrent, simultaneous'
    },
    
    # Event Venue
    {
        'question': "Where do the events take place?",
        'answer': '''<h3>Event Venues</h3>
<p><strong>Main Venue:</strong> NEC Campus Main Grounds</p>
<p><strong>Event Locations:</strong></p>
<ul>
<li>Technical Events - Computer Lab & Tech Arena</li>
<li>Non-Technical Events - Main Hall & Auditorium</li>
<li>Opening/Closing Ceremony - Main Auditorium</li>
<li>Registration - Main Entrance</li>
<li>Food & Break Area - Cafeteria</li>
</ul>
<p><strong>Note:</strong> Check your event schedule for specific venue details!</p>''',
        'intent': 'venue',
        'keywords': 'venue, location, where, place, area, grounds'
    },
    
    # Duration Information
    {
        'question': "How long is each event?",
        'answer': '''<h3>Event Duration</h3>
<p><strong>Hackathon - Suzie's Never Ending Story:</strong> 5.5 hours (9:30 AM - 3:00 PM)</p>
<p><strong>Solo Technical Events (No.8, Code, Hawkins):</strong> 2 hours (2:00 PM - 4:00 PM)</p>
<p><strong>Dungeons & Dragons:</strong> 2.5 hours (2:00 PM - 4:30 PM)</p>
<p><strong>Make Your Hellfire Club:</strong> 1 hour (4:30 PM - 5:30 PM)</p>
<p><strong>Eleven's Reality Check:</strong> 2 hours (2:00 PM - 4:00 PM)</p>
<p><strong>Awards Ceremony:</strong> 1 hour (6:30 PM - 7:30 PM)</p>''',
        'intent': 'event_info',
        'keywords': 'duration, length, how long, time, hours'
    },
    
    # Break Times
    {
        'question': "When are break times during the festival?",
        'answer': '''<h3>Festival Break Times</h3>
<p><strong>Morning Break:</strong> 9:30 AM - 9:45 AM (Quick refresh)</p>
<p><strong>Lunch Break:</strong> 1:00 PM - 2:00 PM (Main lunch hour)</p>
<p><strong>Afternoon Break:</strong> 5:00 PM - 5:30 PM (Refreshments & rest)</p>
<p><strong>Dinner Break:</strong> After awards ceremony</p>
<p><strong>Note:</strong> Some events like hackathons continue through break times. Plan accordingly!</p>''',
        'intent': 'artifa_info',
        'keywords': 'break, lunch, rest, time, refreshment'
    },
    
    # Registration and Participation
    {
        'question': "Can I participate in multiple events?",
        'answer': '''<h3>Multiple Event Participation</h3>
<p><strong>General Rules:</strong></p>
<ul>
<li>YES, you can participate in multiple events</li>
<li>BUT: Parallel events (same time) require you to choose one</li>
<li>You can do morning event + afternoon/evening events</li>
</ul>
<p><strong>Example Schedule:</strong></p>
<ul>
<li>9:30 AM - 1:00 PM: Suzie's Hackathon (5.5 hours)</li>
<li>2:00 PM - 4:00 PM: Choose ONE solo event</li>
<li>6:30 PM: Awards Ceremony</li>
</ul>
<p><strong>Tip:</strong> Plan your event combinations to maximize participation!</p>''',
        'intent': 'registration_guide',
        'keywords': 'multiple events, participate, several, combine, parallel'
    },
    
    # Event Details - Prizes
    {
        'question': "What are the prizes for the events?",
        'answer': '''<h3>ARTIFA FEST Prize Distribution</h3>
<p><strong>Total Prize Pool:</strong> Over ₹100,000</p>
<p><strong>Prize Categories:</strong></p>
<ul>
<li>1st Place - Cash Prize + Certificate + Trophy</li>
<li>2nd Place - Cash Prize + Certificate</li>
<li>3rd Place - Cash Prize + Certificate</li>
</ul>
<p><strong>Prize Amounts Vary By:</strong></p>
<ul>
<li>Event Category (Technical vs Non-Technical)</li>
<li>Event Difficulty Level</li>
<li>Participation Numbers</li>
</ul>
<p><strong>All Participants Get:</strong> Goodie bags & certificates</p>''',
        'intent': 'event_info',
        'keywords': 'prize, awards, money, cash, trophy, winning'
    },
    
    # Event Preparation
    {
        'question': "How should I prepare for the hackathon?",
        'answer': '''<h3>Hackathon Preparation Guide</h3>
<p><strong>Before the Event:</strong></p>
<ul>
<li>Form your team (1-3 members)</li>
<li>Discuss project ideas</li>
<li>Plan your approach</li>
<li>Test your development setup</li>
</ul>
<p><strong>What to Bring:</strong></p>
<ul>
<li>Laptop with necessary tools installed</li>
<li>Charger and USB cables</li>
<li>Water bottle</li>
<li>Snacks</li>
<li>Headphones for focus</li>
</ul>
<p><strong>Day Of:</strong></p>
<ul>
<li>Arrive early for setup</li>
<li>Attend opening briefing</li>
<li>Manage time effectively</li>
<li>Take short breaks</li>
</ul>''',
        'intent': 'event_info',
        'keywords': 'preparation, prepare, hackathon, tips, how to prepare'
    },
    
    # Technical Event Requirements
    {
        'question': "What programming languages are allowed in technical events?",
        'answer': '''<h3>Programming Languages Allowed</h3>
<p><strong>Most Technical Events Support:</strong></p>
<ul>
<li>Python (Most popular - recommended for all events)</li>
<li>C++</li>
<li>Java</li>
<li>JavaScript</li>
<li>C</li>
<li>Other languages on request</li>
</ul>
<p><strong>Specific Event Requirements:</strong></p>
<ul>
<li><strong>Hawkins Data Files:</strong> Python/SQL preferred</li>
<li><strong>Code from the Upside Down:</strong> Any language</li>
<li><strong>Suzie's Never Ending Story:</strong> Full stack (Frontend + Backend)</li>
</ul>
<p><strong>Note:</strong> Check with organizers for specific event requirements!</p>''',
        'intent': 'event_info',
        'keywords': 'programming language, python, java, c++, allowed'
    },
    
    # Non-Technical Event Details
    {
        'question': "What should I know about the D&D event?",
        'answer': '''<h3>Dungeons & Dragons Event Details</h3>
<p><strong>Format:</strong> Strategy-based adventure game</p>
<p><strong>Team Size:</strong> 2 members per team</p>
<p><strong>Duration:</strong> 2.5 hours (2:00 PM - 4:30 PM)</p>
<p><strong>Prerequisites:</strong> None! No prior D&D experience needed</p>
<p><strong>What Happens:</strong></p>
<ul>
<li>Teams receive game rules</li>
<li>Narrator guides the adventure</li>
<li>Roll dice and make strategic choices</li>
<li>Navigate through challenges</li>
<li>Compete against other teams</li>
</ul>
<p><strong>Winning:</strong> Based on strategy, decisions, and luck</p>''',
        'intent': 'event_info',
        'keywords': 'd&d, dungeons, dragons, game, strategy, adventure'
    },
    
    # Judges and Evaluation
    {
        'question': "How are events judged?",
        'answer': '''<h3>Event Evaluation Criteria</h3>
<p><strong>Technical Events Judged On:</strong></p>
<ul>
<li>Functionality & Correctness</li>
<li>Code Quality & Best Practices</li>
<li>Innovation & Creativity</li>
<li>Documentation</li>
<li>Presentation (for hackathon)</li>
</ul>
<p><strong>Non-Technical Events Judged On:</strong></p>
<ul>
<li>Strategy & Decision Making</li>
<li>Team Coordination</li>
<li>Problem-solving Approach</li>
<li>Final Results/Score</li>
</ul>
<p><strong>Judging Panel:</strong> Industry experts and faculty members</p>
<p><strong>Criteria Communicated:</strong> At event start</p>''',
        'intent': 'event_info',
        'keywords': 'judging, criteria, evaluation, scoring, judges'
    },
    
    # Special Notes
    {
        'question': "Are there any special considerations for the hackathon?",
        'answer': '''<h3>Hackathon Special Details</h3>
<p><strong>Duration:</strong> This is a FULL hackathon (5.5 hours straight)</p>
<p><strong>Intensity:</strong> High-energy, fast-paced event</p>
<p><strong>What's Provided:</strong></p>
<ul>
<li>Wi-Fi access</li>
<li>Seating & workspace</li>
<li>Light refreshments</li>
<li>Power outlets</li>
</ul>
<p><strong>What's NOT Provided:</strong></p>
<ul>
<li>Hardware (bring your own laptop)</li>
<li>Extensive meals (but lunch break available)</li>
</ul>
<p><strong>Tips:</strong></p>
<ul>
<li>Work on a realistic scope</li>
<li>Test thoroughly</li>
<li>Prepare a good presentation</li>
<li>Stay hydrated</li>
</ul>''',
        'intent': 'event_info',
        'keywords': 'hackathon, special, notes, considerations, tips'
    },
    
    # Last Minute Info
    {
        'question': "Can I register for events on the day of the festival?",
        'answer': '''<h3>On-Day Event Registration</h3>
<p><strong>Event Registration:</strong> YES - Available on festival day</p>
<p><strong>Registration Window:</strong> 8:00 AM - 9:00 AM (Early registration)</p>
<p><strong>Late Registration:</strong> Available until 11:30 AM (limited slots)</p>
<p><strong>How to Register:</strong></p>
<ul>
<li>Go to registration desk</li>
<li>Fill in event selection form</li>
<li>Pay any applicable fees</li>
<li>Get your event badge/wristband</li>
</ul>
<p><strong>Note:</strong> Early registration ensures better selection!</p>''',
        'intent': 'registration_guide',
        'keywords': 'register, day of, same day, on-day, registration'
    },
]

def expand_dataset():
    """Add new timeline and event Q&A pairs to the database"""
    print("Starting Timeline & Event Details Dataset Expansion...")
    print("=" * 60)
    
    created_count = 0
    updated_count = 0
    
    for pair in timeline_event_data:
        obj, created = ChatbotTraining.objects.update_or_create(
            question=pair['question'],
            defaults={
                'answer': pair['answer'],
                'intent': pair['intent'],
                'keywords': pair['keywords'],
                'is_active': True
            }
        )
        
        if created:
            created_count += 1
            status = "✓ CREATED"
        else:
            updated_count += 1
            status = "⟳ UPDATED"
        
        print(f"{status} | {pair['question'][:50]}...")
    
    print("=" * 60)
    print(f"\n📊 Expansion Summary:")
    print(f"   • New Q&A Pairs Created: {created_count}")
    print(f"   • Existing Pairs Updated: {updated_count}")
    
    # Get total count
    total_qa = ChatbotTraining.objects.filter(is_active=True).count()
    print(f"   • Total Q&A Pairs in Database: {total_qa}")
    print(f"   • Target Progress: {(total_qa/1000)*100:.1f}% toward 1000 pairs")
    
    print(f"\n✅ Dataset expansion complete!")
    return created_count, updated_count

if __name__ == '__main__':
    created, updated = expand_dataset()
