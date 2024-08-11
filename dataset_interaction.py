# from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
# from langchain_google_vertexai import ChatVertexAI
# import pandas as pd
# import dotenv
# import streamlit as st
# from typing_extensions import TypedDict
#
# dotenv.load_dotenv()
# model = ChatVertexAI(model="gemini-1.5-flash")
#
# df = pd.read_csv("./failure_predictions_1.csv")
# agent = create_pandas_dataframe_agent(model, df, verbose=False, allow_dangerous_code=True)
#
# class State(TypedDict):
#     messages: list
#     ask_human: bool
#
# st.title("CAT Machinery Dataset")
#
# if "state" not in st.session_state:
#     st.session_state.state = State(messages=[""""""], ask_human=False)
#
# user_input = st.text_input("Ask the CAT dataset anything about your machines")
#
# if st.button("Send"):
#     if user_input:
#         output = agent.invoke(f"{user_input}")['output']

#***************************************************************************************************8

from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_google_vertexai import ChatVertexAI
import pandas as pd
import dotenv
import streamlit as st
from typing_extensions import TypedDict

# Load environment variables
dotenv.load_dotenv()

# Initialize the AI model
model = ChatVertexAI(model="gemini-1.5-flash")

# Load the dataset
df = pd.read_csv("./failure_predictions_1.csv")

# Create the agent with the DataFrame
agent = create_pandas_dataframe_agent(model, df, verbose=True, allow_dangerous_code=True)


# Define the state for the chat interface
class State(TypedDict):
    messages: list
    ask_human: bool


# Set up the Streamlit interface
st.title("CAT Machinery Dataset")

# Initialize the state if not already in session
if "state" not in st.session_state:
    st.session_state.state = State(messages=[], ask_human=False)

# Text input for user queries
user_input = st.text_input("Ask the CAT dataset anything about your machines")

# Send button to process the user input
if st.button("Send"):
    if user_input:
        # Append the user's question to the message history
        st.session_state.state['messages'].append(f"User: {user_input}")

        # Invoke the agent with the user query
        output = agent.invoke(f"{user_input}")['output']

        # Append the agent's response to the message history
        st.session_state.state['messages'].append(f"Agent: {output}")

# Display the chat history
for message in st.session_state.state['messages']:
    st.write(message)















