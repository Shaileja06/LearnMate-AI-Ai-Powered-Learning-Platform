import pandas as pd
from langchain_community.tools.tavily_search import TavilySearchResults
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd
import re
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
import time
import json

class BestURL(BaseModel):
  """Best Url """
  Title: str = Field(description="The name of the title")
  url: str = Field(description="the best url among the urls")

class SimpleDocument:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}

def get_related_blogs(study_plan):
  tavilytool = TavilySearchResults()
  final_output = {}
  for day,title in study_plan.items():
    search_query = f"Find Relevant blogs for {title}"
    search_results = tavilytool.invoke(search_query)  # Ensure tavilytool is properly initialized
    blogs = [result['url'] for result in search_results]  # Extract URLs from search results
    final_output[title] = blogs
  df = pd.DataFrame()
  df['Day'] = list(study_plan.keys())
  df['Title'] = list(study_plan.values())
  df['Blogs'] = list(final_output.values())
  df.to_csv('final_outputs/blogs/1_get_related_blogs.csv')
  print('Get Related Blogs Success Fully Runed')
  return df

def scrape_blog(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    else:
        return ""

def clean_text(text):
    # Remove extra whitespaces
    cleaned_text = ' '.join(text.split())

    # Remove HTML artifacts
    cleaned_text = BeautifulSoup(cleaned_text, "html.parser").get_text()

    # Remove non-textual content (if any)
    cleaned_text = re.sub(r'\[[^\]]*\]', '', cleaned_text)  # Remove text within square brackets
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', cleaned_text)
    return cleaned_text.strip()

def selecting_best_blog(blog_df):
    # Initialize the dictionary to store the results
    result_dict = {}

    # Convert the dataframe to a list of dictionaries
    selecting_blog = blog_df[['Title', 'Blogs']].to_dict('records')

    # Loop through each blog entry
    for dic in selecting_blog:
        title = dic['Title']
        urls = dic['Blogs'] # Assuming URLs are comma-separated strings

        # Initialize list to hold content for each URL under the same topic
        content_list = []

        for url in urls:
            url = url.strip()  # Remove any extra whitespace
            if url:  # Ensure URL is not empty
                # Scrape the content
                full_text = scrape_blog(url)

                # Create a SimpleDocument object
                doc = SimpleDocument(page_content=full_text)

                # Split the documents to get the first 2500 words
                ts = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
                fd = ts.split_documents([doc])

                # Store only the first chunk (first 2500 words)
                first_2500_words = clean_text(fd[0].page_content) if fd else ""

                # Add the URL and extracted content to the content list
                content_list.append({url: first_2500_words})

        # Store the result in the dictionary
        result_dict[title] = content_list
    with open('final_outputs/blogs/2_selecting_best_blogs.json', 'w') as json_file:
        json.dump(result_dict, json_file)

    result_list = []
    for title, contents in result_dict.items():
        for content in contents:
            for url, text in content.items():
                result_list.append({'Title': title, 'URL': url, 'Content': text})

    result_df = pd.DataFrame(result_list)
    result_df.to_csv('final_outputs/blogs/2_selecting_best_blogs.csv', index=False)
    print('SELECTING BEST BLOGS SUCCESFLLY RUNED')
    return result_dict



def finding_best_blog(study_plan, gemini_llm, BestURL, distraction_tolerance=5):
    blog_df = get_related_blogs(study_plan)
    result = selecting_best_blog(blog_df)
    structured_llm = gemini_llm.with_structured_output(BestURL)
    template = PromptTemplate(
        input_variables=['topic', 'distraction_tolerance', 'content'],
        template="Select the best blog 1 url on the topic {topic} by analyzing the {content}"
    )

    best_video_urls = {}

    for topic, content in result.items():
        prompt = template.format(topic=topic, distraction_tolerance=distraction_tolerance, content=content)
        try:
            response = structured_llm.invoke(prompt)
            if response:
                if response.url.startswith("https://"):
                    best_video_urls[topic] = {'Title': response.Title, 'blog_url': response.url}
                else:
                    pass  # Handle non-YouTube URLs if necessary
            else:
                best_video_urls[topic] = {'Title': topic, 'blog_url': list(content[0].keys())[0]}
        except Exception as e:
            pass  # Handle exceptions if necessary

    best_blog_urls = list(best_video_urls.values())
    df = pd.DataFrame(best_blog_urls)
    df.to_csv('final_outputs/blogs/3_best_blog_urls.csv', index=False)
    print('BEST BLOG URLS SUCCESSFULLY RUN')

    return df
