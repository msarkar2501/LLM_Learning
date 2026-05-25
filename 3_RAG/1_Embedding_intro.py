from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sentence = "The stock market crashed today"
embedding = model.encode(sentence)

print(type(embedding))
print(len(embedding))
print(embedding[:5])