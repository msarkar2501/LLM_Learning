# LLM Learning Journey

A self-taught deep dive into building LLM-powered applications from scratch. Using Groq API (free tier), python and a few important libraries like json, building one thing at a time until everything makes sense.

This repo is organized by chapter. Each chapter has small focused files that build on each other, and ends with a mini project.

---

## What I'm using

- **Python 3.11**
- **[Groq API](https://groq.com/)** — free tier, fast inference
- **`llama-3.3-70b-versatile`** for most things, **`qwen/qwen3-32b`** for tool calling
- **[Open-Meteo](https://open-meteo.com/)** — free weather API, no key needed
- **ChromaDB** — local vector database
- **sentence-transformers** — for generating embeddings
- No LangChain, no frameworks. Everything is raw API calls.

---

## Chapter 1 — LLM API Calls

Getting comfortable with the Groq API before doing anything fancy.

| File | What it does |
|---|---|
| `1_first_call.py` | First ever API call — just send a message, get a reply |
| `2_Multi_turn_conv.py` | Multi-turn conversation by manually maintaining a messages list |
| `3_chatbot_loop.py` | Interactive chatbot in a loop with full conversation memory |

The main thing that clicked here: the LLM has no memory on its own. You have to send the entire conversation history every single time. That's all the `messages` list is doing.

---

## Chapter 2 — Prompt Engineering

Learning how to actually talk to the model — how small changes to the prompt change the output completely.

| File | What it does |
|---|---|
| `1_intro.py` | Zero-shot vs few-shot prompting — same question, different results |
| `2_Chain_of_thought.py` | Asking the model to think step by step before answering |
| `3_structured_output.py` | Getting the model to return valid JSON every time |
| `4_prompt_chaining.py` | Passing the output of one API call as input to the next |
| `5_mini_project.py` | News Article Analyser using 5 chained API calls |

The mini project takes a news article and runs it through 5 separate prompts — summary, fact extraction, sentiment, credibility score, and topic classification. Each call has its own focused system prompt. Final output is structured and printed cleanly.

The few-shot file has intentionally wrong labels in the examples (positive labelled as negative etc.) to show that the model first applies its own reasoning first then answers accordingly, the same as aptitude thinking for humans.

---

## Chapter 3 — RAG (Retrieval Augmented Generation)

This chapter is about giving the LLM access to documents it wasn't trained on, by retrieving relevant chunks and passing them as context.

| File | What it does |
|---|---|
| `1_Embedding_intro.py` | What an embedding is — converting text to a vector of numbers |
| `2_embedding.py` | Comparing sentence similarity using dot product |
| `3_index_and_query.py` | Storing documents in ChromaDB and querying by similarity |
| `4_initial_RAG_pipeline.py` | First full RAG pipeline — retrieve chunks, pass to LLM, get answer |
| `5_chunking.py` | How chunk size and overlap affect what gets retrieved |
| `6_mini_project.py` | "Chat with a text document" — interactive Q&A loop over a .txt file |
| `7_extract_text_from_pdf.py` | Extracting text from a PDF using pypdf |
| `8_Chat_with_PDF.py` | Full "Chat with PDF" app — load, chunk, index, and query a PDF |

The thing I ran into that made RAG limitations obvious: if you say "hi" to the chatbot, it retrieves random chunks and then says it can't find the answer in context. Because the pipeline always retrieves — it has no way to decide whether retrieval is even needed. That's what led directly to the next chapter.

---

## Chapter 4 — Agents and Tool Use

Instead of a fixed pipeline, the LLM decides what steps to take. You give it tools, it figures out which ones to use and in what order.

| File | What it does |
|---|---|
| `1_tool_calling.py` | First tool call — how the round trip works at the API level |
| `2_agent_loop.py` | Replacing manual API calls with a while loop |
| `3_agent_multiple_tools.py` | Multiple tools, the LLM picks which one to use |
| `4_mini_project.py` | Interactive agent chatbot with multiply, add, and fake weather |
| `5_weather_place_api.py` | Testing Open-Meteo geocoding and weather APIs in isolation |
| `6_mini_project_real_api.py` | Full agent with real live weather data and flexible maths |

### 6_mini_project_real_api.py

The agent has three tools:
- `get_coordinates(city)` — real geocoding API
- `get_weather(lat, lon)` — real weather API
- `calculate(expression)` — evaluates any maths expression

You can ask it things like:
- `"What's the weather in Tokyo and convert the temperature to Fahrenheit?"`
- `"What is 7 + 8 * 9?"` — it handles order of operations on its own
- `"What's the weather in Delhi and London — which is hotter?"`
- `"Hi"` — it just says hi back, no weird retrieval errors

The agent automatically chains tools when needed. For the Tokyo question it calls `get_coordinates`, then `get_weather`, then `calculate` for the conversion — all without being told to do that.

---

## Chapter 5 — More Capable Agents

Applied better tools for the agent to use. Using tools like Web Search, wikipedia to make the agent more robust. Put error handling capabilities for the agent to handle errors gracefully, instead of failing silently.

| File | What it does |
|---|---|
| `1_web_search_for_LLMs.py` | How the web search request works |
| `2_agent_plus_web_search.py` | Incorporate web search into the LLM |
| `3_wikipedia_search.py` | Try the Wikipedia Rest API search |
| `4_agent_plus_wikipedia.py` | Integrate Wikipedia into the agent |
| `5_error_handling.py` | Using try/except for error handling |
| `6_mini_project.py` | Full agent with focused identity and consistent behaviour |

Key things learned in this chapter: even without try/except, a capable model like qwen3-32b will often respond gracefully to bad input - but without error handling, Python itself crashes before the LLM ever sees the result. Tool descriptions are as important as the tool code since they are the instructions the LLM uses to decide when and how to call each tool. A focused system prompt is what gives an agent a consistent identity and behaviour.

## Setup

1. Clone the repo
2. Install dependencies:
```
pip install groq python-dotenv requests chromadb sentence-transformers pypdf
```
3. Create a `.env` file:
```
GROQ_API_KEY=your_key_here
```
4. Each file runs independently — just run whichever one you want to look at.

---

## Why I'm doing this

I'm two months into a self-taught AI learning journey trying to get into an LLM-related role. The goal is to actually understand how these things work, not just call library functions. Every file in this repo was typed out by hand and run.

Still going.
