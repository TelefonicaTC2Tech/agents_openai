from __future__ import annotations
import asyncio
from dataclasses import dataclass
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import Agent, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, RunContextWrapper, Runner, TResponseInputItem, input_guardrail

# -----------------------------
# Objeto contexto
# -----------------------------
@dataclass
class MathContext:
    session_id: str
    math_attempts: int = 0

# -----------------------------
# Esquema de salida del guardrail
# -----------------------------
class MathHomeworkOutput(BaseModel):
    reasoning: str
    is_math_homework: bool

# -----------------------------
# Agente que detecta tarea de matemáticas
# -----------------------------
agente_guardrail = Agent(
    name="Chequeo de guardrail",
    instructions="Detecta si el usuario está pidiendo resolver tareas de matemáticas.",
    output_type=MathHomeworkOutput,
)

# -----------------------------
# Guardrail de entrada que usa contexto
# -----------------------------
@input_guardrail
async def math_guardrail(context: RunContextWrapper[MathContext], agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    """Verifica si el mensaje es tarea de matemáticas usando un agente y actualiza el contexto."""
    
    result = await Runner.run(agente_guardrail, input, context=context.context)
    salida = result.final_output_as(MathHomeworkOutput)
    
    # Si se dispara el guardrail, incrementamos el contador en el contexto
    if salida.is_math_homework:
        context.context.math_attempts += 1
    
    return GuardrailFunctionOutput(
        output_info=salida,
        tripwire_triggered=salida.is_math_homework,
    )

# -----------------------------
# Agente principal con guardrail
# -----------------------------
async def main():
    load_dotenv()

    contexto = MathContext(session_id="usuario123")
    
    agente_soporte = Agent(
        name="Agente de soporte al cliente",
        instructions="Ayuda a los clientes con sus preguntas, pero no resuelvas tareas de matemáticas.",
        input_guardrails=[math_guardrail],
    )

    input_data: list[TResponseInputItem] = []

    while True:
        user_input = input("Escribe un mensaje: ")
        input_data.append({"role": "user", "content": user_input})

        try:
            result = await Runner.run(agente_soporte, input_data, context=contexto)
            print(f"Agente: {result.final_output}")
            input_data = result.to_input_list()
        except InputGuardrailTripwireTriggered:
            mensaje = f"Lo siento, no puedo ayudarte con tu tarea de matemáticas. Intentos hasta ahora: {contexto.math_attempts}"
            print(mensaje)
            input_data.append({"role": "assistant", "content": mensaje})

if __name__ == "__main__":
    asyncio.run(main())
