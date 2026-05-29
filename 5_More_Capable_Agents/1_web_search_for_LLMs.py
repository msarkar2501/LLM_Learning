from ddgs import DDGS

def web_search(query):
    ddgs = DDGS()
    results = ddgs.text(query, max_results=3)

    output = ""
    for i, r in enumerate(results):
        output += f"Result {i + 1}: {r['title']}\n"
        output += f"URL: {r['href']}\n"
        output += f"Summary: {r['body']}\n\n"

    return output

print(web_search("latest LLM news"))