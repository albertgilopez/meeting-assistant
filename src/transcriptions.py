"""
Módulo para manejar transcripciones y traducciones de audio.

Este módulo proporciona funciones para transcribir audio a texto,
traducir transcripciones y gestionar los archivos resultantes.
"""

import os
import logging
from pathlib import Path
from typing import List, Optional, Set
from tqdm import tqdm

from .audio_divide import convert_to_audio, get_audio_duration, split_audio
from .config import DEFAULT_LANGUAGE, MAX_AUDIO_LENGTH_MINUTES
from .llm import chat_completion, get_completion_text, transcribe_with_whisper

logger = logging.getLogger(__name__)

# Extensiones de archivo de audio soportadas
SUPPORTED_AUDIO_EXTENSIONS: Set[str] = {'.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac'}
# Extensiones de archivo de video soportadas
SUPPORTED_VIDEO_EXTENSIONS: Set[str] = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'}

def is_audio_file(file_path: str) -> bool:
    """
    Verifica si un archivo es un archivo de audio soportado.

    Args:
        file_path: Ruta al archivo.

    Returns:
        bool: True si es un archivo de audio soportado, False en caso contrario.
    """
    return Path(file_path).suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS

def is_video_file(file_path: str) -> bool:
    """
    Verifica si un archivo es un archivo de video soportado.

    Args:
        file_path: Ruta al archivo.

    Returns:
        bool: True si es un archivo de video soportado, False en caso contrario.
    """
    return Path(file_path).suffix.lower() in SUPPORTED_VIDEO_EXTENSIONS

def transcribe_audio(
    audio_path: str,
    language: Optional[str] = DEFAULT_LANGUAGE
) -> str:
    """
    Transcribe un archivo de audio a texto.

    Args:
        audio_path: Ruta al archivo de audio/video.
        language: Código ISO del idioma del audio.

    Returns:
        str: Texto transcrito del audio.

    Raises:
        FileNotFoundError: Si no se encuentra el archivo.
        ValueError: Si el formato no es soportado.
    """
    if not os.path.exists(audio_path):
        logger.error(f"No se encontró el archivo: {audio_path}")
        raise FileNotFoundError(f"No se encontró el archivo: {audio_path}")

    logger.info(f"Iniciando procesamiento de: {audio_path}")

    # Verificar el tipo de archivo
    if not (is_audio_file(audio_path) or is_video_file(audio_path)):
        logger.error(f"Formato de archivo no soportado: {Path(audio_path).suffix}")
        raise ValueError(
            f"Formato no soportado. Formatos soportados: "
            f"Audio: {', '.join(SUPPORTED_AUDIO_EXTENSIONS)}, "
            f"Video: {', '.join(SUPPORTED_VIDEO_EXTENSIONS)}"
        )

    # Convertir a formato de audio si es un video
    if is_video_file(audio_path):
        logger.info("Detectado archivo de video, convirtiendo a formato de audio...")
        audio_path = convert_to_audio(audio_path)
    else:
        logger.info("Detectado archivo de audio, no es necesaria la conversión")

    # Verificar duración
    duration = get_audio_duration(audio_path)
    logger.info(f"Duración del audio: {duration:.1f} minutos")
    
    if duration > MAX_AUDIO_LENGTH_MINUTES:
        logger.info(f"Audio muy largo ({duration:.1f} min), dividiendo en segmentos...")
        segments = split_audio(audio_path, MAX_AUDIO_LENGTH_MINUTES)
        return _transcribe_segments(segments, language)

    logger.info("Transcribiendo audio...")
    try:
        transcription = transcribe_with_whisper(audio_path, language)
        logger.info("Transcripción completada exitosamente")
        return transcription
    except Exception as e:
        logger.error(f"Error durante la transcripción: {str(e)}")
        raise

def translate_transcription(text: str, target_language: str = "es") -> str:
    """
    Traduce una transcripción al idioma especificado.

    Args:
        text: Texto a traducir.
        target_language: Código ISO del idioma objetivo.

    Returns:
        str: Texto traducido.
    """
    system_prompt = (
        f"Eres un traductor profesional. Traduce el siguiente texto al {target_language} "
        "manteniendo el tono y contexto original. Si hay términos técnicos, "
        "mantenlos en su forma original si es apropiado."
    )

    prompt = f"Traduce el siguiente texto:\n\n{text}"

    response = chat_completion(prompt, system_prompt)
    return get_completion_text(response)

def _transcribe_segments(segments: List[str], language: Optional[str] = None) -> str:
    """
    Transcribe múltiples segmentos de audio y los combina.

    Args:
        segments: Lista de rutas a los segmentos de audio.
        language: Código ISO del idioma del audio.

    Returns:
        str: Texto transcrito combinado.
    """
    transcriptions = []
    total_segments = len(segments)
    logger.info(f"Iniciando transcripción de {total_segments} segmentos")
    print(f"\nTranscribiendo {total_segments} segmentos de audio...")

    pbar = tqdm(total=total_segments, desc="Progreso")
    for i, segment in enumerate(segments, 1):
        logger.info(f"Transcribiendo segmento {i}/{total_segments}...")
        try:
            text = transcribe_with_whisper(segment, language)
            transcriptions.append(text)
            logger.info(f"Segmento {i}/{total_segments} transcrito exitosamente")
            pbar.update(1)
        except Exception as e:
            logger.error(f"Error al transcribir segmento {i}: {str(e)}")
            transcriptions.append("")
            pbar.update(1)

    pbar.close()
    logger.info("Combinando transcripciones...")
    return "\n".join(transcriptions)

def save_transcription(text: str, output_path: str) -> None:
    """
    Guarda una transcripción en un archivo.

    Args:
        text: Texto a guardar.
        output_path: Ruta donde guardar el archivo.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

def save_translation(text: str, output_path: str) -> None:
    """
    Guarda una traducción en un archivo.

    Args:
        text: Texto a guardar.
        output_path: Ruta donde guardar el archivo.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

def open_transcription(file_path: str) -> str:
    """
    Lee una transcripción desde un archivo.

    Args:
        file_path: Ruta al archivo de transcripción.

    Returns:
        str: Contenido del archivo.

    Raises:
        FileNotFoundError: Si no se encuentra el archivo.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def open_translation(file_path: str) -> str:
    """
    Lee una traducción desde un archivo.

    Args:
        file_path: Ruta al archivo de traducción.

    Returns:
        str: Contenido del archivo.

    Raises:
        FileNotFoundError: Si no se encuentra el archivo.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
