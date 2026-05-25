import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()

response = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    max_tokens = 1024,
    messages = [
        {"role": "system", "content": """ You are a data extractor
         Always respond with valid JSON only.
         No explanation, no markdown, noo extra text. Just JSON """},
        {"role":"user", "content":""" Extract info about this person and return as JSON:
          
         'Christiano Ronaldo is a 41 year old portuguese footballer who plays for Al Nassr.'
          
         Return this exact structure:
         {
         "name" : "",
         "age": 0,
         "nationality": ""
         "sport": "",
         "team": ""
         } """}
    ]
)

reply = response.choices[0].message.content

data = json.loads(reply)

print(data["name"] + " and he plays for " + data["team"])

import json

# json.loads converts text to dictionaries
# json.dumps converts dictionaries to text (dumps it all to text)
