import requests
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.prompts import PromptTemplate
import pandas as pd
import json
load_dotenv()


def request_video(topic: str, api_key: str):
    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': topic,
        'type': 'video',
        'maxResults': 5,
        'videoCaption': 'closedCaption',  # Filter for videos with captions
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    result = response.json()
    video_links = []
    for item in result.get('items', []):
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_links.append(video_url)
    return {topic: video_links}



def get_related_videos(study_plan, api_key: str):
    study_topics = list(study_plan.values())
    video_links = []
    for topic in study_topics:
        video = request_video(topic, api_key)
        video_links.append(video)
    return video_links



def make_df_for_videos(video_data):
  keys = []
  values = []
  for dic in video_data:
    for k,v in dic.items():
      keys.append(k)
      values.append(v)
  df = pd.DataFrame({'Title':keys,'Videos':values})
  df.to_csv('final_outputs/videos/1_youtube_api_return_df.csv')
  return df



def extract_video_id(video_link):
  """Extracts the video ID from a YouTube video link."""
  video_id = video_link.split("v=")[1]
  return video_id



def request_data_using_api(video_id):
  """Requests transcript data for a YouTube video using the YouTube Transcript API.

  Handles potential exceptions like disabled subtitles and generic errors.
  """
  try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
  except Exception as e:
    if "Subtitles are disabled for this video" in str(e):
      transcript = 'Subtitles are disabled for this video'
    else:
      transcript = f'An unexpected error occurred: {e}'
  return transcript




def extract_text(transcript):
  """Extracts text from the transcript data.

  If the transcript is a list, iterates through each dictionary and concatenates the text.
  Handles cases where the transcript is not a list (e.g., error message).

  Returns the first 1500 words of the extracted text and the full transcript.
  """
  if isinstance(transcript, list):
    video_text = ''
    word_count = 0
    for dictionary in transcript:
      data = dictionary['text'].strip()  # Remove leading/trailing whitespace
      words = data.split()
      word_count += len(words)
      video_text += ' '.join(words) + ' '  # Add space between sentences
      if word_count >= 1000:
        break
    return video_text, transcript
  else:
    video_text = ''
    return video_text, transcript



def return_first_1000_words(video_link):
  """Returns the first 1000 words of the transcript text and the full transcript.

  Calls the helper functions to extract video ID, request transcript data,
  and extract the desired portion of the text.
  """
  video_id = extract_video_id(video_link)
  transcript = request_data_using_api(video_id)
  first_1000_words, full_transcript = extract_text(transcript)
  return first_1000_words, full_transcript

def prepare_data_for_best_video(video_df):
    # Initialize the dictionary to store the results
    result_dict = {}
    selecting_video = video_df[['Title', 'Videos']].to_dict('records')

    # Loop through each blog entry
    for dic in selecting_video:
        title = dic['Title']
        urls = dic['Videos']  # Assuming URLs are comma-separated strings

        # Initialize list to hold content for each URL under the same topic
        content_list = []

        for url in urls:
            url = url.strip()  # Remove any extra whitespace
            first_1500_words, full_transcript = return_first_1000_words(url)
            # Add the URL and extracted content to the content list
            content_list.append({url: first_1500_words})

        # Store the result in the dictionary
        result_dict[title] = content_list

    with open('final_outputs/videos/2_prepare_data_for_best_video.json', 'w') as json_file:
        json.dump(result_dict, json_file)

    result_list = []
    for title, contents in result_dict.items():
        for content in contents:
            for url, text in content.items():
                result_list.append({'Title': title, 'URL': url, 'Content': text})

    result_df = pd.DataFrame(result_list)
    result_df.to_csv('final_outputs/videos/2_prepare_data_for_best_video.csv', index=False)
    print('SELECTING BEST Youtbe SUCCESFLLY RUNED')
    return result_dict


def finding_best_video(study_plan, gemini_llm, BestURL, distraction_tolerance=5):
    video_data = get_related_videos(study_plan, os.getenv('YOUTUBE_API_KEY'))
    video_df = make_df_for_videos(video_data)
    result_dict = prepare_data_for_best_video(video_df)
    structured_llm = gemini_llm.with_structured_output(BestURL)

    template = PromptTemplate(
        input_variables=['topic', 'distraction_tolerance', 'content'],
        template="Select the best 1 url on the topic {topic} by analyzing the {content}"
    )

    best_video_urls = {}

    for topic, content in result_dict.items():
        prompt = template.format(topic=topic, distraction_tolerance=distraction_tolerance, content=content)

        try:
            response = structured_llm.invoke(prompt)

            if response:
                if response.url.startswith("https://www.youtube.com/watch?"):
                    best_video_urls[topic] = {'Title': response.Title, 'youtube_url': response.url}
                else:
                    pass  # Handle non-YouTube URLs if necessary
            else:
                best_video_urls[topic] = {'Title': topic, 'youtube_url': list(content[0].keys())[0]}
        except Exception as e:
            pass  # Handle exceptions if necessary

    best_video_urls_list = list(best_video_urls.values())
    df = pd.DataFrame(best_video_urls_list)
    df.to_csv('final_outputs/videos/3_best_video_urls.csv', index=False)
    print('BEST VIDEO URLS SUCCESSFULLY RUN')

    return df
