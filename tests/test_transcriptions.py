"""
Tests para el módulo de transcripciones.
"""

import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.transcriptions import (
    open_transcription,
    open_translation,
    save_transcription,
    save_translation,
    transcribe_audio,
    translate_transcription,
    _transcribe_segments
)

@pytest.fixture
def temp_output_dir(tmp_path):
    """Fixture que proporciona un directorio temporal para pruebas."""
    return tmp_path

@pytest.fixture
def sample_text():
    """Fixture que proporciona un texto de ejemplo."""
    return "Esta es una transcripción de prueba"

@pytest.fixture
def mock_audio_file(tmp_path):
    """Fixture que crea un archivo de audio temporal."""
    audio_path = tmp_path / "test.mp3"
    # Crear un archivo con contenido mínimo para que exista
    audio_path.write_bytes(b"MOCK_AUDIO_CONTENT")
    return audio_path

def test_save_and_open_transcription(temp_output_dir, sample_text):
    """Prueba que la transcripción se guarda y lee correctamente."""
    test_file = temp_output_dir / "test_transcription.txt"
    
    # Guardar transcripción
    save_transcription(sample_text, str(test_file))
    assert test_file.exists()
    
    # Leer transcripción
    loaded_text = open_transcription(str(test_file))
    assert loaded_text == sample_text

def test_save_and_open_translation(temp_output_dir, sample_text):
    """Prueba que la traducción se guarda y lee correctamente."""
    test_file = temp_output_dir / "test_translation.txt"
    
    # Guardar traducción
    save_translation(sample_text, str(test_file))
    assert test_file.exists()
    
    # Leer traducción
    loaded_text = open_translation(str(test_file))
    assert loaded_text == sample_text

def test_open_nonexistent_file(temp_output_dir):
    """Prueba que se maneja correctamente el error de archivo no encontrado."""
    nonexistent_file = temp_output_dir / "nonexistent.txt"
    
    with pytest.raises(FileNotFoundError):
        open_transcription(str(nonexistent_file))
    
    with pytest.raises(FileNotFoundError):
        open_translation(str(nonexistent_file))

def test_save_to_nonexistent_directory(temp_output_dir, sample_text):
    """Prueba que se pueden crear directorios automáticamente."""
    nested_dir = temp_output_dir / "nested" / "path"
    test_file = nested_dir / "test.txt"
    
    save_transcription(sample_text, str(test_file))
    assert test_file.exists()
    assert test_file.parent.exists()

@patch('src.transcriptions.transcribe_with_whisper')
@patch('src.transcriptions.convert_to_audio')
@patch('src.transcriptions.get_audio_duration')
@patch('os.path.exists')
def test_transcribe_audio_video_file(
    mock_exists,
    mock_duration,
    mock_convert,
    mock_transcribe,
    mock_audio_file
):
    """Prueba la transcripción de un archivo de video."""
    # Configurar mocks
    mock_exists.return_value = True
    mock_duration.return_value = 5  # 5 minutos
    mock_convert.return_value = str(mock_audio_file)
    mock_transcribe.return_value = "Transcripción de prueba"
    
    # Probar con archivo de video
    result = transcribe_audio("video.mp4")
    
    assert isinstance(result, str)
    assert result == "Transcripción de prueba"
    mock_convert.assert_called_once()
    mock_transcribe.assert_called_once()

@patch('src.transcriptions.transcribe_with_whisper')
@patch('src.transcriptions.get_audio_duration')
@patch('src.transcriptions.split_audio')
@patch('os.path.exists')
def test_transcribe_audio_long_file(
    mock_exists,
    mock_split,
    mock_duration,
    mock_transcribe,
    mock_audio_file
):
    """Prueba la transcripción de un archivo de audio largo."""
    # Configurar mocks
    mock_exists.return_value = True
    mock_duration.return_value = 90  # 90 minutos
    mock_split.return_value = ["part1.mp3", "part2.mp3"]
    mock_transcribe.return_value = "Parte de transcripción"
    
    # Probar con archivo largo
    result = transcribe_audio(str(mock_audio_file))
    
    assert isinstance(result, str)
    mock_split.assert_called_once()
    assert mock_transcribe.call_count == 2  # Una vez por cada parte

@patch('src.transcriptions.chat_completion')
def test_translate_transcription(mock_chat, sample_text):
    """Prueba la traducción de texto."""
    mock_chat.return_value = {
        'choices': [{
            'message': {
                'content': 'Texto traducido'
            }
        }]
    }
    
    result = translate_transcription(sample_text)
    
    assert isinstance(result, str)
    assert result == "Texto traducido"
    mock_chat.assert_called_once()

@patch('src.transcriptions.transcribe_with_whisper')
def test_transcribe_segments(mock_transcribe):
    """Prueba la transcripción de múltiples segmentos."""
    segments = ["seg1.mp3", "seg2.mp3", "seg3.mp3"]
    mock_transcribe.return_value = "Segmento transcrito"
    
    result = _transcribe_segments(segments)
    
    assert isinstance(result, str)
    assert mock_transcribe.call_count == len(segments)
    assert len(result.split("\n")) == len(segments)