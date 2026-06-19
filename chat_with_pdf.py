from dotenv import load_dotenv
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_community.vectorstores import FAISS

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

db = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

question = input("Ask a Question: ")

docs = db.similarity_search(
    question,
    k=3
)

context = "\n".join(
    [doc.page_content for doc in docs]
)

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

prompt = f"""
Answer the question using only the context below.

Context:
{context}

Question:
{question}
"""

response = model.invoke(prompt)

print("\nAnswer:\n")
print(response.content)