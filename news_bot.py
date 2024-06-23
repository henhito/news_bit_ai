import os
from crewai import Agent, Task, Crew, Process
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

# Define the search tool
search = DuckDuckGoSearchRun()

# Define the agents
researcher = Agent(
    role="Senior Research Analyst",
    goal="""Uncover the latest trends and developments in the accounting and business sectors relevant to small businesses,
            with a focus on financial understanding, clarity, and overcoming growth challenges and how Bean Sprout could
            help ambitious business owners to grow their business using our Numbers, Narrative, and Nurture approach.""",
    verbose=True,
    tools=[search],
    allow_delegation=False,
    backstory="""You work at Bean Sprout, a consultancy firm for small businesses. Your expertise lies in identifying emerging
                trends and providing actionable insights to help small businesses thrive in a competitive market. You emphasize
                Bean Sprout’s commitment to exceptional financial business coaching and personalized solutions."""
)

writer = Agent(
    role="Tech Content Strategist",
    goal="Craft compelling and informative content that showcases the latest tech advancements and business strategies beneficial to small businesses, while reflecting Bean Sprout’s core values of clarity, confidence, and overcoming challenges.",
    verbose=True,
    allow_delegation=True,
    backstory="""As a renowned Content Strategist at Bean Sprout, you are known for your insightful and engaging articles. You excel in transforming complex concepts into compelling narratives that resonate with small business owners, ensuring the content aligns with Bean Sprout’s values and mission."""
)

seo_agent = Agent(
    role="SEO Specialist",
    goal="Optimize content for search engines to ensure maximum visibility and engagement, highlighting Bean Sprout’s unique value proposition.",
    verbose=True,
    allow_delegation=True,
    backstory="""You are an expert in SEO at Bean Sprout with a deep understanding of search engine algorithms and strategies to optimize content for better rankings. You focus on ensuring that the content reaches a wider audience, driving more traffic to Bean Sprout’s website while emphasizing their mission and values."""
)

editor = Agent(
    role="Content Editor",
    goal="Ensure the content is polished, coherent, and aligns with Bean Sprout’s brand voice, core values, and mission.",
    verbose=True,
    allow_delegation=False,
    backstory="""You are a skilled editor at Bean Sprout, dedicated to maintaining the quality and consistency of all published content. You have a keen eye for detail and a strong understanding of the company’s brand voice, ensuring that every piece of content reflects Bean Sprout’s commitment to exceptional financial coaching and personalized business solutions."""
)

# Define the tasks
research_task = Task(
    description="Conduct a comprehensive analysis of the latest trends and developments in the UK business sectors relevant to small businesses.",
    agent=researcher,
    expected_output="Full analysis report in bullet points",
)

writing_task = Task(
    description="Using the insights provided, develop an engaging blog post that highlights the most significant trends and strategies beneficial to small businesses.",
    agent=writer,
    expected_output="Full blog post of at least 4 paragraphs",
)

seo_task = Task(
    description="Optimize the blog post for search engines to ensure it reaches a wider audience. Implement SEO best practices including keyword optimization, meta descriptions, and internal linking.",
    agent=seo_agent,
    expected_output="SEO-optimized blog post",
)

editing_task = Task(
    description="Review the blog post to ensure it is polished, coherent, and aligns with Bean Sprout’s brand voice. Make necessary edits and adjustments.",
    agent=editor,
    expected_output="Final edited blog post ready for publication",
)

# Instantiate the crew with a sequential process
crew = Crew(
    agents=[researcher, writer, seo_agent, editor],
    tasks=[research_task, writing_task, seo_task, editing_task],
    verbose=True,
    process=Process.sequential,
)

# Execute the tasks
result = crew.kickoff()

print("-----------------------------")
print(result)

# Summarize the results
#if isinstance(result, list):
#    for res in result:
#        if 'content' in res:
#            summarized_result = summarize_with_gpt4(res['content'])
#            print(summarized_result)
#else:
#    summarized_result = summarize_with_gpt4(result)
#    print(summarized_result)
