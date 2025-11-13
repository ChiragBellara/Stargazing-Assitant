# ConversationBufferWindowMemeory using RunnabelMessageHistory
from pydantic import BaseModel, Field
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage


HISTORY_MAP = {}


class BufferWindowMessageHistory(BaseChatMessageHistory, BaseModel):
    messages: list[BaseMessage] = Field(default_factory=list)
    k: int = Field(default_factory=int)

    def __init__(self, k: int):
        super().__init__(k=k)
        print(f"Initialization BufferWindowMessageHistory with k = {k}")

    def add_messages(self, messages: list[BaseMessage]) -> None:
        # Add new messages to the message history, removing any messages that fall beyond the k boundary
        self.messages.extend(messages)
        self.messages = self.messages[-self.k:]

    def clear(self) -> None:
        # Clear the message history
        self.messages = []


def get_chat_history(session_id: str, k: int) -> BufferWindowMessageHistory:
    if session_id not in HISTORY_MAP:
        HISTORY_MAP[session_id] = BufferWindowMessageHistory(k=k)
    return HISTORY_MAP[session_id]
