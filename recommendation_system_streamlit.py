from typing import Annotated, Literal
import dotenv

from langchain_google_vertexai import ChatVertexAI

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.pydantic_v1 import BaseModel
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

dotenv.load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]
    ask_human: bool


class RequestAssistance(BaseModel):
    """Escalate the conversation to an expert. Use this if you are unable to assist directly or if the user requires support beyond your permissions.

    To use this function, relay the user's 'request' so the expert can provide the right guidance.
    """
    request: str


tool = TavilySearchResults(max_results=7)
tools = [tool]
llm = ChatVertexAI(model="gemini-1.5-flash")
# We can bind the llm to a tool definition, a pydantic model, or a json schema
llm_with_tools = llm.bind_tools(tools + [RequestAssistance])


def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    ask_human = False
    if (
        response.tool_calls
        and response.tool_calls[0]["name"] == RequestAssistance.__name__
    ):
        ask_human = True
    return {"messages": [response], "ask_human": ask_human}


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=[tool]))


def create_response(response: str, ai_message: AIMessage):
    return ToolMessage(
        content=response,
        tool_call_id=ai_message.tool_calls[0]["id"],
    )


def human_node(state: State):
    new_messages = []
    if not isinstance(state["messages"][-1], ToolMessage):
        # Typically, the user will have updated the state during the interrupt.
        # If they choose not to, we will include a placeholder ToolMessage to
        # let the LLM continue.
        new_messages.append(
            create_response("No response from human.", state["messages"][-1])
        )
    return {
        # Append the new messages
        "messages": new_messages,
        # Unset the flag
        "ask_human": False,
    }


graph_builder.add_node("human", human_node)


def select_next_node(state: State) -> Literal["human", "tools", "__end__"]:
    if state["ask_human"]:
        return "human"
    # Otherwise, we can route as before
    return tools_condition(state)


graph_builder.add_conditional_edges(
    "chatbot",
    select_next_node,
    {"human": "human", "tools": "tools", "__end__": "__end__"},
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("human", "chatbot")
graph_builder.add_edge(START, "chatbot")
memory = MemorySaver()
graph = graph_builder.compile(
    checkpointer=memory,
    interrupt_before=["human"],
)

import streamlit as st
from typing_extensions import TypedDict


class State(TypedDict):
    messages: list
    ask_human: bool


st.title("CAT Machinery Support Chatbot")
if "state" not in st.session_state:
    st.session_state.state = State(messages=["""You are a specialised chatbot for the construction company caterpillar or commonly known as CAT. You will be asked questions regarding issues in machinery for which you must always search the web and give machine specific answers. Make sure to always return a comprehensive response that may be of some or the other use to the user. Your answer must be of the following format:

Possible Reasons:
1. Reason 1
2. Reason 2

Possible Fixes:
1. Fix 1
2. Fix 2"""], ask_human=False)

user_input = st.text_input("Ask the CAT chatbot about your machinery issues:")

if st.button("Send"):
    if user_input:
        st.session_state.state["messages"].append(user_input)

    config = {"configurable": {"thread_id": "5"}}
    events = graph.stream(
        {
            "messages": [
                ("system", """You are a specialised chatbot for the construction company caterpillar or commonly known as CAT. You will be asked questions regarding issues in machinery for which you must always search the web and give machine specific answers. Make sure to always return a comprehensive response that may be of some or the other use to the user. Your answer must be of the following format:

Possible Reasons:
1. Reason 1
2. Reason 2

Possible Fixes:
1. Fix 1
2. Fix 2"""),
                ("user", f"{user_input}")
            ]
        },
        config,
        stream_mode="values",
    )

    for event in events:
        if "messages" in event:
            response_message = event["messages"][-1].content
            st.session_state.state["messages"].append(event["messages"][-1])
            st.write(response_message)


