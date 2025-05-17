import streamlit as st
st.title("StreamLit ChatBot")
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os
os.environ["GOOGLE_API_KEY"]=st.secrets["GOOGLE_API_KEY"]
# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Streamlit page config
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("💬 Gemini Chatbot")
st.write("Type something to begin chatting with Gemini!")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content="You are a helpful assistant.")]

# Display previous messages
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# User input
if prompt := st.chat_input("Say something..."):
    # Add user message to history
    st.session_state.chat_history.append(HumanMessage(content=prompt))

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get model response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = llm.invoke(st.session_state.chat_history)
            st.markdown(result.content)
            st.session_state.chat_history.append(AIMessage(content=result.content))
