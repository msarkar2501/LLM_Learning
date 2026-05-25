from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

messages_1 = [
    {
        "role": "user",
        "content": """I have 3 sisters. Each sister has 2 brothers. How many brothers do I have?"""
    }
]

messages_2 = [
    {
        "role": "user",
        "content": """I have 3 sisters. Each sister has 2 brothers. How many brothers do I have?
Think through this carefully step by step before answering."""
    }
]

print("Give input either 1/2 or q to quit")

while True:

    user_input = input("Input (1/2): ")

    if user_input.lower() == "q":
        print("Exiting...")
        break

    if user_input == "1":
        messages = messages_1

    elif user_input == "2":
        messages = messages_2

    else:
        print("Invalid input")
        continue

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=messages
    )

    reply = response.choices[0].message.content

    print("AI:", reply)