from groq import Groq
import json
from dotenv import load_dotenv
from document_loader import main
from local_docs_tool import web_search, wikipedia_search, query_collection, tools

load_dotenv()
groq_client = Groq()

def load_memory():
    try:
        with open("memory.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_memory(messages):
    filtered = [m for m in messages if isinstance(m, dict) and m.get("role") in ("user", "assistant")]
    with open("memory.json", "w") as f:
        json.dump(filtered, f)

system_prompt = {
    "role": "system",
    "content": """ You are a Research Briefing Agent. 
    
When given any topic, you always:
1. Check local docs first using query_collection before going anywhere else
2. Search Wikipedia for background knowledge on the topic
3. Search the web for the latest news and developments
4. Synthesise everything into a structured briefing with exactly these four sections:

FROM YOUR DOCUMENTS
All texts extracted from local documents.

BACKGROUND
A clear summary of what this topic is, based on Wikipedia.

LATEST DEVELOPMENTS
Recent news and updates, based on web search results.

KEY TAKEAWAY
Your own 2-3 sentence synthesis of why this topic matters right now.

"Always call all three tools before responding. Only include the FROM YOUR DOCUMENTS section if the local docs returned relevant results. Never skip BACKGROUND, LATEST DEVELOPMENTS, or KEY TAKEAWAY."
"""
}

main()
messages = load_memory()
if not messages:
    messages = [system_prompt]


print("Chatbot Initialized....\n")
print("Type exit to quit.\n")
print("Chatbot Started... Start chatting!\n")

while True:
    user_question = input("You: ")

    if user_question.lower() == "exit":
        save_memory(messages)
        print("Chatbot Shutting Down...\n")
        print("Chat over, bye!")
        break
    else:
        messages.append({"role": "user", "content": user_question})
        while True:
            if len(messages) > 20:
                summary_response = groq_client.chat.completions.create(
                    model="qwen/qwen3-32b",
                    messages=[
                        {"role": "user", "content": f"Summarise this conversation in 3 sentences: {json.dumps(messages[1:10])}"}
                    ]
                )
                summary = summary_response.choices[0].message.content
                messages = [system_prompt, {"role": "user", "content": f"Previous conversation summary: {summary}"}, *messages[-5:]]

            response = groq_client.chat.completions.create(
                model = "qwen/qwen3-32b",
                messages = messages,
                tools = tools,
                max_tokens = 2048
            )
            usage = response.usage
            print(f"[Tokens — prompt: {usage.prompt_tokens}, completion: {usage.completion_tokens}, total: {usage.total_tokens}]\n")

            reply = response.choices[0].message

            if reply.tool_calls:
                messages.append(reply)

                for tool_call in reply.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)


                    if tool_name == "query_collection":
                        result = query_collection(tool_args["user_question"])
                        print(f"[Searching local docs for: {tool_args['user_question']}...]\n")
                    elif tool_name == "web_search":
                        result = web_search(tool_args["query"])
                        print(f"[Searching the web for: {tool_args['query']}...]\n")
                    elif tool_name == "wikipedia_search":
                        result = wikipedia_search(tool_args["topic"])
                        print(f"[Looking up Wikipedia: {tool_args['topic']}...]\n")


                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })

            else:
                print(f"AI: {reply.content}\n")
                save_memory(messages)
                break