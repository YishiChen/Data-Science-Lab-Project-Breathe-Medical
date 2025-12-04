from rag.query_index import rag_filter 


def develop_phase_description(i):
    intro = f"""
        Based on the generated scenario's outline, develop the description section for phase {i + 1} of the medical simulation. 
        In this section you should specify what should participants do, how will the patient react, how does the phase end?
    """ 

    if i == 0:
        intro += """
            The first phase should be about the initial assessment of the patient, 
            what the participants should do when they first see the patient, 
            what they should look for and how they should react. This section should be less than 5 bullet points long.
        """
    else: 
        intro += """
            The phase should be about the progression of the patient's deteriorating or improving condition. 
            This section should be less than 5 bullet points long.
        """


    return {
        "type": "develop",
        "location": ["medical_simulation", "phases", i, "description"],
        "intro": intro,
        "format": """
            {
                "value": "<description in bullet points in markdown. Only include bullet points and no headings>"
            }
        """
    }

def develop_expected_action(phase, num_expected_actions, rag):

    return {
        "type": "develop",
        "location": ["medical_simulation", "phases", phase, "expected_actions"],
        "intro": f"""
            Based on the generated scenario's outline and the generated phase's outline, develop all the {num_expected_actions} expected actions for phase {phase + 1} of the medical_simulation section.
            Make sure the flow is in the correct order, consider also team interaction task (e.g. inform superior), the immediate results of actions are important to note down. Explain clearly why is this action relevant.
            
            When generating the expected action you should keep inline with these medical guidlines from the National Department of Health, South Africa. Essential Drugs Programme. Hospital level (Adults) Standard Treatment Guidelines and Essential Medicines List. 5th ed. 2019. and follow them closely.
            Here are the relevant guidelines: {rag}. 
        """,
        "format": """
            {
                "value": [{
                    "title": "<title of the expected action>",
                    "instructions": "<instructions for the expected action>",
                    "mandatory": "<is the action mandatory? true/false>",
                    "time_out": "<This should be some action that if the participants do it wrong, the simulation should end>",
                    "additional_information": <Additional medical information / Troubleshooting / Learn more about it>,
                    "vital_changes": {
                        <vital changes that should be observed during the action. If there is no change to a vital, report it as N/A. Rember to include both unit and value in the JSON>
                         "RR": {
                            "value": "<respiratory rat in breath/min>"
                            "unit": "breath/min"
                        },
                        "HR": {
                            "value": "<heart rate in beats/min>"
                            "unit": "beats/min"
                        },
                        "SpO2": {
                            "value": "<oxygen saturation in %>"
                            "unit": "%"
                        },
                        "BP": {
                            "value": "<blood pressure mmHg/mmHg>"
                            "unit": "mmHg/mmHg"
                        },
                        "Glucose": {
                            "value": "<glucose level in mmol/L>"
                            "unit": "mmol/L"
                        },
                        "Temperature": {
                            "value": "<temperature in C>"
                            "unit": "C"
                        },
                        "LOC/GCS": {
                            "value": "<level of consciousness/Glasgow Coma Scale>"
                            "unit": ""
                        },
                    },
                    "explanation": "<explanation of the expected action. Why is this action relevant to the generated scenario?>"
                    "references": {
                        "source": "<source of the information>",
                        "value": "<relevant chapters and sections used from the provided guidelines in generating the expected action.>"
                    }
                }]
            }
        """,
    }

def develop_phase(i, num_expected_actions, rag):
    return [
        develop_phase_description(i),
        # develop_vitals(i),
        # develop_blood_gas_findings(i),
        develop_expected_action(i, num_expected_actions, rag) 
    ]

def generate_phase_outline(i, disease, outline, num_expected_actions = (5,15)):
    rag = rag_filter(f'{disease} {outline["medical_simulation"]["phases"][i]}')

    intro = f"""
    Based on the generated scenario's outline, develop the outline of phase {i + 1} of the medical_scenarios section. 
    

    When generating the outline of phase {i+1}, you should keep inline with these provided medical guidelines from the National Department of Health, South Africa. 
    Essential Drugs Programme. Hospital level (Adults) Standard Treatment Guidelines and Essential Medicines List. 5th ed. 2019. and follow them closely.
    Here are the relevant guidelines: {rag}. 
    """

    return {
        "type": "outline",
        "location": ["medical_simulation", "phases", i],
        "intro": intro,
        "format": """
            {
                "value": {
                    "description": "<What should participants do, how will the patient react, how does the phase end?>",
                    "vitals": {
                        <Report the initial vital values for this phase. Report only the value in number, not including the unit in the string>
                        "RR": {
                            "value": "<respiratory rat in breath/min>"
                            "unit": "breath/min"
                        },
                        "HR": {
                            "value": "<heart rate in beats/min>"
                            "unit": "beats/min"
                        },
                        "SpO2": {
                            "value": "<oxygen saturation in %>"
                            "unit": "%"
                        },
                        "BP": {
                            "value": "<blood pressure mmHg/mmHg>"
                            "unit": "mmHg/mmHg"
                        },
                        "Glucose": {
                            "value": "<glucose level in mmol/L>"
                            "unit": "mmol/L"
                        },
                        "Temperature": {
                            "value": "<temperature in C>"
                            "unit": "C"
                        },
                        "LOC/GCS": {
                            "value": "<level of consciousness/Glasgow Coma Scale>"
                            "unit": ""
                        },
                    },
                    "blood_gas_findings": {
                        <Report the initial blood gas findings for this phase. Report only the value in number, not including the unit in the string>
                        "pH": {
                            "value": "<pH level>"
                            "unit": ""
                        },
                        "PaO2": {
                            "value": "<partial pressure of oxygen in mmHg>"
                            "unit": "mmHg"
                        },
                        "PaCO2": {
                            "value": "<partial pressure of carbon dioxide in mmHg>"
                            "unit": "mmHg"
                        },
                        "O2 Sat": {
                            "value": "<oxygen saturation in %>"
                            "unit": "%"
                        },
                        "HCO3-": {
                            "value": "<bicarbonate level in mEq/L>"
                            "unit": "mEq/L"
                        },
                        "Hemoglobin": {
                            "value": "<hemoglobin values in g/mL>"
                            "unit": "g/mL"
                        },
                        "BE": {
                            "value": "<base excess in mEq/L>"
                            "unit": "mEq/L"
                        }
                    },
                    "expected_actions": [
                        <Please provide at least """ + str(num_expected_actions[0]) + " and at most " + str(num_expected_actions[1]) + """ expected actions for the phase. These should be chronologically ordered>
                        "<string containing the summary of the expected action>",
                    ]
                }
            }
        """,
        "further_develop": {
            "function": develop_phase,
            "parameters": [
                {
                    "type": "number",
                    "value": i
                },
                {
                    "type": "length",
                    "value": ["value", "expected_actions"]
                },
                {
                    "type": "string",
                    "value": rag
                }
            ]
        },
        "assertions": [
            ("medical_simulation", "phases", i, "description", str),
            ("medical_simulation", "phases", i, "vitals", dict),
            ("medical_simulation", "phases", i, "blood_gas_findings", dict),
            ("medical_simulation", "phases", i, "expected_actions", 1, list)
        ]
    }