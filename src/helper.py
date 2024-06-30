import os
from dotenv import load_dotenv
import json
import pandas as pd
from crewai.task import TaskOutput
from crewai import Agent, Task, Crew
from src.crewaisection.agent import planner_Agent
from src.crewaisection.callbacks import planner_callback_function
from src.crewaisection.task import planner_Task
from crewai.process import Process
from src.crewaisection.crew import planner_Crew
from langchain_community.tools.tavily_search import TavilySearchResults
from src.extra.blogs import finding_best_blog, BestURL
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.prompts import PromptTemplate
from src.extra.youtube import finding_best_video

# Load environment variables
load_dotenv()

def load_env_variable():
    os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')
    os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
    os.environ["SERPER_API_KEY"] = os.getenv('SERPER_API_KEY')
    os.environ["GROQ_API_KEY"] = os.getenv('GROQ_API_KEY')
    os.environ["YOUTUBE_API_KEY"] = os.getenv('YOUTUBE_API_KEY')
    return 'LOADED'

def prepare_final_output(gemini_llm, data_input, distraction_tolerance=5):
    # Load Planner Agent
    study_planner_agent = planner_Agent(llm=gemini_llm, tools=[], max_iter=3)
    
    # Load Planner Task
    planner_task = planner_Task(study_planner_agent, planner_callback_function)
    
    # Load Crew Task
    study_plan = planner_Crew(study_planner_agent, planner_task, data_input)

    # Best Blog DataFrame
    blog_df = finding_best_blog(study_plan, gemini_llm, BestURL, distraction_tolerance)
    
    # Best Video DataFrame
    video_df = finding_best_video(study_plan, gemini_llm, BestURL, distraction_tolerance)
    
    # Merge DataFrames on 'Title'
    final_df = blog_df.merge(video_df, on='Title', how='inner')

    return study_plan, final_df
