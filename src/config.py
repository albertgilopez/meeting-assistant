"""
Módulo de configuración para el asistente de reuniones.

Este módulo maneja la configuración global y las variables de entorno.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno desde .env si existe
load_dotenv()
logger.info("Variables de entorno cargadas")

# Configuración de rutas
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Configuración de audio
MAX_AUDIO_LENGTH_MINUTES = int(os.getenv('MAX_AUDIO_LENGTH_MINUTES', 10))
DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'es')

# Configuración de OpenAI
DEFAULT_MODEL = os.getenv('MODEL', 'gpt-3.5-turbo')
WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'whisper-1')
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 4000))

def load_config() -> Dict[str, str]:
    """
    Carga la configuración del sistema desde variables de entorno.

    Returns:
        Dict[str, str]: Diccionario con la configuración cargada.
    """
    config = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'MODEL': os.getenv('MODEL', DEFAULT_MODEL),
        'WHISPER_MODEL': os.getenv('WHISPER_MODEL', WHISPER_MODEL),
        'MAX_TOKENS': int(os.getenv('MAX_TOKENS', MAX_TOKENS)),
        'DEFAULT_LANGUAGE': os.getenv('DEFAULT_LANGUAGE', DEFAULT_LANGUAGE),
        'MAX_AUDIO_LENGTH_MINUTES': int(os.getenv('MAX_AUDIO_LENGTH_MINUTES', MAX_AUDIO_LENGTH_MINUTES)),
    }
    return config

def get_api_key() -> Optional[str]:
    """
    Obtiene la API key de OpenAI.

    Returns:
        Optional[str]: API key si está configurada, None en caso contrario.
    """
    return os.getenv('OPENAI_API_KEY')

def validate_config() -> None:
    """
    Valida que la configuración necesaria esté presente.

    Raises:
        ValueError: Si falta alguna configuración necesaria.
    """
    if not get_api_key():
        raise ValueError(
            "No se encontró la API key de OpenAI. "
            "Por favor, configura la variable de entorno OPENAI_API_KEY"
        )

    if not OUTPUT_DIR.exists():
        raise ValueError(
            f"No se pudo crear el directorio de salida: {OUTPUT_DIR}"
        )