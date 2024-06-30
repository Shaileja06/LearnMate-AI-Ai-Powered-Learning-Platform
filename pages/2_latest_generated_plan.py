import pandas as pd
import streamlit as st
from streamlit_player import st_player

output = pd.read_csv('final_outputs/final_df.csv')

# Displaying the study plan and output
st.header("Your Study Plan")

for i, row in enumerate(output.iterrows(), start=1):
    st.subheader(f"Day {i}: {row[1]['Title']}")
    st.write(f"**Blog**: {row[1]['blog_url']}")
    st.write(f"**Video**: {row[1]['youtube_url']}")
    
    # Display video with unique key
    st_player(str(row[1]['youtube_url']).strip(), key=f"video_{i}")
    
    # Create columns for buttons
    col1, col2 = st.columns(2)
    
    with col1:
        solve_doubts = st.button(f'Solve Doubts {i}', key=f'solve_{i}')
    with col2:
        take_test = st.button(f'Take Test {i}', key=f'test_{i}')
    
    # Check if Solve Doubts button is clicked
    if solve_doubts:
        title = row[1]['Title']
        blog_url = row[1]['blog_url']
        youtube_url = row[1]['youtube_url']

        # Redirect to the next page with parameters
        st.markdown(f'<a href="https://8501-01j1fn3yqsg5xbvybfsgw8p2kh.cloudspaces.litng.ai/doubts_solving?title={title}&blog_url={blog_url}&youtube_url={youtube_url}" target="_self">Solve Doubts</a>', unsafe_allow_html=True)

    # Check if Take Test button is clicked
    if take_test:
        title = row[1]['Title']
        blog_url = row[1]['blog_url']
        youtube_url = row[1]['youtube_url']
        
        # Redirect to the next page with parameters
        st.markdown(f'<a href="https://8501-01j1fn3yqsg5xbvybfsgw8p2kh.cloudspaces.litng.ai/rag?title={title}&blog_url={blog_url}&youtube_url={youtube_url}" target="_self">Take Test</a>', unsafe_allow_html=True)

    st.markdown("---")
