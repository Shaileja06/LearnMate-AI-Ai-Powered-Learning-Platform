from crewai.process import Process
from crewai import Crew
import json
from src.crewaisection.callbacks import clean_raw_output

def planner_Crew(study_planner_agent,planner_task,data_input):
    crew = Crew(
        agents=[study_planner_agent],
        tasks=[planner_task],
        process=Process.sequential,
        verbose=True
    )
    study_plan = crew.kickoff(data_input)
    study_plan = json.loads(clean_raw_output(study_plan))

    return study_plan