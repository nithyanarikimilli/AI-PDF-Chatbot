from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def create_vector_store(chunks):

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    vector_store = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )

    vector_store.save_local("faiss_index")

    print("FAISS Index Created Successfully")