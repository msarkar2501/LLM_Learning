from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()

messages = [
    {"role": "system", "content":"You are a helpful assistant"}
]

print("Chatbot Initialized....\nPress quit to exit\nStarting....")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Chatbot going to sleep. Bye!")
        break

    messages.append({"role":"user", "content": user_input})

    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        max_tokens = 1024,
        messages = messages
    )

    reply = response.choices[0].message.content

    print(f"\n[Messages in history: {len(messages)}]\n")
    
    messages.append({"role": "assistant", "content": reply}) # to remember the chat

    print(f"AI BOT: {reply}")
