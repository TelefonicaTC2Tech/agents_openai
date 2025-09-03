from __future__ import annotations
import json
import asyncio

from agents import Agent, FileSearchTool, Runner, run_demo_loop
from dotenv import load_dotenv


# ---------------------------
# Agente con conocimientos
# ---------------------------
vs_agent = Agent(
    name="Agente con conocimientos retailmax",
    instructions=(
        "Responde en español de manera breve. "
        "Para responder a consultas sobre clientes, busca primero en los vector stores locales:\n"
        "- Vector store de tecnología y actuaciones (cliente, tecnología, actuación)\n"
        "- Vector store organizativo (cliente, ubicación, número de empleados)\n"
        "Si la consulta menciona un cliente específico, proporciona la información disponible de manera clara y concisa. "
        "Si no hay información disponible, indica que no se encontró información para ese cliente."),
    model="gpt-4.1-mini",
        tools=[
        FileSearchTool(
            max_num_results=3,
            vector_store_ids=["vs_68b847ce61348191be5b628512e3474b"],
        ),
    ],
)

async def main():
    load_dotenv()
    await run_demo_loop(vs_agent)


if __name__ == "__main__":
    asyncio.run(main())
