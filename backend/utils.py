"""Utility functions for the mental health chatbot."""

def sentiment_score(text):
    """
    Simple sentiment analysis function.
    Returns a score between -1 (negative) and 1 (positive).
    """
    # This is a very simplified version - in production, use a proper NLP model
    negative_words = ["sad", "depressed", "anxious", "worried", "hopeless", 
                      "stressed", "overwhelmed", "tired", "exhausted", "lonely"]
    positive_words = ["happy", "calm", "peaceful", "hopeful", "excited", 
                      "grateful", "relaxed", "confident", "loved", "supported"]
    
    text = text.lower()
    neg_count = sum(word in text for word in negative_words)
    pos_count = sum(word in text for word in positive_words)
    
    if neg_count == 0 and pos_count == 0:
        return 0
    
    return (pos_count - neg_count) / (pos_count + neg_count)

def detect_crisis_language(text):
    """
    Detects potential crisis keywords in text.
    Returns True if crisis language is detected.
    """
    crisis_keywords = [
        # Direct self-harm indicators
        "suicide", "kill myself", "end my life", "want to die", 
        "hurt myself", "self harm", "cutting myself", "no reason to live",
        
        # New patterns from examples
        "don't want to live like this anymore", "don't want to live anymore",
        "everything feels pointless", "everything is pointless",
        "people would be better off without me", "better off without me",
        "feel like I can't keep going", "can't keep going",
        "wish I could just disappear", "want to disappear",
        "no point in living", "life is meaningless",
        
        # Indirect but concerning patterns
        "give up completely", "nothing matters anymore",
        "tired of everything", "can't take it anymore",
        "world without me", "everyone hates me"
    ]
    
    text = text.lower()
    return any(keyword in text for keyword in crisis_keywords)

def get_crisis_resources():
    """Return crisis support resources for US and India."""
    return {
        "immediate": "If you're in immediate danger, please call emergency services immediately.",
        "us_resources": {
            "national_suicide_prevention": "988 (US National Suicide Prevention Lifeline)",
            "crisis_text": "Text HOME to 741741 (Crisis Text Line)",
            "online": "https://suicidepreventionlifeline.org/"
        },
        "india_resources": {
            "aasra": "91-9820466726 (Aasra - 24/7 suicide prevention)",
            "sneha": "91-44-24640050 (Sneha India - suicide prevention)",
            "sumaitri": "91-11-23389090 (Sumaitri - Delhi crisis helpline)",
            "online": "http://www.aasra.info/"
        },
        "message": "Please reach out to a trusted friend, family member, or mental health professional. You are not alone, and help is available. 🌸💕"
    }
