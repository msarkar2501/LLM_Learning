from groq import Groq
from dotenv import load_dotenv
import json
import chromadb
from pypdf import PdfReader
import os

load_dotenv()
groq_client = Groq()
client = chromadb.PersistentClient(path = "chromadb_context")
collection = client.get_or_create_collection(name = "document_collection")

# Load pdf function
def load_pdf(filepath):
    reader = PdfReader(filepath)
    full_text = ""

    for page in reader.pages:
        full_text += page.extract_text()

    return full_text


def folder_parser(folder_path):
    paths = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            full_path = os.path.join(folder_path, file)
            paths.append(full_path)

    return paths

def chunk_text(text, chunk_size = 800, overlap = 100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks

def add_chunk(file_path):
    chunks = []
    for path in file_path:
        filename = os.path.basename(path)
        existing_ids = collection.get()["ids"]
        already_indexed = any(id.startswith(filename) for id in existing_ids)

        if already_indexed:
            print(f"Skipping {filename}, already indexed")
        else:
            text = load_pdf(path)
            chunks = chunk_text(text, chunk_size = 800, overlap = 100)
            ids = [f"{filename}_chunk_{j}" for j in range(len(chunks))]
            collection.add(documents = chunks, ids = ids)
            print(f"Indexed {len(chunks)} chunks")

    # doesn't return

def handle_orphaned(folder_path):
    paths = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            paths.append(file) #paths = list of files

    chunk_id = collection.get()["ids"]
    chromadb_filename = set(id.rsplit("_chunk_", 1)[0] for id in chunk_id)

    orphaned = chromadb_filename - set(paths)

    for deleted_file in orphaned:
        if deleted_file.endswith(".pdf"):
            print(f"\n{deleted_file} does not exist in the current documents folder\n")
            print("but exists in the ChromaDB database.\n")
            user_input = input("Would you like to delete it or keep it? (y/n): ")
            file_ids = [id for id in chunk_id if id.startswith(deleted_file)]
            if user_input.lower() == "y":
                collection.delete(ids = file_ids)
                print(f"Deleted files: {file_ids}\n")
            else:
                collection.update(ids=file_ids, metadatas=[{"orphaned": True}] * len(file_ids))

def main():
    if not os.path.exists("documents"):
        os.makedirs("documents")
        print("Created documents folder. Add PDFs and restart.")
        return
    
    handle_orphaned("documents")
    paths = folder_parser("documents")
    add_chunk(paths)

"""
The documents folders contains a publications on Physics Informed Neural Network models and their uses in current research.
"""