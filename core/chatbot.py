"""
SweKeer Chatbot - AI Assistant for ARTIFA FEST Website
Enhanced with NLP, semantic understanding, and database-driven Q&A
Provides intelligent answers about NEC, AIDS Department, and ARTIFA FEST
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
    logger.warning("TextBlob not installed. Install with: pip install textblob")

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
    logger.warning("language-tool-python not installed. Install with: pip install language-tool-python")

# Try to import spaCy for advanced semantic understanding
try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
        SPACY_AVAILABLE = True
    except OSError:
        logger.warning("spaCy model not found.")
        nlp = None
        SPACY_AVAILABLE = False
except ImportError:
    SPACY_AVAILABLE = False
    nlp = None
    logger.warning("spaCy not installed. Install with: pip install spacy")


class SweKeerChatbot:
    """Main chatbot class for ARTIFA FEST with semantic understanding"""
    
    def __init__(self):
        self.name = "SweKeer"
        self.website_name = "ARTIFA FEST"
        self.college_name = "NEC - Department of AI & DS"
        
        # Protected words that should NOT be spell-corrected
        self.protected_words = {
            'nec': 'National Engineering College',
            'aids': 'Artificial Intelligence & Data Science',
            'ai': 'Artificial Intelligence',
            'ds': 'Data Science',
            'artifa': 'ARTIFA FEST',
            'fest': 'Festival',
            'covid': 'COVID',
            'html': 'HTML',
            'css': 'CSS',
            'js': 'JavaScript',
            'python': 'Python',
            'java': 'Java',
            'website': 'Website',
            'venue': 'Venue',
            'timing': 'Timing',
            'team': 'Team',
            'member': 'Member',
            'event': 'Event',
            'kovilpathi': 'Kovilpathi',
            'tamil': 'Tamil',
            'nadu': 'Nadu',
            'register': 'Register',
            'registration': 'Registration',
        }
        
        # Knowledge Base about NEC, AIDS, and ARTIFA FEST
        self.knowledge_base = {
            'nec': {
                'full_name': 'National Engineering College',
                'location': 'Kovilpathi, Tamil Nadu',
                'established': '1981',
                'about': [
                    'Premier engineering institution in South India',
                    'ISO 9001:2015 certified autonomous college',
                    'Top ranking in NIRF and other national rankings',
                    'Strong focus on academics, research, and innovation',
                    'Active placement record with top companies'
                ]
            },
            'aids': {
                'full_name': 'Department of Artificial Intelligence & Data Science',
                'established': '2020',
                'about': [
                    'Latest and most sought-after department at NEC',
                    'Offers BTech in AI & DS (4-year program)',
                    'Strong curriculum covering AI, ML, DL, NLP, Computer Vision',
                    'Excellent placement and higher studies opportunities',
                    'Active research in emerging technologies'
                ]
            },
            'artifa': {
                'full_name': 'ARTIFA FEST',
                'type': 'AI & DS Department Festival',
                'about': [
                    'Premier technical and non-technical event festival',
                    'Platform for showcasing talent and innovation',
                    'Attracts participants from multiple colleges',
                    'Opportunities for networking and learning',
                    'Multiple events covering coding, gaming, innovation, and more'
                ]
            }
        }

    def search_training_database(self, user_message, confidence_threshold=0.2):
        """
        Search ChatbotTraining database for matching answer using semantic similarity
        Optimized for short queries like acronyms
        Returns (answer, confidence, found) tuple
        """
        try:
            from core.models import ChatbotTraining
            
            user_msg_lower = user_message.lower().strip()
            user_words = set(user_msg_lower.split())
            
            training_pairs = ChatbotTraining.objects.filter(is_active=True)
            
            best_match = None
            best_confidence = 0
            
            # For very short queries (1-2 words), apply special handling
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
                
                # For short queries, boost keyword matching
                if is_short_query and keyword_similarity > 0:
                    keyword_similarity = min(1.0, keyword_similarity * 1.2)
                
                # Check 2: Question similarity using TF-IDF
                question_similarity = 0
                if SKLEARN_AVAILABLE:
                    try:
                        from sklearn.feature_extraction.text import TfidfVectorizer
                        from sklearn.metrics.pairwise import cosine_similarity
                        
                        vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', min_df=1)
                        vectors = vectorizer.fit_transform([user_msg_lower, pair.question.lower()])
                        question_similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
                    except Exception as e:
                        logger.debug(f"TF-IDF error: {e}")
                        # Fallback word overlap
                        pair_words = set(pair.question.lower().split())
                        if user_words and pair_words:
                            intersection = len(user_words & pair_words)
                            union = len(user_words | pair_words)
                            question_similarity = intersection / union if union > 0 else 0
                
                # Check 3: Intent matching
                intent_similarity = 0
                if pair.intent:
                    for word in user_words:
                        if word in pair.intent.lower():
                            intent_similarity = 0.3
                            break
                
                # Boost intent for short queries
                if is_short_query and intent_similarity > 0:
                    intent_similarity = 0.4
                
                # Combined confidence (weighted)
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

    def check_grammar_and_correct(self, user_message):
        """
        Check grammar and spelling with protected words
        Returns corrected message and error details
        """
        corrections = {
            'original': user_message,
            'corrected': user_message,
            'errors': [],
            'spell_check_available': False,
            'grammar_check_available': False
        }
        
        corrected_message = user_message
        
        # TextBlob spell correction
        if TEXTBLOB_AVAILABLE:
            try:
                blob = TextBlob(user_message)
                corrected = str(blob.correct())
                
                # Check if correction removes protected words
                user_lower = user_message.lower()
                corrected_lower = corrected.lower()
                
                protected_removed = False
                for protected in self.protected_words.keys():
                    if protected in user_lower and protected not in corrected_lower:
                        protected_removed = True
                        logger.debug(f"Skipping spell correction - would remove protected word: {protected}")
                        break
                
                if not protected_removed:
                    corrected_message = corrected
                    corrections['spell_check_available'] = True
                    
            except Exception as e:
                logger.debug(f"TextBlob correction error: {e}")
        
        # Language Tool grammar checking
        if LANGUAGE_TOOL_AVAILABLE and grammar_tool:
            try:
                matches = grammar_tool.check(corrected_message)
                if matches:
                    corrections['grammar_check_available'] = True
                    for match in matches[:5]:  # Limit to 5 errors
                        corrections['errors'].append({
                            'message': match.message,
                            'offset': match.offset,
                            'length': match.length
                        })
            except Exception as e:
                logger.debug(f"Grammar check error: {e}")
        
        corrections['corrected'] = corrected_message
        return corrections

    def extract_time_from_message(self, user_message):
        """Extract time from user message"""
        time_patterns = [
            r'(\d{1,2}):(\d{2})\s*(am|pm|AM|PM)',
            r'(\d{1,2})\s*(am|pm|AM|PM)',
            r'at\s*(\d{1,2})',
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, user_message.lower())
            if match:
                return user_message[match.start():match.end()]
        return None

    def get_schedule_by_time(self, time_query):
        """Get schedule information by time"""
        try:
            schedules = Schedule.objects.filter(
                Q(start_time__icontains=time_query) |
                Q(end_time__icontains=time_query)
            ).values()
            return list(schedules)
        except:
            return []

    def search_event_by_name(self, search_query):
        """Search events by name"""
        try:
            events = Event.objects.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(event_type__icontains=search_query)
            ).values()[:5]
            return list(events)
        except:
            return []

    def extract_search_term(self, user_message):
        """Extract search term from message"""
        patterns = [
            r'tell\s+me\s+about\s+([a-zA-Z\s]+)',
            r'what\s+(?:is|about)\s+([a-zA-Z\s]+)',
            r'search\s+(?:for\s+)?([a-zA-Z\s]+)',
            r'find\s+(?:me\s+)?([a-zA-Z\s]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_message.lower())
            if match:
                return match.group(1).strip()
        return user_message.strip()

    def understand_intent(self, user_message):
        """Understand user intent from message"""
        user_lower = user_message.lower()
        
        # Intent patterns
        intents = {
            'greeting': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good evening'],
            'nec_info': ['nec', 'college', 'engineering', 'institution', 'about nec'],
            'aids_info': ['aids', 'ai', 'data science', 'department', 'ds'],
            'artifa_info': ['artifa', 'fest', 'event', 'festival', 'competition'],
            'registration': ['register', 'registration', 'sign up', 'enroll'],
            'schedule': ['schedule', 'timeline', 'when', 'date', 'time'],
            'venue': ['venue', 'location', 'where', 'place', 'address'],
            'farewell': ['goodbye', 'bye', 'see you', 'exit', 'quit']
        }
        
        for intent, keywords in intents.items():
            if any(keyword in user_lower for keyword in keywords):
                return (intent, 0.7)
        
        return ('general', 0.3)

    def _keyword_fallback(self, user_message):
        """Fallback keyword matching"""
        user_lower = user_message.lower()
        
        if any(w in user_lower for w in ['nec', 'college', 'engineering']):
            return 'nec_info'
        elif any(w in user_lower for w in ['aids', 'ai', 'data science']):
            return 'aids_info'
        elif any(w in user_lower for w in ['artifa', 'fest', 'event']):
            return 'artifa_info'
        else:
            return 'general'

    def get_nec_info(self):
        """Get NEC information"""
        nec = self.knowledge_base['nec']
        response = f"<b>{nec['full_name']} (NEC)</b><br><br>"
        response += f"<b>Location:</b> {nec['location']}<br>"
        response += f"<b>Established:</b> {nec['established']}<br><br>"
        response += "<b>About:</b><br>"
        for point in nec['about']:
            response += f"• {point}<br>"
        return response

    def get_aids_info(self):
        """Get AIDS department information"""
        aids = self.knowledge_base['aids']
        response = f"<b>Department of {aids['full_name']}</b><br><br>"
        response += f"<b>Established:</b> {aids['established']}<br><br>"
        response += "<b>About:</b><br>"
        for point in aids['about']:
            response += f"• {point}<br>"
        return response

    def get_artifa_info(self):
        """Get ARTIFA information"""
        artifa = self.knowledge_base['artifa']
        response = f"<b>{artifa['full_name']}</b><br>"
        response += f"<b>Type:</b> {artifa['type']}<br><br>"
        response += "<b>About:</b><br>"
        for point in artifa['about']:
            response += f"• {point}<br>"
        return response

    def get_response(self, user_message):
        """
        Main method to get chatbot response
        Returns dict with response, type, intent, and confidence
        """
        if not user_message or len(user_message.strip()) == 0:
            return {
                "response": "Please ask me something! I'm here to help with NEC, AIDS Department, and ARTIFA FEST information.",
                "type": "error",
                "intent": "empty",
                "confidence": 0
            }
        
        # Step 1: Grammar and spelling check
        corrections = self.check_grammar_and_correct(user_message)
        corrected_message = corrections['corrected']
        user_message_clean = corrected_message.lower().strip()
        
        # PRIORITY 1: Search ChatbotTraining database first
        db_answer, db_confidence, db_found = self.search_training_database(user_message_clean, confidence_threshold=0.2)
        if db_found and db_answer:
            logger.info(f"Found database answer for '{user_message}' with confidence {db_confidence}")
            return {
                "response": db_answer,
                "type": "database",
                "intent": "database_match",
                "confidence": db_confidence
            }
        
        # Check for time-based queries
        time_query = self.extract_time_from_message(user_message)
        if time_query:
            schedules = self.get_schedule_by_time(time_query)
            if schedules:
                response = f"<b>What's happening at {time_query}?</b><br><br>"
                for sched in schedules:
                    response += f"<b>{sched.get('title', 'Event')}</b><br>"
                    response += f"Time: {sched.get('start_time')} - {sched.get('end_time')}<br>"
                    response += f"{sched.get('description', '')}<br><br>"
                return {
                    "response": response,
                    "type": "schedule",
                    "intent": "time_search",
                    "confidence": 0.95
                }
        
        # Try event search for multi-word queries
        if len(user_message_clean.split()) >= 2:
            search_query = self.extract_search_term(user_message)
            if search_query and len(search_query) > 1:
                events = self.search_event_by_name(search_query)
                if events:
                    response = f"<b>Information about '{search_query}':</b><br><br>"
                    for event in events:
                        response += f"<b>{event.get('name', 'Event')}</b><br>"
                        response += f"Type: {event.get('event_type', 'N/A')}<br>"
                        response += f"{event.get('description', '')}<br><br>"
                    return {
                        "response": response,
                        "type": "search",
                        "intent": "search",
                        "confidence": 0.95
                    }
        
        # Understand intent
        intent, confidence = self.understand_intent(user_message_clean)
        
        # Fallback to keyword matching if confidence is low
        if confidence < 0.3:
            intent = self._keyword_fallback(user_message_clean)
        
        # Generate response based on intent
        if intent == 'greeting':
            return {
                "response": f"Hello! I'm {self.name}, your {self.website_name} assistant. I can help you learn about NEC, AIDS Department, ARTIFA FEST, events, timeline, and more. What would you like to know?",
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
        
        elif intent == 'farewell':
            return {
                "response": "Thank you for using ARTIFA FEST Assistant! Feel free to ask anytime. Good luck with ARTIFA FEST!",
                "type": "farewell",
                "intent": intent,
                "confidence": confidence
            }
        
        else:
            return {
                "response": "I couldn't find a specific answer to that question. Try asking about NEC, AIDS Department, ARTIFA FEST, events, registration, or timeline. What would you like to know?",
                "type": "fallback",
                "intent": "unknown",
                "confidence": 0.1
            }


# Create global chatbot instance for use in views
chatbot = SweKeerChatbot()
