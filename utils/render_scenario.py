import streamlit as st
import copy

def add_to_markdown(output, part, level = 1):
    output += "\n"
    if level > 6:
        level = 6

    output += "#" * level
    output += " " 

    output += part
    output += "\n"
    
    return output

def key_to_str(key):
    return key.replace("_", " ")

def iterate_json(output, object, level = 1):
    if type(object) == str:
        output = add_to_markdown(output, object, 0)
        
    elif type(object) == int:
        output = add_to_markdown(output, str(object), 0)

    elif type(object) == list:
        for thing in object: 
            output = iterate_json(output, thing, 0)

    elif type(object) == dict:
        for key in object.keys(): 
            output = add_to_markdown(output, key_to_str(key).title(), level)
            output = iterate_json(output, object[key], level + 1)

    else:
        raise ValueError(f"Object type {type(object)} not supported.")

    return output

def make_table_with_vitals(vals, title, description, none_message):
    table = ""

    if description:
        table = f"""{description}

        """

    table += f"""
| {title}     | Value |
|-------------|-------|
"""
    
    num_rows = 0
    
    for key in vals.keys():
        if 'value' in vals[key] and vals[key]['value'] != 'N/A' and vals[key]['value'] != None:
            value = f"{vals[key]['value']}"
            if 'unit' in vals[key]:
                value += f" {vals[key]['unit']}"
            num_rows += 1
            table += f"| {key} | {value} |\n"

    if num_rows == 0:
        return none_message

    return table

def list_expected_actions(actions, vital_changes, previous_vitals = None):
    output = ""

    for i in range(len(actions)):
        if actions[i]["mandatory"]:
            output = add_to_markdown(output, f"{i+1}. **{actions[i]['title']}** {'(Optional)' if not actions[i]['mandatory'] else ''}: {actions[i]['instructions']}", 0)
            output = add_to_markdown(output, f"Explanation: {actions[i]['explanation']}", 0)

            # vital changes
            if vital_changes and "vital_changes" in actions[i].keys() and len(actions[i]["vital_changes"]) > 0:
                new_vitals = copy.deepcopy(actions[i]["vital_changes"].copy())

                if i > 0:
                    previous_vitals = copy.deepcopy(actions[i-1]["vital_changes"])
                
                if previous_vitals is not None:
                    for key in previous_vitals.keys():
                        if 'value' in previous_vitals[key] and 'value' in new_vitals[key] and previous_vitals[key]['value'] == new_vitals[key]['value']:
                            new_vitals[key]['value'] = 'N/A'

                table = make_table_with_vitals(new_vitals, "Vital", "After successful completion of the action, the following vital changes occur:", "")
                output = add_to_markdown(output, table, 0)
                output += "    \n"
    
    return output 

def list_questions(object, outline = False):
    output = ""

    for i in range(len(object)):
        q = None

        if outline:
            q = f"* {object[i]}"
        else:
            q = f"""
* **Question:** {object[i]['question']}
    * **Answer:** {object[i]['answer']}
    * **Learning Goals:** {object[i]['learning_goals']}
    """
            
        output = add_to_markdown(output, q, 0)
    
    return output 

def list_references(actions):
    output = ""

    unique_references = set()

    for i in range(len(actions)):
        if actions[i]['references']['value'] != "N/A":
            unique_references.add(f"{actions[i]['references']['source']} - {actions[i]['references']['value']}")

    for i, reference in enumerate(unique_references):
        output = add_to_markdown(output, f"{i + 1}. {reference}", 0)

    return output

