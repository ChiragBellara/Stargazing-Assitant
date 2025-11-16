import requests
from dotenv import load_dotenv
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables.config import RunnableConfig


load_dotenv()


@dataclass
class Context:
    user_id: str


@dataclass
class ResponseFormat:
    summary: str
    temperature_celsius: float
    temperature_fahrenheit: float
    humidity: float


# If return_direct is True, it means that the agent should return the output of this tool directly
@tool('get_weather', description="Return weather information for a given city", return_direct=False)
def get_weather(city: str):
    weather_url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(weather_url)
    return response.json()


@tool('locate_user', description="Look up a user's city based on the context", return_direct=False)
def locate_user(runtime: ToolRuntime[Context]):
    match runtime.context.user_id:
        case 'ABC123':
            return 'Mumbai'
        case 'XYZ567':
            return 'Los Angeles'
        case _:
            return 'Unknown'


model = init_chat_model('gpt-4o-mini', temperature=0.3)
checkpointer = InMemorySaver()

agent = create_agent(
    # Requires OPENAI_API_KEY present and Langchain OpenAI installed.
    model=model,
    tools=[get_weather, locate_user],
    system_prompt="You are a helpful weather assistant, who always cracks jokes and is humorous while being helpful.",
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

config: RunnableConfig = {'configurable': {'thread_id': 1}}
outcome = agent.invoke({
    'messages': [
        {'role': 'user', 'content': 'What is the weather like?'}
    ]},
    config=config,
    context=Context(user_id='XYZ567'))

print(outcome['structured_response'])
print("\n\n\n")
print(outcome['structured_response'].humidity)


# Simple Chat function with streaming
# model = init_chat_model(model='gpt-4o-mini', temperature=0.1)

# for chunk in model.stream('What is Python?'):
#     print(chunk.text, end='', flush=True)
