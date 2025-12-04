from openai import OpenAI
import os
import time
import json
import streamlit as st

from prompt.combine import generate_outline, part_by_part_prompts
from utils.manipulate_output import retrieve_output, update_output
from utils.render_scenario import render_scenario

from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def render_location(location):
    return " > ".join([x.replace('_', ' ') if type(x) == str else str(x + 1) for x in location])

def generate_from_prompt(prompt, thread, output, progress_bar, percent_complete, retries = 0):
    summary = retrieve_output(output, prompt['location'])

    progress_text = f'Generating {render_location(prompt["location"])}{f" (retry {retries})" if retries > 0 else ""}...'
    progress_bar.progress(percent_complete, text=progress_text)

    content = f"""
        {prompt['intro']}

        For reference, the current output is:
        {summary}

        The JSON output should be structured as follows:
        {prompt['format']}
    """

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=os.getenv('ASSISTANT_MODEL_ID'),
    )

    wait_on_run(run, thread)

    completion = client.beta.threads.messages.list(thread_id=thread.id)

    # If the output is not in JSON format, retry
    try: 
        message = json.loads(str(completion.data[0].content[0].text.value))
    except:
        if retries >= 3:
            raise Exception("Something went wrong with the generation. Please try again.")

        generate_from_prompt(prompt, thread, output, progress_bar, percent_complete, retries + 1)
        return

    update_output(output, prompt['location'], message['value'])

    if prompt['type'] == 'outline':
        assertions = prompt['assertions']

        try:
            for assertion in assertions:
                if assertion[-1] == list:
                    assert len(retrieve_output(output, assertion[:-2])) >= assertion[-2]
                else:
                    relevant_col = retrieve_output(output, assertion[:-1])
                    assert isinstance(relevant_col, assertion[-1])
        except:
            if retries >= 3:
                raise Exception("Something went wrong with the generation. Please try again.")
            
            generate_from_prompt(prompt, thread, output, progress_bar, percent_complete, retries + 1)
            return

        parameters = []

        for parameter in prompt['further_develop']['parameters']:
            if parameter['type'] == 'number':
                parameters.append(parameter['value'])
            elif parameter['type'] == 'length':
                parameters.append(len(retrieve_output(message, parameter['value'])))
            elif parameter['type'] == 'string':
                parameters.append(parameter['value'])

        next_prompts = prompt['further_develop']['function'](*parameters)

        for next_prompt in next_prompts:
            try:
                generate_from_prompt(next_prompt, thread, output, progress_bar, percent_complete)
            except:
                raise Exception("Something went wrong with the generation. Please try again.")


def generate_scenario(department, resources, number_of_participants, level_of_difficulty, clinical_skills, soft_skills, algorithms, training_topic, 
                      available_equipment, additional_text, number_of_phases, phases_names, patient_gender, patient_age, retries = 0):
    progress_text = "Initiating connection"
    progress_container = st.sidebar.empty()
    progress_bar = progress_container.container().progress(0, text=progress_text)

    thread = client.beta.threads.create()

    outline_prompt, assertions = generate_outline(department, resources, number_of_participants, level_of_difficulty, clinical_skills, soft_skills, 
                                                  algorithms, training_topic, available_equipment, additional_text, number_of_phases, phases_names, 
                                                  patient_gender, patient_age)
    

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=outline_prompt,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=os.getenv('ASSISTANT_MODEL_ID'),
    )

    progress_text = f"Generating outline{ f' (retry {retries})' if retries > 0 else ''}..."
    progress_bar.progress(0, text=progress_text)

    wait_on_run(run, thread)

    completion = client.beta.threads.messages.list(thread_id=thread.id)

    # Assert that the outline has correct structure, if not retry
    try:
        output = json.loads(str(completion.data[0].content[0].text.value))
        for assertion in assertions:
            if assertion[-1] == list:
                assert len(retrieve_output(output, assertion[:-2])) >= assertion[-2]
            else:
                relevant_col = retrieve_output(output, assertion[:-1])
                assert isinstance(relevant_col, assertion[-1])
    except:
        if retries >= 3:
            progress_container.empty()
            raise Exception("Something went wrong with the generation. Please try again.")
        
        progress_container.empty()
        generate_scenario(department, resources, number_of_participants, level_of_difficulty, clinical_skills, soft_skills, algorithms, training_topic, 
                      available_equipment, additional_text, number_of_phases, phases_names, 
                      patient_gender, patient_age, retries = retries + 1)
        return

    output['medical_simulation']['phases'] = output['medical_simulation']['phases'][:number_of_phases]

    st.title('Scenario Outline')
    st.write('For better results, the scenario is generated in multiple parts. While you wait for the scenario to generate, here is an outline of the scenario.')
    render_scenario(output, "", outline = True)

    prompts = part_by_part_prompts(number_of_phases, training_topic, output)

    num_steps = 2 + len(prompts)
    percent_complete = 0

    # Steps for step-by-step generation

    for prompt in prompts:
        percent_complete += 1 / num_steps

        try:
            generate_from_prompt(prompt, thread, output, progress_bar, percent_complete)
        except:
            progress_container.empty()
            raise Exception("Something went wrong with the generation. Please try again.")

    progress_bar.progress(1, text=progress_text)

    progress_bar.empty()

    scenario = {
        "metadata": {
            "Patient Gender": patient_gender,
            "Patient Age" : patient_age,
            "Department": department,
            "Level of resource": resources,
            "Number of participants": number_of_participants,
            "Level of difficulty": level_of_difficulty,
            "Clinical Skills": clinical_skills, 
            "Soft Skills": soft_skills, 
            "Algorithms": algorithms,
            "Training topic": training_topic,
            "Available Equipment": available_equipment,
            "Additional Text": additional_text,
            "Number of Phases": number_of_phases,
            "Names of phases": phases_names,
            "Time Taken": None
        },
        "scenario": output
    }

    return scenario