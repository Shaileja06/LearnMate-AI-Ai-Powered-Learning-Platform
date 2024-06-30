from src.helper import load_env_variable, prepare_final_output
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from streamlit_player import st_player
import pandas as pd
import time

# Load Variables
load_dotenv()
load_variable = load_env_variable()

# Load Gemini
gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Function to create the user input form in the sidebar
def user_input_form():
    st.sidebar.header("What you wish to learn?")

    # Collecting user inputs in the sidebar
    topic = st.sidebar.text_input("Topic", key="topic")
    duration = st.sidebar.selectbox("In How much Duration (days)", [i for i in range(1, 11)], key="duration")
    studytime = st.sidebar.selectbox("How much hours in a day you can give", [i for i in range(1, 6)], key="studytime")
    style = st.sidebar.selectbox("Your learning style", ["Theory", "Video"], key="style")
    grade = st.sidebar.text_input("Your Grade", key="grade")
    stream = st.sidebar.text_input("Your Stream", key="stream")
    knowledge = st.sidebar.text_input("Do you have any experience in this domain you wish to learn?", key="knowledge")
    distraction_tolerance = st.sidebar.selectbox("Distraction Tolerance", ["Easily Distracted", "Not Easily Distracted"], key="distraction_tolerance")

    # Submit button
    submit_button = st.sidebar.button("Submit", key="submit_button")

    data_input = {
        'topic': topic,
        'duration': duration,
        'studytime': studytime,
        'style': style,
        'grade': grade,
        'stream': stream,
        'knowledge': knowledge,
        'distraction_tolerance': distraction_tolerance,
    }

    return data_input, submit_button

# Set the layout of the Streamlit page
st.set_page_config(layout="wide")

# Collect user input from the sidebar
data_input, submit_button = user_input_form()

# Main page - Study plan and output
st.header('Study Plan')
if submit_button:
    st.success("Your preferences have been recorded!")

    # Prepare final output
    study_plan, output = prepare_final_output(gemini_llm, data_input)
    output.to_csv("final_outputs/final_df.csv")

    for i, row in enumerate(output.iterrows(), start=1):
        st.subheader(f"Day {i}: {row[1]['Title']}")
        st.write(f"**Blog**: {row[1]['blog_url']}")
        st.write(f"**Video**: {row[1]['youtube_url']}")
        st_player(str(row[1]['youtube_url']).strip(), key=f"video_{i}")

        st.markdown("---") 

# Any additional information or output can be displayed here
st.write("Additional information or output will be displayed here")
