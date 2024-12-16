"""
Tests para el módulo de procesamiento de audio.
"""

import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from pydub import AudioSegment

from src.audio_divide import (
    convert_to_audio,
    get_audio_duration,
    split_audio
)

@pytest.fixture
def temp_audio_file(tmp_path):
    """Fixture que crea un archivo de audio temporal para pruebas."""
    # Crear un archivo de audio de prueba usando pydub
    audio = AudioSegment.silent(duration=5000)  # 5 segundos de silencio
    audio_path = tmp_path / "test_audio.mp3"
    audio.export(str(audio_path), format="mp3")
    return audio_path

@pytest.fixture
def temp_video_file(tmp_path):
    """Fixture que simula un archivo de video temporal."""
    video_path = tmp_path / "test_video.mp4"
    # Crear un archivo vacío
    video_path.write_text("")
    return video_path

def test_get_audio_duration(temp_audio_file):
    """Prueba la función de obtención de duración de audio."""
    duration = get_audio_duration(str(temp_audio_file))
    assert isinstance(duration, float)
    assert duration > 0
    assert duration <= 1  # El archivo de prueba dura 5 segundos = 0.0833 minutos

def test_get_audio_duration_nonexistent_file(tmp_path):
    """Prueba el manejo de error para archivos inexistentes."""
    nonexistent_file = tmp_path / "nonexistent.mp3"
    with pytest.raises(FileNotFoundError):
        get_audio_duration(str(nonexistent_file))

@patch('moviepy.editor.VideoFileClip')
def test_convert_to_audio(mock_video_clip, temp_video_file, tmp_path):
    """Prueba la conversión de video a audio."""
    # Configurar el mock
    mock_audio = Mock()
    mock_video = Mock()
    mock_video.audio = mock_audio
    mock_video_clip.return_value = mock_video

    # Ejecutar la función
    output_path = convert_to_audio(str(temp_video_file))
    
    # Verificaciones
    assert isinstance(output_path, str)
    assert output_path.endswith('.mp3')
    mock_video_clip.assert_called_once_with(str(temp_video_file))
    mock_audio.write_audiofile.assert_called_once()
    mock_video.close.assert_called_once()

def test_convert_to_audio_nonexistent_file(tmp_path):
    """Prueba el manejo de error para archivos de video inexistentes."""
    nonexistent_file = tmp_path / "nonexistent.mp4"
    with pytest.raises(FileNotFoundError):
        convert_to_audio(str(nonexistent_file))

def test_split_audio_short_file(temp_audio_file):
    """Prueba que no se dividen archivos cortos."""
    result = split_audio(str(temp_audio_file), max_length_minutes=1)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == str(temp_audio_file)

@pytest.fixture
def long_audio_file(tmp_path):
    """Fixture que crea un archivo de audio largo para pruebas."""
    # Crear un audio de 2 minutos
    audio = AudioSegment.silent(duration=120000)  # 120 segundos
    audio_path = tmp_path / "long_audio.mp3"
    audio.export(str(audio_path), format="mp3")
    return audio_path

def test_split_audio_long_file(long_audio_file):
    """Prueba la división de archivos largos."""
    # Dividir en segmentos de 1 minuto
    result = split_audio(str(long_audio_file), max_length_minutes=1)
    
    assert isinstance(result, list)
    assert len(result) > 1
    assert all(os.path.exists(path) for path in result)
    assert all(path.endswith('.mp3') for path in result)

def test_split_audio_nonexistent_file(tmp_path):
    """Prueba el manejo de error para archivos inexistentes."""
    nonexistent_file = tmp_path / "nonexistent.mp3"
    with pytest.raises(FileNotFoundError):
        split_audio(str(nonexistent_file)) 