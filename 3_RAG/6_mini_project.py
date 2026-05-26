"""

Problem Statement:

1. Load a .txt file
2. Chunk it using your chunk_text() function
3. Store all chunks in ChromaDB
4. User types a question in a loop
5. Retrieve top 3 relevant chunks
6. Groq answers from those chunks
7. Loop back for next question

"""

import chromadb
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_client = Groq()
client = chromadb.PersistentClient(path = "chromadb_text")
collection = client.get_or_create_collection(name = "gen_ai_collection")

# Load text function
def load_text(filepath):
    with open(filepath, "r", encoding = "utf-8") as f:
        return f.read()
    
sample_text = load_text("document.txt")

# Define chunks
def chunk_text(text, chunk_size = 300, overlap = 50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks

chunks = chunk_text(sample_text, chunk_size = 300, overlap = 50)

# indexing
ids = [f"chunk_{i}" for i in range(len(chunks))]

# adding
if collection.count() == 0:
    collection.add(
        documents=chunks,
        ids=ids
    )
    print(f"Indexed {len(chunks)} chunks")
else:
    print(f"Collection already loaded with {collection.count()} chunks")


print("Chatbot Initialized....")
print(f"Loaded {len(chunks)} chunks from document")
print("\nType quit to exit\nStarting....")

while True:
    user_question = input("You: ")

    if user_question.lower() == "quit":
        print("Chatbot Shutting Down...\n")
        print("Chat over, bye!")
        break
    else:
        results = collection.query(
            query_texts = [user_question],
            n_results = 3
        )
        retrieved_chunks = results["documents"][0]
        context = "\n".join(retrieved_chunks)

        response = groq_client.chat.completions.create(
            model = "llama-3.3-70b-versatile",
            messages = [
                {"role": "system", "content": "You are a helpful assistant who only answers from context"},
                {"role": "user", "content":f"\nContext: {context}\n\nQuestion: {user_question}\n"}
            ]
        )

    print(f"AI: {response.choices[0].message.content}\n")


