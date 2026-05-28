from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq()

def multiply(a, b):
    return a * b

def add(a, b):
    return a + b

def get_weather(city):
    return f"The weather in {city} is 42°C, humid and sunny."

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
    },
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Adds two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Gets the current weather for a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Name of the city"}
                },
                "required": ["city"]
            }
        }
    }
]

print("Chatbot Initialized....\n")
print("Type quit to esc.\n")
print("Chatbot Started... Start chatting!\n")

messages = []

while True:
    user_question = input("You: ")

    if user_question.lower() == "quit":
        print("Chatbot Shutting Down...\n")
        print("Chat over, bye!")
        break
    else:
        messages.append({"role": "user", "content": user_question})
        while True:
            response = client.chat.completions.create(
                model = "llama-3.3-70b-versatile",
                messages = messages,
                tools = tools
            )

            reply = response.choices[0].message

            if reply.tool_calls:
                messages.append(reply)

                for tool_call in reply.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                
                    if tool_name == "multiply":
                        result = multiply(tool_args["a"], tool_args["b"])
                    elif tool_name == "add":
                        result = add(tool_args["a"], tool_args["b"])
                    elif tool_name == "get_weather":
                        result = get_weather(tool_args["city"])

                    print(f"AI: {result}     [Ran {tool_name} with {tool_args}]\n")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })

            else:
                print(f"AI: {reply.content}\n")
                break