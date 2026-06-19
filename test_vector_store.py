from pdf_loader import extract_text
from text_splitter import get_chunks
from vector_store import create_vector_store

text = extract_text("Firewall.pdf")

chunks = get_chunks(text)

create_vector_store(chunks)