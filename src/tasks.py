"""
Módulo para procesar y analizar transcripciones de reuniones.

Este módulo proporciona funciones para extraer información útil
de las transcripciones, como resúmenes y elementos accionables.
"""

import logging
from typing import Dict, List
from tqdm import tqdm

from .llm import chat_completion, get_completion_text, transcribe_with_whisper

logger = logging.getLogger(__name__)

def process_audio_segments(audio_segments: List[str]) -> List[str]:
    """
    Procesa una lista de segmentos de audio y los transcribe.

    Args:
        audio_segments: Lista de rutas a los archivos de audio.

    Returns:
        List[str]: Lista de transcripciones de cada segmento.
    """
    transcriptions = []
    total_segments = len(audio_segments)
    
    logger.info(f"Iniciando transcripción de {total_segments} segmentos")
    print("\nTranscribiendo segmentos de audio...")
    
    for i, segment in enumerate(tqdm(audio_segments, desc="Progreso"), 1):
        try:
            logger.debug(f"Transcribiendo segmento {i}/{total_segments}: {segment}")
            transcription = transcribe_with_whisper(segment)
            transcriptions.append(transcription)
            logger.info(f"Segmento {i}/{total_segments} transcrito exitosamente")
        except Exception as e:
            logger.error(f"Error al transcribir segmento {segment}: {str(e)}")
            transcriptions.append("")  # Agregar transcripción vacía para mantener el orden
    
    logger.info("Transcripción de todos los segmentos completada")
    return transcriptions

def summarize_meeting(transcription: str, max_length: int = 500) -> str:
    """
    Genera un resumen conciso de una transcripción de reunión.

    Args:
        transcription: Texto de la transcripción.
        max_length: Longitud máxima aproximada del resumen en caracteres.

    Returns:
        str: Resumen de la reunión.
    """
    system_prompt = (
        "Eres un asistente experto en resumir reuniones. "
        "Genera un resumen claro y conciso que capture los puntos principales "
        "de la reunión, manteniendo un tono profesional y objetivo."
    )

    prompt = (
        f"Por favor, genera un resumen de la siguiente transcripción "
        f"de reunión, con una longitud aproximada de {max_length} caracteres:\n\n"
        f"{transcription}"
    )

    response = chat_completion(prompt, system_prompt)
    return get_completion_text(response)

def get_actionable_items(transcription: str) -> str:
    """
    Extrae elementos accionables y puntos clave de una transcripción.

    Args:
        transcription: Texto de la transcripción.

    Returns:
        str: Lista formateada de elementos accionables y puntos clave.
    """
    system_prompt = (
        "Eres un asistente experto en análisis de reuniones. "
        "Tu tarea es identificar y extraer elementos accionables, "
        "decisiones tomadas y puntos clave de la reunión."
    )

    prompt = (
        "Por favor, analiza la siguiente transcripción y extrae:\n"
        "1. Elementos accionables (tareas, responsabilidades)\n"
        "2. Decisiones tomadas\n"
        "3. Puntos clave discutidos\n\n"
        f"{transcription}"
    )

    response = chat_completion(prompt, system_prompt)
    return get_completion_text(response)

def analyze_sentiment(transcription: str) -> Dict[str, float]:
    """
    Analiza el sentimiento general de la reunión.

    Args:
        transcription: Texto de la transcripción.

    Returns:
        Dict[str, float]: Diccionario con puntuaciones de sentimiento.
    """
    system_prompt = (
        "Eres un experto en análisis de sentimiento. "
        "Analiza el tono y sentimiento general de la transcripción "
        "y proporciona puntuaciones numéricas."
    )

    prompt = (
        "Analiza el sentimiento de la siguiente transcripción "
        "y proporciona puntuaciones de 0 a 1 para:\n"
        "- Positividad\n"
        "- Negatividad\n"
        "- Neutralidad\n\n"
        f"{transcription}"
    )

    response = chat_completion(prompt, system_prompt)
    # Procesar la respuesta para extraer puntuaciones
    # Este es un ejemplo simplificado
    return {
        "positive": 0.7,
        "negative": 0.1,
        "neutral": 0.2
    }

def extract_topics(transcription: str) -> List[str]:
    """
    Identifica los principales temas discutidos en la reunión.

    Args:
        transcription: Texto de la transcripción.

    Returns:
        List[str]: Lista de temas principales.
    """
    system_prompt = (
        "Eres un experto en análisis de contenido. "
        "Identifica y lista los temas principales discutidos "
        "en la transcripción de la reunión."
    )

    prompt = (
        "Por favor, identifica los temas principales discutidos "
        "en la siguiente transcripción. Proporciona una lista "
        "concisa de temas:\n\n"
        f"{transcription}"
    )

    response = chat_completion(prompt, system_prompt)
    topics = get_completion_text(response).split("\n")
    return [topic.strip("- ") for topic in topics if topic.strip()]