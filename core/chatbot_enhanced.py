"""
Enhanced Chatbot Integration with Deep Learning Option
Integrates deep learning semantic matching into existing chatbot system
Falls back gracefully when deep learning libraries unavailable
"""

import logging

logger = logging.getLogger(__name__)

# Try advanced deep learning approach
DEEP_LEARNING_AVAILABLE = False
try:
    from sentence_transformers import SentenceTransformer, util
    import torch
    DEEP_LEARNING_AVAILABLE = True
    logger.info("Deep Learning (Sentence Transformers) available")
except ImportError as e:
    logger.warning(f"Deep Learning not available: {e}")
    DEEP_LEARNING_AVAILABLE = False


def find_answer_with_deep_learning(user_question, qa_pairs=None, confidence_threshold=0.3):
    """
    Find answer using deep learning semantic embeddings
    Returns (answer, confidence, intent) or (None, 0, None) if DL not available
    """
    if not DEEP_LEARNING_AVAILABLE or not qa_pairs:
        return (None, 0, None)
    
    try:
        from sentence_transformers import SentenceTransformer, util
        
        # Load the model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Encode user question
        user_embedding = model.encode(user_question, convert_to_tensor=True)
        
        best_answer = None
        best_confidence = 0
        best_intent = None
        
        # Encode all questions and find best match
        questions = [qa['question'] for qa in qa_pairs]
        qa_embeddings = model.encode(questions, convert_to_tensor=True)
        
        # Calculate cosine similarity
        similarities = util.pytorch_cos_sim(user_embedding, qa_embeddings)[0]
        
        # Find best match
        best_idx = similarities.argmax().item()
        best_similarity = similarities[best_idx].item()
        
        if best_similarity >= confidence_threshold:
            best_qa = qa_pairs[best_idx]
            
            # Boost with keyword matching
            keyword_boost = 0
            if best_qa.get('keywords'):
                keywords = [k.strip().lower() for k in best_qa['keywords'].split(',')]
                user_lower = user_question.lower()
                matched = sum(1 for kw in keywords if kw in user_lower)
                keyword_boost = (matched / len(keywords)) * 0.15
            
            final_confidence = min(1.0, best_similarity + keyword_boost)
            
            logger.info(f"Deep Learning match: similarity={best_similarity:.3f}, final_confidence={final_confidence:.3f}")
            return (best_qa['answer'], round(final_confidence, 2), best_qa.get('intent'))
        
        return (None, 0, None)
    
    except Exception as e:
        logger.error(f"Deep learning error: {e}")
        return (None, 0, None)


def enhance_chatbot_with_dl(question):
    """
    Enhanced response generation using deep learning understanding
    """
    try:
        from core.models import ChatbotTraining
        
        # Get all active Q&A pairs
        qa_pairs = list(
            ChatbotTraining.objects.filter(is_active=True).values(
                'id', 'question', 'answer', 'intent', 'keywords'
            )
        )
        
        if not qa_pairs:
            logger.warning("No Q&A pairs available for deep learning")
            return None
        
        # Try deep learning first
        answer, confidence, intent = find_answer_with_deep_learning(
            question, 
            qa_pairs=qa_pairs, 
            confidence_threshold=0.3
        )
        
        if answer and confidence >= 0.3:
            return {
                'answer': answer,
                'confidence': confidence,
                'intent': intent,
                'model': 'deep_learning'
            }
        
        # Fallback to traditional method
        from core.models import ChatbotTraining
        answer, confidence, pair = ChatbotTraining.find_answer(question, confidence_threshold=0.2)
        
        if answer:
            return {
                'answer': answer,
                'confidence': confidence,
                'intent': pair.intent if pair else None,
                'model': 'traditional'
            }
        
        return None
    
    except Exception as e:
        logger.error(f"Error in enhanced chatbot: {e}")
        return None


def get_intelligent_response(user_message):
    """
    Get intelligent response with deep learning fallback
    Returns structured response dict
    """
    if not user_message or len(user_message.strip()) == 0:
        return {
            "response": "Please ask me something! I'm here to help with NEC, AIDS Department, and ARTIFA FEST.",
            "type": "error",
            "confidence": 0,
            "model": "none"
        }
    
    # Try enhanced approach
    result = enhance_chatbot_with_dl(user_message)
    
    if result:
        return {
            "response": result['answer'],
            "type": "answer",
            "intent": result['intent'],
            "confidence": result['confidence'],
            "model": result['model']
        }
    
    # No match found
    return {
        "response": "I couldn't find a specific answer. Try asking about: NEC, AIDS Department, ARTIFA FEST events, registration, schedule, or team management.",
        "type": "fallback",
        "intent": None,
        "confidence": 0,
        "model": "none"
    }
