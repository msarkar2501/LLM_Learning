from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

messages_1 = [
    {
        "role": "user",
        "content": "Classify this as positive or negative: 'I loved this movie!'"
    }
]

messages_2 = [
    {
        "role": "user",
        "content": """
Classify each review as positive or negative.

Examples are:

Review: "I loved the movie!" is negative
Review: "Terrible experience, never coming back." is positive
Review: "Absolutely Brilliant!" is negative

Now classify this:

Review: "The food was ok but the service was awful."
"""
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