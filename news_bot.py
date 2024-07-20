import os
from crewai import Agent, Task, Crew
from langchain_community.tools import DuckDuckGoSearchRun
import openai
from agent_config import (
    political_analyst_goal, fact_checker_goal, content_strategist_goal,
    blog_writer_goal, seo_specialist_goal, editor_goal,
    political_analyst_backstory, fact_checker_backstory, content_strategist_backstory,
    blog_writer_backstory, seo_specialist_backstory, editor_backstory,
    political_analyst_task_description, political_analyst_task_expected_output,
    fact_checker_task_description, fact_checker_task_expected_output,
    content_strategist_task_description, content_strategist_task_expected_output,
    blog_writer_task_description, blog_writer_task_expected_output,
    seo_specialist_task_description, seo_specialist_task_expected_output,
    editor_task_description, editor_task_expected_output
)

# Function to read API keys from config file
def read_config(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip():
                    key, value = line.strip().split('=')
                    os.environ[key] = value.strip('"')
    except Exception as e:
        print(f"Error reading config file: {e}")

# Read the API key from config.txt
config_file_path = "config.txt"
read_config(config_file_path)

# Ensure the OpenAI API key is set
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    openai.api_key = openai_api_key
else:
    raise ValueError("OpenAI API key is not set. Please check your config.txt file.")

# Define agents for the blog article crew
search_tool = DuckDuckGoSearchRun()

political_analyst = Agent(
    role='Political Analyst',
    goal=political_analyst_goal,
    backstory=political_analyst_backstory,
    verbose=True,
    allow_delegation=False,
    tools=[search_tool]
)

fact_checker = Agent(
    role='Fact Checker',
    goal=fact_checker_goal,
    backstory=fact_checker_backstory,
    verbose=True,
    allow_delegation=False
)

content_strategist = Agent(
    role='Content Strategist',
    goal=content_strategist_goal,
    backstory=content_strategist_backstory,
    verbose=True,
    allow_delegation=True
)

blog_writer = Agent(
    role='Blog Writer',
    goal=blog_writer_goal,
    backstory=blog_writer_backstory,
    verbose=True,
    allow_delegation=True
)

seo_specialist = Agent(
    role='SEO Specialist',
    goal=seo_specialist_goal,
    backstory=seo_specialist_backstory,
    verbose=True,
    allow_delegation=True
)

editor = Agent(
    role='Editor',
    goal=editor_goal,
    backstory=editor_backstory,
    verbose=True,
    allow_delegation=False
)

# Define tasks for the blog article crew
task1 = Task(
    description=political_analyst_task_description,
    expected_output=political_analyst_task_expected_output,
    agent=political_analyst
)

task2 = Task(
    description=fact_checker_task_description,
    expected_output=fact_checker_task_expected_output,
    agent=fact_checker
)

task3 = Task(
    description=content_strategist_task_description,
    expected_output=content_strategist_task_expected_output,
    agent=content_strategist
)

task4 = Task(
    description=blog_writer_task_description,
    expected_output=blog_writer_task_expected_output,
    agent=blog_writer
)

task5 = Task(
    description=seo_specialist_task_description,
    expected_output=seo_specialist_task_expected_output,
    agent=seo_specialist
)

task6 = Task(
    description=editor_task_description,
    expected_output=editor_task_expected_output,
    agent=editor
)

# Instantiate the blog article crew
blog_article_crew = Crew(
    agents=[political_analyst, fact_checker, content_strategist, blog_writer, seo_specialist, editor],
    tasks=[task1, task2, task3, task4, task5, task6],
    verbose=2
)

# Execute the blog article crew's tasks
try:
    result = blog_article_crew.kickoff()
    print("-----------------------------")
    print("Blog Article Creation Phase Completed")
    print(result)
except openai.error.OpenAIError as e:
    print(f"OpenAI API error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
