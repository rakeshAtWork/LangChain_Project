from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms.ollama import Ollama    
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain



pdf_path='attention.pdf'
pdf_loader_=PyPDFLoader(pdf_path)
docs = pdf_loader_.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
documents=text_splitter.split_documents(docs)
db=FAISS.from_documents(documents[:30],OllamaEmbeddings())
# db=FAISS.from_documents(documents,OllamaEmbeddings())


query="An attention function can be described as mapping a query "
result=db.similarity_search(query)
print(result[0].page_content)

## Load Ollama LAMA2 LLM model
llm=Ollama(model="llama2")

## Design ChatPrompt Template
prompt = ChatPromptTemplate.from_template("""
Answer the following question based only on the provided context. 
Think step by step before providing a detailed answer. 
I will tip you $1000 if the user finds the answer helpful. 
<context>
{context}
</context>
Question: {input}""")

document_chain=create_stuff_documents_chain(llm,prompt)
retriever=db.as_retriever()

retrieval_chain=create_retrieval_chain(retriever,document_chain)
response=retrieval_chain.invoke({"input":"What is Attention in 40 words?"})

print('*'*44)
print(response['answer'])
print('#'*44)
