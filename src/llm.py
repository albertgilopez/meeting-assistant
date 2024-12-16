"""
Módulo de integración con modelos de lenguaje de OpenAI.

Este módulo proporciona funciones para interactuar con los modelos GPT y Whisper
de OpenAI, manejando la comunicación con la API y el procesamiento de respuestas.
"""

from typing import Any, Dict, Optional

import openai

from .config import MAX_TOKENS, DEFAULT_MODEL, get_api_key, WHISPER_MODEL
from .token_cost import calculate_token_cost

# Configurar la API key
openai.api_key = get_api_key()

def transcribe_with_whisper(audio_file_path: str, language: Optional[str] = None) -> str:
    """
    Transcribe un archivo de audio usando el modelo Whisper de OpenAI.

    Args:
        audio_file_path: Ruta al archivo de audio a transcribir.
        language: Código ISO del idioma del audio (opcional).

    Returns:
        str: Texto transcrito del audio.

    Raises:
        FileNotFoundError: Si no se encuentra el archivo de audio.
        openai.error.OpenAIError: Si hay un error en la API de OpenAI.
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            response = openai.Audio.transcribe(
                model=WHISPER_MODEL,
                file=audio_file,
                language=language
            )
        return response["text"]
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {audio_file_path}")
    except Exception as e:
        raise openai.error.OpenAIError(f"Error en la transcripción: {str(e)}")

def chat_completion(
    prompt: str,
    system_prompt: Optional[str] = None,
    max_tokens: int = MAX_TOKENS,
    temperature: float = 0.7
) -> Dict[str, Any]:
    """
    Genera una respuesta usando el modelo GPT de OpenAI.

    Args:
        prompt: Texto de entrada para el modelo.
        system_prompt: Instrucciones de sistema para el modelo (opcional).
        max_tokens: Número máximo de tokens en la respuesta.
        temperature: Temperatura para la generación (0-1).

    Returns:
        Dict[str, Any]: Respuesta completa de la API.

    Raises:
        openai.error.OpenAIError: Si hay un error en la API de OpenAI.
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    try:
        # Calcular costo estimado
        estimated_cost = calculate_token_cost(prompt, max_tokens)
        print(f"Costo estimado: ${estimated_cost:.4f}")

        response = openai.ChatCompletion.create(
            model=DEFAULT_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            n=1,
            stop=None
        )
        return response
    except Exception as e:
        raise openai.error.OpenAIError(f"Error en la generación de texto: {str(e)}")

def get_completion_text(response: Dict[str, Any]) -> str:
    """
    Extrae el texto de la respuesta de la API.

    Args:
        response: Respuesta completa de la API de OpenAI.

    Returns:
        str: Texto generado por el modelo.
    """
    return response['choices'][0]['message']['content'].strip()

def generate_summary(text: str) -> str:
    """
    Genera un resumen del texto proporcionado.

    Args:
        text: Texto a resumir.

    Returns:
        str: Resumen generado.

    Raises:
        openai.error.OpenAIError: Si hay un error en la API de OpenAI.
    """
    system_prompt = """
    Eres un asistente experto en resumir reuniones. 
    Genera un resumen conciso pero informativo que incluya:
    1. Puntos principales discutidos
    2. Decisiones tomadas
    3. Acciones a realizar
    4. Próximos pasos
    """
    
    prompt = f"Por favor, resume el siguiente texto de una reunión:\n\n{text}"
    
    try:
        response = chat_completion(prompt, system_prompt=system_prompt)
        return get_completion_text(response)
    except Exception as e:
        raise openai.error.OpenAIError(f"Error al generar el resumen: {str(e)}")