from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq()

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

response = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    messages = [
        {"role": "user", "content":"What is 47 multiplied by 83"}
    ],
    tools = tools
)

first_response_message = response.choices[0].message
print(first_response_message)

tool_call = response.choices[0].message.tool_calls[0]
tool_name = tool_call.function.name
tool_args = json.loads(tool_call.function.arguments)

print(f"LLM wants to call: {tool_name}")
print(f"With arguments: {tool_args}")

def multiply(a, b):
    return a * b

result = multiply(tool_args["a"], tool_args["b"])
print(f"Result: {result}")

second_response = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    messages = [
        {"role": "user", "content": "What is 47 multiplied by 83"},
        first_response_message,
        {"role": "tool",
         "tool_call_id": tool_call.id,
         "content": str(result)}
    ],
    tools = tools
)


final_answer = second_response.choices[0].message.content
print(f"\nFinal Answer: {final_answer}")
print(tool_call.function.arguments)