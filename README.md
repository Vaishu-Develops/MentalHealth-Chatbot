# MindfulCompanion Chatbot 💙

A supportive AI companion for mental well-being with healing poetry integration.

## Features

- 🤖 **AI-Powered Conversations** using Google Gemini 2.5 Flash-Lite
- 🌸 **Healing Poetry** triggered by emotional context
- 👤 **Age-Sensitive Responses** (children, teens, adults, seniors)
- 🆘 **Crisis Detection** with immediate support resources
- 📝 **Mental Health Assessments** (PHQ-9, GAD-7)
- 🌬️ **Breathing Exercises** and relaxation techniques

## Deployment to Streamlit Cloud

### Step 1: Prepare Your Repository

1. Push your code to GitHub (make sure all files are committed)
2. Ensure `requirements.txt` includes all dependencies
3. Use `app_deploy.py` as your main Streamlit app

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `YourUsername/MentalHealth-Chatbot`
5. Set main file path: `app_deploy.py`
6. Click "Deploy!"

### Step 3: Configure Secrets

1. In your Streamlit Cloud app dashboard, go to "Settings" → "Secrets"
2. Add your environment variables in TOML format:

```toml
GEMINI_API_KEY = "your_actual_api_key_here"
TEST_MODE = "false"
```

### Step 4: Test Your Deployment

Your app will be available at: `https://your-app-name.streamlit.app`

## Local Development

To run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the app
streamlit run app_deploy.py
```

## Poetry System

The chatbot includes an advanced healing poetry system that triggers based on emotional context:

- **Sadness/Loneliness**: 30% chance of poetry
- **Anxiety/Stress**: 25% chance of poetry  
- **Direct Comfort Requests**: 100% chance of poetry
- **Self-Doubt**: 35% chance of poetry
- **Crisis Situations**: Always includes supportive poetry

## Crisis Support

The app includes automatic crisis detection and provides immediate access to:
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741
- KIRAN Helpline (India): 1800-599-0019

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
