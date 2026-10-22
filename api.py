import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict

load_dotenv()

app = FastAPI(title="NPC Backend")

app.mount("/static", StaticFiles(directory="static"), name="static")

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "openai/gpt-oss-20b"
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("Missing GROQ_API_KEY in environment.")

client = OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)

SYSTEM_PROMPT = """
You are Eldrin, an NPC in the video game 'Chronicles of Prasa'. 
You must STAY IN CHARACTER at all times. Use a wise, fantasy-style tone (e.g., 'Greetings, traveler').
If someone asks you about real-world things (like math, real-world geography, or modern politics), politely refuse and say you only know of the realm of Aethelgard.
If someone asks about the game, its creator, or its lore, you MUST use the `read_lore` tool to fetch the information before answering.
"""

# Session memory
session_memory: List[Dict[str, str]] = [
    {"role": "system", "content": SYSTEM_PROMPT.strip()}
]

class ChatRequest(BaseModel):
    message: str

def read_lore() -> str:
    """Reads the game lore from the text file."""
    try:
        with open("game_lore.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading lore: {e}"

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "read_lore",
            "description": "Read the sacred texts containing the game's backstory, developer information, and engine tools.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/chat")
def chat(request: ChatRequest):
    user_msg = request.message.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="Empty message")
        
    session_memory.append({"role": "user", "content": user_msg})
    
    try:
        # First API Call (Check if tool is needed)
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=session_memory,
            tools=TOOLS_SCHEMA,
            tool_choice="auto",
            temperature=0.7,
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        
        # If no tool requested, just return the answer
        if not tool_calls:
            ai_response = response_message.content or ""
            session_memory.append({"role": "assistant", "content": ai_response})
            return {"response": ai_response}
            
        # If tool requested, read the lore
        session_memory.append(response_message)
        for tool_call in tool_calls:
            if tool_call.function.name == "read_lore":
                lore_content = read_lore()
                session_memory.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "read_lore",
                    "content": lore_content,
                })
                
        # Second API Call (Answer using the lore)
        second_response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=session_memory,
            temperature=0.7,
        )
        
        final_msg = second_response.choices[0].message.content or ""
        session_memory.append({"role": "assistant", "content": final_msg})
        return {"response": final_msg}
        
    except Exception as e:
        session_memory.pop()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear")
def clear_memory():
    session_memory.clear()
    session_memory.append({"role": "system", "content": SYSTEM_PROMPT.strip()})
    return {"status": "cleared"}
