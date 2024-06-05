import streamlit as st
import numpy as np
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
import base64
import datetime

DB_FAISS_PATH = r"db"
img_path = r".\logo\logo2.png"

custom_prompt_template = """Use the following pieces of information to answer the user's question.
your name is COZBOT.you are very good at greeting people in a helpful and respectful manner and give good responses when someone ends the conversation.
please don't give any extra information as response apart from the user's question.
If you don't know the answer, just say that you don't know in a respectful and helpful manner, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
"""


def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=custom_prompt_template,
                             input_variables=['context', 'question'])
    return prompt


# Loading the model (load outside function for caching)
llm = Ollama(model='llama2')
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                    model_kwargs={'device': 'cpu'})


def qa_bot():
    # Load FAISS index once
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

    qa_prompt = set_custom_prompt()
    qa = RetrievalQA.from_chain_type(llm=llm,
                                     chain_type='stuff',
                                     retriever=db.as_retriever(search_kwargs={'k': 2}),
                                     return_source_documents=True,
                                     chain_type_kwargs={'prompt': qa_prompt}
                                     )
    return qa


# Response cache (consider adding expiration)
response_cache = {}


def final_result(query):
    if query in response_cache:
        return response_cache[query]

    qa_result = qa_bot()
    response = qa_result.invoke({'query': query})
    response_cache[query] = response
    return response


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# Streamlit UI
st.set_page_config(page_title="CozBot", page_icon=":robot_face:")

img_base64 = get_base64_of_bin_file(img_path)

# Add CSS for fixed header
st.markdown(
    """
    <style>
    .fixed-title {
        position: fixed;
        top: 20px;
        width: 50%;
        background-color: white;
        z-index: 999991;
        /*padding:30px 10px;*/
        box-shadow: 0 ;
    }
    .main-content {
        padding-top: 50px;
        z-index: 1; 
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Fixed title with logo
st.markdown(
    f'<div class="fixed-title"><img src="data:image/png;base64,{img_base64}" style="height: 50px; margin-right: 10px;"></div>',
    unsafe_allow_html=True
)

# Main content with padding
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Initialize session state




if "messages" not in st.session_state:
    st.session_state.messages = []

    # Personalize greeting based on time of day
    current_time = st.session_state.get("current_time", None)  # Cache time for efficiency

    if not current_time:
        current_time = datetime.datetime.now().hour

    if 5 <= current_time < 12:
        greeting = "Good morning!"
    elif 12 <= current_time < 17:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"

    st.session_state.messages.append({"role": "assistant", "content": greeting + " Welcome to CozBot! How can I assist you today?"})

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input and responses
if user_input := st.chat_input("Hello?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    print(user_input)

    with st.spinner('Thinking ...'):
        response = final_result(user_input)

    with st.chat_message("assistant"):
        st.markdown(response['result'])
        st.session_state.messages.append({"role": "assistant", "content": response['result']})
    print(response['result'])

st.markdown('</div>', unsafe_allow_html=True)
