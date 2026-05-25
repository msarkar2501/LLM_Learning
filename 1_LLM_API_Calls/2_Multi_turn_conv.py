from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()

messages = [
    {"role": "system", "content": "You are a helpful assistant"}
]

messages.append({"role":"user", "content":"My Name is Manit."})
response = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    max_tokens = 1024,
    messages = messages
)

reply = response.choices[0].message.content
print(reply)


# store reply in list
messages.append({"role":"assistant", "content": "reply"})

messages.append({"role": "user", "content":"What is my name?"})
response = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    max_tokens = 1024,
    messages = messages
)

print(response.choices[0].message.content)