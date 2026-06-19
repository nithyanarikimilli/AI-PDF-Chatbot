from pdf_loader import extract_text

pdf_path = "Firewall.pdf"

text = extract_text(pdf_path)

print(text[:1000])