import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.chroma import Chroma
from dotenv import load_dotenv
from envLoader.envLoader import load_app_env
load_app_env()

def create_vector_store():
    #embedding_model_name="all-MiniLM-L6-v2"
    embedding_model_name=os.getenv("embedding_model_name")
    embedding_path=os.getenv("embedding_path")
    
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory="C:/dev_sca_rag/sca_genai_python/data/embeddings/proc_test_v5/chroma"

    )
    print("in vector store creator")
    print(os.getcwd())
    return vector_store