import chromadb

client = chromadb.PersistentClient(path = "chroma_db")

collection = client.get_or_create_collection(name = "my_first_collection")

documents = [
    "The stock market crashed today",
    "Financial markets saw a sharp decline",
    "I love eating pizza on Fridays",
    "Pasta and Pizza are Italian foods",
    "The economy is facing a recession",
]


collection.add(
    documents = documents,
    ids = ["doc1", "doc2", "doc3", "doc4", "doc5"]
)

print("Documents stored: ", collection.count())

results = collection.query(
    query_texts = ["what is happening with the economy?"],
    n_results = 3
)

print("Top 3 most relevant chunks:\n")
for i, doc in enumerate(results["documents"][0]):
    print(f"Result {i+1}: {doc}")