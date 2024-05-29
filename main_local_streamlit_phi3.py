import os
# from constant import openai_key  # Ensure you have this constant defined with your OpenAI key
# from langchain.llms import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
import streamlit as st

import time


prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please respond to the user queries"),
        ("user","Question:{question}")
    ]
)

st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center; height: 100vh;">
        <h1 style="font-family: Arial, sans-serif; font-size: 48px; font-weight: bold;">CozBot</h1>
    </div>
    """,
    unsafe_allow_html=True
)



llm = Ollama(model = "phi3")
output_parser=StrOutputParser()
chain = prompt|llm|output_parser

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        
        response = chain.invoke({
            "question": user_input
        })
        st.markdown(response)
        
        # for line in response.splitlines():
        #     st.markdown(line)
        #     # Optional delay for dramatic effect
        #     time.sleep(0.2)
        

    st.session_state.messages.append({"role": "assistant", "content": response})
