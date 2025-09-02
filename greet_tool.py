from typing import Any
from pydantic import BaseModel
from agents import FunctionTool

# ---------------------------
# Definir argumentos con Pydantic
# ---------------------------
class GreetArgs(BaseModel):
    name: str

# ---------------------------
# Lógica de negocio
# ---------------------------
def do_greet(name: str) -> str:
    """Genera un saludo personalizado."""
    return f"¡Hola, {name}! Encantado de saludarte."

# ---------------------------
# Adaptador para que el agente la pueda usar
# ---------------------------
async def run_greet(ctx: Any, args: str) -> str:
    """Parsea los argumentos y ejecuta la lógica del saludo."""
    parsed = GreetArgs.model_validate_json(args)  # Convierte JSON a objeto Pydantic
    return do_greet(parsed.name)

# ---------------------------
# Registrar la tool
# ---------------------------
greet_tool = FunctionTool(
    name="greet_user",
    description="Saluda a un usuario por su nombre.",
    params_json_schema=GreetArgs.model_json_schema(),
    on_invoke_tool=run_greet,
)
