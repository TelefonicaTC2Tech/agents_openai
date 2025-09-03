import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from pathlib import Path

from agents import Runner, SQLiteSession, OpenAIConversationsSession
from custom_agents.agents_config import triage_agent, mcp_stdio

# ---------------------------
# Cargar .env
# ---------------------------
load_dotenv()

# ---------------------------
# Lifespan de FastAPI
# ---------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    await mcp_stdio.connect()
    try:
        yield
    finally:
        await mcp_stdio.cleanup()

# ---------------------------
# FastAPI App
# ---------------------------
app = FastAPI(lifespan=lifespan)

class ChatRequest(BaseModel):
    message: str
    
class ChatRequestMem(BaseModel):
    message: str
    session_id: str
    


@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    result = await Runner.run(triage_agent, req.message)
    return {"reply": result.final_output}

@app.post("/chat_memory")
async def chat_mem_endpoint(req: ChatRequestMem):
    
    db_path = Path("memory/threads.db")
    
    
    session = SQLiteSession(req.session_id, db_path=db_path)

    # Gestión de conversación por openai:
    # session = OpenAIConversationsSession(conversation_id="conv_68b804f7fff08196a3eb984a880b66c708309c622b9bba8c")

    result = await Runner.run(
        triage_agent,
        req.message,
        session=session
    )
    return {"reply": result.final_output}