def render_scenario(generated_scenario, title, outline = False, references = False, vital_changes = False):
    output = ""
    output = add_to_markdown(output, title, 1)
    output = add_to_markdown(output, "---", 0)

    if outline:
        add_to_markdown(output, 'While you wait for the scenario to generate, here is an outline of the scenario.', 1)

    #preparation part
    output = add_to_markdown(output, "Preparation" , 2)
    st.write(output)
    
    output = ""
    output = iterate_json(output, generated_scenario["preparation"], 3)
    output = add_to_markdown(output, "___", 0)
    st.write(output)

    #Medical simulation part
    exclude = []
    phases = len(generated_scenario["medical_simulation"]["phases"])
    
    output = ""
    output = add_to_markdown(output, "Medical Simulation" , 2)
    st.write(output)
    
    for i in range(phases):
        output = ""
        output = add_to_markdown(output, f"Phase {i+1}" , 3)
        
        if outline is True:
            output = iterate_json(output, generated_scenario["medical_simulation"]["phases"][i], 0)
            st.write(output)
            output = add_to_markdown(output, "___", 0)
            continue
        output = add_to_markdown(output, "Description", 4)
        output = iterate_json(output, generated_scenario["medical_simulation"]["phases"][i]["description"], 0)
        st.write(output)

        table1 = make_table_with_vitals(generated_scenario["medical_simulation"]["phases"][i]["vitals"], "Vital", None, "No vital changes.")
        table2 = make_table_with_vitals(generated_scenario["medical_simulation"]["phases"][i]["blood_gas_findings"], "Blood Gas Finding", None, "No new blood gas findings.")

        col1, col2 = st.columns(2)
        with col1:
            output = ""
            output = add_to_markdown(output, "Initial Vitals for This Phase", 4)
            output = add_to_markdown(output, table1, 0)
            st.write(output)

        
        with col2: 
            output = ""
            output = add_to_markdown(output, "Blood Gas Findings", 4)
            output = add_to_markdown(output, table2, 0)
            st.write(output)
        

        output = ""
        st.write("  \n")

        output = add_to_markdown(output, "Expected Actions", 4)
        expected_actions = list_expected_actions(generated_scenario["medical_simulation"]["phases"][i]["expected_actions"], vital_changes=vital_changes, previous_vitals = generated_scenario["medical_simulation"]["phases"][i]["vitals"])
        output = add_to_markdown(output, expected_actions, 0)

        output += "\n"

        if references:
            output = add_to_markdown(output, "References For The Expected Actions", 4)
            references = list_references(generated_scenario["medical_simulation"]["phases"][i]["expected_actions"])
            output = add_to_markdown(output, references, 0)


        output = add_to_markdown(output, "___", 0)
        st.markdown(output)

        
    #debriefing part
    output = ""
    output = add_to_markdown(output, "Debriefing", 2)
    output = add_to_markdown(output, generated_scenario["debriefing"]["description"], 0)
    output = add_to_markdown(output, "Analysis", 3)
    if 'description' in generated_scenario["debriefing"]["analysis"]:
        output = add_to_markdown(output, generated_scenario["debriefing"]["analysis"]["description"], 0)

    output = add_to_markdown(output, "Questions", 4)
    questions = list_questions(generated_scenario["debriefing"]["analysis"]["questions"], outline = outline)
    output = add_to_markdown(output, questions, 0)
    output = add_to_markdown(output, "Summary", 3)
    output = add_to_markdown(output, generated_scenario["debriefing"]["summary"], 0)


    st.markdown(output)
    return

def render_metadata(metadata):

    output = ""
    output = add_to_markdown(output, "Scenario Metadata", 3)
    st.markdown(output)
    output = ""
    for key in metadata.keys():
        
        if type(metadata[key]) == str:
            
            output += f'**{key_to_str(key)}**: {metadata[key]}'
            output += "  \n"

        elif type(metadata[key]) == list:
            output += f'**{key_to_str(key)}**: '
            for i in range(len(metadata[key])):
                output += metadata[key][i]
                output += ", " if i < len(metadata[key]) - 1 else "  \n"

        elif type(metadata[key]) == int:
            output += f'**{key_to_str(key)}**: {str(metadata[key])}'
            output += "  \n"
    st.markdown(output)

  


    return