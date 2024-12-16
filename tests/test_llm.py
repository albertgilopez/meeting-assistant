"""
Tests para el módulo de integración con OpenAI.
"""

import pytest
from unittest.mock import Mock, patch

from src.llm import (
    chat_completion,
    get_completion_text,
    transcribe_with_whisper
)

@pytest.fixture
def mock_openai_response():
    """Fixture que simula una respuesta de la API de OpenAI."""
    return {
        'choices': [{
            'message': {
                'content': 'Respuesta simulada de OpenAI'
            }
        }]
    }

@pytest.fixture
def mock_audio_file(tmp_path):
    """Fixture que crea un archivo de audio temporal."""
    audio_path = tmp_path / "test_audio.mp3"
    audio_path.write_text("")  # Crear archivo vacío
    return audio_path

@patch('openai.ChatCompletion.create')
def test_chat_completion(mock_create, mock_openai_response):
    """Prueba la función de chat completion."""
    mock_create.return_value = mock_openai_response
    
    result = chat_completion(
        prompt="Test prompt",
        system_prompt="Test system prompt"
    )
    
    assert result == mock_openai_response
    mock_create.assert_called_once()
    
    # Verificar argumentos
    call_args = mock_create.call_args[1]
    assert len(call_args['messages']) == 2
    assert call_args['messages'][0]['role'] == 'system'
    assert call_args['messages'][1]['role'] == 'user'

@patch('openai.ChatCompletion.create')
def test_chat_completion_no_system_prompt(mock_create, mock_openai_response):
    """Prueba chat completion sin prompt de sistema."""
    mock_create.return_value = mock_openai_response
    
    result = chat_completion(prompt="Test prompt")
    
    assert result == mock_openai_response
    mock_create.assert_called_once()
    
    # Verificar que solo hay un mensaje
    call_args = mock_create.call_args[1]
    assert len(call_args['messages']) == 1
    assert call_args['messages'][0]['role'] == 'user'

@patch('openai.Audio.transcribe')
def test_transcribe_with_whisper(mock_transcribe, mock_audio_file):
    """Prueba la función de transcripción."""
    mock_transcribe.return_value = {"text": "Transcripción simulada"}
    
    result = transcribe_with_whisper(str(mock_audio_file))
    
    assert isinstance(result, str)
    assert result == "Transcripción simulada"
    mock_transcribe.assert_called_once()

def test_transcribe_with_whisper_nonexistent_file(tmp_path):
    """Prueba el manejo de error para archivos inexistentes."""
    nonexistent_file = tmp_path / "nonexistent.mp3"
    with pytest.raises(FileNotFoundError):
        transcribe_with_whisper(str(nonexistent_file))

def test_get_completion_text(mock_openai_response):
    """Prueba la extracción de texto de la respuesta."""
    text = get_completion_text(mock_openai_response)
    assert isinstance(text, str)
    assert text == "Respuesta simulada de OpenAI"

def test_get_completion_text_invalid_response():
    """Prueba el manejo de respuestas inválidas."""
    invalid_response = {}
    with pytest.raises(KeyError):
        get_completion_text(invalid_response) 