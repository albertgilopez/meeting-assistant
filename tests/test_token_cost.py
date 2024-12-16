"""
Tests para el módulo de cálculo de tokens.
"""

import pytest

from src.token_cost import (
    MODEL_PRICES,
    calculate_token_cost,
    format_token_info,
    get_token_count
)

@pytest.fixture
def sample_text():
    """Fixture que proporciona un texto de ejemplo."""
    return "Este es un texto de prueba para contar tokens."

def test_get_token_count(sample_text):
    """Prueba que el conteo de tokens funciona correctamente."""
    token_count = get_token_count(sample_text)
    assert token_count > 0
    assert isinstance(token_count, int)

def test_get_token_count_invalid_model():
    """Prueba que se maneja correctamente un modelo inválido."""
    with pytest.raises(ValueError):
        get_token_count("texto", model="modelo-invalido")

def test_calculate_token_cost(sample_text):
    """Prueba que el cálculo de costos funciona correctamente."""
    cost = calculate_token_cost(sample_text, 100)
    assert cost > 0
    assert isinstance(cost, float)

def test_calculate_token_cost_invalid_model():
    """Prueba que se maneja correctamente un modelo inválido."""
    with pytest.raises(ValueError):
        calculate_token_cost("texto", 100, model="modelo-invalido")

def test_format_token_info(sample_text):
    """Prueba que el formato de información de tokens es correcto."""
    info = format_token_info(sample_text)
    
    assert isinstance(info, dict)
    assert "token_count" in info
    assert "estimated_cost" in info
    assert "model" in info
    
    assert isinstance(info["token_count"], int)
    assert isinstance(info["estimated_cost"], float)
    assert isinstance(info["model"], str)

def test_model_prices_structure():
    """Prueba que la estructura de precios es correcta."""
    for model, prices in MODEL_PRICES.items():
        assert isinstance(model, str)
        assert isinstance(prices, dict)
        assert "input" in prices
        assert "output" in prices
        assert isinstance(prices["input"], (int, float))
        assert isinstance(prices["output"], (int, float)) 