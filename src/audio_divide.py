"""
Módulo para el procesamiento y manipulación de archivos de audio/video.

Este módulo proporciona funciones para dividir, convertir y procesar
archivos de audio y video en formatos manejables para la transcripción.
"""

import os
import logging
import subprocess
import time
from pathlib import Path
from typing import List, Optional

import ffmpeg
import moviepy.editor as mp
from pydub import AudioSegment
from tqdm import tqdm

from .config import MAX_AUDIO_LENGTH_MINUTES, OUTPUT_DIR

logger = logging.getLogger(__name__)

def convert_to_audio(video_path: str, output_path: Optional[str] = None) -> str:
    """
    Convierte un archivo de video a audio.

    Args:
        video_path: Ruta al archivo de video.
        output_path: Ruta donde guardar el archivo de audio. Si no se especifica,
                    se usa el mismo nombre del video con extensión .mp3.

    Returns:
        str: Ruta al archivo de audio generado.

    Raises:
        FileNotFoundError: Si no se encuentra el archivo de video.
        ValueError: Si el formato de video no es soportado.
    """
    if not os.path.exists(video_path):
        logger.error(f"No se encontró el archivo: {video_path}")
        raise FileNotFoundError(f"No se encontró el archivo: {video_path}")

    if output_path is None:
        # Usar la carpeta output para archivos temporales
        output_path = str(OUTPUT_DIR / f"{Path(video_path).stem}_audio.mp3")
    
    logger.info(f"Iniciando conversión de {video_path} a {output_path}")
    print("\nConvirtiendo video a audio...")

    try:
        # Intentar primero con ffmpeg directamente
        logger.debug("Intentando conversión con ffmpeg...")
        
        # Obtener duración del video para la barra de progreso
        probe = ffmpeg.probe(video_path)
        duration = float(probe['streams'][0]['duration'])
        
        process = (
            ffmpeg
            .input(video_path)
            .output(output_path, acodec='libmp3lame')
            .overwrite_output()
            .run_async(pipe_stdout=True, pipe_stderr=True)
        )
        
        # Barra de progreso
        pbar = tqdm(total=100, desc="Progreso")
        start_time = time.time()
        last_progress = 0
        
        while process.poll() is None:
            time_elapsed = time.time() - start_time
            progress = min(100, int((time_elapsed / duration) * 100))
            pbar.update(progress - last_progress)
            last_progress = progress
            time.sleep(0.1)
        
        pbar.close()
        logger.info("Conversión con ffmpeg exitosa")
        return output_path
        
    except ffmpeg.Error as e:
        logger.warning(f"FFmpeg error: {str(e)}, intentando con moviepy...")
        try:
            # Si ffmpeg falla, intentar con moviepy
            logger.debug("Iniciando conversión con moviepy...")
            video = mp.VideoFileClip(video_path)
            if video.audio is not None:
                # Configurar callback para la barra de progreso
                def progress_callback(t):
                    pbar.update(int(t * 100) - pbar.n)
                
                pbar = tqdm(total=100, desc="Progreso")
                video.audio.write_audiofile(output_path, logger=None, progress_callback=progress_callback)
                pbar.close()
                video.close()
                logger.info("Conversión con moviepy exitosa")
                return output_path
            else:
                logger.error("El video no contiene audio")
                raise ValueError("El video no contiene audio")
        except Exception as e:
            logger.error(f"Error en la conversión con moviepy: {str(e)}")
            raise ValueError(f"Error al convertir el video: {str(e)}")
        finally:
            if 'video' in locals():
                video.close()

