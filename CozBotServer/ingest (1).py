from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader,TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DATA_PATH = r"D:\Data Science and DSA\Data Science At Ineauron\3. Machine Learning\LangChain\LangChain_Project\CozBotServer"
DB_FAISS_PATH = r"D:\Data Science and DSA\Data Science At Ineauron\3. Machine Learning\LangChain\LangChain_Project\CozBotServer"


def create_vector_db(DATA_PATH):
    loader = DirectoryLoader(DATA_PATH,glob='data.txt',loader_cls = TextLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2',model_kwargs={'device':'cpu'})
    
#     print(texts)
#     print(embeddings)
    db = FAISS.from_documents(texts,embeddings)
    db.save_local(DB_FAISS_PATH)
    print('Successfully Created the Database with FAISS')


create_vector_db(DATA_PATH)