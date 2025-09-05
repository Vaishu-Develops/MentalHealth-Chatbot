"""Mental health assessment tools."""

class MentalHealthScreening:
    """Mental health screening tools and questionnaires."""
    
    @staticmethod
    def get_phq9_questions():
        """Return the PHQ-9 depression screening questionnaire."""
        return [
            "Little interest or pleasure in doing things?",
            "Feeling down, depressed, or hopeless?",
            "Trouble falling or staying asleep, or sleeping too much?",
            "Feeling tired or having little energy?",
            "Poor appetite or overeating?",
            "Feeling bad about yourself - or that you are a failure or have let yourself or your family down?",
            "Trouble concentrating on things, such as reading the newspaper or watching television?",
            "Moving or speaking so slowly that other people could have noticed? Or so fidgety or restless that you have been moving a lot more than usual?",
            "Thoughts that you would be better off dead, or thoughts of hurting yourself in some way?"
        ]
    
    @staticmethod
    def get_gad7_questions():
        """Return the GAD-7 anxiety screening questionnaire."""
        return [
            "Feeling nervous, anxious, or on edge?",
            "Not being able to stop or control worrying?",
            "Worrying too much about different things?",
            "Trouble relaxing?",
            "Being so restless that it's hard to sit still?",
            "Becoming easily annoyed or irritable?",
            "Feeling afraid as if something awful might happen?"
        ]
    
    @staticmethod
    def interpret_phq9_score(score):
        """Interpret PHQ-9 score."""
        if score <= 4:
            return "Minimal depression"
        elif score <= 9:
            return "Mild depression"
        elif score <= 14:
            return "Moderate depression"
        elif score <= 19:
            return "Moderately severe depression"
        else:
            return "Severe depression"
    
    @staticmethod
    def interpret_gad7_score(score):
        """Interpret GAD-7 score."""
        if score <= 4:
            return "Minimal anxiety"
        elif score <= 9:
            return "Mild anxiety"
        elif score <= 14:
            return "Moderate anxiety"
        else:
            return "Severe anxiety"
    
    @staticmethod
    def get_coping_strategies(assessment_type, severity):
        """Return coping strategies based on assessment type and severity."""
        strategies = {
            "depression": {
                "mild": [
                    "Try to maintain a regular daily routine",
                    "Get regular exercise, even if it's just a short walk",
                    "Connect with friends or family members",
                    "Practice gratitude by noting things you're thankful for"
                ],
                "moderate": [
                    "Consider speaking with a mental health professional",
                    "Try mindfulness meditation to stay present",
                    "Set small, achievable goals each day",
                    "Limit consumption of news and social media"
                ],
                "severe": [
                    "Please consider reaching out to a mental health professional",
                    "Speak with your doctor about treatment options",
                    "Focus on basic self-care: sleep, nutrition, and rest",
                    "Remember that severe symptoms can improve with proper support"
                ]
            },
            "anxiety": {
                "mild": [
                    "Practice deep breathing exercises",
                    "Try progressive muscle relaxation",
                    "Limit caffeine and alcohol",
                    "Get regular physical activity"
                ],
                "moderate": [
                    "Consider speaking with a mental health professional",
                    "Practice mindfulness meditation",
                    "Create a worry schedule to contain anxious thoughts",
                    "Try journaling about your concerns"
                ],
                "severe": [
                    "Please consider reaching out to a mental health professional",
                    "Speak with your doctor about treatment options",
                    "Practice grounding techniques when feeling overwhelmed",
                    "Remember that severe anxiety can be effectively treated"
                ]
            }
        }
        
        if assessment_type == "phq9":
            if severity <= 4:
                return strategies["depression"]["mild"]
            elif severity <= 14:
                return strategies["depression"]["moderate"]
            else:
                return strategies["depression"]["severe"]
        elif assessment_type == "gad7":
            if severity <= 4:
                return strategies["anxiety"]["mild"]
            elif severity <= 14:
                return strategies["anxiety"]["moderate"]
            else:
                return strategies["anxiety"]["severe"]
        
        return []
