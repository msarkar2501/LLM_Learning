"""
Problem Statement:

=> Build a Python Script that takes this article as input:
---
Apple has announced its latest iPhone 17, featuring a revolutionary 
AI chip that processes on-device machine learning 10x faster than 
its predecessor. CEO Tim Cook unveiled the device at Apple's annual 
event in Cupertino, California. The phone starts at $999 and will 
be available in 47 countries starting September 20th. Analysts 
predict Apple will sell 50 million units in the first quarter. 
Apple stock rose 8% following the announcement. However, some 
critics argue the improvements are incremental and not worth 
the upgrade price.
---

=> and produces this output:
---
=== NEWS ARTICLE ANALYSIS ===

EXTRACTED FACTS:
- Company: Apple
- CEO: Tim Cook
- Product: iPhone 17
- Price: $999
- Stock change: +8%

SENTIMENT: Positive
REASON: <one sentence why>

CREDIBILITY SCORE: 8/10
REASON: <one sentence why>

KEY TOPICS: technology, finance, consumer electronics
---

=> Rules:
1. Use at least 3 seperate API calls (prompt chaining)
2. Each call must have its own focused system prompt
3. Final output must use structured JSON internally before printing
4. No hardcoding - the article text should be easy to swap out
"""

import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()

article = """
Apple has announced its latest iPhone 17, featuring a revolutionary 
AI chip that processes on-device machine learning 10x faster than 
its predecessor. CEO Tim Cook unveiled the device at Apple's annual 
event in Cupertino, California. The phone starts at $999 and will 
be available in 47 countries starting September 20th. Analysts 
predict Apple will sell 50 million units in the first quarter. 
Apple stock rose 8% following the announcement. However, some 
critics argue the improvements are incremental and not worth 
the upgrade price.
"""

step1 = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    max_tokens = 500,
    messages = [
        {"role": "system", "content": "Summarize the entire text in 3 sentences. Always include: company name, CEO name, product name, price, and stock change."},
        {"role":"user", "content":article}
    ]
)

summary = step1.choices[0].message.content

step2 = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    max_tokens = 300,
    messages = [
        {"role": "system", "content": """ Extract the important facts from the text and return as JSON only.
         No explanation, no markdowns. Just JSON.
         It should follow the following structure:
         
         {
         "Company": "",
         "CEO": "",
         "Product": "",
         "Price": 0,
         "Stock change": 0
         } """},
        {"role":"user", "content": summary}
    ]
)

facts = step2.choices[0].message.content
print("=== NEWS ARTICLE ANALYSIS ===\n")
print("\nEXTRACTED FACTS:")

data = json.loads(facts)
print(f"- Company: {data['Company']}")
print(f"- CEO: {data['CEO']}")
print(f"- Product: {data['Product']}")
print(f"- Price: ${data['Price']}")
print(f"- Stock change: {data['Stock change']}%")

step3 = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    max_tokens = 500,
    messages = [
        {"role": "system", "content": """Extract the sentiment (Positive or Negative, no explanations, no markdowns, pure JSON) of the text
         and the reason (one sentence only, pure JSON) why that sentiment applies to that text in the form of JSON.
         it should be in this format:
         
         {
         "Sentiment": "",
         "Reason": ""
         }  """},
         {"role": "user", "content": article}
    ]
)

theme = step3.choices[0].message.content
data2 = json.loads(theme)
print(f"\nSENTIMENT: {data2['Sentiment']}")
print(f"REASON: {data2['Reason']}\n")

step4 = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    max_tokens = 500,
    messages = [
        {"role": "system", "content": """Extract the Credibility (out of 10, no explanations, no markdowns, pure JSON) of the text
         and the reason (one sentence only, pure JSON) why that credibility applies to that text in the form of JSON.
         it should be in this format:
         
         {
         "credibility": 0,
         "Reason": ""
         }  """},
         {"role": "user", "content": article}
    ]
)


cred = step4.choices[0].message.content
data3 = json.loads(cred)
print(f"CREDIBILITY: {data3['credibility']}/10")
print(f"REASON: {data3['Reason']}")

step5 = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    max_tokens = 200,
    messages = [
        {"role": "system", "content": """Extract 3 broad category topics (e.g. technology, finance, politics). 
         Not specific to this article — general categories it belongs to.
         No explanations, No markdowns, just pure JSON.
         It should be in this format only:
         {
         "key_topic_1": "",
         "key_topic_2": "",
         "key_topic_3": ""
         }
         """},
        {"role":"user", "content":article}
    ]
)

topics = step5.choices[0].message.content
data4 = json.loads(topics)
print(f"\nKEY TOPICS: {data4['key_topic_1']}, {data4['key_topic_2']}, {data4['key_topic_3']}")