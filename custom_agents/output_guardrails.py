from __future__ import annotations
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    output_guardrail,
    TResponseInputItem,
)

# ---------------------------
# Modelo de salida del agente
# ---------------------------
class SalidaMensaje(BaseModel):
    razonamiento: str = Field(description="Pensamiento sobre cómo responder")
    respuesta: str = Field(description="Respuesta final al usuario")

# ---------------------------
# Guardrail de salida
# ---------------------------
@output_guardrail
async def phone_guardrail(
    context: RunContextWrapper,
    agent: Agent,
    output: SalidaMensaje
) -> GuardrailFunctionOutput:
    contiene_numero = any(digito.isdigit() for digito in output.respuesta)
    return GuardrailFunctionOutput(
        output_info={"contiene_numero": contiene_numero},
        tripwire_triggered=contiene_numero,
    )

# ---------------------------
# Agente con guardrail
# ---------------------------
agente = Agent(
    name="Asistente",
    instructions="Eres un asistente útil. Nunca debes dar números de teléfono.",
    output_type=SalidaMensaje,
    output_guardrails=[phone_guardrail],
)

# ---------------------------
# Agente principal con guardrail
# ---------------------------
async def main():
    load_dotenv()
    input_data: list[TResponseInputItem] = []

    while True:
        user_input = input("Escribe un mensaje: ")
        input_data.append({"role": "user", "content": user_input})

        try:
            result = await Runner.run(agente, input_data)
            salida = result.final_output_as(SalidaMensaje)
            print(f"Agente: {salida.respuesta}")
            input_data = result.to_input_list()
        except OutputGuardrailTripwireTriggered as e:
            print("Guardrail activado: No puedo compartir números de teléfono.")
            input_data.append(
                {"role": "assistant", "content": "Lo siento, no puedo compartir números de teléfono."}
            )

if __name__ == "__main__":
    asyncio.run(main())
