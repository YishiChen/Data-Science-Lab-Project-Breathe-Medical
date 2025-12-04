def develop_clinical_course():
    return {
        "type": "develop",
        "location": ["preparation", "clinical_course"], 
        "intro": f"""
            Based on the generated scenario's outline, develop the clinical course section. 
            In this section you need to give a detailed summary of the course of the scenario.
            Please focus strictly on medically relevant information and omit any unrelated content. This section should be less than 500 characters.
        """,
        "format": """
            {
                "value": "<clinical course summary>"
            }
        """
    }

def develop_patient_story():
    return {
        "type": "develop",
        "location": ["preparation", "patient_history", "patient_story"],
        "intro": """
            Based on the generated scenario's outline, develop the patient story section. 
            In this section you should specify how the patient is when they arrive into the ER, why they were taken to the hospital, what symptoms they are feeling etc.
            Please focus strictly on medically relevant information and omit any unrelated content. This section should be less than 500 characters.
        """,
        "format": """
            {
                "value": "<patient story>"
            }
        """
    }

def develop_collateral_history():
    return {
        "type": "develop",
        "location": ["preparation", "patient_history", "collateral_history"],
        "intro": """
            Based on the generated scenario's outline, develop the collateral history section. 
            In this section you should specify previous health information about the patient, usually gotten from family members.
            Please focus strictly on medically relevant information and omit any unrelated content. This section should be less than 500 characters.
        """,
        "format": """
            {
                "value": "<collateral history>"
            }
        """
    }

def develop_preparation_other():
    return {
        "type": "develop",
        "location": ["preparation", "prepare_before_simulation"],
        "intro": """
            Based on the generated scenario's outline, develop the prepare_before_simulation subsection in the preparation section. 
            In this section you should specify anything else to prepare? e.g. Turn off a device to increase difficulty, hang up a checklist that you want people to use.
            Please focus strictly on medically relevant information and omit any unrelated content. This section should be less than 500 characters.
        """,
        "format": """
            {
                "value": "<other>"
            }
        """
    }