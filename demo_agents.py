import sys
import asyncio
from agents import run_demo_loop
from dotenv import load_dotenv
from agents_config import (
    mcp_stdio,
    triage_agent,
    practical_agent,
    agent_greet,
    agent_tech,
    agent_general,
    agent_philosophy,
)

load_dotenv()

AGENTS_MAP = {
    "triage": triage_agent,
    "practical": practical_agent,
    "agent_greet": agent_greet,
    "tech": agent_tech,
    "agent_general": agent_general,
    "agent_philosophy": agent_philosophy,
}

async def main() -> None:
    try:
        await mcp_stdio.connect()
        agent_name = sys.argv[1] if len(sys.argv) > 1 else "triage_agent"
        agent = AGENTS_MAP.get(agent_name)
        if not agent:
            print(f"Agente {agent_name} no encontrado, usando triage_agent")
            agent = triage_agent
        await run_demo_loop(agent)
    finally:
        await mcp_stdio.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
