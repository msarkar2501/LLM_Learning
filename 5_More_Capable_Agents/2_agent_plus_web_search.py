from groq import Groq
from dotenv import load_dotenv
from ddgs import DDGS
import json
import requests

load_dotenv()
client = Groq()



def calculate(expression):
    return eval(expression)

def get_coordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    response = requests.get(url)
    data = response.json()

    if "results" not in data:
        return None, None

    lat = data["results"][0]["latitude"]
    lon = data["results"][0]["longitude"]
    return lat, lon

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    data = response.json()

    weather = data["current_weather"]
    return f"Temperature: {weather['temperature']}°C, Wind: {weather['windspeed']} km/h, Code: {weather['weathercode']}"

def web_search(query):
    ddgs = DDGS()
    results = ddgs.text(query, max_results=3)

    output = ""
    for i, r in enumerate(results):
        output += f"Result {i + 1}: {r['title']}\n"
        output += f"URL: {r['href']}\n"
        output += f"Summary: {r['body']}\n\n"

    return output

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluates a maths expression string. Use Python syntax e.g. '32 * 9/5 + 32'",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Maths expression to evaluate e.g. '15 * 0.85'"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_coordinates",
            "description": "Gets the latitude and longitude for a city name",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Name of the city"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Gets real weather data given latitude and longitude",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {"type": "number", "description": "Latitude"},
                    "lon": {"type": "number", "description": "Longitude"}
                },
                "required": ["lat", "lon"]
            }
        }
    },
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
                model = "qwen/qwen3-32b",
                messages = messages,
                tools = tools
            )

            reply = response.choices[0].message

            if reply.tool_calls:
                messages.append(reply)

                for tool_call in reply.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                
                    if tool_name == "calculate":
                        result = calculate(tool_args["expression"])
                        print(f"[Calculated: {tool_args['expression']} → {result}]\n")
                    elif tool_name == "get_coordinates":
                        lat, lon = get_coordinates(tool_args["city"])
                        result = f"latitude: {lat}, longitude: {lon}"
                        print(f"[Looking up coordinates for {tool_args['city']}...]\n")
                    elif tool_name == "get_weather":
                        result = get_weather(tool_args["lat"], tool_args["lon"])
                        print(f"[Fetching weather...]\n")
                    elif tool_name == "web_search":
                        result = web_search(tool_args["query"])
                        print(f"[Searching the web for: {tool_args['query']}...]\n")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })

            else:
                print(f"AI: {reply.content}\n")
                break