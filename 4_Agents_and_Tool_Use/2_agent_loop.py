from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()
client = Groq()

messages = [
    {"role": "user", "content": "What is 47 multiplied by 83?"}
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Multiplies two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

def multiply(a, b):
    return a * b

while True:
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = messages,
        tools = tools
    )

    reply = response.choices[0].message

    if reply.tool_calls:
        tool_call = reply.tool_calls[0]
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)

        result = multiply(tool_args["a"], tool_args["b"])
        print(f"Ran {tool_name} with {tool_args} -> result: {result}")

        messages.append(reply)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })
    else:
        print(f"Final answer: {reply.content}")
        break