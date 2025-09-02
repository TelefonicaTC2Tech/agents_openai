from typing import Any
from pydantic import BaseModel
from agents import FunctionTool

# ---------------------------
# Definir argumentos con Pydantic
# ---------------------------
class TextLengthArgs(BaseModel):
    text: str

# ---------------------------
# Lógica de negocio
# ---------------------------
def get_text_length(text: str) -> str:
    length = len(text)
    return f"El texto tiene {length} caracteres."

# ---------------------------
# Adaptador para que el agente la pueda usar
# ---------------------------
async def run_text_length(ctx: Any, args: str) -> str:
    parsed = TextLengthArgs.model_validate_json(args)
    return get_text_length(parsed.text)

# ---------------------------
# Registrar la tool
# ---------------------------
text_length_tool = FunctionTool(
    name="text_length",
    description="Devuelve la cantidad de caracteres de un texto dado",
    params_json_schema=TextLengthArgs.model_json_schema(),
    on_invoke_tool=run_text_length,
)
