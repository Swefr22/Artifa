"""
Enhanced Chatbot with Deep Learning
Uses Sentence Transformers for semantic understanding of questions and answers
Provides state-of-the-art semantic similarity matching
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artifa_fest.settings')
django.setup()

import logging
import numpy as np
from django.db.models import Q
from core.models import ChatbotTraining, Event, Schedule

logger = logging.getLogger(__name__)

# Try to import deep learning libraries
try:
    from sentence_transformers import SentenceTransformer, util
    SENTENCE_TRANSFORMER_AVAILABLE = True
    logger.info("Sentence Transformers available - using deep learning embeddings")
except ImportError:
    SENTENCE_TRANSFORMER_AVAILABLE = False
    logger.warning("Sentence Transformers not available. Install with: pip install sentence-transformers")

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logger.warning("PyTorch not available. Install with: pip install torch")

try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("Transformers not available. Install with: pip install transformers")


class DeepLearningChatbot:
    """Advanced chatbot using deep learning for semantic understanding"""
    
    def __init__(self):
        self.name = "SweKeer-DL"
        self.website_name = "ARTIFA FEST"
        self.college_name = "NEC - Department of AI & DS"
        
        # Initialize embedding model
        self.embedding_model = None
        self.intent_classifier = None
        self.qa_embeddings_cache = {}
        
        if SENTENCE_TRANSFORMER_AVAILABLE:
            try:
                # Load pre-trained sentence transformer model
                # all-MiniLM-L6-v2 is lightweight and fast
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("Loaded Sentence Transformer model: all-MiniLM-L6-v2")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                self.embedding_model = None
        
        # Precompute embeddings for all active Q&A pairs
        self._precompute_embeddings()
    
    def _precompute_embeddings(self):
        """Precompute embeddings for all active Q&A pairs"""
        if not self.embedding_model:
            logger.warning("Embedding model not available, skipping precomputation")
            return
        
        try:
            active_pairs = ChatbotTraining.objects.filter(is_active=True)
            total = active_pairs.count()
            
            logger.info(f"Precomputing embeddings for {total} Q&A pairs...")
            
            questions = [pair.question for pair in active_pairs]
            
            # Batch encode for efficiency
            embeddings = self.embedding_model.encode(questions, convert_to_tensor=True, batch_size=32)
            
            # Cache embeddings with their corresponding pairs
            for idx, pair in enumerate(active_pairs):
                self.qa_embeddings_cache[pair.id] = {
                    'question': pair.question,
                    'answer': pair.answer,
                    'intent': pair.intent,
                    'keywords': pair.keywords,
                    'embedding': embeddings[idx]
                }
            
            logger.info(f"Successfully precomputed embeddings for {len(self.qa_embeddings_cache)} pairs")
        
        except Exception as e:
            logger.error(f"Error precomputing embeddings: {e}")
            self.qa_embeddings_cache = {}
    
    def find_answer_deep_learning(self, user_question, confidence_threshold=0.3):
        """
        Find answer using deep learning semantic similarity
        Returns (answer, confidence, intent) tuple
        """
        if not self.embedding_model or not self.qa_embeddings_cache:
            logger.warning("Deep learning model or embeddings not available, using fallback")
            return (None, 0, None)
        
        try:
            # Encode user question
            user_embedding = self.embedding_model.encode(user_question, convert_to_tensor=True)
            
            best_answer = None
            best_confidence = 0
            best_intent = None
            
            # Compare with cached Q&A embeddings
            for pair_id, cached_data in self.qa_embeddings_cache.items():
                qa_embedding = cached_data['embedding']
                
                # Calculate cosine similarity (0 to 1)
                similarity = util.pytorch_cos_sim(user_embedding, qa_embedding).item()
                
                # Boost confidence if keywords match
                keyword_boost = 0
                if cached_data['keywords']:
                    keywords = [k.strip().lower() for k in cached_data['keywords'].split(',')]
                    user_lower = user_question.lower()
                    matched = sum(1 for kw in keywords if kw in user_lower)
                    keyword_boost = (matched / len(keywords)) * 0.15  # 15% boost max
                
                # Final confidence
                confidence = min(1.0, similarity + keyword_boost)
                
                if confidence > best_confidence and confidence >= confidence_threshold:
                    best_confidence = confidence
                    best_answer = cached_data['answer']
                    best_intent = cached_data['intent']
            
            if best_answer:
                logger.info(f"Deep learning match for '{user_question}' with confidence {best_confidence:.3f}")
                return (best_answer, round(best_confidence, 2), best_intent)
            
            return (None, 0, None)
        
        except Exception as e:
            logger.error(f"Error in deep learning matching: {e}")
            return (None, 0, None)
    
    def get_semantic_intent(self, user_question):
        """Determine intent using semantic understanding"""
        intent_keywords = {
            'nec_info': ['nec', 'college', 'engineering', 'institution', 'infrastructure', 'department', 'campus'],
            'aids_info': ['aids', 'ai', 'data science', 'ml', 'machine learning', 'artificial intelligence'],
            'artifa_info': ['artifa', 'fest', 'event', 'festival', 'competition', 'tournament'],
            'registration': ['register', 'sign up', 'enroll', 'join', 'participant'],
            'schedule': ['schedule', 'timeline', 'when', 'date', 'time', 'timing'],
            'venue': ['venue', 'location', 'where', 'place', 'address', 'kovilpathi'],
            'team': ['team', 'member', 'leader', 'group', 'participants'],
            'event_rules': ['rules', 'regulation', 'guideline', 'policy', 'requirement'],
        }
        
        user_lower = user_question.lower()
        best_intent = None
        best_score = 0
        
        # Semantic matching with keyword boost
        for intent, keywords in intent_keywords.items():
            matches = sum(1 for kw in keywords if kw in user_lower)
            score = matches / len(keywords) if keywords else 0
            
            if score > best_score:
                best_score = score
                best_intent = intent
        
        return best_intent or 'general', best_score
    
    def enhance_understanding(self, user_question):
        """
        Enhanced understanding combining multiple techniques
        Returns enriched context dict
        """
        context = {
            'original': user_question,
            'lower': user_question.lower(),
            'words': set(user_question.lower().split()),
            'length': len(user_question.split()),
            'semantic_intent': None,
            'intent_confidence': 0,
            'is_short_query': len(user_question.split()) <= 2,
        }
        
        # Get semantic intent
        intent, conf = self.get_semantic_intent(user_question)
        context['semantic_intent'] = intent
        context['intent_confidence'] = conf
        
        return context
    
    def get_response(self, user_message):
        """
        Main response method using deep learning
        Returns dict with response, type, intent, and confidence
        """
        if not user_message or len(user_message.strip()) == 0:
            return {
                "response": "Please ask me something! I'm here to help with NEC, AIDS Department, and ARTIFA FEST.",
                "type": "error",
                "intent": "empty",
                "confidence": 0,
                "model": "deep_learning"
            }
        
        # Enhance understanding
        context = self.enhance_understanding(user_message)
        
        # PRIORITY 1: Deep learning semantic search
        if self.embedding_model:
            # Lower threshold for short queries
            threshold = 0.25 if context['is_short_query'] else 0.3
            answer, confidence, intent = self.find_answer_deep_learning(user_message, confidence_threshold=threshold)
            
            if answer and confidence >= threshold:
                logger.info(f"Deep learning answer found: confidence={confidence}, intent={intent}")
                return {
                    "response": answer,
                    "type": "deep_learning",
                    "intent": intent or context['semantic_intent'],
                    "confidence": confidence,
                    "model": "sentence_transformer"
                }
        
        # FALLBACK: Database search with traditional method
        try:
            from core.models import ChatbotTraining
            answer, db_confidence, pair = ChatbotTraining.find_answer(user_message, confidence_threshold=0.2)
            
            if answer:
                logger.info(f"Traditional database match: confidence={db_confidence}")
                return {
                    "response": answer,
                    "type": "database",
                    "intent": pair.intent if pair else context['semantic_intent'],
                    "confidence": db_confidence,
                    "model": "traditional"
                }
        except Exception as e:
            logger.error(f"Fallback database search error: {e}")
        
        # No match found
        return {
            "response": "I couldn't find a specific answer, but I can help with: NEC information, AIDS Department details, ARTIFA FEST events, registration, schedule, and team management. What would you like to know?",
            "type": "fallback",
            "intent": context['semantic_intent'],
            "confidence": 0,
            "model": "none"
        }


# Create global instance
try:
    chatbot_dl = DeepLearningChatbot()
    logger.info("Deep Learning Chatbot initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Deep Learning Chatbot: {e}")
    chatbot_dl = None
