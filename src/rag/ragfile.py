import requests
from bs4 import BeautifulSoup
import re
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
import os
load_dotenv()
# Functions for scraping and cleaning
def scrape_blog(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    else:
        return ""

def clean_text(text):
    cleaned_text = ' '.join(text.split())
    cleaned_text = BeautifulSoup(cleaned_text, "html.parser").get_text()
    cleaned_text = re.sub(r'\[[^\]]*\]', '', cleaned_text)
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', cleaned_text)
    return cleaned_text.strip()

def get_transcript(youtube_url):
    video_id = youtube_url.split("v=")[1]
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = " ".join([item['text'] for item in transcript_list])
    return clean_text(transcript)

def prepare_data_for_rag(blog_url, youtube_url):
    blog_content = scrape_blog(blog_url)
    video_transcript = get_transcript(youtube_url)
    full_text = blog_content + " " + video_transcript
    full_text = full_text.replace('\n','')
    return full_text

def creating_chunks(full_text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=350,
        chunk_overlap=35,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_text(full_text)
    return chunks

def create_vec_db(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    docsearch = FAISS.from_texts(chunks, embeddings)
    return docsearch.as_retriever()

def create_prompt():
    prompt = ChatPromptTemplate.from_template("""
    Answer the following question based only on the provided context.
    Think step by step before providing a detailed answer.
    I will tip you $1000 if the user finds the answer helpful.
    <context>
    {context}
    </context>
    Question: {input}""")
    return prompt

def setup_chat_model():
    llm = ChatGroq(
        temperature=0,
        model="llama3-70b-8192",
        api_key=os.getenv('GROQ_API_KEY')
    )
    return llm

def create_document_chain(llm, prompt):
    document_chain = create_stuff_documents_chain(llm, prompt)
    return document_chain

def build_retrieval_chain(retriever, document_chain):
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    return retrieval_chain

def initialize_system(blog_url, youtube_url):
    full_text = prepare_data_for_rag(blog_url, youtube_url)
    chunks = creating_chunks(full_text)
    retriever = create_vec_db(chunks)
    llm = setup_chat_model()
    prompt = create_prompt()
    document_chain = create_document_chain(llm, prompt)
    retrieval_chain = build_retrieval_chain(retriever, document_chain)
    return retrieval_chain

def answer_query(retrieval_chain, query):
    response = retrieval_chain.invoke({"input": query})
    final_response = response['answer']
    return final_response

# Initialize the system (this step is done only once)
title = "Introduction to Deep Learning"
blog_url = "https://www.dataquest.io/blog/tutorial-introduction-to-deep-learning/"
youtube_url = "https://www.youtube.com/watch?v=aircAruvnKk"
retrieval_chain = initialize_system(blog_url, youtube_url)

# Answer a new query (this step can be repeated with different queries)
query = "What is it used for in deep learning?"
answer = answer_query(retrieval_chain, query)
print(answer)
