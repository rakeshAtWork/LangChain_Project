import streamlit as st
import pickle
import faiss
import openai
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
import time
import base64

DB_FAISS_PATH = ""

# custom_prompt_template = """Use the following pieces of information to answer the user's question.
# If you don't know the answer, just say that you don't know, don't try to make up an answer.

# Context: {context}
# Question: {question}

# Only return the helpful answer below and nothing else.
# Helpful answer:
# """

custom_prompt_template = """Use the following pieces of information to answer the user's question.
your name is COZBOT.you are very good at greeting people in a helpful and respectful manner and give good responses when someone ends the conversation.
please don't give any extra information as response apart from the user's question.
If you don't know the answer, just say that you don't know in a respectful and helpful manner, don't try to make up an answer.
 
Context: {context}
Question: {question}
 
Only return the helpful answer below and nothing else.
Helpful answer:
"""


def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'question'])
    
    # prompt = prompt_t
    return prompt

# Retrieval QA Chain
def retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=db.as_retriever(search_kwargs={'k': 2}),
                                       return_source_documents=True,
                                       chain_type_kwargs={'prompt': prompt}
                                       )
    return qa_chain


# Loading the model
def load_llm():
    llm = Ollama(model='llama3')
    return llm


# QA Model Function
def qa_bot():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    print("Embedding finished")
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    print("embedding loaded")
    llm = load_llm()
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)
    print("retrieval chain created")
    return qa

# Output function
def final_result(query):
    qa_result = qa_bot()
    response = qa_result.invoke({'query': query})
    print("Response Result.")
    return response

# Streamlit UI
st.set_page_config(page_title="CozBot", page_icon=":robot_face:")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Add CSS for fixed header
st.markdown(
    """
    <style>
    .fixed-title {
        position: fixed;
        top: 0;
        width: 50%;
        background-color: white;
        z-index: 100;
        padding:30px 10px;
        box-shadow: 0 ;
    }
    .main-content {
        padding-top: 50px;
    }
    
      [data-testid="ScrollToBottomContainer"]{
             background-image: url("data:image/png;base64,{img_base64}");
             background-size: cover;
             background-repeat: no-repeat;
             background-attachment: fixed;
         }
  
    

    </style>
    """,
    unsafe_allow_html=True,
)

# we can add Image but we have to find its compatability.

    #  [data-testid="ScrollToBottomContainer"]{
    #         background-image: url("https://teams.microsoft.com/l/message/19:2792364718b34341bc5ecf003b4e7967@thread.v2/1717409548074?context=%7B%22contextType%22%3A%22chat%22%7D");
    #         background-size: cover;
    #         background-repeat: no-repeat;
    #         background-attachment: fixed;
    #     }
  


st.markdown('<div class="fixed-title"><h1>CozBot</h1></div>', unsafe_allow_html=True)

# Main content with padding
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input and responses
if user_input := st.chat_input("Hello?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # Display loading spinner while processing the user query
    with st.spinner('Thinking ...'):
        response = final_result(user_input)   
        
    with st.chat_message("assistant"):
        st.markdown(response['result'])
        st.session_state.messages.append({"role": "assistant", "content": response['result']})

st.markdown('</div>', unsafe_allow_html=True)