from agents.tools import fetch_weather
import os
from dotenv import load_dotenv
from agents.prompt import SYSTEM_PROMPT
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from agents.history import get_chat_history
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
import streamlit as st

load_dotenv(override=True)

# Get the OPENAI_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def create_stars_agent():
    """Create the Stars agent with Streamlit-integrated memory"""

    try:
        system_prompt = SystemMessage(cotent=SYSTEM_PROMPT)
    except Exception as e:
        st.error(f"Failed to create agent: {str(e)}")
        return None
