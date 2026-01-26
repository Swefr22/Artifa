"""
SweKeer Chatbot - AI Assistant for ARTIFA FEST Website
Enhanced with NLP and powerful semantic understanding
Provides intelligent point-by-point answers about NEC, AIDS Department, and ARTIFA FEST
Uses spaCy for advanced English meaning understanding and entity recognition
"""

from django.db.models import Q
from .models import Event, Schedule
import re
from difflib import get_close_matches
import logging

logger = logging.getLogger(__name__)

# Try to import advanced NLP libraries
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("scikit-learn not installed. Using fallback similarity matching.")

try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    NLTK_AVAILABLE = True
    # Download required NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
except ImportError:
    NLTK_AVAILABLE = False
    logger.warning("NLTK not installed. Using basic text processing.")

# Try to import TextBlob for grammar and spell checking
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    logger.warning("TextBlob not installed. Grammar checking disabled. Install with: pip install textblob")

# Try to import language-tool-python for advanced grammar checking
try:
    import language_tool_python
    LANGUAGE_TOOL_AVAILABLE = True
    try:
        grammar_tool = language_tool_python.LanguageTool('en-US')
    except:
        LANGUAGE_TOOL_AVAILABLE = False
        grammar_tool = None
except ImportError:
    LANGUAGE_TOOL_AVAILABLE = False
    grammar_tool = None
    logger.warning("language-tool-python not installed. Advanced grammar checking disabled. Install with: pip install language-tool-python")

# Try to import spaCy for advanced semantic understanding
try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
        SPACY_AVAILABLE = True
    except OSError:
        logger.warning("spaCy model not found. Downloading en_core_web_sm...")
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], quiet=True)
        nlp = spacy.load("en_core_web_sm")
        SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    nlp = None
    logger.warning("spaCy not installed. Advanced semantic understanding disabled. Install with: pip install spacy")


