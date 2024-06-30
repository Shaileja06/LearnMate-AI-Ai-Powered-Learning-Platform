from crewai import Task

def planner_Task(study_planner_agent,planner_callback_function):
    planner_task = Task(
        description='Prepare steps to achieve the goal of learning {topic} within {duration}.The title should not be more than 5 words and it should be such that it should be wasy to search it on internet',
        expected_output='A json response where the keys are Day Numbers and values are the titles of important things to study.',
        agent=study_planner_agent,
        callback=planner_callback_function,
        output_file='outputs/studyplan.json',
        create_directory=True
    )
    return planner_task