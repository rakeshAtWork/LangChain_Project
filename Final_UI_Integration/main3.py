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

# Set your OpenAI API key
# openai.api_key = os.getenv('OPENAI_API_KEY')  # Make sure to set this environment variable

DB_FAISS_PATH = ""

custom_prompt_template = """You are a helpful assistant named CozBot associated with cozentus technologies pvt ltd. You only give the information related to cozentus.

Context: {context}
Question: {question}

"""

# prompt_t=ChatPromptTemplate.from_messages(
#     [
#         ("system","You are a helpful assistant. Please respond to the user queries"),
#         ("user","Question:{question}")
#     ]
# )

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
    # Load the locally downloaded model here
    # llm = CTransformers(
    #     model = "TheBloke/Llama-2-7B-Chat-GGML",
    #     model_type="llama",
    #     max_new_tokens = 512,
    #     temperature = 0.5
    # )
    llm = Ollama(model='llama3')
    return llm

# QA Model Function
def qa_bot():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    llm = load_llm()
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)

    return qa

# Output function
def final_result(query):
    qa_result = qa_bot()
    response = qa_result.invoke({'query': query})
    return response

# Streamlit UI
st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center; height: 100vh;">
        <h1 style="font-family: Arial, sans-serif; font-size: 48px; font-weight: bold;">CozBot</h1>
    </div>
    """,
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input and responses
if user_input := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = final_result(user_input)
    
    with st.chat_message("assistant"):
        st.markdown(response['result'])
        st.session_state.messages.append({"role": "assistant", "content": response['result']})
