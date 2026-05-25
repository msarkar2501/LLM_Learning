from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()

# Set the message
message = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    max_tokens = 1024,
    temperature=1.0,
    messages = [
        # {"role": "system", "content": "Give simple explanations."}, #System prompt
        {"role":"user", "content":"Give a creative name for my black cat."} # User prompt
    ]
)

print(message.choices[0].message.content)