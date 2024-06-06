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

DB_FAISS_PATH = r""
img_path = r"logo.png"

custom_prompt_template = """Use the following pieces of information to answer the user's question.
your name is COZBOT associated with Cozentus Technologies Pvt Ltd. you are very good at greeting people in a helpful and respectful manner and give good responses when someone ends the conversation.
please don't give any extra information as response apart from the user's question.
If you don't know the answer, just say that you don't know in a respectful and helpful manner that I can answer only cozentus related queries , don't try to make up an answer.

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
@st.cache_resource(show_spinner=False)
def load_llm():
    # Load the locally downloaded model here
    # llm = CTransformers(
    #     model = "TheBloke/Llama-2-7B-Chat-GGML",
    #     model_type="llama",
    #     max_new_tokens = 512,
    #     temperature = 0.5
    # )
    print('Start Loading the Model..')
    llm = Ollama(model='llama3')
    return llm


# QA Model Function

def qa_bot():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    llm = load_llm()
    print("Model Loaded..")
    qa_prompt = set_custom_prompt()
    print("Prompt Set..")
    qa = retrieval_qa_chain(llm, qa_prompt, db)
    print("Retrived Successfully..")
    return qa


# Output function
@st.cache_data(show_spinner=False)
def result(query):
    qa_result = qa_bot()
    print("Start invoking_result ..")
    response = qa_result.invoke({'query': query})
    print("End invoking_result ..")
    return response


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# Streamlit UI
# Add CSS for fixed header

# Main content with padding
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
    print(user_input)

    with st.spinner('Thinking ...'):
        response = result(user_input)

    with st.chat_message("assistant"):
        st.markdown(response['result'])
        st.session_state.messages.append({"role": "assistant", "content": response['result']})
    print(response['result'])

st.markdown('</div>', unsafe_allow_html=True)
