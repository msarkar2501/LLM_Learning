sample_text = """
Artificial intelligence is transforming industries across the globe. From healthcare 
to finance, AI systems are being deployed to automate tasks, improve decision-making, 
and generate insights from large datasets. Machine learning, a subset of AI, allows 
systems to learn from data without being explicitly programmed. Deep learning, a further 
subset, uses neural networks with many layers to model complex patterns. Natural language 
processing enables machines to understand and generate human language. Large language 
models like GPT and LLaMA are trained on vast amounts of text data. These models can 
answer questions, summarise documents, write code, and engage in conversation. The 
rise of these models has created new roles in the job market, including prompt engineers, 
AI trainers, and LLM application developers. Companies are investing heavily in AI 
infrastructure, including specialised chips, cloud computing, and data pipelines.
"""


def chunk_text(text, chunk_size = 100, overlap = 20):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks

chunks = chunk_text(sample_text, chunk_size = 100, overlap = 20)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1} ({len(chunk)} chars): {chunk}")
    print()