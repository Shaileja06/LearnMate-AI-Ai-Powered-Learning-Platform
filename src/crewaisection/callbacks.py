from crewai.task import TaskOutput
import json
import os
import pandas as pd

os.makedirs('final_outputs', exist_ok=True)

# Function to clean the raw output
def clean_raw_output(raw_output):
    return raw_output.replace("```", "").replace("json", "").replace(r"\n", '')

# Function to parse JSON with fallback
def parse_json_with_fallback(cleaned_output, output_description):
    try:
        return json.loads(cleaned_output)
    except json.JSONDecodeError as e:
        # Log the error and save the raw output for debugging
        with open(f'final_outputs/studyplan_raw.txt', 'w') as f:
            f.write(cleaned_output)
        print(f"Error decoding JSON: {e}")
        print(f"Raw output stored in studyplan_raw.txt")
        return None

# Callback function for Task 1
def planner_callback_function(output: TaskOutput):
    print("Task completed!")
    task1_output = output.raw_output
    cleaned_output = clean_raw_output(task1_output)
    output_dict = parse_json_with_fallback(cleaned_output, output.description)
    if output_dict is None:
        return None

    final_output = list(output_dict.values())
    with open(f'final_outputs/{output.description}.txt', 'w') as f:
        for item in final_output:
            f.write(str(item) + '\n')
    return final_output