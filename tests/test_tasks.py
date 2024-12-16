"""
Tests para el módulo de tareas.
"""

import pytest
from unittest.mock import patch

from src.tasks import (
    summarize_meeting,
    get_actionable_items,
    analyze_sentiment,
    extract_topics
)

@pytest.fixture
def sample_transcription():
    """Fixture que proporciona una transcripción de ejemplo."""
    return """
    Juan: Buenos días a todos. Hoy discutiremos el proyecto X.
    María: Me parece bien. Necesitamos definir los plazos.
    Juan: De acuerdo, propongo terminar la fase 1 en dos semanas.
    María: Perfecto, yo me encargaré de la documentación.
    """

@pytest.fixture
def mock_chat_completion():
    """Fixture que simula la respuesta de la API de OpenAI."""
    return {
        'choices': [{
            'message': {
                'content': 'Texto de respuesta simulada'
            }
        }]
    }

@patch('src.tasks.chat_completion')
def test_summarize_meeting(mock_chat, mock_chat_completion, sample_transcription):
    """Prueba la función de resumen de reuniones."""
    mock_chat.return_value = mock_chat_completion
    
    result = summarize_meeting(sample_transcription)
    assert isinstance(result, str)
    assert len(result) > 0
    
    mock_chat.assert_called_once()
    args = mock_chat.call_args[0]
    assert sample_transcription in args[0]  # Verifica que se usa la transcripción
    assert "resumen" in args[1].lower()  # Verifica el prompt del sistema

@patch('src.tasks.chat_completion')
def test_get_actionable_items(mock_chat, mock_chat_completion, sample_transcription):
    """Prueba la función de extracción de elementos accionables."""
    mock_chat.return_value = mock_chat_completion
    
    result = get_actionable_items(sample_transcription)
    assert isinstance(result, str)
    assert len(result) > 0
    
    mock_chat.assert_called_once()
    args = mock_chat.call_args[0]
    assert sample_transcription in args[0]
    assert "accionables" in args[1].lower()

@patch('src.tasks.chat_completion')
def test_analyze_sentiment(mock_chat, mock_chat_completion, sample_transcription):
    """Prueba la función de análisis de sentimiento."""
    mock_chat.return_value = mock_chat_completion
    
    result = analyze_sentiment(sample_transcription)
    assert isinstance(result, dict)
    assert all(k in result for k in ['positive', 'negative', 'neutral'])
    assert all(isinstance(v, float) for v in result.values())
    assert all(0 <= v <= 1 for v in result.values())
    
    mock_chat.assert_called_once()

@patch('src.tasks.chat_completion')
def test_extract_topics(mock_chat, mock_chat_completion, sample_transcription):
    """Prueba la función de extracción de temas."""
    mock_chat.return_value = {
        'choices': [{
            'message': {
                'content': 'Tema 1\nTema 2\nTema 3'
            }
        }]
    }
    
    result = extract_topics(sample_transcription)
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(topic, str) for topic in result)
    
    mock_chat.assert_called_once() 