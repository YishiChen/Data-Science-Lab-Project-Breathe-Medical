def develop_team_warm_up_description():
    return {
        "type": "develop",
        "location": ["team_warm_up", "description"],
        "intro": """
            Based on the generated scenario's outline, develop the description subsection in the team warm up section. 
            In this section you should specify what should participants do, what should they consider, how does the phase end?. it needs to spark the communication between doctors and nurses in setting up the hospital room.
            Please focus strictly on medically relevant information and omit any unrelated content. This section should be less than 500 characters.
        """,
        "format": """
            {
                "value": "<description>"
            }
        """
    }

def develop_team_warm_engagement_of_nurses():
    return {
        "type": "develop",
        "location": ["team_warm_up", "engagement_of_nurses"],
        "intro": """
            Based on the generated scenario's outline, develop the engagement of nurses subsection in the team warm up section. 
            This section is about engaging nurses by e.g. using them as actors (carrying the dummy), make them write on the board during the sim, etc.
            Please focus strictly on medically relevant information and omit any unrelated content. This section should be less than 500 characters.
        """,
        "format": """
            {
                "value": "<engagement_of_nurses>"
            }
        """
    }

def develop_end_of_team_warm_up():
    return {
        "type": "develop",
        "location": ["team_warm_up", "end_of_team_warm_up"],
        "intro": """
            Based on the generated scenario's outline, develop the end of team warm up subsection in the team warm up section. 
            In this section you should specify what is required from the participants to start the medical case.
            Please focus strictly on medically relevant information and omit any unrelated content. This section should be less than 500 characters.
        """,
        "format": """
            {
                "value": "<end_of_team_warm_up>"
            }
        """
    }
    