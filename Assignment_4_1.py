# Link to server
# https://assignment41-avbmtotvaktlgvaek6lar2.streamlit.app/


import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

serper_dev_api_key = os.getenv('SERPER_DEV_API_KEY')

def get_news_summary(personality):
    """Fetches recent news articles about a personality and generates a summary."""
    SEARCH_URL = "https://google.serper.dev/search"
    
    headers = {
        "X-API-KEY": serper_dev_api_key,
        "Content-Type": "application/json"
    }
    
    payload = json.dumps({"q": personality})
    response = requests.post(SEARCH_URL, headers=headers, data=payload)
    
    if response.status_code != 200:
        return "Error fetching news. Please try again later."
    
    response_dict = response.json()
    articles = response_dict.get("organic", [])
    
    if not articles:
        return "No recent news found for this personality."
    
    links_summary = ""
    article_content = ""
    
    for i, article in enumerate(articles[:5]):  # Fetching top 5 articles
        title = article.get("title", "No Title")
        snippet = article.get("snippet", "No Summary Available")
        link = article.get("link", "#")
        
        links_summary += f"**{title}**\n{snippet}\n[Read more]({link})\n\n"
        article_content += f"{snippet} "
    
    # Creating a 3-paragraph article
    paragraphs = article_content.split('. ')
    article_text = "\n\n".join([". ".join(paragraphs[i:i+3]) for i in range(0, len(paragraphs), 3)])
    
    return links_summary + "\n### Summary Article\n" + article_text

def main():
    st.title("News Summarizer Bot")
    st.write("Enter a personality's name to get the most recent news summarized in an article.")
    
    personality = st.text_input("Personality Name:")
    
    if st.button("Get News Summary"):
        if personality:
            with st.spinner("Fetching latest news..."):
                summary = get_news_summary(personality)
                st.markdown(summary)
        else:
            st.warning("Please enter a personality's name.")

if __name__ == "__main__":
    main()

