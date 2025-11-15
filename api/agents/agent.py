import os
import streamlit as st
from dotenv import load_dotenv
from agents.prompt import SYSTEM_PROMPT
from langchain_core.runnables.history import RunnableWithMessageHistory
from agents.history import get_chat_history
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_agent
from agents.tools import fetch_weather

load_dotenv(override=True)

# Get the OPENAI_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def create_stars_agent():
    """Create the Stars agent with Streamlit-integrated memory"""

    try:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            timeout=60,
            max_retries=2
        )

        tools = [fetch_weather]

        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            # where memory will be injected
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            # where tool thoughts/actions go
            MessagesPlaceholder("agent_scratchpad"),
        ])

        agent = create_agent(llm, tools=tools, system_prompt=SYSTEM_PROMPT)

    except Exception as e:
        st.error(f"Failed to create agent: {str(e)}")
        return None
