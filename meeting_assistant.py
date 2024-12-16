#!/usr/bin/env python3
"""
Script principal para el asistente de reuniones.
Procesa archivos de audio/video y genera transcripciones y resúmenes.
"""

import os
import sys
import logging
from pathlib import Path
from tqdm import tqdm

from src.audio_divide import check_ffmpeg_installation
from src.config import load_config, OUTPUT_DIR
from src.llm import generate_summary
from src.tasks import process_audio_segments
from src.transcriptions import (
    transcribe_audio,
    is_audio_file,
    is_video_file,
    SUPPORTED_AUDIO_EXTENSIONS,
    SUPPORTED_VIDEO_EXTENSIONS
)

logger = logging.getLogger(__name__)

def main():
    """Función principal del script."""
    if len(sys.argv) != 2:
        print("Uso: python meeting_assistant.py <ruta_al_archivo>")
        print(f"\nFormatos de archivo soportados:")
        print(f"Audio: {', '.join(SUPPORTED_AUDIO_EXTENSIONS)}")
        print(f"Video: {', '.join(SUPPORTED_VIDEO_EXTENSIONS)}")
        sys.exit(1)

    # Verificar la instalación de ffmpeg
    if not check_ffmpeg_installation():
        print("Error: ffmpeg no está instalado en el sistema.")
        print("Por favor, instale ffmpeg antes de continuar:")
        print("Windows (con chocolatey): choco install ffmpeg")
        print("Linux: sudo apt-get install ffmpeg")
        print("macOS (con homebrew): brew install ffmpeg")
        sys.exit(1)

    # Cargar configuración
    config = load_config()
    if not config.get('OPENAI_API_KEY'):
        print("Error: No se ha configurado la API key de OpenAI")
        print("Por favor, configure la variable de entorno OPENAI_API_KEY")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: No se encontró el archivo: {input_file}")
        sys.exit(1)

    try:
        # Verificar tipo de archivo
        if not (is_audio_file(input_file) or is_video_file(input_file)):
            print(f"Error: Formato de archivo no soportado: {Path(input_file).suffix}")
            print(f"\nFormatos soportados:")
            print(f"Audio: {', '.join(SUPPORTED_AUDIO_EXTENSIONS)}")
            print(f"Video: {', '.join(SUPPORTED_VIDEO_EXTENSIONS)}")
            sys.exit(1)

        print("\n=== Iniciando procesamiento del archivo ===")
        if is_video_file(input_file):
            print("Tipo de archivo: Video")
            print("Se convertirá a formato de audio...")
        else:
            print("Tipo de archivo: Audio")
            print("Procesando directamente...")

        # Crear directorio de salida si no existe
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directorio de salida: {OUTPUT_DIR}")

        # Mostrar progreso general
        steps = ["Preparación", "Transcripción", "Generación de resumen", "Guardado"]
        with tqdm(total=len(steps), desc="Progreso general", position=0) as pbar:
            # Paso 1: Preparación y transcripción
            pbar.set_description("Preparando archivo...")
            transcription = transcribe_audio(input_file)
            pbar.update(1)
            
            # Paso 2: Transcripción completada
            pbar.set_description("Transcripción completada")
            pbar.update(1)
            
            # Paso 3: Generación de resumen
            pbar.set_description("Generando resumen...")
            summary = generate_summary(transcription)
            pbar.update(1)
            
            # Paso 4: Guardado de archivos
            pbar.set_description("Guardando archivos...")
            base_name = Path(input_file).stem
            
            # Guardar en el directorio de salida
            transcription_file = OUTPUT_DIR / f"{base_name}_transcripcion.txt"
            with open(transcription_file, "w", encoding="utf-8") as f:
                f.write(transcription)
            
            summary_file = OUTPUT_DIR / f"{base_name}_resumen.txt"
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write(summary)
            
            pbar.update(1)

        print("\n=== Proceso completado exitosamente ===")
        print(f"Archivos generados en: {OUTPUT_DIR}")
        print(f"1. Transcripción: {transcription_file.name}")
        print(f"2. Resumen: {summary_file.name}")

    except Exception as e:
        logger.error(f"Error al procesar el archivo: {str(e)}")
        print(f"\nError al procesar el archivo: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()