def split_audio(audio_path: str, max_length_minutes: int = MAX_AUDIO_LENGTH_MINUTES) -> List[str]:
    """
    Divide un archivo de audio en segmentos más pequeños.

    Args:
        audio_path: Ruta al archivo de audio.
        max_length_minutes: Duración máxima en minutos de cada segmento.

    Returns:
        List[str]: Lista de rutas a los segmentos de audio generados.

    Raises:
        FileNotFoundError: Si no se encuentra el archivo de audio.
        ValueError: Si el formato de audio no es soportado.
    """
    if not os.path.exists(audio_path):
        logger.error(f"No se encontró el archivo: {audio_path}")
        raise FileNotFoundError(f"No se encontró el archivo: {audio_path}")

    try:
        # Cargar el audio
        logger.info(f"Cargando archivo de audio: {audio_path}")
        print("\nCargando archivo de audio...")
        audio = AudioSegment.from_file(audio_path)
        logger.debug(f"Duración del audio: {len(audio)/1000:.2f} segundos")
        
        # Calcular la duración máxima en milisegundos
        max_length_ms = max_length_minutes * 60 * 1000
        
        # Si el audio es más corto que el máximo, devolverlo sin dividir
        if len(audio) <= max_length_ms:
            logger.info("El audio no necesita ser dividido")
            return [audio_path]
        
        # Dividir el audio en segmentos
        segments = []
        total_segments = len(audio) // max_length_ms + (1 if len(audio) % max_length_ms > 0 else 0)
        logger.info(f"Dividiendo audio en {total_segments} segmentos")
        print(f"\nDividiendo audio en {total_segments} segmentos...")
        
        pbar = tqdm(total=total_segments, desc="Progreso")
        for i in range(0, len(audio), max_length_ms):
            segment = audio[i:i + max_length_ms]
            # Usar la carpeta output para los segmentos
            segment_path = str(OUTPUT_DIR / f"{Path(audio_path).stem}_part{len(segments)+1}.mp3")
            logger.debug(f"Exportando segmento {len(segments)+1} a {segment_path}")
            segment.export(segment_path, format="mp3")
            segments.append(segment_path)
            pbar.update(1)
        
        pbar.close()
        logger.info("División de audio completada")
        return segments
    except Exception as e:
        logger.error(f"Error al procesar el audio: {str(e)}")
        raise ValueError(f"Error al procesar el audio: {str(e)}")

def get_audio_duration(audio_path: str) -> float:
    """
    Obtiene la duración de un archivo de audio en minutos.

    Args:
        audio_path: Ruta al archivo de audio.

    Returns:
        float: Duración del audio en minutos.

    Raises:
        FileNotFoundError: Si no se encuentra el archivo de audio.
        ValueError: Si el formato de audio no es soportado.
    """
    if not os.path.exists(audio_path):
        logger.error(f"No se encontró el archivo: {audio_path}")
        raise FileNotFoundError(f"No se encontró el archivo: {audio_path}")

    try:
        # Intentar primero con ffmpeg
        logger.debug(f"Obteniendo duración con ffmpeg: {audio_path}")
        probe = ffmpeg.probe(audio_path)
        duration = float(probe['streams'][0]['duration'])
        logger.info(f"Duración del audio: {duration/60:.2f} minutos")
        return duration / 60  # Convertir segundos a minutos
    except ffmpeg.Error:
        try:
            # Si ffmpeg falla, intentar con pydub
            logger.debug("FFmpeg falló, intentando con pydub")
            audio = AudioSegment.from_file(audio_path)
            duration = len(audio) / (1000 * 60)  # Convertir de milisegundos a minutos
            logger.info(f"Duración del audio: {duration:.2f} minutos")
            return duration
        except Exception as e:
            logger.error(f"Error al obtener la duración del audio: {str(e)}")
            raise ValueError(f"Error al obtener la duración del audio: {str(e)}")

def check_ffmpeg_installation() -> bool:
    """
    Verifica si ffmpeg está instalado en el sistema.

    Returns:
        bool: True si ffmpeg está instalado, False en caso contrario.
    """
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True)
        logger.info("FFmpeg está instalado en el sistema")
        return True
    except FileNotFoundError:
        logger.warning("FFmpeg no está instalado en el sistema")
        return False
