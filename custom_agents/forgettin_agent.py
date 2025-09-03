from __future__ import annotations
import json
import asyncio

from agents import Agent, Runner, HandoffInputData, handoff, run_demo_loop
from dotenv import load_dotenv

# ---------------------------
# Filtro: borra los dos primeros mensajes de la historia (user - assitente)
# ---------------------------
def forget_first_two_filter(handoff_message_data: HandoffInputData) -> HandoffInputData:
    history = tuple(handoff_message_data.input_history[3:])
    return HandoffInputData(
        input_history=history,
        pre_handoff_items=tuple(handoff_message_data.pre_handoff_items),
        new_items=tuple(handoff_message_data.new_items),
    )

# ---------------------------
# Agente al que se transfiere la conversación
# ---------------------------
spanish_agent = Agent(
    name="Agente Español",
    instructions="Responde en español de manera breve.",
    handoff_description="Un agente que habla español.",
    model="gpt-4.1-mini"
)

# ---------------------------
# Agente principal que decide si hacer handoff
# ---------------------------
forgettin_agent = Agent(
    name="Forgetting Agent",
    instructions="Si el usuario escribe en español, transfiere al Agente Español.",
    handoffs=[handoff(spanish_agent, input_filter=forget_first_two_filter)],
    model="gpt-4.1-mini"
)


async def main():
    load_dotenv()
    await run_demo_loop(forgettin_agent)


if __name__ == "__main__":
    asyncio.run(main())
