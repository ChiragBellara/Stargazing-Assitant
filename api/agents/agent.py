import os
import streamlit as st
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables.config import RunnableConfig

from agents.prompt import SYSTEM_PROMPT
from agents.tools import fetch_weather

load_dotenv()

MODEL_NAME = 'gpt-4o-mini'
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.0))


def create_stars_agent():
    """Create the Stars agent with Streamlit-integrated memory"""
    model = init_chat_model(MODEL_NAME, temperature=TEMPERATURE)
    checkpointer = InMemorySaver()

    agent = create_agent(
        model=model,
        tools=[fetch_weather],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer
    )

    return agent
