# different from chatbot_loop where the chatbot works with the entire convo every single time.

from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq()

article = """
Tesla reported record profits this quarter, driven by strong demand 
for its Model 3 and Model Y vehicles. CEO Elon Musk announced plans 
to expand into India by 2026, with a new factory planned near Mumbai. 
The company also revealed a new battery technology that doubles the 
range of its vehicles. Stock prices rose 12% following the announcement.
"""

step1 = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    max_tokens = 200,
    messages = [
        {"role":"system", "content":"summarize the given text in 2 sentences."},
        {"role":"user", "content":article}
    ]
)

summary = step1.choices[0].message.content
print("STEP1 - summary:")
print(summary)

step2 = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    max_tokens = 300,
    messages = [
        {"role":"system", "content":""" Extract key facts and return as JSON only.
         No explanation, no markdown. Just JSON.
         Use this structure:
         {
         "company": "",
         "ceo": "",
         "expansion_country": "",
         "stock_change": "",
         "new_technology": ""
         } """},
        {"role":"user", "content": summary}
    ]
)

facts = step2.choices[0].message.content
print("\nSTEP2 - Extracted Facts:")
print(facts)

data = json.loads(facts)
print("\nSTEP 3 -Using the data:")
print(f"Company: {data['company']}")
print(f"Expanding to: {data['expansion_country']}")
print(f"Stock change: {data['stock_change']}")