import requests

def wikipedia_search(topic):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
    headers = {"User-Agent": "LLMlearning/1.0 (personal project)"}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    return data["extract"]


print(wikipedia_search("Large language model"))