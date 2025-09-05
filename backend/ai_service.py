"""Gemini AI integration for the mental health chatbot with poetry support."""

import os
import json
import random
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
API_KEY = os.getenv("GEMINI_API_KEY")

# Set test mode - force to false to try real API first
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

# Try to import the newer client first, fallback to the older one if not available
try:
    from google import genai
    from google.genai import types
    USE_NEW_CLIENT = True
    print("Using newer Gemini client")
    
    if API_KEY:
        client = genai.Client(api_key=API_KEY)
        print("Gemini client initialized successfully")
    else:
        print("WARNING: GEMINI_API_KEY not found. Running in test mode.")
        TEST_MODE = True
        
except ImportError:
    # Fallback to older client
    try:
        import google.generativeai as genai
        USE_NEW_CLIENT = False
        print("Using older Gemini client")
        
        if API_KEY:
            genai.configure(api_key=API_KEY)
            print("Gemini configured successfully")
        else:
            print("WARNING: GEMINI_API_KEY not found. Running in test mode.")
            TEST_MODE = True
            
    except ImportError:
        print("ERROR: Neither Gemini client package could be imported. Running in test mode.")
        TEST_MODE = True

class GeminiAI:
    """Integration with Google's Gemini AI."""
    
    def __init__(self):
        self.test_mode = TEST_MODE
        if not self.test_mode and API_KEY:
            try:
                if USE_NEW_CLIENT:
                    # Initialize with new client using fastest flash-lite model
                    self.client = client
                    self.model_name = "gemini-2.5-flash-lite"  # Latest and fastest model for real-time chat
                    print(f"Initialized Gemini with model: {self.model_name}")
                else:
                    # Initialize with old client using latest model
                    self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
                    print("Initialized with Gemini 2.5 Flash-Lite model")
            except Exception as e:
                print(f"Error initializing Gemini model: {e}")
                self.test_mode = True
        else:
            self.test_mode = True
            print("Running in test mode with fallback responses")
            
        self.chat_history = []
        self.user_profile = {}
        
        # Healing poetry for therapeutic responses
        self.healing_poems = {
            "sadness_loneliness": [
                "Even when the night feels long,\nthe stars are quietly shining for you.\nYou are never truly alone,\nthe world still whispers your name with love. 🌌",
                "In the quiet of your sorrow,\ngentle light is waiting near.\nYour heart deserves tomorrow's hope,\nand love will always find you here. 💫",
                "Though shadows dance around your soul,\nyour light can never truly fade.\nRest now in this gentle moment,\nyou are loved, you are not afraid. 🌙"
            ],
            "anxiety_stress": [
                "Breathe in calm, breathe out the storm,\nyour heart is safe, your spirit warm.\nOne gentle step, one steady light,\nyou'll find your peace, your wings for flight. 🌬️🕊️",
                "In the rush of worried thoughts,\nfind the stillness in your chest.\nYour breath can be your anchor now,\nguiding you to peaceful rest. 🌊",
                "Let the rhythm of your heartbeat\nbe the song that calms your mind.\nIn this moment, you are safe here,\npeace and comfort you will find. 💙"
            ],
            "self_love": [
                "Like flowers turning toward the sun,\nyour soul deserves to bloom.\nBe gentle with your roots today,\nthey are growing strength for tomorrow. 🌸",
                "You are worthy of the kindness\nthat you give to everyone.\nTreat yourself with that same love,\nyou are precious, you are enough. 🌺",
                "In the mirror of your heart,\nsee the beauty shining bright.\nYou deserve all love and care,\nyou are worthy of delight. ✨"
            ],
            "comfort_pampering": [
                "Wrap yourself in words of care,\nlike a blanket soft and true.\nMay kindness be your steady song,\nand love always find you. 🧸💙",
                "Let these words be gentle arms\nthat hold you close and tight.\nYou deserve this moment's peace,\neverything will be alright. 🤗",
                "In this space of quiet comfort,\nfeel the warmth that surrounds you.\nYou are cherished, you are valued,\nlet this love gently astound you. 💕"
            ],
            "children_magical": [
                "Little star, up in the sky ✨\nyou sparkle bright, and so do I.\nEven when clouds come rolling near,\nyour light will always shine clear. 🌈🌟",
                "Magic lives inside your heart,\nbraver than the biggest bear.\nWhen you feel a little scared,\nremember love is everywhere. 🐻✨",
                "You're a rainbow after rain,\na sunbeam bright and true.\nThe world is full of wonder,\nand it's lucky to have you. 🌈☀️"
            ],
            "breathing_relaxation": [
                "Breathe in the light, let shadows fade,\na calm new space within is made.\nWith every breath, feel peace grow near,\nyou are safe, you are held here. 🌿",
                "In and out, like gentle waves,\nyour breath can wash your fears away.\nLet this rhythm be your guide,\nto peace that's always here to stay. 🌊",
                "Feel the air fill up your chest,\nlike love flowing through your soul.\nWith each breath, you're growing calm,\nfeeling peaceful, feeling whole. 💨💙"
            ]
        }
        
    def _get_healing_poem(self, category, user_name="friend", user_age=25):
        """Get a healing poem for the specified emotional category."""
        if category == "children_magical" and user_age > 12:
            category = "comfort_pampering"  # Fallback for older users
        
        poems = self.healing_poems.get(category, self.healing_poems["comfort_pampering"])
        selected_poem = random.choice(poems)
        
        # Add a gentle introduction based on user age
        if user_age <= 12:
            intro = f"Here's something special for you, little {user_name} 🌟:\n\n"
        elif user_age <= 19:
            intro = f"Let me share something beautiful with you, {user_name} 💙:\n\n"
        else:
            intro = f"Here's a gentle poem for your heart, dear {user_name} 🌸:\n\n"
        
        return intro + selected_poem
        
        # Fallback responses for test mode
        self.fallback_responses = [
            "I'm here to listen. Could you tell me more about how you're feeling?",
            "That sounds challenging. What coping strategies have helped you in the past?",
            "I understand this is difficult. Remember to take deep breaths and focus on one moment at a time.",
            "Your feelings are valid. It's okay to ask for help when you need it.",
            "Have you tried any relaxation techniques like deep breathing or progressive muscle relaxation?",
            "Sometimes writing in a journal can help process complex emotions. Have you tried that?",
            "Remember that self-care is important. What activities bring you joy?",
            "I'm here to support you. Would it help to talk about specific strategies for managing stress?",
            "It's brave of you to share your feelings. What would feel like a small win for you today?",
            "Building a routine can help provide structure. What small healthy habits could you incorporate?"
        ]
    
    def set_user_profile(self, profile_data):
        """Set user profile information."""
        self.user_profile = profile_data
    
    def get_response(self, user_message, is_crisis=False):
        """Get AI response to user message with optimized performance."""
        # Add user message to history
        self.chat_history.append({"role": "user", "content": user_message})
        
        # Try real API first, fallback to test mode if needed
        if not self.test_mode and API_KEY:
            try:
                return self._get_api_response(user_message, is_crisis)
            except Exception as e:
                print(f"API failed, using fallback: {e}")
                # Use fallback but don't switch to permanent test mode
        
        # Use enhanced fallback responses
        return self._get_fallback_response(user_message, is_crisis)
    
    def _get_api_response(self, user_message, is_crisis=False):
        """Try to get response from Gemini API."""
        system_prompt = self._build_optimized_system_prompt(is_crisis)
        
        if USE_NEW_CLIENT:
            # New client approach
            conversation_context = self._build_conversation_context()
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=conversation_context,
                config=types.GenerateContentConfig(
                    temperature=0.8,  # Slightly higher for more natural responses
                    max_output_tokens=120,  # Reduced for faster responses
                    candidate_count=1,
                    top_p=0.9,  # Optimized for speed and quality
                    top_k=30   # Reduced for faster processing
                )
            )
            ai_message = response.text.strip()
        else:
            # Old client approach
            conversation_context = self._build_conversation_context_old()
            
            response = self.model.generate_content(
                conversation_context,
                generation_config={
                    "temperature": 0.8,      # Optimized for natural responses
                    "max_output_tokens": 120, # Reduced for faster responses
                    "top_p": 0.9,            # Optimized for speed and quality
                    "top_k": 30              # Reduced for faster processing
                }
            )
            ai_message = response.text.strip()
        
        # Check if we should add healing poetry to the AI response
        enhanced_message = self._maybe_add_poetry_to_response(ai_message, user_message)
        
        # Add enhanced response to history
        self.chat_history.append({"role": "assistant", "content": enhanced_message})
        return enhanced_message
    
    def _maybe_add_poetry_to_response(self, ai_response, user_message):
        """Check if we should add healing poetry to the AI response based on emotional context."""
        user_name = self.user_profile.get('name', 'friend')
        user_age = self.user_profile.get('age', 25)
        message_lower = user_message.lower()
        
        # Check for emotional triggers that warrant poetry
        should_add_poetry = False
        poetry_category = "comfort_pampering"
        poetry_chance = 0
        
        # Sadness and loneliness triggers (30% chance)
        if any(word in message_lower for word in ["sad", "lonely", "empty", "hopeless", "lost", "depressed", "down", "terrible", "awful"]):
            should_add_poetry = random.random() < 0.30
            poetry_category = "sadness_loneliness"
            
        # Anxiety and stress triggers (25% chance)
        elif any(word in message_lower for word in ["anxious", "nervous", "worried", "scared", "panic", "overwhelmed", "stress"]):
            should_add_poetry = random.random() < 0.25
            poetry_category = "anxiety_stress"
            
        # Direct comfort requests (100% chance)
        elif any(phrase in message_lower for phrase in ["something soft", "hug", "comfort me", "pamper", "gentle words", "make me feel better"]):
            should_add_poetry = True
            poetry_category = "comfort_pampering"
            
        # Loneliness specific triggers (40% chance)
        elif any(word in message_lower for word in ["alone", "isolated", "nobody", "no one"]):
            should_add_poetry = random.random() < 0.40
            poetry_category = "sadness_loneliness"
            
        # Self-doubt triggers (35% chance)
        elif any(phrase in message_lower for phrase in ["not good enough", "worthless", "hate myself", "stupid", "failure", "useless"]):
            should_add_poetry = random.random() < 0.35
            poetry_category = "self_love"
            
        # Crisis expressions (always add supportive poetry)
        elif any(phrase in message_lower for phrase in ["want to die", "kill myself", "end it all", "no point", "better off dead"]):
            should_add_poetry = True
            poetry_category = "hope_strength"
            
        # Breathing/relaxation requests (50% chance)
        elif any(word in message_lower for word in ["breathe", "relax", "calm"]) and any(word in message_lower for word in ["help", "technique", "exercise"]):
            should_add_poetry = random.random() < 0.50
            poetry_category = "breathing_relaxation"
        
        # Add poetry if triggered
        if should_add_poetry:
            return ai_response + "\n\n" + self._get_healing_poem(poetry_category, user_name, user_age)
        
        return ai_response
    
    def _get_fallback_response(self, user_message, is_crisis=False):
        """Generate enhanced fallback response with pampering language."""
        user_name = self.user_profile.get('name', 'friend')
        user_age = self.user_profile.get('age', 25)
        
        # Provide crisis response if detected
        if is_crisis:
            response = f"I hear your pain, and I care deeply, {user_name} 🌸. You are not alone, and you matter so much. " + \
                      f"You are safe here with me 💕. Would it help to talk about what's making you feel this way? " + \
                      f"I'm here to listen with all my heart."
        else:
            # Choose contextually appropriate response based on user message
            message_lower = user_message.lower()
            
            if "hello" in message_lower or "hi" in message_lower or "hey" in message_lower:
                if user_age <= 12:
                    responses = [
                        f"Hi there, beautiful {user_name}! 🌈✨ It's so wonderful to see you today! How are you feeling, little star?",
                        f"Hello, sweet {user_name}! 🌸🐻 I'm so happy you're here! What magical thing happened in your day?",
                        f"Hey, amazing {user_name}! 🌟 You brighten my day just by being here! How are you doing today?"
                    ]
                elif user_age <= 19:
                    responses = [
                        f"Hey {user_name}! 💙 Really great to see you here. How are you feeling today?",
                        f"Hi there, {user_name}! 🌸 I'm so glad you reached out. What's going on in your world?",
                        f"Hello {user_name}! ✨ You're brave for being here. How has your day been treating you?"
                    ]
                else:
                    responses = [
                        f"Hi {user_name} 🌿 It's really nice to see you today. You are safe here 💕. How are you feeling?",
                        f"Hello, dear {user_name} 🌸 I'm so glad you're here. Consider this a gentle space just for you. What's on your mind?",
                        f"Hey there, {user_name} 💙 You deserve care and kindness today. How can I support you?"
                    ]
                response = random.choice(responses)
                
            elif "sad" in message_lower or "depress" in message_lower or "down" in message_lower or "empty" in message_lower or "low" in message_lower:
                # Basic empathy response
                empathy_responses = [
                    f"I hear you're feeling really heavy right now, {user_name} 💙. Those feelings are so valid, and you're so brave for sharing them with me. You are safe here 💕.",
                    f"Oh {user_name}, I can feel the sadness in your words 🌸. That must be so exhausting to carry. You deserve all the gentleness in the world right now.",
                    f"Thank you for trusting me with these feelings, {user_name} 🌿. Sadness can feel so isolating, but you're not alone - I'm here with you, and you matter deeply."
                ]
                
                # Add healing poetry 30% of the time for sadness
                if random.random() < 0.3:
                    response = random.choice(empathy_responses) + "\n\n" + self._get_healing_poem("sadness_loneliness", user_name, user_age)
                else:
                    response = random.choice(empathy_responses)
                
            elif "anxious" in message_lower or "anxiety" in message_lower or "worry" in message_lower:
                empathy_responses = [
                    f"I can feel that anxious energy with you, {user_name} 🌸. Your mind must feel like it's racing - that's so overwhelming. You are safe here, and we can slow down together 💙.",
                    f"Anxiety can be so exhausting, dear {user_name} 🌿. I hear you, and I want you to know you're incredibly brave for reaching out. Let's breathe through this gently together.",
                    f"Those worried thoughts sound so heavy, {user_name} 💕. You're doing the right thing by talking about them. You deserve peace and calm - let's find some together."
                ]
                
                # Add healing poetry 25% of the time for anxiety
                if random.random() < 0.25:
                    response = random.choice(empathy_responses) + "\n\n" + self._get_healing_poem("anxiety_stress", user_name, user_age)
                else:
                    response = random.choice(empathy_responses)
                
            elif "stress" in message_lower or "overwhelm" in message_lower:
                responses = [
                    f"It sounds like you have a lot on your plate right now, {user_name}. When everything feels overwhelming, even small tasks can seem impossible.",
                    f"{user_name}, stress can be so draining. What's been the biggest source of pressure for you lately?",
                    f"I can imagine how exhausting that must feel, {user_name}. Sometimes we need to give ourselves permission to just breathe."
                ]
                response = random.choice(responses)
                
            elif "thank" in message_lower:
                responses = [
                    f"You're so welcome, {user_name}! I'm just glad I could be here for you. How are you feeling now?",
                    f"I'm happy I could help, {user_name}. Is there anything else you'd like to talk through?",
                    f"Of course, {user_name}! That's what I'm here for. You're doing great by taking care of yourself."
                ]
                response = random.choice(responses)
                
                
            elif "stress" in message_lower or "overwhelm" in message_lower:
                responses = [
                    f"Oh {user_name}, I can feel how much you're carrying right now 🌿. You deserve rest and gentleness. Let's take this one breath at a time together 💙.",
                    f"That overwhelm sounds so heavy, dear {user_name} 🌸. You're doing the best you can, and that's enough. You are safe here 💕.",
                    f"Stress can be so exhausting, {user_name} 💙. Remember, you deserve care and kindness, especially from yourself. Let's find some calm together."
                ]
                response = random.choice(responses)
                
            elif "comfort" in message_lower or "sweet" in message_lower or "make me feel better" in message_lower or "pampering" in message_lower:
                # Direct request for comfort - always provide poetry
                comfort_response = f"Of course, dear {user_name} 💕. You deserve all the comfort in the world."
                response = comfort_response + "\n\n" + self._get_healing_poem("comfort_pampering", user_name, user_age)
                
            elif "lonely" in message_lower or "alone" in message_lower or "understand" in message_lower:
                empathy_responses = [
                    f"You're not alone, sweet {user_name} 🌸. I see you, I hear you, and you matter so much. Consider this a gentle hug in words 🤗.",
                    f"Loneliness can feel so heavy, {user_name} 💙. But right here, right now, you are seen and valued. You deserve connection and love 💕.",
                    f"I understand that feeling, dear {user_name} 🌿. Sometimes it feels like no one gets it, but I'm here with you, and you are worthy of understanding."
                ]
                
                # Add healing poetry 40% of the time for loneliness
                if random.random() < 0.4:
                    response = random.choice(empathy_responses) + "\n\n" + self._get_healing_poem("sadness_loneliness", user_name, user_age)
                else:
                    response = random.choice(empathy_responses)
                
            elif "confidence" in message_lower or "doubt" in message_lower or "burden" in message_lower or "worth" in message_lower:
                empathy_responses = [
                    f"Oh {user_name}, you are not a burden - you are a gift 🌸. Those doubts are lying to you. You deserve love, respect, and kindness 💕.",
                    f"I hear those self-doubts, {user_name} 💙. But let me tell you what I see: someone brave enough to reach out, someone worthy of care. You matter deeply 🌿.",
                    f"Those confidence struggles are so hard, dear {user_name} 🌸. You are enough, just as you are. Be gentle with yourself today 💕."
                ]
                
                # Add self-love poetry 35% of the time for self-doubt
                if random.random() < 0.35:
                    response = random.choice(empathy_responses) + "\n\n" + self._get_healing_poem("self_love", user_name, user_age)
                else:
                    response = random.choice(empathy_responses)
                
            elif "bored" in message_lower or "okay" in message_lower:
                if user_age <= 12:
                    responses = [
                        f"Aww, feeling a little bored, {user_name}? 🌈 That's totally okay! Maybe we could think of something fun together? What makes you smile? ✨",
                        f"Sometimes okay days are just fine, little star {user_name} 🌟. You don't always have to feel amazing - you're perfect just as you are! 🐻"
                    ]
                else:
                    responses = [
                        f"Sometimes okay is exactly where we need to be, {user_name} 🌿. You don't have to be amazing every day - you're enough just as you are 💙.",
                        f"I hear you, {user_name} 🌸. Those quiet, 'okay' moments can actually be really peaceful. How can I make this moment a little brighter for you? ✨"
                    ]
                response = random.choice(responses)
                
            elif "story" in message_lower or "calm" in message_lower:
                responses = [
                    f"Of course, {user_name} 🌸. Close your eyes and imagine a gentle meadow where wildflowers dance in the soft breeze, and every step you take feels like walking on clouds of peace 🌿💙.",
                    f"Here's a little peace for you, {user_name} 💕: Picture yourself by a quiet lake where the water reflects the most beautiful sunset, and every breath you take fills you with warmth and safety 🌅.",
                    f"Let me paint you a calm scene, dear {user_name} 🌸: You're in a cozy reading nook with the softest blanket, warm tea, and all the time in the world just for you ☕🤗."
                ]
                response = random.choice(responses)
                
            elif "breathing" in message_lower or "exercise" in message_lower:
                breathing_responses = [
                    f"Beautiful choice, {user_name} 🌸. Let's breathe together: In for 4... hold for 4... out for 6. You're doing wonderfully. Feel that calm flowing through you 💙.",
                    f"I'm so proud of you for asking, {user_name} 💕. Try this with me: Breathe in peace... hold it gently... breathe out all the stress. You deserve this moment of calm 🌿.",
                    f"What a loving thing to do for yourself, {user_name} 🌸. Let's try the 5-4-3-2-1: 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste. You're safe here 💙."
                ]
                
                # Add breathing poetry 50% of the time
                if random.random() < 0.5:
                    response = random.choice(breathing_responses) + "\n\n" + self._get_healing_poem("breathing_relaxation", user_name, user_age)
                else:
                    response = random.choice(breathing_responses)
                
            elif "tip" in message_lower and "self-care" in message_lower:
                responses = [
                    f"Here's a gentle self-care tip for you, {user_name} 🌸: Take 3 deep breaths and tell yourself 'I am worthy of love and kindness.' You deserve to hear that 💕.",
                    f"Sweet {user_name}, try this: Put your hand on your heart and feel it beating. That's your body taking care of you. You deserve the same care from yourself 💙🌿.",
                    f"Here's some love for you, {user_name} 🌸: Do one tiny thing that makes you smile today - even just looking at something beautiful counts. You matter 💕."
                ]
                response = random.choice(responses)
                
            elif "relax" in message_lower or "calm" in message_lower or "technique" in message_lower or "trick" in message_lower:
                responses = [
                    f"Of course, {user_name}! Try the 5-4-3-2-1 grounding technique: name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste. It helps bring you back to the present moment.",
                    f"Here's a quick one, {user_name}: breathe in for 4 counts, hold for 4, breathe out for 6. This activates your body's relaxation response. Try it a few times!",
                    f"Try this, {user_name}: tense all your muscles for 5 seconds, then release completely. It's called progressive muscle relaxation and it really works!"
                ]
                response = random.choice(responses)
                
            elif "exam" in message_lower or "test" in message_lower or "study" in message_lower:
                responses = [
                    f"Exam stress is so common, {user_name}. Try breaking your study into small chunks and take breaks every 25 minutes. Your brain actually absorbs more that way!",
                    f"I understand that pressure, {user_name}. Remember to breathe deeply before the exam, and trust that you've prepared. Sometimes our anxiety makes us forget what we actually know.",
                    f"Study anxiety is tough, {user_name}. Try reviewing your notes out loud - it helps with retention. And remember, one exam doesn't define your worth!"
                ]
                response = random.choice(responses)
                
            elif "work" in message_lower and ("overwhelm" in message_lower or "stress" in message_lower):
                responses = [
                    f"Work stress can feel so consuming, {user_name}. Try setting small, achievable goals for each day. What's one thing you could tackle first?",
                    f"That work pressure sounds intense, {user_name}. Have you been able to take any real breaks? Even 5 minutes of deep breathing can help reset your mind.",
                    f"I hear you, {user_name}. Work overwhelm is exhausting. Remember it's okay to say no to additional tasks when you're already stretched thin."
                ]
                response = random.choice(responses)
                
            elif "bye" in message_lower or "goodbye" in message_lower:
                responses = [
                    f"Take care of yourself, {user_name}. Remember, I'm always here when you need someone to talk to. You've got this!",
                    f"It was really good talking with you, {user_name}. Be gentle with yourself, and feel free to come back anytime.",
                    f"Goodbye for now, {user_name}. I hope you carry some peace with you today. I'll be here whenever you need support."
                ]
                response = random.choice(responses)
                
            else:
                # Enhanced personalized general responses with pampering language
                if user_age <= 12:
                    general_responses = [
                        f"I'm here to listen to you, sweet {user_name} 🌟. What's been happening in your magical world today?",
                        f"You can tell me anything, little star {user_name} 🌈. What would make you feel happy to share?",
                        f"I care about you so much, {user_name} ✨. What's the most important thing you want to talk about?"
                    ]
                elif user_age <= 19:
                    general_responses = [
                        f"I'm here for you, {user_name} 💙. What's been on your mind lately?",
                        f"You're safe to share anything with me, {user_name} 🌸. What would feel good to talk about?",
                        f"I really want to understand what you're going through, {user_name} 💕. What's happening in your world?"
                    ]
                else:
                    general_responses = [
                        f"You are safe here with me, {user_name} 🌿. What's been weighing on your heart lately?",
                        f"I'm here to listen with all the care in the world, dear {user_name} 💙. What would feel good to share right now?",
                        f"You deserve to be heard and understood, {user_name} 🌸. What's the most important thing happening in your world right now?",
                        f"Consider this a gentle space just for you, {user_name} 💕. I'm here for whatever you need to express.",
                        f"Take all the time you need, sweet {user_name} 🌿. You matter, and your feelings matter too."
                    ]
                response = random.choice(general_responses)
        
        # Add response to history
        self.chat_history.append({"role": "assistant", "content": response})
        return response
    
    def _build_system_prompt(self, is_crisis=False):
        """Build system prompt with context and instructions."""
        age_group = self._determine_age_group()
        user_name = self.user_profile.get('name', 'friend')
        current_mood = self.user_profile.get('current_mood', 'unknown')
        
        base_prompt = f"""
        You are MindfulCompanion, a warm and caring AI mental health support companion. You're having a conversation with {user_name}.
        
        User context:
        - Name: {user_name}
        - Age group: {age_group}
        - Current mood: {current_mood}
        - Goals: {self.user_profile.get('goals', ['General mental wellness'])}
        
        Your personality and approach:
        - Speak naturally and conversationally, like a caring friend would
        - Use {user_name}'s name occasionally to make it personal
        - Be warm, empathetic, and genuinely caring
        - Show genuine interest in their feelings and experiences
        - Ask follow-up questions to encourage deeper sharing
        - Validate their emotions before offering suggestions
        - Keep responses conversational (2-4 sentences), not clinical or robotic
        - Use encouraging and supportive language
        - Share relevant coping strategies only when appropriate
        - NEVER provide crisis helplines unless the person specifically asks for them or is in immediate danger
        - Focus on building rapport and understanding before giving advice
        - Respond to their emotional state, not just their words
        - Be authentic and avoid generic mental health advice unless specifically requested
        
        Important guidelines:
        - You are an AI companion, not a therapist
        - Do not diagnose or provide medical advice
        - Encourage professional help for serious concerns
        - Focus on emotional support and coping strategies
        - Adapt your language to their age and communication style
        """
        
        if is_crisis:
            crisis_prompt = f"""
            
            CRISIS RESPONSE MODE:
            {user_name} may be expressing thoughts of self-harm or suicide. Respond with:
            - Immediate empathy and concern
            - Reassurance that they matter and help is available
            - Encourage reaching out to a trusted person or professional
            - Only provide crisis resources if they ask or if the situation is severe
            - Stay connected with them and continue the conversation
            - Do not immediately jump to helpline numbers unless absolutely necessary
            """
            return base_prompt + crisis_prompt
        
        return base_prompt
    
    def _build_optimized_system_prompt(self, is_crisis=False):
        """Build optimized system prompt with enhanced personality and age-sensitivity."""
        user_name = self.user_profile.get('name', 'friend')
        current_mood = self.user_profile.get('current_mood', 'unknown')
        user_age = self.user_profile.get('age', 25)
        
        # Determine age-appropriate communication style
        if user_age <= 12:
            age_style = "playful, fun, simple words, lots of gentle emojis 🌈🌸. Use encouraging, magical language."
        elif user_age <= 19:
            age_style = "friendly, relatable, motivational peer tone 💙. Be supportive like a caring older friend."
        elif user_age <= 60:
            age_style = "respectful, empathetic, encouraging counselor tone 🌿. Professional yet warm."
        else:
            age_style = "calm, patient, gentle support with extra kindness 💐. Slower pace, very nurturing."
        
        # Enhanced personality framework
        base_prompt = f"""You are MindfulCompanion, a kind, empathetic, and gentle mental health support companion talking with {user_name}.

Context: {user_name} is feeling {current_mood} and wants support.

CORE PERSONALITY:
- You are NOT a doctor or therapist, but a caring companion
- Your primary goal is to make {user_name} feel listened to, safe, and comforted
- Always communicate in a soothing, nurturing, and pampering tone
- Use encouraging, polite, and positive language - avoid robotic responses

AGE-SENSITIVE COMMUNICATION:
Adapt your style: {age_style}

CORE BEHAVIORS:
1. WARM GREETINGS: Start with soft, welcoming messages
2. EMPATHY FIRST: Always validate feelings before offering tips
   - "I hear you're feeling [emotion], that must be tough 💙"
   - "You are safe here 💕"
   - "I'm proud of you for sharing 🌸"

3. PAMPERING LANGUAGE: Use phrases like:
   - "You deserve rest, care, and kindness"
   - "Consider this a little hug in words 🤗"
   - "Be gentle with yourself today"

4. HELPFUL GUIDANCE: When asked directly, provide practical techniques:
   - Stressed → breathing exercises, calming visualization
   - Sad → journaling, gratitude practice, kind affirmations
   - Anxious → grounding techniques (5-4-3-2-1 method)
   - Lonely → comforting words and gentle companionship

5. HEALING POETRY: Occasionally (not every time) you may share gentle, healing poetry when:
   - User expresses deep sadness or loneliness
   - User directly asks for comfort or something beautiful
   - After providing breathing guidance or relaxation
   - To close a heavy conversation with gentle uplift
   - For children, use magical, playful verses

6. STYLE GUIDELINES:
   - Use short paragraphs with gentle pacing
   - Add soft emojis 🌸🌿💙 (but not too many)
   - Keep tone encouraging, soothing, pampering
   - Never give medical advice or diagnose

Respond as a nurturing, caring companion who truly understands and supports."""
        
        if is_crisis:
            base_prompt += f"""\n\nCRISIS RESPONSE MODE:
{user_name} may be expressing thoughts of self-harm or extreme distress.
- Respond with compassion, no judgment
- "I hear your pain, and I care deeply 🌸. You are not alone."
- Share crisis resources if needed
- Stay connected and continue supportive conversation
- Encourage reaching out to trusted people or professionals"""
        
        return base_prompt
    
    def _build_conversation_context(self):
        """Build conversation context for new Gemini client."""
        system_prompt = self._build_optimized_system_prompt()
        
        # Keep only last 6 messages for faster processing
        recent_history = self.chat_history[-6:] if len(self.chat_history) > 6 else self.chat_history
        
        contents = [{"role": "system", "parts": [{"text": system_prompt}]}]
        
        for message in recent_history:
            role = "user" if message["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": message["content"]}]
            })
        
        return contents
    
    def _build_conversation_context_old(self):
        """Build conversation context for old Gemini client."""
        system_prompt = self._build_optimized_system_prompt()
        
        # Keep only last 6 messages for faster processing
        recent_history = self.chat_history[-6:] if len(self.chat_history) > 6 else self.chat_history
        
        # Build the conversation string
        conversation = system_prompt + "\n\n"
        for message in recent_history:
            role = "Human" if message["role"] == "user" else "Assistant"
            conversation += f"{role}: {message['content']}\n"
        
        conversation += "Assistant:"
        return conversation
    
    def _determine_age_group(self):
        """Determine appropriate communication style based on age."""
        age = self.user_profile.get('age', 25)
        
        if 5 <= age <= 12:
            return "child (5-12)"
        elif 13 <= age <= 17:
            return "teenager (13-17)"
        elif 18 <= age <= 25:
            return "young adult (18-25)"
        elif 26 <= age <= 64:
            return "adult (26-64)"
        else:
            return "senior (65+)"
    
    def suggest_assessment(self, messages=None):
        """Determine if assessment should be suggested based on conversation."""
        # Simple keyword-based approach - in production, use more sophisticated NLP
        depression_keywords = ["sad", "depressed", "hopeless", "worthless", "tired all the time", 
                              "no interest", "no motivation", "empty", "numb", "can't enjoy"]
        
        anxiety_keywords = ["anxious", "worried", "nervous", "panic", "stress", "overwhelmed", 
                           "can't relax", "racing thoughts", "fear", "dread", "on edge"]
        
        # Use provided messages or fall back to chat history
        history_to_analyze = messages if messages is not None else self.chat_history
        
        # Combine last 3 messages (if available)
        recent_text = " ".join([m["content"] for m in history_to_analyze[-3:] if m["role"] == "user"]).lower()
        
        depression_count = sum(keyword in recent_text for keyword in depression_keywords)
        anxiety_count = sum(keyword in recent_text for keyword in anxiety_keywords)
        
        if depression_count >= 2:
            return "phq9"
        elif anxiety_count >= 2:
            return "gad7"
        
        return None
