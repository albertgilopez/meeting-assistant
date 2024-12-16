# Guía de Inicio Rápido

## Instalación

1. Asegúrate de tener Python 3.7 o superior instalado
2. Clona el repositorio
3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Configuración

1. Obtén una clave API de OpenAI desde https://platform.openai.com/
2. Configura la clave API como variable de entorno:
```bash
# Windows
set OPENAI_API_KEY=tu-clave-api

# Linux/Mac
export OPENAI_API_KEY=tu-clave-api
```

## Uso Básico

1. Coloca tu archivo de audio/video en la carpeta `examples/audio/`
2. Ejecuta el asistente:
```bash
python meeting_assistant.py examples/audio/tu_archivo.mp4
```

## Opciones Disponibles

- `--no-translate`: Omite la traducción de la transcripción
```bash
python meeting_assistant.py examples/audio/tu_archivo.mp4 --no-translate
```

## Archivos de Salida

Todos los archivos generados se guardan en la carpeta `output/`:
- `*_transcription.txt`: Transcripción del audio
- `*_translation.txt`: Traducción (si está habilitada)
- `*_summary.txt`: Resumen de la reunión
- `*_action_items.txt`: Puntos clave y elementos accionables 