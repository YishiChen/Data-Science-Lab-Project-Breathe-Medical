from prompt.preparation import develop_clinical_course, develop_patient_story, develop_collateral_history, develop_preparation_other
from prompt.team_warm_up import develop_team_warm_up_description, develop_team_warm_engagement_of_nurses, develop_end_of_team_warm_up
from prompt.medical_simulation import generate_phase_outline
from prompt.debriefing import develop_debriefing_description, develop_debriefing_analysis, develop_debriefing_summary


def generate_outline(department, resources, number_of_participants, level_of_difficulty, clinical_skills, soft_skills, algorithms, training_topic, 
                     available_equipment, additional_text, number_of_phases, phases_names,
                     patient_gender, patient_age):
    return f'''
            Generate an outline of a scenario for these requirements:
         
            Location where the sim take place: {department}

            Level of resources: {resources}

            Number of participants: {number_of_participants}

            Level of difficulty: {level_of_difficulty}

            Clinical skills to be learned: {clinical_skills}

            {f"Soft skills to be learned: {soft_skills}" if soft_skills else ""}

            {f"Algorithms to be learned: {algorithms}" if algorithms else ""}

            Training topic: {training_topic}

            Available equipment: {available_equipment}

            Number of phases: {number_of_phases}

            {f"Phase names: {phases_names}" if phases_names else ""}

            Patient Age: {patient_age}

            Patient Gender: {patient_gender}

            The scenario should have the following JSON structure:

            {initial_outline_structure(number_of_phases)}

            {f"Also consider the additional info: {additional_text}" if additional_text else ""}
         ''', [
            ('preparation', 'clinical_course', str),
            ('preparation', 'patient_history', 'patient_story', str),
            ('preparation', 'patient_history', 'collateral_history', str),
            ('preparation', 'prepare_before_simulation', str),
            ('medical_simulation', 'phases', number_of_phases, list),
            ('debriefing', 'description', str),
            ('debriefing', 'analysis', dict),
            ('debriefing', 'summary', str),
        ]

def initial_outline_structure(num_phases):
    return """
        {
            "preparation": {
                "clinical_course": "<Summary of the best case for the scenario>",
                "patient_history": {
                    "patient_story": "<How the patient is when they arrive into the simulation, why they were taken to the hospital, what symptoms they are feeling etc.>",
                    "collateral_history": "<Previous health information about the patient, usually gotten from family members>"
                },
                "prepare_before_simulation": "<Anything else to prepare for the scenario?>"
            },
            "medical_simulation": {
                phases: [
                    <This section should include the phases of the simulation in an array. Remember that the scenario has """ + str(num_phases) + """ phases so the array should have length """ + str(num_phases) + """.
                    The first phase should be about the initial assessment of the patient, what the participants should do when they first see the patient, what they should look for and how they should react. 
                    Make sure that the participants will learn all the required clinical skills, soft skills and algorithms.
                    Make sure to respect the provided names of the phases.
                    The next phases (if any) should be about the progression of the patient's deteriorating or improving condition. Take the level of difficulty into account.>
                    <Each phase should have the following structure>
                    "<A string containing the summary of the phase, how the condition of the patient deteriorates (if it does), what the expected actions are, how the vitals change>" 
                ]
            },
            "debriefing": {
                "description": "<Clarify facts, develop shared understanding of the case>",
                "analysis": {
                    <
                        Medical question for teaching purposes that should be linked to the learning goals of the simulation.
                        Add as many questions as you think could be helpful for participants. Try to anticipate things that 
                        could go wrong or are commonly done wrong.
                    >
                    "questions": [
                        "<question, answer, learning goals for the question>"
                    ]
                }
                "summary": "<Identify key take-aways>"
            }
        }
    """
def part_by_part_prompts(num_phases, training_topic, outline):
    preparation = [
        develop_clinical_course(),
        develop_patient_story(),
        develop_collateral_history(),
        develop_preparation_other(),
    ]

    procedure = [generate_phase_outline(i, training_topic, outline) for i in range(num_phases)]

    debriefing = [
        develop_debriefing_description(),
        develop_debriefing_analysis(),
        develop_debriefing_summary(),
    ]

    return [
        *preparation,
        *procedure,
        *debriefing
    ]