class SweKeerChatbot:
    def __init__(self):
        self.name = "SweKeer"
        self.website_name = "ARTIFA FEST"
        self.college_name = "NEC - Department of AI & DS"
        
        # Knowledge Base about NEC, AIDS, and ARTIFA FEST
        self.knowledge_base = {
            'nec': {
                'full_name': 'National Engineering College',
                'location': 'Kovilpatti, Tamil Nadu',
                'established': '1981',
                'about': [
                    '<i class="fas fa-check-circle"></i> Premier engineering institution in South India',
                    '<i class="fas fa-check-circle"></i> ISO 9001:2015 certified autonomous college',
                    '<i class="fas fa-check-circle"></i> Top ranking in NIRF and other national rankings',
                    '<i class="fas fa-check-circle"></i> Strong focus on academics, research, and innovation',
                    '<i class="fas fa-check-circle"></i> Active placement record with top companies',
                    '<i class="fas fa-check-circle"></i> Modern infrastructure and facilities'
                ],
                'contact': 'info@nec.edu.in',
                'website': 'www.nec.edu.in'
            },
            'aids': {
                'full_name': 'Department of Artificial Intelligence & Data Science',
                'established': '2021',
                'about': [
                    '<i class="fas fa-check-circle"></i> Latest department offering cutting-edge AI & DS curriculum',
                    '<i class="fas fa-check-circle"></i> Focus on machine learning, deep learning, and data analytics',
                    '<i class="fas fa-check-circle"></i> Industry-aligned projects and internships',
                    '<i class="fas fa-check-circle"></i> State-of-the-art computing labs and resources',
                    '<i class="fas fa-check-circle"></i> Partnerships with leading tech companies',
                    '<i class="fas fa-check-circle"></i> Active research in AI, ML, NLP, and Computer Vision'
                ],
                'highlights': [
                    'Modern AI/ML frameworks and tools',
                    'Real-world data science projects',
                    'Guest lectures from industry experts',
                    'Hackathons and innovation challenges'
                ]
            },
            'artifa_fest': {
                'full_name': 'ARTIFA FEST - AI & Data Science Intra-College Festival',
                'date': 'February 7, 2026',
                'about': [
                    '<i class="fas fa-check-circle"></i> Premier festival celebrating AI & Data Science talents',
                    '<i class="fas fa-check-circle"></i> Showcasing innovative projects and ideas',
                    '<i class="fas fa-check-circle"></i> Platform for technical and non-technical competitions',
                    '<i class="fas fa-check-circle"></i> Organized by AI & DS Department students',
                    '<i class="fas fa-check-circle"></i> Open to all college students and participants',
                    '<i class="fas fa-check-circle"></i> Focus on learning, innovation, and fun'
                ],
                'event_categories': [
                    'Technical Events: Coding, Hackathons, AI competitions',
                    'Non-Technical Events: Gaming, Quizzes, Creative events',
                    'Workshops and Guest Sessions',
                    'Project Showcases'
                ],
                'organizers': [
                    'ARUN KATHIRESAN M',
                    'KEERTHANA A R',
                    'SHARAVANAN S',
                    'SWEETY FROST A',
                    'MANO SATHIYA MOORTHI M'
                ]
            },
            'registration_guide': {
                'title': 'How to Register',
                'steps': [
                    '<b>Step 1</b>: Go to the Registration page',
                    '<b>Step 2</b>: Fill in your personal details (Name, Email, Phone)',
                    '<b>Step 3</b>: Enter your college name and department',
                    '<b>Step 4</b>: Create a password (Minimum 8 characters)',
                    '<b>Step 5</b>: Select your interested events/categories',
                    '<b>Step 6</b>: Accept terms and conditions',
                    '<b>Step 7</b>: Click "Register" button',
                    '<b>Step 8</b>: You will receive a confirmation email',
                    '<b>Step 9</b>: Verify your email by clicking the link',
                    '<b>Step 10</b>: Login with your credentials'
                ],
                'tips': [
                    '<i class="fas fa-lightbulb"></i> Use a valid email address',
                    '<i class="fas fa-lightbulb"></i> Remember your password securely',
                    '<i class="fas fa-lightbulb"></i> Select all events you\'re interested in',
                    '<i class="fas fa-lightbulb"></i> Check your spam folder for confirmation email'
                ]
            },
            'team_guide': {
                'title': 'How to Manage Team',
                'steps': [
                    '<b>Step 1</b>: Login to your account',
                    '<b>Step 2</b>: Go to "Team Dashboard"',
                    '<b>Step 3</b>: Click "Create Team" or "Join Team"',
                    '<b>Step 4</b>: Enter team name and description',
                    '<b>Step 5</b>: Set team password for security',
                    '<b>Step 6</b>: Go to "Team Members" section',
                    '<b>Step 7</b>: Click "Add Member" button',
                    '<b>Step 8</b>: Enter team member email or registration number',
                    '<b>Step 9</b>: Select member role (Leader/Co-leader/Member)',
                    '<b>Step 10</b>: Click "Send Invite" and wait for acceptance'
                ],
                'edit_member': [
                    '<b>To Edit Member</b>:',
                    '1. Go to Team Dashboard → Team Members',
                    '2. Find the member you want to edit',
                    '3. Click the "Edit" button next to their name',
                    '4. Modify their role or details',
                    '5. Click "Save Changes"'
                ],
                'remove_member': [
                    '<b>To Remove Member</b>:',
                    '1. Go to Team Dashboard → Team Members',
                    '2. Find the member to remove',
                    '3. Click the "Remove" button',
                    '4. Confirm the removal',
                    '5. Member will receive notification'
                ]
            },
            'view_team_guide': {
                'title': 'How to View Team Information',
                'steps': [
                    '<b>Step 1</b>: Login to your account',
                    '<b>Step 2</b>: Click on "Team Dashboard" or "My Team"',
                    '<b>Step 3</b>: View your team information',
                    '<b>Step 4</b>: See all team members listed',
                    '<b>Step 5</b>: Check member status (Approved/Pending/Rejected)',
                    '<b>Step 6</b>: View team events registration',
                    '<b>Step 7</b>: See team performance/scores if available',
                    '<b>Step 8</b>: Check team messages and announcements'
                ],
                'sections': [
                    '<i class="fas fa-users"></i> Team Members: View all members and their roles',
                    '<i class="fas fa-info-circle"></i> Team Info: Basic team details and description',
                    '<i class="fas fa-calendar"></i> Registered Events: Events your team joined',
                    '<i class="fas fa-chart-bar"></i> Team Statistics: Performance metrics',
                    '<i class="fas fa-comments"></i> Team Messages: Communication with members'
                ]
            },
            'navigation_guide': {
                'title': 'Website Navigation Guide',
                'pages': [
                    '<b><i class="fas fa-home"></i> Home Page</b>: Overview of ARTIFA FEST, featured events, announcements',
                    '<b><i class="fas fa-list"></i> Events Page</b>: Browse all technical and non-technical events',
                    '<b><i class="fas fa-calendar-alt"></i> Schedule Page</b>: View timeline and event schedule',
                    '<b><i class="fas fa-user-circle"></i> Profile Page</b>: Update your personal information',
                    '<b><i class="fas fa-users"></i> Team Dashboard</b>: Manage your team and members',
                    '<b><i class="fas fa-edit"></i> Edit Profile</b>: Change password, email, phone',
                    '<b><i class="fas fa-file-alt"></i> Participants Page</b>: View registered participants'
                ],
                'restrictions': [
                    '<i class="fas fa-ban"></i> Dashboard access is restricted to admin users only',
                    '<i class="fas fa-lock"></i> You cannot view other teams\' private information',
                    '<i class="fas fa-info-circle"></i> Admin features are hidden from regular users'
                ]
            },
            'profile_guide': {
                'title': 'How to Manage Your Profile',
                'sections': [
                    '<b>View Profile</b>:',
                    '1. Click your name/avatar in top-right corner',
                    '2. Select "My Profile"',
                    '3. View all your information',
                    '',
                    '<b>Edit Profile</b>:',
                    '1. Go to "My Profile"',
                    '2. Click "Edit Profile" button',
                    '3. Update desired information',
                    '4. Click "Save Changes"',
                    '',
                    '<b>Change Password</b>:',
                    '1. Go to Settings → Change Password',
                    '2. Enter current password',
                    '3. Enter new password twice',
                    '4. Click "Update Password"'
                ]
            }
        }
        
        # Define intent templates for semantic matching
        self.intents = {
            'greeting': [
                "hello", "hi", "hey", "greetings", "namaste", "howdy", "good morning",
                "good afternoon", "good evening", "sup", "what's up", "yo", "hey whats",
                "hey what's", "what's up"
            ],
            'nec_info': [
                "nec", "national engineering", "college", "about nec", "tell nec",
                "what is nec", "nec details", "national engineering college"
            ],
            'aids_info': [
                "aids", "ai and ds", "data science", "artificial intelligence",
                "about aids", "tell aids", "what is aids", "ai ds department",
                "department of ai", "ai and data science"
            ],
            'artifa_info': [
                "artifa", "artifa fest", "festival", "about artifa", "what is artifa",
                "artifa details", "artifa competition", "tell artifa"
            ],
            'website_info': [
                "what is this", "tell me about", "about", "info", "information", 
                "festival details", "who organizes", "website info", "website details"
            ],
            'events': [
                "events", "competitions", "activities", "contest", "participate",
                "list events", "show events", "all events", "what events", "event list",
                "tell me events", "competitions", "activity", "show me activities"
            ],
            'technical_events': [
                "technical", "coding", "programming", "hackathon", "tech", "it",
                "tech events", "technical competitions", "programming contest",
                "show tech", "tech events", "technical activities", "coding competitions"
            ],
            'nontechnical_events': [
                "non-technical", "nontechnical", "non technical", "cultural",
                "games", "fun", "entertainment", "sports", "activities",
                "non tech", "nontechnical events"
            ],
            'timeline': [
                "timeline", "schedule", "when", "time", "timing", "event timing",
                "festival schedule", "what time", "start time", "end time",
                "when are", "schedule activities", "timing", "when is"
            ],
            'registration_guide': [
                "register", "registration", "how to register", "sign up", "create account",
                "register guide", "registration process", "how do i register",
                "registration steps", "how to sign up", "how to create account",
                "registration help", "register help"
            ],
            'team_guide': [
                "team", "create team", "manage team", "team members", "edit members",
                "add members", "how to manage team", "team management", "team guide",
                "how to create team", "how to add members", "team help",
                "edit team members", "team members guide"
            ],
            'view_team_guide': [
                "view team", "see team", "team info", "team information", "my team",
                "team dashboard", "show team", "team details", "view team info",
                "how to view team", "team view guide", "see my team",
                "view team members"
            ],
            'navigation_guide': [
                "navigation", "website", "pages", "how to use", "website guide",
                "navigate", "where to", "how to find", "site guide", "website help",
                "page guide", "all pages", "explore website", "website navigation",
                "how to navigate"
            ],
            'profile_guide': [
                "profile", "my profile", "edit profile", "change password", "account",
                "user profile", "profile guide", "how to edit profile", "manage profile",
                "account settings", "profile help", "update profile",
                "change password guide"
            ],
            'help': [
                "help", "what can you", "guide", "options", "assist", "support",
                "how can you help", "what do you do", "what can i ask", "capabilities",
                "what can help", "assist me", "guide me", "guidance", "help me"
            ]
        }
        
    def search_training_database(self, user_message, confidence_threshold=0.2):
        """
        Search ChatbotTraining database for matching answer using semantic similarity
        Checks if question meaning matches stored training data
        Returns (answer, confidence, found) tuple
        Optimized for short queries like acronyms
        """
        try:
            from core.models import ChatbotTraining
            
            user_msg_lower = user_message.lower().strip()
            user_words = set(user_msg_lower.split())
            
            training_pairs = ChatbotTraining.objects.filter(is_active=True)
            
            best_match = None
            best_confidence = 0
            
            # For very short queries (1-2 words), check keywords more aggressively
            is_short_query = len(user_words) <= 2
            
            for pair in training_pairs:
                # Check 1: Exact keyword match (highest priority)
                keyword_similarity = 0
                if pair.keywords:
                    keywords = [k.strip().lower() for k in pair.keywords.split(',')]
                    # Check for exact or partial matches
                    matched_keywords = sum(1 for kw in keywords if kw in user_msg_lower or any(w in kw for w in user_words))
                    if keywords:
                        keyword_similarity = matched_keywords / len(keywords)
                    else:
                        keyword_similarity = 0
                
                # For short queries, boost keyword matching
                if is_short_query and keyword_similarity > 0:
                    keyword_similarity = min(1.0, keyword_similarity * 1.2)
                
                # Check 2: Question similarity using TF-IDF if available
                question_similarity = 0
                if SKLEARN_AVAILABLE:
                    try:
                        from sklearn.feature_extraction.text import TfidfVectorizer
                        from sklearn.metrics.pairwise import cosine_similarity
                        
                        vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', min_df=1)
                        vectors = vectorizer.fit_transform([user_msg_lower, pair.question.lower()])
                        question_similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
                    except Exception as e:
                        logger.debug(f"TF-IDF similarity error: {e}")
                        # Fallback to simple word overlap
                        pair_words = set(pair.question.lower().split())
                        if user_words and pair_words:
                            intersection = len(user_words & pair_words)
                            union = len(user_words | pair_words)
                            question_similarity = intersection / union if union > 0 else 0
                
                # Check 3: Intent matching (bonus for short queries matching intent)
                intent_similarity = 0
                if pair.intent:
                    # Check if any user word is in intent name
                    for word in user_words:
                        if word in pair.intent.lower():
                            intent_similarity = 0.3
                            break
                
                # For short acronym queries, give intent matching more weight
                if is_short_query and intent_similarity > 0:
                    intent_similarity = 0.4
                
                # Combined confidence (weighted)
                # For short queries, keyword and intent matter more
                if is_short_query:
                    confidence = (keyword_similarity * 0.6) + (question_similarity * 0.25) + (intent_similarity * 0.15)
                else:
                    confidence = (keyword_similarity * 0.5) + (question_similarity * 0.35) + (intent_similarity * 0.15)
                
                if confidence > best_confidence and confidence >= confidence_threshold:
                    best_confidence = confidence
                    best_match = pair.answer
            
            if best_match:
                logger.info(f"Found training match for '{user_message}' with confidence {best_confidence:.2f}")
                return (best_match, round(best_confidence, 2), True)
            else:
                logger.debug(f"No training match found for '{user_message}'")
                return (None, 0, False)
                
        except ImportError:
            logger.warning("ChatbotTraining model not available")
            return (None, 0, False)
        except Exception as e:
            logger.error(f"Error searching training database: {e}")
            return (None, 0, False)
    
    def get_website_info(self):
        """Get basic website information"""
        return {
            "name": self.website_name,
            "college": self.college_name,
            "type": "AI & DS Department Festival",
            "description": "An interactive platform showcasing technical and non-technical events from NEC's Department of AI & DS"
        }
    
    def check_grammar_and_correct(self, user_message):
        """
        Check grammar and spelling using available tools
        Returns corrected message and error details if any
        Preserves known acronyms and proper nouns from being "corrected"
        """
        corrections = {
            'original': user_message,
            'corrected': user_message,
            'errors': [],
            'spell_check_available': False,
            'grammar_check_available': False
        }
        
        # List of known acronyms and proper nouns that should NOT be corrected
        protected_words = {
            'nec': 'National Engineering College',
            'aids': 'Artificial Intelligence & Data Science',
            'ai': 'Artificial Intelligence',
            'artifa': 'ARTIFA FEST',
            'fest': 'Festival',
            'ds': 'Data Science',
            'covid': 'COVID',
            'html': 'HTML',
            'css': 'CSS',
            'js': 'JavaScript',
            'python': 'Python',
            'java': 'Java',
            'website': 'Website',
            'venue': 'Venue',
            'timing': 'Timing',
            'register': 'Register',
            'registration': 'Registration',
            'team': 'Team',
            'member': 'Member',
            'event': 'Event',
            'kovilpathi': 'Kovilpathi',
            'tamil': 'Tamil',
            'nadu': 'Nadu'
        }
        
        # Try TextBlob for spell checking
        if TEXTBLOB_AVAILABLE:
            try:
                blob = TextBlob(user_message)
                corrected = str(blob.correct())
                
                # Check if correction removed any protected words
                # If so, use original instead
                message_lower = user_message.lower()
                corrected_lower = corrected.lower()
                
                should_skip_correction = False
                for protected_word in protected_words.keys():
                    if protected_word in message_lower and protected_word not in corrected_lower:
                        should_skip_correction = True
                        logger.debug(f"Skipping spell correction - would remove protected word: {protected_word}")
                        break
                
                if not should_skip_correction and corrected != user_message:
                    corrections['corrected'] = corrected
                    corrections['spell_check_available'] = True
                    corrections['errors'].append(f"Spell check: '{user_message}' → '{corrected}'")
            except Exception as e:
                logger.debug(f"TextBlob error: {e}")
        
        # Try LanguageTool for advanced grammar checking
        if LANGUAGE_TOOL_AVAILABLE and grammar_tool:
            try:
                matches = grammar_tool.check(user_message)
                if matches:
                    corrections['grammar_check_available'] = True
                    for match in matches[:5]:  # Limit to 5 errors
                        if match.replacements:
                            correction = match.replacements[0]
                            error_info = f"Grammar: {match.message} → '{correction}'"
                            corrections['errors'].append(error_info)
                            # Apply first correction
                            if not corrections['corrected'].startswith(match.context):
                                corrections['corrected'] = corrections['corrected'].replace(
                                    match.context.strip(), 
                                    match.context.replace(match.matchedText, correction)
                                )
            except Exception as e:
                logger.debug(f"LanguageTool error: {e}")
        
        return corrections
    
    def extract_meaning_and_intent(self, user_message):
        """
        Extract deep meaning from complex user messages
        Uses spaCy NLP for semantic analysis, entity recognition, and relationship extraction
        """
        meaning = {
            'original': user_message,
            'cleaned': user_message.lower().strip(),
            'entities': [],
            'keywords': [],
            'noun_chunks': [],
            'verbs': [],
            'sentiment': None,
            'complexity_score': 0,
            'intent_clues': [],
            'confidence': 0.0
        }
        
        if not SPACY_AVAILABLE or nlp is None:
            return meaning
        
        try:
            # Parse with spaCy
            doc = nlp(user_message)
            
            # Extract entities (people, places, concepts, etc.)
            for ent in doc.ents:
                meaning['entities'].append({
                    'text': ent.text,
                    'type': ent.label_,
                    'description': f"Named Entity: {ent.text} ({ent.label_})"
                })
            
            # Extract noun chunks (meaningful phrases)
            for chunk in doc.noun_chunks:
                meaning['noun_chunks'].append(chunk.text)
            
            # Extract keywords (nouns and important words)
            for token in doc:
                if token.pos_ in ['NOUN', 'PROPN']:
                    meaning['keywords'].append({
                        'text': token.text,
                        'pos': token.pos_,
                        'lemma': token.lemma_
                    })
                elif token.pos_ == 'VERB':
                    meaning['verbs'].append({
                        'text': token.text,
                        'lemma': token.lemma_
                    })
            
            # Calculate complexity based on multiple factors
            sentence_count = len(list(doc.sents))
            token_count = len(doc)
            entity_count = len(doc.ents)
            verb_count = len([t for t in doc if t.pos_ == 'VERB'])
            
            # Complexity score (0-10)
            complexity_components = [
                sentence_count / 2,  # More sentences = more complex
                token_count / 20,     # Longer queries = more complex
                entity_count / 3,     # More entities = more complex
                verb_count / 2        # More verbs = more complex
            ]
            meaning['complexity_score'] = min(10, sum(complexity_components) / len(complexity_components))
            
            # Confidence in understanding
            if meaning['keywords'] or meaning['noun_chunks']:
                meaning['confidence'] = min(1.0, (len(meaning['keywords']) + len(meaning['noun_chunks'])) / 10)
            
            # Intent clues based on verbs and dependencies
            question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which']
            for token in doc:
                if token.text.lower() in question_words:
                    meaning['intent_clues'].append(f"Question word: {token.text}")
                if token.dep_ in ['ROOT', 'nsubj']:
                    meaning['intent_clues'].append(f"Key concept: {token.text}")
            
        except Exception as e:
            logger.debug(f"spaCy semantic extraction error: {e}")
        
        return meaning
    
    def get_nec_info(self):
        """Get detailed information about NEC"""
        kb = self.knowledge_base['nec']
        response = "<i class='fas fa-building'></i> <b>National Engineering College (NEC)</b><br>"
        response += "<br><i class='fas fa-map-marker-alt'></i> <b>Location</b>: Kovilpatti, Tamil Nadu<br>"
        response += "<br><i class='fas fa-calendar'></i> <b>Established</b>: 1981<br>"
        response += "<br><b>About NEC:</b><br>"
        for point in kb['about']:
            response += f"<br>{point}<br>"
        response += "<br><i class='fas fa-envelope'></i> <b>Contact</b>: info@nec.edu.in<br>"
        response += "<br><i class='fas fa-globe'></i> <b>Website</b>: www.nec.edu.in<br>"
        return response
    
    def get_aids_info(self):
        """Get detailed information about AIDS Department"""
        kb = self.knowledge_base['aids']
        response = "<i class='fas fa-robot'></i> <b>Department of Artificial Intelligence & Data Science (AIDS)</b><br>"
        response += "<br><i class='fas fa-calendar'></i> <b>Established</b>: 2021<br>"
        response += "<br><b>About the Department:</b><br>"
        for point in kb['about']:
            response += f"<br>{point}<br>"
        response += "<br><b>Key Highlights:</b><br>"
        for highlight in kb['highlights']:
            response += f"<br><i class='fas fa-star'></i> {highlight}<br>"
        return response
    
    def get_artifa_info(self):
        """Get detailed information about ARTIFA FEST"""
        kb = self.knowledge_base['artifa_fest']
        response = "<i class='fas fa-party-horn'></i> <b>ARTIFA FEST - AI & Data Science Intra-College Festival</b><br>"
        response += "<br><i class='fas fa-calendar'></i> <b>Date</b>: February 7, 2026<br>"
        response += "<br><b>About the Festival:</b><br>"
        for point in kb['about']:
            response += f"<br>{point}<br>"
        response += "<br><b>Event Categories:</b><br>"
        for category in kb['event_categories']:
            response += f"<br><i class='fas fa-bullseye'></i> {category}<br>"
        response += "<br><b>Organized by:</b><br>"
        for organizer in kb['organizers']:
            response += f"<br><i class='fas fa-code'></i> {organizer}<br>"
        return response
    
    def get_registration_guide(self):
        """Get registration guide"""
        kb = self.knowledge_base['registration_guide']
        response = "<i class='fas fa-user-plus'></i> <b>How to Register for ARTIFA FEST</b><br>"
        response += "<br><b>Registration Steps:</b><br>"
        for step in kb['steps']:
            response += f"<br>{step}<br>"
        response += "<br><br><b>Registration Tips:</b><br>"
        for tip in kb['tips']:
            response += f"<br>{tip}<br>"
        return response
    
    def get_team_guide(self):
        """Get team management guide"""
        kb = self.knowledge_base['team_guide']
        response = "<i class='fas fa-users'></i> <b>How to Create and Manage Teams</b><br>"
        response += "<br><b>Create Team Steps:</b><br>"
        for step in kb['steps']:
            response += f"<br>{step}<br>"
        response += "<br><br>"
        for edit_step in kb['edit_member']:
            response += f"{edit_step}<br>"
        response += "<br><br>"
        for remove_step in kb['remove_member']:
            response += f"{remove_step}<br>"
        return response
    
    def get_view_team_guide(self):
        """Get view team guide"""
        kb = self.knowledge_base['view_team_guide']
        response = "<i class='fas fa-eye'></i> <b>How to View Your Team Information</b><br>"
        response += "<br><b>Steps to View Team:</b><br>"
        for step in kb['steps']:
            response += f"<br>{step}<br>"
        response += "<br><br><b>Team Dashboard Sections:</b><br>"
        for section in kb['sections']:
            response += f"<br>{section}<br>"
        return response
    
    def get_navigation_guide(self):
        """Get website navigation guide"""
        kb = self.knowledge_base['navigation_guide']
        response = "<i class='fas fa-map'></i> <b>Website Navigation Guide</b><br>"
        response += "<br><b>Website Pages:</b><br>"
        for page in kb['pages']:
            response += f"<br>{page}<br>"
        response += "<br><br><b>Important Restrictions:</b><br>"
        for restriction in kb['restrictions']:
            response += f"<br>{restriction}<br>"
        return response
    
    def get_profile_guide(self):
        """Get profile management guide"""
        kb = self.knowledge_base['profile_guide']
        response = "<i class='fas fa-user-cog'></i> <b>How to Manage Your Profile</b><br>"
        response += "<br>"
        for section in kb['sections']:
            response += f"{section}<br>"
        return response
    
    def get_all_events(self):
        """Get all events from database"""
        events = Event.objects.all().values('id', 'name', 'description', 'event_type', 'created_at')
        return list(events)
    
    def get_events_by_category(self, event_type):
        """Get events filtered by event_type"""
        events = Event.objects.filter(event_type__icontains=event_type).values('id', 'name', 'description', 'event_type', 'created_at')
        return list(events)
    
    def get_timeline(self):
        """Get festival timeline/schedule"""
        schedule = Schedule.objects.all().order_by('date', 'start_time').values(
            'title', 'description', 'date', 'start_time', 'end_time'
        )
        return list(schedule)
    
    def get_timeline_by_date(self, date_str):
        """Get timeline items for a specific date"""
        schedule = Schedule.objects.filter(date=date_str).order_by('start_time').values(
            'title', 'description', 'start_time', 'end_time'
        )
        return list(schedule)
    
    def extract_time_from_message(self, message):
        """
        Extract time information from user message
        Returns time string or None
        """
        import re
        # Match time patterns: HH:MM, H:MM, HH.MM, etc.
        time_patterns = [
            r'(\d{1,2}):(\d{2})\s*(am|pm|AM|PM)?',
            r'(\d{1,2})\.(\d{2})\s*(am|pm|AM|PM)?',
            r'(\d{1,2})\s*oclock|o\'clock',
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, message.lower())
            if match:
                return match.group(0)
        return None
    
    def get_schedule_by_time(self, time_query):
        """
        Find schedule items happening at a specific time
        Returns matching schedule items
        """
        try:
            # Parse the time query
            import re
            time_match = re.search(r'(\d{1,2}):?(\d{2})?', time_query)
            if not time_match:
                return []
            
            hour = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            
            # Get all schedules and filter by time
            from datetime import time as datetime_time
            target_time = datetime_time(hour, minute)
            
            schedules = Schedule.objects.all().order_by('date', 'start_time')
            matching_schedules = []
            
            for sched in schedules:
                # Check if target time falls within event time range
                if sched.start_time <= target_time <= sched.end_time:
                    matching_schedules.append({
                        'title': sched.title,
                        'description': sched.description,
                        'start_time': sched.start_time.strftime('%H:%M'),
                        'end_time': sched.end_time.strftime('%H:%M'),
                        'is_break': sched.is_break,
                        'event': sched.event.name if sched.event else 'No specific event'
                    })
            
            return matching_schedules
        except Exception as e:
            print(f"Error parsing time: {e}")
            return []
    
    def extract_search_term(self, message):
        """
        Extract the main search term from the message
        Removes common words and returns the core search term
        """
        # Remove common search words
        clean_msg = message.lower()
        remove_words = ['tell', 'me', 'about', 'show', 'what', 'is', 'are', 'the', 'a', 'an', 'in', 'on', 'at']
        
        for word in remove_words:
            clean_msg = re.sub(r'\b' + word + r'\b', ' ', clean_msg)
        
        # Clean up extra spaces and punctuation
        clean_msg = re.sub(r'[^\w\s]', '', clean_msg)
        clean_msg = ' '.join(clean_msg.split())
        
        return clean_msg.strip()
    
    def understand_user_meaning(self, message):
        """
        Use spaCy to understand the exact meaning of user's question
        Extracts entities, verbs, nouns, and semantic relationships
        Returns detailed understanding of what user is asking
        """
        if not SPACY_AVAILABLE or nlp is None:
            return self._basic_meaning_extraction(message)
        
        try:
            doc = nlp(message.lower())
            
            # Extract entities (PERSON, ORG, EVENT, etc.)
            entities = {}
            for ent in doc.ents:
                if ent.label_ not in entities:
                    entities[ent.label_] = []
                entities[ent.label_].append(ent.text)
            
            # Extract verbs (actions) and nouns (subjects)
            verbs = []
            nouns = []
            for token in doc:
                if token.pos_ == 'VERB':
                    verbs.append(token.text)
                elif token.pos_ == 'NOUN':
                    nouns.append(token.text)
            
            # Get lemmatization (base form of words)
            lemmas = [token.lemma_ for token in doc if not token.is_stop]
            
            # Get noun chunks (meaningful phrases)
            noun_chunks = [chunk.text for chunk in doc.noun_chunks]
            
            understanding = {
                'entities': entities,
                'verbs': verbs,
                'nouns': nouns,
                'lemmas': lemmas,
                'noun_chunks': noun_chunks,
                'original': message,
                'tokens': [token.text for token in doc]
            }
            
            return understanding
        except Exception as e:
            logger.error(f"Error in spaCy processing: {e}")
            return self._basic_meaning_extraction(message)
    
    def _basic_meaning_extraction(self, message):
        """
        Fallback method if spaCy is not available
        Extracts meaning using NLTK and regex
        """
        from nltk.tokenize import word_tokenize
        from nltk.corpus import stopwords
        
        try:
            tokens = word_tokenize(message.lower())
            stop_words = set(stopwords.words('english'))
            meaningful_tokens = [t for t in tokens if t.isalnum() and t not in stop_words]
            
            understanding = {
                'tokens': meaningful_tokens,
                'original': message,
                'method': 'basic_nltk'
            }
            return understanding
        except:
            return {
                'tokens': message.lower().split(),
                'original': message,
                'method': 'basic_split'
            }
    
    def find_semantic_answer(self, user_message, understood_meaning):
        """
        Find the most relevant answer based on semantic understanding
        Matches user's intent with knowledge base using semantic similarity
        """
        # Get the noun chunks or main keywords
        keywords = understood_meaning.get('noun_chunks', 
                  understood_meaning.get('tokens', user_message.lower().split()))
        
        if not keywords:
            return None
        
        # Check for specific topics in knowledge base
        keyword_str = ' '.join(keywords).lower()
        
        # Match against knowledge base topics
        nec_keywords = ['nec', 'engineering', 'college', 'kovilpatti', 'institution']
        aids_keywords = ['aids', 'ai', 'data science', 'department', 'artificial intelligence']
        artifa_keywords = ['artifa', 'fest', 'festival', 'competition', 'event']
        
        # Check keyword matches
        nec_match = sum(1 for kw in nec_keywords if kw in keyword_str)
        aids_match = sum(1 for kw in aids_keywords if kw in keyword_str)
        artifa_match = sum(1 for kw in artifa_keywords if kw in keyword_str)
        
        match_scores = {
            'nec': nec_match,
            'aids': aids_match,
            'artifa': artifa_match
        }
        
        # Return the best matching topic
        if max(match_scores.values()) > 0:
            best_match = max(match_scores, key=match_scores.get)
            return best_match
        
        return None
    
    def search_event_by_name(self, query):
        """
        Search for events by name with fuzzy matching
        Returns exact matches first, then fuzzy matches
        """
        if not query or len(query.strip()) < 2:
            return []
        
        query_clean = query.strip().lower()
        
        # Exact or partial match
        exact_matches = Event.objects.filter(
            Q(name__icontains=query_clean) | Q(description__icontains=query_clean)
        ).values('id', 'name', 'description', 'event_type', 'created_at')
        
        exact_list = list(exact_matches)
        
        # If no exact matches, try fuzzy matching
        if not exact_list:
            all_events = Event.objects.all().values('id', 'name', 'description', 'event_type', 'created_at')
            event_names = [event['name'] for event in all_events]
            
            # Find close matches using difflib
            close_matches = get_close_matches(query_clean, event_names, n=3, cutoff=0.5)
            
            fuzzy_list = []
            for match in close_matches:
                event = Event.objects.filter(name=match).values('id', 'name', 'description', 'event_type', 'created_at').first()
                if event:
                    fuzzy_list.append(event)
            
            return fuzzy_list
        
        return exact_list
    
    def understand_intent(self, user_message):
        """
        Enhanced semantic intent recognition using advanced NLP
        First uses spaCy for semantic understanding
        Then uses scikit-learn TF-IDF for similarity or fallback to keyword matching
        """
        user_message_clean = user_message.lower().strip()
        user_message_clean = re.sub(r'[^\w\s]', '', user_message_clean)
        
        # IMPORTANT: Check direct keyword matches FIRST for common short queries
        # This ensures single-word queries are recognized immediately
        
        # Direct NEC queries (check FIRST before anything else)
        if user_message_clean in ['nec', 'national engineering', 'college', 'engineering college']:
            return 'nec_info', 0.99
        if any(word in user_message_clean.split() for word in ['nec', 'engineering']) and len(user_message_clean) < 20:
            return 'nec_info', 0.99
        
        # Direct AIDS queries (check FIRST before anything else)
        if user_message_clean in ['aids', 'ai', 'data science', 'artificial intelligence', 'ai and ds']:
            return 'aids_info', 0.99
        if any(word in user_message_clean.split() for word in ['aids', 'ai and ds', 'data science']) and len(user_message_clean) < 20:
            return 'aids_info', 0.99
        
        # Direct ARTIFA queries (check FIRST before anything else)
        if user_message_clean in ['artifa', 'artifa fest', 'fest', 'festival']:
            return 'artifa_info', 0.99
        if 'artifa' in user_message_clean or 'fest' in user_message_clean:
            return 'artifa_info', 0.99
        
        # IMPORTANT: Check guide keywords FIRST before spaCy semantic matching
        # This ensures guides are prioritized over general information
        
        # Registration guide (check first - more specific)
        if any(word in user_message_clean for word in ['register', 'registration', 'sign up']):
            return 'registration_guide', 0.95
        
        # View team guide (check before team guide - more specific)
        if any(word in user_message_clean for word in ['view team', 'see team', 'my team', 'team dashboard', 'team info', 'team information']):
            return 'view_team_guide', 0.95
        
        # Team guide
        if any(word in user_message_clean for word in ['team', 'manage team', 'add member', 'team member', 'edit team', 'edit member']):
            return 'team_guide', 0.95
        
        # Navigation guide
        if any(word in user_message_clean for word in ['navigation', 'how to navigate', 'pages', 'how to use', 'navigate', 'guide', 'dashboard']):
            return 'navigation_guide', 0.95
        
        # Profile guide
        if any(word in user_message_clean for word in ['profile', 'my profile', 'edit profile', 'account', 'password', 'change password']):
            return 'profile_guide', 0.95
        
        # Use spaCy for semantic understanding of difficult questions
        if SPACY_AVAILABLE and nlp is not None:
            semantic_meaning = self.understand_user_meaning(user_message)
            semantic_topic = self.find_semantic_answer(user_message, semantic_meaning)
            
            if semantic_topic:
                intent_map = {
                    'nec': 'nec_info',
                    'aids': 'aids_info',
                    'artifa': 'artifa_info'
                }
                if semantic_topic in intent_map:
                    return intent_map[semantic_topic], 0.92
        
        # Info queries
        if any(word in user_message_clean for word in ['nec', 'national engineering']):
            return 'nec_info', 0.95
        if any(word in user_message_clean for word in ['aids', 'artificial intelligence', 'data science', 'ai and ds']):
            return 'aids_info', 0.95
        if any(word in user_message_clean for word in ['artifa', 'artifa fest', 'festival', 'competition']):
            return 'artifa_info', 0.95
        if any(word in user_message_clean for word in ['non-technical', 'nontechnical', 'non technical']):
            return 'nontechnical_events', 0.9
        
        # Use scikit-learn TF-IDF if available for better accuracy
        if SKLEARN_AVAILABLE:
            return self._understand_intent_sklearn(user_message_clean)
        else:
            return self._understand_intent_fallback(user_message_clean)
    
    def _understand_intent_sklearn(self, user_message_clean):
        """Intent recognition using TF-IDF and cosine similarity"""
        try:
            # Create keyword lists for each intent
            intent_keywords = {}
            for intent, keywords in self.intents.items():
                intent_keywords[intent] = ' '.join(keywords)
            
            # Prepare documents
            documents = [user_message_clean] + list(intent_keywords.values())
            
            # TF-IDF vectorization
            vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(documents)
            
            # Calculate cosine similarity
            user_vector = tfidf_matrix[0:1]
            intent_scores = {}
            
            for idx, intent in enumerate(intent_keywords.keys(), 1):
                similarity = cosine_similarity(user_vector, tfidf_matrix[idx:idx+1])[0][0]
                intent_scores[intent] = float(similarity)
            
            # Get best matching intent
            best_intent = max(intent_scores, key=intent_scores.get)
            best_score = intent_scores[best_intent]
            
            if best_score >= 0.15:
                return best_intent, best_score
            
            return None, 0.0
        except Exception as e:
            logger.warning(f"Error in sklearn intent recognition: {e}")
            return self._understand_intent_fallback(user_message_clean)
    
    def _understand_intent_fallback(self, user_message_clean):
        """Fallback intent recognition using Jaccard similarity"""
        user_words = set(user_message_clean.split())
        
        best_intent = None
        best_score = 0.0
        
        # Compare with each intent's keywords
        for intent, keywords in self.intents.items():
            intent_words = set()
            for keyword in keywords:
                intent_words.update(keyword.split())
            
            # Calculate Jaccard similarity
            if intent_words and user_words:
                intersection = len(user_words & intent_words)
                union = len(user_words | intent_words)
                similarity = intersection / union if union > 0 else 0
                
                if similarity > best_score:
                    best_score = similarity
                    best_intent = intent
        
        # Return intent only if confidence is reasonable
        if best_score >= 0.15:
            return best_intent, best_score
        
        return None, 0.0
    
    def get_response(self, user_message):
        """
        Generate chatbot response based on user message
        Uses grammar checking and semantic understanding for complex queries
        """
        # Step 1: Check grammar and spelling
        grammar_result = self.check_grammar_and_correct(user_message)
        corrected_message = grammar_result['corrected']
        
        # Step 2: Extract meaning if query is complex
        meaning_result = self.extract_meaning_and_intent(user_message)
        
        # Step 3: Use corrected or original message
        user_message_clean = corrected_message.lower().strip()
        
        # Log complexity for debugging
        if meaning_result['complexity_score'] > 5:
            logger.info(f"Complex query detected (score: {meaning_result['complexity_score']:.2f}): {user_message}")
            logger.info(f"Extracted entities: {meaning_result['entities']}")
            logger.info(f"Key concepts: {meaning_result['noun_chunks']}")
        
        # PRIORITY 1: Search ChatbotTraining database first
        # This allows answers to be managed from admin panel
        db_answer, db_confidence, db_found = self.search_training_database(user_message_clean, confidence_threshold=0.2)
        if db_found and db_answer:
            logger.info(f"Found database answer for '{user_message}' with confidence {db_confidence}")
            return {
                "response": db_answer,
                "type": "database",
                "intent": "database_match",
                "confidence": db_confidence
            }
        
        # Check if user is asking about a specific time
        time_query = self.extract_time_from_message(user_message)
        if time_query:
            schedules = self.get_schedule_by_time(time_query)
            if schedules:
                response = f"📍 <b>What's happening at {time_query}?</b><br><br>"
                for sched in schedules:
                    response += f"⏰ <b>{sched['title']}</b><br>"
                    response += f"   🕐 {sched['start_time']} - {sched['end_time']}<br>"
                    response += f"   📝 {sched['description']}<br>"
                    if sched['event']:
                        response += f"   🎯 Event: {sched['event']}<br>"
                    if sched['is_break']:
                        response += f"   ☕ Break time<br>"
                    response += "<br>"
                return {
                    "response": response,
                    "type": "schedule",
                    "intent": "time_search",
                    "confidence": 0.95
                }
        
        # Try event search first for multi-word queries
        # This prevents words like "about" from being matched to website_info
        if len(user_message_clean.split()) >= 2:
            # Extract and search for event names
            search_query = self.extract_search_term(user_message) if 'tell' in user_message_clean or 'about' in user_message_clean else user_message_clean
            
            if search_query and len(search_query) > 1:
                events = self.search_event_by_name(search_query)
                
                if events:
                    response = f"🔍 <b>Information about '{search_query}'</b>:<br><br>"
                    for event in events:
                        response += f"✨ <b>{event['name']}</b><br>"
                        response += f"   📂 Type: {event['event_type']}<br>"
                        response += f"   📝 {event['description']}<br><br>"
                    
                    return {
                        "response": response,
                        "type": "search",
                        "intent": "search",
                        "confidence": 0.95
                    }
        
        # Use semantic understanding for intent
        intent, confidence = self.understand_intent(user_message_clean)
        
        # Fallback to keyword matching if semantic confidence is low
        if confidence < 0.3:
            intent = self._keyword_fallback(user_message_clean)
        
        # Generate response based on detected intent
        if intent == 'greeting':
            return {
                "response": f"Hello! 👋 I'm {self.name}, your {self.website_name} assistant. I can help you learn about NEC, AIDS Department, ARTIFA FEST, events, timeline, and more. What would you like to know?",
                "type": "greeting",
                "intent": intent,
                "confidence": confidence
            }
        
        elif intent == 'nec_info':
            return {
                "response": self.get_nec_info(),
                "type": "info",
                "intent": intent,
                "confidence": confidence
            }
        
        elif intent == 'aids_info':
            return {
                "response": self.get_aids_info(),
                "type": "info",
                "intent": intent,
                "confidence": confidence
            }
        
        elif intent == 'artifa_info':
            return {
                "response": self.get_artifa_info(),
                "type": "info",
                "intent": intent,
                "confidence": confidence
            }
        
        elif intent == 'website_info':
            info = self.get_website_info()
            return {
                "response": f"Welcome to {info['name']}! 🎉<br><br>"
                           f"📍 <b>College</b>: {info['college']}<br>"
                           f"📋 <b>Type</b>: {info['type']}<br>"
                           f"📝 <b>Description</b>: {info['description']}<br><br>"
                           f"I can tell you about our events, timeline, and more!",
                "type": "info",
                "intent": intent,
                "confidence": confidence
            }
        
        elif intent == 'timeline':
            timeline = self.get_timeline()
            if timeline:
                response = f"<i class='fas fa-calendar'></i> <b>Festival Timeline:</b><br>"
                for item in timeline[:5]:
                    response += f"<br><i class='fas fa-clock'></i> <b>{item['title']}</b><br>"
                    response += f"   <i class='fas fa-hourglass-start'></i> {item['start_time']} - {item['end_time']}<br>"
                    response += f"   <i class='fas fa-file-alt'></i> {item['description']}<br>"
                if len(timeline) > 5:
                    response += f"<br>... and {len(timeline) - 5} more events!"
                return {
                    "response": response,
                    "type": "timeline",
                    "intent": intent,
                    "confidence": confidence
                }
            else:
                return {
                    "response": "Timeline information will be available soon! <i class='fas fa-calendar'></i>",
                    "type": "timeline",
                    "intent": intent,
                    "confidence": confidence
                }
        
        elif intent == 'events':
            events = self.get_all_events()
            response = "<i class='fas fa-bullseye'></i> <b>All Events:</b><br>"
            if events:
                for event in events[:5]:
                    response += f"<br><i class='fas fa-star'></i> <b>{event['name']}</b> ({event['event_type']})<br>"
                    response += f"   {event['description']}<br>"
                if len(events) > 5:
                    response += f"<br>... and {len(events) - 5} more events!"
                return {
                    "response": response,
                    "type": "events",
                    "intent": intent,
                    "confidence": confidence
                }
            else:
                return {
                    "response": "No events found. <i class='fas fa-search'></i>",
                    "type": "events",
                    "intent": intent,
                    "confidence": confidence
                }
        
        elif intent == 'technical_events':
            events = self.get_events_by_category('technical')
            response = "<i class='fas fa-laptop'></i> <b>Technical Events:</b><br>"
            if events:
                for event in events[:5]:
                    response += f"<br><i class='fas fa-star'></i> <b>{event['name']}</b><br>"
                    response += f"   {event['description']}<br>"
                if len(events) > 5:
                    response += f"<br>... and {len(events) - 5} more events!"
                return {
                    "response": response,
                    "type": "events",
                    "intent": intent,
                    "confidence": confidence
                }
            else:
                return {
                    "response": "No technical events found. <i class='fas fa-search'></i>",
                    "type": "events",
                    "intent": intent,
                    "confidence": confidence
                }
        
        elif intent == 'nontechnical_events':
            events = self.get_events_by_category('non-technical')
            response = "<i class='fas fa-gamepad'></i> <b>Non-Technical Events:</b><br>"
            if events:
                for event in events[:5]:
                    response += f"<br><i class='fas fa-star'></i> <b>{event['name']}</b><br>"
                    response += f"   {event['description']}<br>"
                if len(events) > 5:
                    response += f"<br>... and {len(events) - 5} more events!"
                return {
                    "response": response,
                    "type": "events",
                    "intent": intent,
                    "confidence": confidence
                }
            else:
                return {
                    "response": "No non-technical events found. <i class='fas fa-search'></i>",
                    "type": "events",
                    "intent": intent,
                    "confidence": confidence
                }
        
        elif intent == 'registration_guide':
            return {
                "response": self.get_registration_guide(),
                "type": "guide",
                "intent": intent,
                "confidence": confidence
            }
        
        elif intent == 'team_guide':
            return {
                "response": self.get_team_guide(),
                "type": "guide",
                "intent": intent,
                "confidence": confidence
            }
        
        elif intent == 'view_team_guide':
            return {
                "response": self.get_view_team_guide(),
                "type": "guide",
                "intent": intent,
                "confidence": confidence
            }
        
        elif intent == 'navigation_guide':
            return {
                "response": self.get_navigation_guide(),
                "type": "guide",
                "intent": intent,
                "confidence": confidence
            }
        
        elif intent == 'profile_guide':
            return {
                "response": self.get_profile_guide(),
                "type": "guide",
                "intent": intent,
                "confidence": confidence
            }
        
        elif intent == 'help':
            return {
                "response": f"I can help you with:<br>"
                           f"<br><i class='fas fa-building'></i> <b>About NEC</b><br>"
                           f"   Ask 'Tell me about NEC'<br>"
                           f"<br><i class='fas fa-robot'></i> <b>About AIDS Department</b><br>"
                           f"   Ask 'What is AIDS?'<br>"
                           f"<br><i class='fas fa-party-horn'></i> <b>About ARTIFA FEST</b><br>"
                           f"   Ask 'Tell me about ARTIFA'<br>"
                           f"<br><i class='fas fa-bullseye'></i> <b>All Events</b><br>"
                           f"   Ask 'What are the events?'<br>"
                           f"<br><i class='fas fa-laptop'></i> <b>Technical Events</b><br>"
                           f"   Ask 'Show technical events'<br>"
                           f"<br><i class='fas fa-gamepad'></i> <b>Non-Technical Events</b><br>"
                           f"   Ask 'Show non-technical events'<br>"
                           f"<br><i class='fas fa-calendar'></i> <b>Timeline</b><br>"
                           f"   Ask 'What's the timeline?'<br>"
                           f"<br><i class='fas fa-search'></i> <b>Event Search</b><br>"
                           f"   Ask 'Search for [event name]'<br>"
                           f"<br><i class='fas fa-user-plus'></i> <b>Registration Guide</b><br>"
                           f"   Ask 'How to register?'<br>"
                           f"<br><i class='fas fa-users'></i> <b>Team Management</b><br>"
                           f"   Ask 'How to manage team?'<br>"
                           f"<br><i class='fas fa-eye'></i> <b>View Team Guide</b><br>"
                           f"   Ask 'How to view team?'<br>"
                           f"<br><i class='fas fa-map'></i> <b>Website Navigation</b><br>"
                           f"   Ask 'Guide me through website'<br>"
                           f"<br><i class='fas fa-user-cog'></i> <b>Profile Management</b><br>"
                           f"   Ask 'How to manage profile?'<br>"
                           f"<br><br>Feel free to ask me anything about {self.website_name}! <i class='fas fa-smile'></i>",
                "type": "help",
                "intent": intent,
                "confidence": confidence
            }
        
        # Default response
        return {
            "response": f"I'm {self.name}, your {self.website_name} guide! 👋\n"
                       f"\nI can tell you about:\n"
                       f"\n• 🏢 National Engineering College (NEC)\n"
                       f"• 🤖 Artificial Intelligence & Data Science Department\n"
                       f"• 🎉 ARTIFA FEST - Our intra-college festival\n"
                       f"• 🎯 Events and competitions\n"
                       f"• 📅 Festival timeline and schedule\n"
                       f"\nType 'help' to see all options or ask me anything! 😊",
            "type": "default",
            "intent": "unknown",
            "confidence": 0.0
        }
    
    def _keyword_fallback(self, user_message):
        """Fallback keyword-based intent matching"""
        keywords = {
            'greeting': ['hi', 'hello', 'hey', 'greetings', 'namaste'],
            'nec_info': ['nec', 'national engineering', 'college'],
            'aids_info': ['aids', 'artificial intelligence', 'data science', 'ai and ds'],
            'artifa_info': ['artifa', 'artifa fest', 'festival'],
            'website_info': ['website', 'about', 'info', 'information', 'what is'],
            'technical_events': ['technical', 'coding', 'programming', 'hackathon'],
            'nontechnical_events': ['non-technical', 'cultural', 'games', 'fun'],
            'timeline': ['timeline', 'schedule', 'when', 'time', 'timing'],
            'events': ['event', 'competition', 'activity', 'contest'],
            'help': ['help', 'what can', '?']
        }
        
        for intent, kw_list in keywords.items():
            if any(kw in user_message for kw in kw_list):
                return intent
        
        return None


# Create chatbot instance
chatbot = SweKeerChatbot()
