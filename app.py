"""
Mental Health Screening & Support Chatbot
Streamlit Frontend Application
"""

import streamlit as st
import httpx
import time
import json
from datetime import datetime
import random
import os
from dotenv import load_dotenv
import asyncio
from contextlib import contextmanager

# Load environment variables
load_dotenv()

# Constants - Dynamic backend URL for deployment
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")  # FastAPI backend URL

# Simple performance monitoring
@contextmanager
def timer():
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        if 'performance_metrics' not in st.session_state:
            st.session_state.performance_metrics = []
        st.session_state.performance_metrics.append(end - start)

# Page configuration
st.set_page_config(
    page_title="MindfulCompanion",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# HTTP client with connection pooling and timeout
@st.cache_resource
def get_http_client():
    """Create a persistent HTTP client with connection pooling."""
    return httpx.Client(
        timeout=httpx.Timeout(5.0, connect=2.0),  # Faster timeouts for quicker responses
        limits=httpx.Limits(max_keepalive_connections=10, max_connections=20)
    )

# Load custom CSS only once
@st.cache_data
def load_css():
    """Load CSS with caching to avoid repeated file reads."""
    try:
        with open("static/styles.css", "r") as f:
            return f"<style>{f.read()}</style>"
    except FileNotFoundError:
        return "<style>/* CSS file not found */</style>"

# Initialize session state variables
def init_session_state():
    """Initialize all session state variables with proper defaults."""
    # Core state variables
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(random.randint(1000, 9999))
    if "user_profile_set" not in st.session_state:
        st.session_state.user_profile_set = False
    if "current_assessment" not in st.session_state:
        st.session_state.current_assessment = None
    if "assessment_responses" not in st.session_state:
        st.session_state.assessment_responses = []
    if "crisis_mode" not in st.session_state:
        st.session_state.crisis_mode = False
    if "breathing_exercise" not in st.session_state:
        st.session_state.breathing_exercise = False
    if "mood_history" not in st.session_state:
        st.session_state.mood_history = []
    
    # Performance monitoring
    if "performance_metrics" not in st.session_state:
        st.session_state.performance_metrics = []
    if "backend_status" not in st.session_state:
        st.session_state.backend_status = "unknown"
    if "health_check_counter" not in st.session_state:
        st.session_state.health_check_counter = 0
    
    # User profile
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {}
        
    # Form inputs for onboarding (to prevent widget ID errors)
    if "user_name" not in st.session_state:
        st.session_state.user_name = "Friend"
    if "user_age" not in st.session_state:
        st.session_state.user_age = 25
    if "user_goals" not in st.session_state:
        st.session_state.user_goals = ["General well-being"]
    if "user_mood" not in st.session_state:
        st.session_state.user_mood = "Neutral"

# Reset session state (for debugging/testing)
def reset_session_state():
    """Reset all session state variables to defaults."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()

# API client with timeout and error handling
def safe_api_call(endpoint, data=None, method="GET"):
    """Make API calls with proper error handling and loading indicators."""
    client = get_http_client()
    
    try:
        if method == "GET":
            response = client.get(f"{BACKEND_URL}/{endpoint}")
        else:
            response = client.post(f"{BACKEND_URL}/{endpoint}", json=data)
        
        if response.status_code == 200:
            st.session_state.backend_status = "connected"
            return response.json(), None
        else:
            st.session_state.backend_status = "connected"  # Connected but error response
            return None, f"API Error: {response.status_code}"
    except httpx.TimeoutException:
        st.session_state.backend_status = "disconnected"
        return None, "Request timed out. Please try again."
    except httpx.ConnectError:
        st.session_state.backend_status = "disconnected"
        return None, "Cannot connect to server. Please check if the backend is running."
    except Exception as e:
        st.session_state.backend_status = "disconnected"
        return None, f"Error: {str(e)}"

# Cached API calls for questions
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_assessment_questions(assessment_type):
    """Get assessment questions with caching."""
    endpoint = f"{assessment_type}-questions"
    data, error = safe_api_call(endpoint)
    if error:
        return None, error
    return data.get("questions", []), None

# User onboarding
def user_onboarding():
    st.markdown("## Welcome to MindfulCompanion 💙")
    st.markdown("I'm here to support your mental well-being. Let's get to know each other a bit first.")
    
    with st.form("user_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "What name would you like me to call you?", 
                value=st.session_state.user_name,
                key="input_user_name"
            )
            age = st.slider(
                "What's your age range?", 
                13, 80, 
                value=st.session_state.user_age,
                key="input_user_age"
            )
        
        with col2:
            goals = st.multiselect(
                "What are you looking for help with?",
                options=[
                    "Stress management",
                    "Anxiety relief",
                    "Mood tracking",
                    "Depression support",
                    "Coping strategies",
                    "Crisis support",
                    "General well-being"
                ],
                default=st.session_state.user_goals,
                key="input_user_goals"
            )
            
            st.markdown("#### Initial Mood Check")
            mood = st.select_slider(
                "How are you feeling right now?",
                options=["Very bad", "Bad", "Neutral", "Good", "Very good"],
                value=st.session_state.user_mood,
                key="input_user_mood"
            )
        
        st.markdown("#### Privacy Notice")
        st.info(
            "Your conversations are private. I'm here to support you, but I'm not a replacement for "
            "professional mental health care. If you're in crisis, please reach out to a mental health "
            "professional or crisis line."
        )
        
        submitted = st.form_submit_button("Start Chatting")
        
        if submitted:
            if name and goals:
                with st.spinner("Setting up your profile..."):
                    # Save user inputs to session state
                    st.session_state.user_name = name
                    st.session_state.user_age = age
                    st.session_state.user_goals = goals
                    st.session_state.user_mood = mood
                    
                    # Save profile to backend
                    profile_data = {
                        "name": name,
                        "age": age,
                        "goals": goals,
                        "current_mood": mood
                    }
                    
                    result, error = safe_api_call("set-profile", profile_data, "POST")
                    
                    if error:
                        st.error(f"Failed to save profile: {error}")
                        return
                    
                    # Add welcome message
                    welcome_message = f"Hi {name}! It's great to meet you. I'm here to support you with your mental well-being. How can I help you today?"
                    st.session_state.messages.append({"role": "assistant", "content": welcome_message, "time": datetime.now().strftime("%H:%M")})
                    
                    # Set session state
                    st.session_state.user_profile = profile_data
                    st.session_state.user_profile_set = True
                    st.session_state.mood_history.append({"mood": mood, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")})
                    
                    # Force page refresh by using a success message that will auto-clear
                    st.success("Profile saved! Welcome to your mental health journey!")
                    st.balloons()
                    # Session state change will trigger automatic rerun
            else:
                st.error("Please fill in your name and select at least one goal.")

# Display chat messages with performance optimization
def display_chat():
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display only the last 30 messages for performance
        recent_messages = st.session_state.messages[-30:] if len(st.session_state.messages) > 30 else st.session_state.messages
        
        for message in recent_messages:
            if message["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.write(f"{message['content']}")
            elif message["role"] == "assistant":
                with st.chat_message("assistant", avatar="💙"):
                    st.write(f"{message['content']}")
            elif message["role"] == "system":
                st.info(message["content"])
        
        # Show message count if there are more than 30 messages
        if len(st.session_state.messages) > 30:
            st.caption(f"Showing last 30 of {len(st.session_state.messages)} messages")

# Process and display assessment
def process_assessment(assessment_type, questions):
    st.markdown(f"## {assessment_type.upper()} Assessment")
    st.markdown("Please rate how often you've been bothered by the following problems over the last 2 weeks:")
    
    # Add back button
    if st.button("← Back to Chat"):
        st.session_state.current_assessment = None
        # Session state change will trigger automatic rerun
    
    responses = []
    
    for i, question in enumerate(questions):
        response = st.radio(
            f"{i+1}. {question}",
            options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
            key=f"q{i}",
            horizontal=True
        )
        
        # Convert response to score (0-3)
        score = ["Not at all", "Several days", "More than half the days", "Nearly every day"].index(response)
        responses.append(score)
    
    if st.button("Submit Assessment"):
        with st.spinner("Processing your assessment..."):
            assessment_data = {
                "assessment_type": assessment_type,
                "responses": responses
            }
            
            # API call to process assessment
            result, error = safe_api_call("process-assessment", assessment_data, "POST")
            
            if error:
                st.error(error)
                return
            
            # Display results
            st.session_state.current_assessment = None
            st.session_state.messages.append({
                "role": "system",
                "content": f"Assessment Result: {result['interpretation']} (Score: {result['score']})"
            })
            
            # Add strategies
            strategy_message = "Based on your responses, here are some strategies that might help:\n"
            for strategy in result["strategies"]:
                strategy_message += f"- {strategy}\n"
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": strategy_message,
                "time": datetime.now().strftime("%H:%M")
            })
            
            return  # Will automatically refresh on next run

# Breathing exercise
def breathing_exercise():
    st.markdown("## Breathing Exercise")
    st.markdown("Take a moment to breathe deeply and relax.")
    
    # Display breathing circle with CSS animation
    st.markdown(
        """
        <div class="breathing-circle"></div>
        <p style="text-align: center;">Breathe in as the circle expands...</p>
        <p style="text-align: center;">Breathe out as it contracts...</p>
        """, 
        unsafe_allow_html=True
    )
    
    if st.button("End Exercise"):
        st.session_state.breathing_exercise = False
        st.session_state.messages.append({
            "role": "assistant",
            "content": "I hope that breathing exercise helped you feel a bit more relaxed. Remember that you can come back to this technique anytime you need to center yourself.",
            "time": datetime.now().strftime("%H:%M")
        })
        return  # Will automatically refresh on next run

# Sidebar content
def display_sidebar():
    with st.sidebar:
        st.markdown("## MindfulCompanion 💙")
        st.markdown("A supportive AI companion for mental well-being")
        
        st.markdown("---")
        
        if st.session_state.user_profile_set:
            st.markdown(f"### Hello, {st.session_state.user_profile['name']}!")
            
            # Quick mood check
            st.markdown("### Quick Mood Check")
            mood_options = {
                "😔 Very Bad": -2,
                "🙁 Bad": -1,
                "😐 Neutral": 0,
                "🙂 Good": 1,
                "😊 Very Good": 2
            }
            
            cols = st.columns(5)
            for i, (mood, value) in enumerate(mood_options.items()):
                with cols[i]:
                    if st.button(mood, key=f"mood_{i}"):
                        st.session_state.mood_history.append({
                            "mood": mood.split(" ")[1],
                            "value": value,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                        st.session_state.messages.append({
                            "role": "system",
                            "content": f"You selected a mood: {mood}"
                        })
            
            # Tools
            st.markdown("### Tools")
            
            if st.button("Start Breathing Exercise"):
                st.session_state.breathing_exercise = True
                return  # Will automatically refresh on next run
            
            if st.button("Depression Screening (PHQ-9)"):
                with st.spinner("Loading assessment questions..."):
                    questions, error = get_assessment_questions("phq9")
                    if error:
                        st.error(error)
                    else:
                        st.session_state.current_assessment = {
                            "type": "phq9",
                            "questions": questions
                        }
                        return  # Will automatically refresh on next run
            
            if st.button("Anxiety Screening (GAD-7)"):
                with st.spinner("Loading assessment questions..."):
                    questions, error = get_assessment_questions("gad7")
                    if error:
                        st.error(error)
                    else:
                        st.session_state.current_assessment = {
                            "type": "gad7",
                            "questions": questions
                        }
                        return  # Will automatically refresh on next run
            
            st.markdown("---")
            
            # Crisis resources
            st.markdown("### Crisis Resources")
            st.markdown("""
            - **National Suicide Prevention Lifeline**: 1-800-273-8255
            - **Crisis Text Line**: Text HOME to 741741
            - **Emergency**: Call 911 (US) or local emergency services
            """)
        
        st.markdown("---")
        st.caption("This is an AI support tool, not a replacement for professional mental health care.")

# Health check function
def check_backend_health():
    """Check if backend is healthy and responsive."""
    try:
        client = get_http_client()
        response = client.get(f"{BACKEND_URL}/docs", timeout=2.0)
        if response.status_code == 200:
            st.session_state.backend_status = "connected"
            return True
    except:
        pass
    
    st.session_state.backend_status = "disconnected"
    return False

# Main app function
def main():
    # Initialize
    css_style = load_css()
    st.markdown(css_style, unsafe_allow_html=True)
    init_session_state()

    # Check backend health periodically (every 10 page loads)
    if 'health_check_counter' not in st.session_state:
        st.session_state.health_check_counter = 0

    st.session_state.health_check_counter += 1
    if st.session_state.health_check_counter % 10 == 1:
        check_backend_health()

    # Add a reset button in developer mode (hidden in sidebar footer)
    with st.sidebar:
        st.markdown("---")
        st.caption("Developer options:")
        if st.button("🔄 Reset App State", key="reset_app"):
            reset_session_state()
            return  # Will automatically refresh on next run

    # Display sidebar
    display_sidebar()

    # Main content
    if not st.session_state.user_profile_set:
        user_onboarding()
    else:
        if st.session_state.breathing_exercise:
            breathing_exercise()
        elif st.session_state.current_assessment:
            process_assessment(
                st.session_state.current_assessment["type"], 
                st.session_state.current_assessment["questions"]
            )
        else:
            # Chat input with immediate display using Streamlit's natural refresh cycle
            user_input = st.chat_input("Type your message here... (Press Enter to send)")

            # Handle new user input FIRST
            if user_input:
                # Add user message to state
                st.session_state.messages.append({
                    "role": "user", 
                    "content": user_input, 
                    "time": datetime.now().strftime("%H:%M")
                })
                # Force immediate rerun to show the user's message
                st.rerun()

            # Display chat messages
            display_chat()

            # Check if we need to process a response (when last message is user message and no processing flag)
            if (st.session_state.messages and 
                st.session_state.messages[-1]["role"] == "user" and 
                not st.session_state.get('processing_response', False)):

                # Set processing flag to prevent duplicate calls
                st.session_state.processing_response = True

                # Get the last user message
                last_user_message = st.session_state.messages[-1]["content"]

                # Send to backend and get response
                with st.spinner("🤔 Thinking..."):
                    with timer():
                        response, error = safe_api_call(
                            "chat", 
                            {"message": last_user_message, "session_id": st.session_state.session_id},
                            "POST"
                        )

                if error:
                    st.error(error)
                    # Add fallback message for offline mode
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "I'm having trouble connecting to my brain right now. Please try again in a moment, or if this persists, check that the backend server is running.",
                        "time": datetime.now().strftime("%H:%M")
                    })
                else:
                    # Check for crisis mode
                    if response.get("is_crisis", False):
                        st.session_state.crisis_mode = True

                    # Add assistant response
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response["response"],
                        "time": datetime.now().strftime("%H:%M")
                    })

                    # Check for suggested assessment
                    if "suggested_assessment" in response:
                        assessment = response["suggested_assessment"]
                        assessment_message = f"Would you like to take a quick {assessment['name']}? It can help me better understand what you're experiencing."
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": assessment_message,
                            "time": datetime.now().strftime("%H:%M")
                        })
                        st.session_state.current_assessment = {
                            "type": assessment["type"],
                            "questions": assessment["questions"]
                        }

                # Clear processing flag
                st.session_state.processing_response = False
                
                # Force rerun to show the assistant's response immediately
                st.rerun()

if __name__ == "__main__":
    main()
