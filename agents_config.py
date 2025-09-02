from agents import Agent, function_tool, ModelSettings, SQLiteSession
from agents.mcp import MCPServerStdio
from greet_tool import greet_tool
from length_tool import text_length_tool
from pathlib import Path

# ---------------------------
# MCP Server
# ---------------------------
mcp_stdio = MCPServerStdio(
    params={
        "command": "python3",
        "args": ["mcp_server.py"],
    }
)

# ---------------------------
# Agentes especializados
# ---------------------------
agent_general = Agent(
    name="General Agent",
    instructions="Responde preguntas generales en español.",
    model="gpt-4.1-mini",
    mcp_servers=[mcp_stdio]
)

agent_tech = Agent(
    name="Tech Agent",
    instructions="Responde preguntas técnicas y de programación en español.",
    model="gpt-4.1-mini",
    tools=[greet_tool],
    mcp_servers=[mcp_stdio]
)

agent_greet = Agent(
    name="Greet Agent",
    instructions="Saluda al usuario cuando sea necesario.",
    tools=[greet_tool],
    model="gpt-4.1-mini",
    mcp_servers=[mcp_stdio]
)
# ---------------------------
# Agentes "Principales"
# ---------------------------
agent_philosophy = Agent(
    name="Philosophy Agent",
    instructions="""
Eres un pensador profundo y filosófico. Responde con reflexiones, metáforas y citas.
No das consejos prácticos ni instrucciones paso a paso.
""",
    model="gpt-4.1-mini",
    mcp_servers=[mcp_stdio]
)

practical_agent = Agent(
    name="Practical Agent",
    instructions="""
Eres un asistente práctico y directo. Da consejos claros y soluciones útiles.
Si la solicitud requiere un saludo, usa la FunctionTool greet_user.
Si requiere hora o leer archivos, usa MCP tools now_iso o read_text.
Si no puedes responder, deriva a Greet, Tech o General Agent.
""",
    model="gpt-4.1-mini",
    mcp_servers=[mcp_stdio],
    tools=[text_length_tool],
    handoffs=[agent_greet, agent_tech, agent_general]
)

# ---------------------------
# Agente de triage
# ---------------------------
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
Eres un agente de triage que decide a qué agente enviar cada mensaje:
- Usa 'Philosophy Agent' para preguntas filosóficas o abstractas.
- Usa 'Practical Agent' para preguntas prácticas, saludos o manejo de archivos/hora.
Devuelve solo el nombre del agente seleccionado.
""",
    model="gpt-4.1-mini",
    handoffs=[agent_philosophy, practical_agent]
)
# ---------------------------
# Agente Forzado
# ---------------------------
@function_tool
def get_weather(city: str) -> str:
    """Returns weather info for the specified city."""
    return f"The weather in {city} is sunny"

forced_agent = Agent(
    name="Weather Agent",
    instructions="Retrieve weather details.",
    tools=[get_weather],
    model_settings=ModelSettings(tool_choice="get_weather") 
)
# ---------------------------
# Agente de contexto como tool
# ---------------------------
@function_tool
async def get_context_summary(session_id: str) -> str:
    """
    Devuelve un mensaje con los items de la sesión.
    """
    session = SQLiteSession(session_id, db_path=Path("memory/threads.db"))
    items = await session.get_items()
    return "\n".join(items)

context_agent = Agent(
    name="Context Agent",
    instructions="Proporciona un resumen contextual de la conversación.",
    tools=[get_context_summary],
    model_settings=ModelSettings(tool_choice="get_context_summary")
)

triage_agent.tools.append(
    context_agent.as_tool(
        tool_name="get_context",
        tool_description="Obtiene un resumen del contexto de la conversación"
    )
)