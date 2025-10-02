from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st

# Title
st.title("🤖 Lojan Chatbot 📝")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous chat messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if user_input := st.chat_input("Enter your query here..."):
    # Add user message to history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful AI Lojan's assistant."),
            ("user", "{query}")
        ]
    )

    # Ollama LLM
    llm = Ollama(model="llama2")
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    # Streaming output
    with st.chat_message("assistant"):
        placeholder = st.empty()
        response_text = ""
        for chunk in chain.stream({"query": user_input}):
            response_text += chunk
            placeholder.markdown(response_text + "▌")  # typing effect

        placeholder.markdown(response_text)  # final response

    # Save bot response to history
    st.session_state["messages"].append({"role": "assistant", "content": response_text})
