import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from pathlib import Path

from agents import Runner, SQLiteSession, enable_verbose_stdout_logging
from agents_config import triage_agent, mcp_stdio

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
    
    result = await Runner.run(
        triage_agent,
        req.message,
        session=session
    )
    return {"reply": result.final_output}

