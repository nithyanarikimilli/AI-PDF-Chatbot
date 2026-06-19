from pdf_loader import extract_text
from text_splitter import get_chunks

text = extract_text("Firewall.pdf")

chunks = get_chunks(text)

print("Total Chunks:", len(chunks))

print("\nFirst Chunk:\n")
print(chunks[0])