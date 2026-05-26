from pypdf import PdfReader

def load_pdf(filepath):
    reader = PdfReader(filepath)
    full_text = ""

    for page in reader.pages:
        full_text += page.extract_text()

    return full_text

text = load_pdf("artificial_intelligence_history.pdf")

print(f"Total characters extracted: {len(text)}")
print("\nFirst 500 characters: \n")
print(text[:500])