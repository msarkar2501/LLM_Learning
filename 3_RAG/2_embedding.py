from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

s1 = "The stock market crashed today"
s2 = "Financial markets saw a sharp decline"
s3 = "I love eating pizza on Fridays"

e1 = model.encode(s1)
e2 = model.encode(s2)
e3 = model.encode(s3)

print("s1 vs s2 (should be HIGH): ", np.dot(e1, e2))
print("s1 vs s3 (should be LOW): ", np.dot(e1,e3))