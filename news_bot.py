import os
import requests
import openai
import json
from datetime import datetime
from crewai import Agent

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

# Fetch news articles using newsdata.io API
def fetch_news(topic):
    try:
        api_key = os.getenv("NEWSDATA_API_KEY")
        url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={topic}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

# Summarize the articles using OpenAI GPT-4
def summarize_article_with_openai(title, description, url):
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = openai_api_key
        prompt = (
            f"Title: {title}\n"
            f"Description: {description}\n"
            f"URL: {url}\n\n"
            "You are writing a summary for an accountancy firm that provides insights to its clients. "
            "The clients are small and medium-sized businesses and entrepreneurs interested in financial growth, tax regulations, "
            "economic changes, and business strategies. Summarize the article, highlighting the key points relevant to these interests and "
            "how it can impact their financial planning and business growth."
        )
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Specify the GPT-4 model
            messages=[
                {"role": "system", "content": "Summarize the following article."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    except Exception as e:
        print(f"Error summarizing article with OpenAI: {e}")
        return "Summary not available."

# Write data to a file
def write_to_file(filename, data):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error writing to file: {e}")

# Main logic
def main():
    config_file_path = "config.txt"
    read_config(config_file_path)

    topic = "budget uk"
    api_key = os.getenv("NEWSDATA_API_KEY")
    if not api_key:
        print("Error: NEWSDATA_API_KEY is not set")
        return

    # Fetch news articles
    print("Fetching news articles...")
    research_results = fetch_news(topic)
    if not research_results:
        print("No research results fetched.")
        return

    # Get current date and time for filenames
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Write raw API output to a file
    raw_filename = f"newsdata_raw_{now}.json"
    print(f"Writing raw data to {raw_filename}...")
    write_to_file(raw_filename, research_results)

    summaries = []
    print("Processing articles...")
    for article in research_results.get('results', []):
        try:
            title = article.get('title', 'No title')
            description = article.get('description', 'No description')
            url = article.get('link', 'No URL')
            if title and description and url:
                # Use OpenAI to summarize the article
                print(f"Summarizing article: {title}")
                summary = summarize_article_with_openai(title, description, url)
                summaries.append({"title": title, "summary": summary, "url": url})
            else:
                print(f"Missing information for article: {title}")
        except Exception as e:
            print(f"Error processing article: {title}, error: {e}")

    # Write all summaries to a file
    summary_filename = f"summaries_{now}.json"
    print(f"Writing summaries to {summary_filename}...")
    write_to_file(summary_filename, summaries)
    print("Finished writing summaries.")

if __name__ == "__main__":
    main()
