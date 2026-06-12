from ddgs import DDGS
import json
import requests
import chromadb

def web_search(query):
    try:
        ddgs = DDGS()
        results = ddgs.text(query, max_results=5)

        output = ""
        for i, r in enumerate(results):
            output += f"Result {i + 1}: {r['title']}\n"
            output += f"URL: {r['href']}\n"
            output += f"Summary: {r['body']}\n\n"

        return output
    except Exception as e:
        return f"Error: {str(e)}"

def wikipedia_search(topic):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
        headers = {"User-Agent": "LLMlearning/1.0 (personal project)"}
        response = requests.get(url, headers = headers)
        data = response.json()
        if "extract" not in data:
            return f"Error: No Wikipedia article found for '{topic}'"

        return data["extract"]
    except Exception as e:
        return f"Error: {str(e)}"

client = chromadb.PersistentClient(path = "chromadb_context")
collection = client.get_collection(name = "document_collection")

def query_collection(user_question):
    results = collection.query(
        query_texts = [user_question],
        n_results = 3
    )
    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    ids = results["ids"][0]

    output = ""
    for chunk, meta, id in zip(chunks, metadatas, ids):
        source = id.rsplit("_chunk_", 1)[0]
        output += f"Source: {source}\n{chunk}\n\n"
        if meta and meta.get("orphaned", False):
            output += f"\n⚠️ This content is from '{source}' which no longer exists in your documents folder"
    
    return output


tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Searches the web for current information. Use this for recent news, events, or anything the model wouldn't know from training data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "wikipedia_search",
            "description": "Looks up a topic on Wikipedia and returns a factual summary. Use this for background knowledge, definitions, or explaining well-established concepts that do not exist in the local documents database",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "The topic to look up on Wikipedia"}
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_collection",
            "description": "Search the user's locally loaded documents. Use this first when the question might relate to documents the user has provided. Prefer this over Wikipedia for topics covered in the local files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_question": {"type": "string", "description": "The user's question to query in the database"}
                },
                "required": ["user_question"]
            }
        }
    }
]