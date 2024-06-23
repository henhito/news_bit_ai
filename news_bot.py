import os
from crewai import Agent, Task, Crew
from langchain_community.tools import DuckDuckGoSearchRun
import openai

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

# Function to summarize text using GPT-4
def summarize_with_gpt4(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in summarizing and analyzing text."},
            {"role": "user", "content": text}
        ],
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message['content']

# Define your agents with roles and goals
search_tool = DuckDuckGoSearchRun()

researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in AI and data science',
    backstory="""You work at a leading tech think tank.
    Your expertise lies in identifying emerging trends.
    You have a knack for dissecting complex data and presenting actionable insights.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool]
)

writer = Agent(
    role='Tech Content Strategist',
    goal='Craft compelling content on tech advancements',
    backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
    You transform complex concepts into compelling narratives.""",
    verbose=True,
    allow_delegation=True
)

seo_agent = Agent(
    role='SEO Specialist',
    goal='Optimize content for search engines to ensure maximum visibility and engagement',
    backstory="""You are an expert in SEO with a deep understanding of search engine algorithms and strategies to optimize content for better rankings.""",
    verbose=True,
    allow_delegation=True
)

# Create tasks for your agents
task1 = Task(
    description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
    Identify key trends, breakthrough technologies, and potential industry impacts.""",
    expected_output="Full analysis report in bullet points",
    agent=researcher
)

task2 = Task(
    description="""Using the insights provided, develop an engaging blog
    post that highlights the most significant AI advancements.
    Your post should be informative yet accessible, catering to a tech-savvy audience.
    Make it sound cool, avoid complex words so it doesn't sound like AI.""",
    expected_output="Full blog post of at least 4 paragraphs",
    agent=writer
)

task3 = Task(
    description="""Optimize the blog post for search engines to ensure it reaches a wider audience.
    Implement SEO best practices including keyword optimization, meta descriptions, and internal linking.""",
    expected_output="SEO-optimized blog post",
    agent=seo_agent
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[researcher, writer, seo_agent],
    tasks=[task1, task2, task3],
    verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Kickoff the crew to work
result = crew.kickoff()

print("-----------------------------")
print(result)
