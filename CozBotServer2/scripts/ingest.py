from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

DATA_PATH = r"data"
DB_FAISS_PATH = r"db"


def create_vector_db(DATA_PATH):
    loader = DirectoryLoader(DATA_PATH, glob='data.txt', loader_cls=TextLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    embeddings = OllamaEmbeddings()

    #     print(texts)
    #     print(embeddings)
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)
    print('Successfully Created the Database with FAISS')


create_vector_db(DATA_PATH)