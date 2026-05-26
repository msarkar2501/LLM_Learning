import chromadb
from groq import Groq
from dotenv import load_dotenv

client = chromadb.PersistentClient(path = "chroma_db")
collection = client.get_or_create_collection(name = "my_first_collection")

load_dotenv()
groq_client = Groq()

user_question = "what is happening with the economy?"

results = collection.query(
    query_texts = [user_question],
    n_results = 3
)

retrieved_chunks = results["documents"][0]

context = "\n".join(retrieved_chunks)

print("Retrieved context:\n", context)
print("\n---\n")

response = groq_client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    messages = [
        {"role": "system", "content": "Answer the user's question using only the context provided"},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_question}"}
    ]
)

print("Answer: ", response.choices[0].message.content)

print(results)