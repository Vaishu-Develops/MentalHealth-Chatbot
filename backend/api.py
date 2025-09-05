"""FastAPI backend for the mental health chatbot."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any

from backend.ai_service import GeminiAI
from backend.utils import detect_crisis_language, get_crisis_resources, sentiment_score
from backend.assessment import MentalHealthScreening

app = FastAPI()

# Initialize AI service
ai = GeminiAI()
assessment_tool = MentalHealthScreening()

class UserMessage(BaseModel):
    """User message model."""
    message: str
    session_id: str

class UserProfile(BaseModel):
    """User profile model."""
    age: int
    name: str
    goals: List[str]
    current_mood: str

class AssessmentRequest(BaseModel):
    """Assessment request model."""
    assessment_type: str
    responses: List[int]

@app.get("/health")
async def health():
    """Health check endpoint for deployment."""
    return {"status": "healthy", "service": "MindfulCompanion Backend"}

@app.post("/chat")
async def chat(user_message: UserMessage):
    """Process user message and return AI response."""
    # Check for crisis language
    is_crisis = detect_crisis_language(user_message.message)
    
    # Get AI response
    response = ai.get_response(user_message.message, is_crisis)
    
    # Calculate sentiment
    message_sentiment = sentiment_score(user_message.message)
    
    # Check if assessment should be suggested
    suggested_assessment = ai.suggest_assessment(ai.chat_history)
    
    result = {
        "response": response,
        "sentiment": message_sentiment,
        "is_crisis": is_crisis
    }
    
    if is_crisis:
        result["crisis_resources"] = get_crisis_resources()
    
    if suggested_assessment:
        if suggested_assessment == "phq9":
            result["suggested_assessment"] = {
                "type": "phq9",
                "name": "Depression Screening",
                "questions": assessment_tool.get_phq9_questions()
            }
        elif suggested_assessment == "gad7":
            result["suggested_assessment"] = {
                "type": "gad7",
                "name": "Anxiety Screening",
                "questions": assessment_tool.get_gad7_questions()
            }
    
    return result

@app.post("/set-profile")
async def set_profile(profile: UserProfile):
    """Set user profile information."""
    ai.set_user_profile(profile.dict())
    
    return {"status": "success", "message": "Profile updated successfully"}

@app.get("/phq9-questions")
async def get_phq9_questions():
    """Get PHQ-9 depression screening questions."""
    return {
        "questions": assessment_tool.get_phq9_questions()
    }

@app.get("/gad7-questions")
async def get_gad7_questions():
    """Get GAD-7 anxiety screening questions."""
    return {
        "questions": assessment_tool.get_gad7_questions()
    }

@app.post("/process-assessment")
async def process_assessment(assessment: AssessmentRequest):
    """Process mental health assessment responses."""
    score = sum(assessment.responses)
    
    if assessment.assessment_type == "phq9":
        interpretation = assessment_tool.interpret_phq9_score(score)
        strategies = assessment_tool.get_coping_strategies("phq9", score)
    elif assessment.assessment_type == "gad7":
        interpretation = assessment_tool.interpret_gad7_score(score)
        strategies = assessment_tool.get_coping_strategies("gad7", score)
    else:
        raise HTTPException(status_code=400, detail="Invalid assessment type")
    
    return {
        "score": score,
        "interpretation": interpretation,
        "strategies": strategies
    }
