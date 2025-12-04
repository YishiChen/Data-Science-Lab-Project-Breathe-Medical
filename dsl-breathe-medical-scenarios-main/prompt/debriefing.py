def develop_debriefing_description():
    return {
        "type": "develop",
        "location": ["debriefing", "description"],
        "intro": """
            Based on the generated scenario's outline, develop the description subsection in the debriefing section. 
            In this section you should clarify facts, develop shared understanding of the case. This section should be less than 500 characters.
        """,
        "format": """
            {
                "value": "<description>"
            }
        """
    }

def develop_debriefing_analysis():
    return {
        "type": "develop",
        "location": ["debriefing", "analysis"],
        "intro": """
            Based on the generated scenario's outline, develop the analysis subsection in the debriefing section. 
            In this section you should give medical questions for teaching purposes that should be linked to the learning goals 
            of the simulation. Add as many questions as you think could be helpful for participants. Try to anticipate things that 
            could go wrong or are commonly done wrong.
        """,
        "format": """
            {
                "value": {
                    "description": "<How to start this part. Suggestions for wording: "Let's spend some time talking about [insert topic] 
                    to better understand what happened/what we could improve” or "Let's go through some of the following questions 
                    together and discuss as a group.">"
                    "questions": [
                        {
                            "question": "<question>",
                            "answer": "<answer>",
                            "learning_goals": "<learning goals for the question>"
                        }
                    ]
                }
            }
        """
    }

def develop_debriefing_summary():
    return {
        "type": "develop",
        "location": ["debriefing", "summary"],
        "intro": """
            Based on the generated scenario's outline, develop the summary subsection in the debriefing section. 
            In this section you should identify key take-aways and add material or links that people can also look up 
            afterwards and that helps them to prepare for future situations like in this simulation (e.g. medication 
            doses, guidelines, ...). This section should be less than 200 characters.
        """,
        "format": """
            {
                "value": "<summary>"
            }
        """
    }
