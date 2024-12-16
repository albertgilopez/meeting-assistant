"""
Módulo para calcular costos y tokens de la API de OpenAI.

Este módulo proporciona funciones para calcular el número de tokens
y el costo estimado de las llamadas a la API de OpenAI.

https://openai.com/pricing
https://github.com/openai/openai-cookbook/blob/main/examples/
How_to_count_tokens_with_tiktoken.ipynb

"""

from typing import Dict, Union

import tiktoken

from .config import DEFAULT_MODEL

# Precios por 1K tokens (actualizar según cambios de OpenAI)
MODEL_PRICES: Dict[str, Dict[str, float]] = {
    "gpt-4": {
        "input": 0.03,
        "output": 0.06
    },
    "gpt-3.5-turbo": {
        "input": 0.0015,
        "output": 0.002
    }
}

def get_token_count(text: str, model: str = DEFAULT_MODEL) -> int:
    """
    Calcula el número de tokens en un texto.

    Args:
        text: Texto a analizar.
        model: Nombre del modelo de OpenAI a usar.

    Returns:
        int: Número de tokens en el texto.

    Raises:
        ValueError: Si el modelo no es soportado.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except KeyError:
        raise ValueError(f"Modelo no soportado: {model}")

def calculate_token_cost(
    input_text: str,
    max_output_tokens: int,
    model: str = DEFAULT_MODEL
) -> float:
    """
    Calcula el costo estimado de una llamada a la API.

    Args:
        input_text: Texto de entrada.
        max_output_tokens: Número máximo de tokens en la respuesta.
        model: Nombre del modelo de OpenAI a usar.

    Returns:
        float: Costo estimado en dólares.

    Raises:
        ValueError: Si el modelo no está en la lista de precios.
    """
    if model not in MODEL_PRICES:
        raise ValueError(
            f"No se encontraron precios para el modelo {model}. "
            f"Modelos soportados: {list(MODEL_PRICES.keys())}"
        )

    input_tokens = get_token_count(input_text, model)
    prices = MODEL_PRICES[model]

    input_cost = (input_tokens / 1000) * prices["input"]
    output_cost = (max_output_tokens / 1000) * prices["output"]

    return input_cost + output_cost

def format_token_info(
    text: str,
    model: str = DEFAULT_MODEL
) -> Dict[str, Union[int, float]]:
    """
    Genera un resumen de tokens y costos para un texto.

    Args:
        text: Texto a analizar.
        model: Nombre del modelo de OpenAI a usar.

    Returns:
        Dict[str, Union[int, float]]: Diccionario con información de tokens y costos.
    """
    token_count = get_token_count(text, model)
    cost = calculate_token_cost(text, token_count, model)

    return {
        "token_count": token_count,
        "estimated_cost": cost,
        "model": model
    }