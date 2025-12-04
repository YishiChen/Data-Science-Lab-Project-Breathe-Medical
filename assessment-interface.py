import streamlit as st

from assessment.fetch_results import fetch_results
import pandas as pd
import numpy as np
from utils.render_scenario import render_scenario, render_metadata

st.set_page_config(
    page_title="Medical Scenario Assessment",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "tab" not in st.session_state:
    st.session_state["tab"] = 0

container = st.container()
container.image('breathe_logo.png', width=500)

results = fetch_results()

col1, col2 = st.columns([0.6,0.4])

if not results or len(results) == 0:
    st.write('No feedback has been submitted yet')
else:
    feedback_per_question = dict()
    question_labels = dict()

    for result in results:
        feedback = result['feedback']

        for question in feedback.keys():
            if question not in feedback_per_question:
                feedback_per_question[question] = []
            
            if question not in question_labels:
                question_labels[question] = feedback[question]['label']

            feedback_per_question[question].append(feedback[question]['value'])

    with col1:
        st.title('Deep Dive')

        scenario_name = st.selectbox('Select a submission', [f"{result['personal_information']['name']} (submission {i + 1})" for i, result in enumerate(results)])

        scenario = [result for i, result in enumerate(results) if f"{result['personal_information']['name']} (submission {i + 1})" == scenario_name][0]

        st.write('## Feedback')
        for question in scenario['feedback'].keys():
            st.write(f'**{question_labels[question]}**:')
            st.write(f'{scenario["feedback"][question]["value"]}')

        render_metadata(scenario['scenario']['metadata'])
        render_scenario(scenario['scenario']['scenario'], "Medical Scenario", vital_changes=True, references=True)

    with col2:
        st.title('Feedback Summary')

        st.write(f'Total number of scenarios submitted: {len(results)}')
        question = st.selectbox('Select a question', question_labels.keys(), format_func=lambda x: question_labels[x])


        # Check if question is numeric, provide a histogram if it is
        if all(isinstance(value, int) for value in feedback_per_question[question]):
            aggregations = np.zeros(5)

            for value in feedback_per_question[question]:
                aggregations[value-1] += 1

            rating_df = pd.DataFrame({
                'ratings': np.arange(1,6),
                'total': aggregations
            })

            st.bar_chart(x='ratings', y = 'total', data=rating_df, use_container_width=True, color='#e85404')
            st.write(f'Average rating: {sum(feedback_per_question[question]) / len(feedback_per_question[question])}')
        else:
            for value in feedback_per_question[question]:
                st.write(value)

        

