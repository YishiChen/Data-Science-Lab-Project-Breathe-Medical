import streamlit as st
from generate.generate import generate_scenario
import json
import time
import traceback
from utils.render_scenario import render_scenario

from assessment.submit_form import submit_scenario
from assessment.report_error import report_error

st.set_page_config(
    page_title="Medical Scenario Builder",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'generated_scenario' not in st.session_state:
    st.session_state['generated_scenario'] = None

with st.sidebar:
    st.image('breathe_logo.png')
    st.title('Medical Scenario Builder')
    st.write('This tool generates medical scenarios for simulation training. Fill in the details below to generate a scenario.')

    st.title('Mandatory Fields:')

    patient_gender = st.selectbox('Select the gender of the patient', ['Female', 'Male'], index=0)

    patient_age = st.slider('Select the patient\'s age', 0, 100, 50)

    #Dummy variable
    region = st.selectbox('Select the region', ["South Africa"], index=0)

    dep_list = ['Pre-hospital', 'Critical Care', 'Emergency', 'Ward']
        
    department = st.selectbox('Select the department/setting of the scenario', dep_list, index=0)
    resources = st.selectbox('Select the resource level of the institution', ['Low', 'Intermediate', 'High'], index=0)

    number_of_participants = st.selectbox('Select the number of participants', ['1-2', '2-5', '5-8'], index=0)

    level_of_difficulty = st.selectbox('Select the experience level of the participants', ['Beginner', 'Intermediate', 'High'], index=0)

    clinical_skills =st.text_area("Enter the clinical skills that participants should learn, separated by commas")

    training_topic = st.text_input('Enter the name of the training topic of the simulation (example: Cardiac arrest):')
    
    phase_list = [1, 2, 3]
    number_of_phases = st.selectbox('Select number of phases for the simulation', phase_list, index=0)
    phases_names = st.text_area("Enter names of the phases separated by commas (optional)")

    available_equipment_list = [
    'Ventilator', 'ECG', 'Ultrasound', 'X-Ray', 'MRI', 'CT Scan', 
    'Blood Pressure Monitor', 'Oxygen Concentrator', 'Pulse Oximeter', 
    'Defibrillator', 'Syringe Pump', 'Infusion Pump', 'Suction Machine', 
    'Surgical Instruments', 'Blood gas analyzer', 'Anaesthesia machine', 
    'Patient Monitor', 'Neonatal Incubator', 'Automated External Defibrillator (AED)', 
    'Blood warmer', 'Capnograph', 'Central venous catheter', 
    'Doppler ultrasound', 'Electrosurgical unit', 'Endoscope', 
    'Fluid warmer', 'Glucose meter', 'Hemodialysis machine', 
    'Intra-aortic balloon pump', 'IV poles', 'Laryngoscope', 
    'Nebulizer', 'Non-invasive ventilation (NIV) machine', 'Orthopedic instruments', 
    'Patient hoist', 'Phototherapy unit', 'Portable X-ray machine', 
    'Spirometer', 'Stethoscope', 'Telemetry', 'Transport ventilator', 
    'Vacuum extractor', 'Video laryngoscope', 'Wound vacuum-assisted closure (VAC) device',
    'Blood centrifuge', 'Electric and manual wheelchairs', 'Infant warmers', 
    'Pulse generators', 'Surgical lights', 'Thermometer', 
    'Vital signs monitor', 'Wound debridement instruments']
    available_equipment = st.multiselect(
        'Select the equipment that should be available in the simulation. Select all that apply',
        available_equipment_list)

    additional_equipment = st.text_area("Enter additional equipment, if any, that should be available in the simulation, separated by commas")
    additional_equipment_list = [item.strip() for item in additional_equipment.split(',') if item.strip()]

    # Concatenate the two lists
    combined_equipment = available_equipment + additional_equipment_list

    #Optional Fields
    advanced_options = st.checkbox('Show Advanced Options (if these fields are left empty, they will be ignored)')

    soft_skills = None
    algorithms = None
    additional_text = None

    if advanced_options:
        soft_skills = st.text_area('Enter the soft skills that participants should learn, separated by commas (example: communication, cognitive offloading)')
        algorithms = st.text_area('Enter the algorithms and/or checklists that participants should learn, separated by commas (example: ABCDE)')

        additional_text = st.text_area('Clinical Course')

    generate = st.button('Generate Scenario')

placeholder = st.empty()

if generate:
    if len(combined_equipment) == 0:
        st.sidebar.write("Please provide some available equipment for the simulation.")
    elif training_topic == "":
        st.sidebar.write("Please provide a training topic for the simulation.")
    else:
        # measure time taken to generate scenario
        start_time = time.time()
 
        with placeholder.container():
            try:
                generated_scenario = generate_scenario(department, resources, number_of_participants, level_of_difficulty, clinical_skills, soft_skills, algorithms,
                                                        training_topic,  combined_equipment, additional_text, number_of_phases, phases_names
                                                            , patient_gender, patient_age)

                placeholder.empty()

                end_time = time.time()
                time_taken = end_time - start_time
                
                st.sidebar.write(f'Time taken to generate scenario: {time_taken:.2f} seconds')

                generated_scenario['metadata']['Time Taken'] = time_taken
                st.session_state['generated_scenario'] = generated_scenario
            except Exception as e:
                placeholder.empty()
                error_message = traceback.format_exc()
                placeholder.write(""" # Error in generation                                  
                Something went wrong with the generation. This error is caused by slight inconsistencies in the generated output and is likely random. Please try again.
                """)
                st.sidebar.write(f"Error: {e}")
                st.sidebar.write(error_message)
                

if st.session_state['generated_scenario'] is not None: 
    success = True
    with placeholder.container():
        try:
            render_scenario(st.session_state['generated_scenario']['scenario'], 'Medical Scenario', outline = False, vital_changes=True, references=True)
        except Exception as e:
            report_error(st.session_state['generated_scenario'])
            error_message = traceback.format_exc()
            success = False
            st.write("Something went wrong with the rendering. Please try again.")
            st.write(f"Error: {e}")
            st.write(error_message)

    if success:        
        with st.form("my_form"):
            st.write("**Please assess the generated scenario and provide feedback.**")
            name = st.text_input("Name")
            email = st.text_input("Email")

            learning_goals = st.slider("**How well does the scenario align with the learning goals provided?** (1 = Does not align at all, 5 = Aligns perfectly)", 1, 5, 3)

            medical_guidelines = st.slider("**How well does the scenario align with medical guidelines?** (1 = Does not align at all, 5 = Aligns perfectly)", 1, 5, 3)

            expected_actions = st.slider("**How appropriate are the expected actions in the scenario?** (1 = Not appropriate at all, 5 = Very appropriate)", 1, 5, 3)

            vitals_realistic = st.slider("**How realistic are the vitals in the scenario?** (1 = Not realistic at all, 5 = Very realistic)", 1, 5, 3)

            scenario_usable = st.slider("**How usable is this scenario for training of healthcare professionals?** (1 = Not usable at all, 5 = Very usable)", 1, 5, 3)

            st.write("**Other feedback**")
            
            correct_and_not = st.text_area("Give a summary of what is wrong/false in the scenario:")
            better = st.text_area("Is there something that is missing in the scenario?")

            submitted = st.form_submit_button("Submit")

            if submitted:
                if name == "" or email == "":
                    st.write("Please provide your name and email.")
                else:
                    submit_scenario(st.session_state['generated_scenario'], {
                        "learning_goals": {
                            "label": "How well does the scenario align with the learning goals provided?",
                            "value": learning_goals,
                        },
                        "medical_guidelines": {
                            "label": "How well does the scenario align with medical guidelines?",
                            "value": medical_guidelines,
                        },
                        "expected_actions": {
                            "label": "How appropriate are the expected actions in the scenario?",
                            "value": expected_actions,
                        },
                        "vitals_realistic": {
                            "label": "How realistic are the vitals in the scenario?",
                            "value": vitals_realistic,
                        },
                        "scenario_usable": {
                            "label": "How usable is this scenario for training of healthcare professionals?",
                            "value": scenario_usable,
                        },
                        "correct_and_not": {
                            "label": "Give a summary of what is wrong/false in the scenario:",
                            "value": correct_and_not,
                        },
                        "better": {
                            "label": "Is there something that is missing in the scenario?",
                            "value": better,
                        }
                    },
                    {
                        "name": name,
                        "email": email
                    })
                    st.write("Thank you for your valuable feedback!")
