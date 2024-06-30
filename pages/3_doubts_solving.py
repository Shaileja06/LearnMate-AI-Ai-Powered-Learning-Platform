import streamlit as st
from src.rag.ragfile import initialize_system, answer_query

# Get query parameters
query_params = st.experimental_get_query_params()
title = query_params.get("title", [""])[0]
blog_url = query_params.get("blog_url", [""])[0]
youtube_url = query_params.get("youtube_url", [""])[0]

st.title(f"Solve Doubt on {title}")
st.write(f"**Blog URL**: {blog_url}")
st.write(f"**YouTube URL**: {youtube_url}")
retrieval_chain = initialize_system(blog_url, youtube_url)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Answer the query
    answer = answer_query(retrieval_chain, prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(answer)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})
