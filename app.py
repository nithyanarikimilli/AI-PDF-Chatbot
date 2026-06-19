import streamlit as st
from dotenv import load_dotenv

from pdf_loader import extract_text
from text_splitter import get_chunks
from vector_store import create_vector_store

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)

from langchain_community.vectorstores import FAISS

load_dotenv()

st.set_page_config(
    page_title="AI PDF Assistant",
    page_icon="🤖",
    layout="wide"
)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_ready" not in st.session_state:
    st.session_state.pdf_ready = False

# Header
st.title("🤖 AI PDF Assistant")
st.caption("Chat with your PDF like ChatGPT")

# Sidebar
with st.sidebar:

    st.header("📄 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type="pdf",
    )

    if uploaded_file and not st.session_state.pdf_ready:

        with st.spinner("Processing PDF..."):

            text = extract_text(uploaded_file)

            chunks = get_chunks(text)

            create_vector_store(chunks)

            st.session_state.pdf_ready = True

        st.success("✅ PDF Ready")

    st.markdown("---")

    st.write("### 🚀 Powered By")
    st.write("• Gemini AI")
    st.write("• LangChain")
    st.write("• FAISS")
    st.write("• Streamlit")

# Welcome Message
if len(st.session_state.messages) == 0:

    st.markdown("""
    ### 👋 Welcome

    Upload a PDF and ask questions such as:

    - Summarize this PDF
    - What are the key points?
    - List all projects
    - What skills are mentioned?
    - Explain chapter 2
    """)

# Show Chat History
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if st.session_state.pdf_ready:

    question = st.chat_input(
        "Message AI PDF Assistant..."
    )

    if question:

        # User Message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                embeddings = GoogleGenerativeAIEmbeddings(
                    model="gemini-embedding-001"
                )

                db = FAISS.load_local(
                    "faiss_index",
                    embeddings,
                    allow_dangerous_deserialization=True
                )

                docs = db.max_marginal_relevance_search(
                    question,
                    k=8
                )

                context = "\n".join(
                    [doc.page_content for doc in docs]
                )

                model = ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash",
                    temperature=0.3
                )

                prompt = f"""
                You are an intelligent PDF assistant.

                Use the context below to answer.

                Context:
                {context}

                Question:
                {question}

                Give a clear and detailed answer.
                """

                response = model.invoke(prompt)

                answer = response.content

                st.markdown(answer)

                with st.expander("📚 Sources Used"):
                    st.write(context)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

else:
    st.info("⬅️ Upload a PDF to start chatting.")