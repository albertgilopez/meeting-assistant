# Meeting Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Este es un asistente de reuniones que procesa archivos de audio/video para generar transcripciones, traducciones, resúmenes y puntos clave de reuniones. Utiliza la API de OpenAI para procesar el contenido y generar resultados útiles.

## 🚀 Características

- 📝 Transcripción automática de audio/video a texto
- 🌍 Traducción de transcripciones
- 📋 Generación de resúmenes de reuniones
- ✅ Extracción de puntos clave y elementos accionables
- 🎵 Soporte para múltiples formatos de audio/video
- 💾 Guardado automático de resultados
- ♻️ Reutilización de transcripciones y traducciones existentes

## 📋 Requisitos Previos

- Python 3.7 o superior
- Una clave API de OpenAI (necesaria para las funciones de IA)
- Conexión a Internet

## 🛠️ Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/[usuario]/meeting-assistant.git
cd meeting-assistant
```

2. Crea y activa un entorno virtual:
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Instala las dependencias:
```bash
# Solo dependencias principales
pip install -r requirements.txt

# Para desarrollo (incluye herramientas de testing y linting)
pip install -r requirements-dev.txt
```

4. Configura las variables de entorno:
```bash
# Copia el archivo de ejemplo
cp .env.example .env

# Edita .env y agrega tu API key de OpenAI
OPENAI_API_KEY=tu-clave-api
```

## 📖 Uso

El script principal acepta varios argumentos de línea de comandos:

```bash
python meeting_assistant.py [ruta-del-archivo] [opciones]
```

### Argumentos

- `ruta-del-archivo`: Ruta al archivo de audio/video a procesar
- `--no-translate`: (Opcional) No realizar traducción de la transcripción

### Ejemplos

1. Procesar un archivo con todas las opciones por defecto:
```bash
python meeting_assistant.py reuniones/mi_reunion.mp4
```

2. Procesar un archivo sin traducción:
```bash
python meeting_assistant.py reuniones/mi_reunion.mp4 --no-translate
```

### Archivos de Salida

El script generará los siguientes archivos en el directorio `output/`:

- `[nombre-archivo]_transcription.txt`: Transcripción del audio
- `[nombre-archivo]_translation.txt`: Traducción (si está habilitada)
- `[nombre-archivo]_summary.txt`: Resumen de la reunión
- `[nombre-archivo]_action_items.txt`: Puntos clave y elementos accionables

## 🧪 Tests

Para ejecutar los tests:

```bash
# Ejecutar todos los tests
pytest

# Ver cobertura de código
pytest --cov=src tests/
```

## 📁 Estructura del Proyecto

```
meeting-assistant/
├── src/                # Código fuente
│   ├── __init__.py    # Inicializador del paquete
│   ├── audio_divide.py # Manejo de audio
│   ├── llm.py         # Integración con OpenAI
│   ├── tasks.py       # Funciones de procesamiento
│   ├── transcriptions.py # Funciones de transcripción
│   └── token_cost.py  # Utilidad de tokens
├── tests/             # Pruebas unitarias y de integración
├── examples/          # Ejemplos de uso y archivos de muestra
├── docs/             # Documentación adicional
├── meeting_assistant.py # Script principal
├── requirements.txt   # Dependencias
├── LICENSE           # Licencia MIT
└── README.md         # Este archivo
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor, lee [CONTRIBUTING.md](CONTRIBUTING.md) para detalles sobre nuestro código de conducta y el proceso para enviarnos pull requests.

## 📝 Notas

- La primera ejecución puede tardar varios minutos dependiendo de la duración del archivo
- Los archivos de transcripción y traducción se guardan localmente para evitar procesamiento redundante
- Se requiere una conexión a Internet estable para las funciones de IA
- El costo del procesamiento dependerá del uso de la API de OpenAI

## ⚠️ Limitaciones Conocidas

- El tamaño máximo de archivo de audio/video es de 25MB (límite de la API de OpenAI)
- La duración máxima del audio es de 60 minutos por defecto
- Solo se procesan archivos en formatos comunes (mp3, mp4, wav, m4a)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- OpenAI por proporcionar las APIs de GPT y Whisper
- Todos los contribuidores que han ayudado a mejorar este proyecto