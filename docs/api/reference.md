# Referencia de la API

## Módulos Principales

### transcriptions.py

#### `transcribe_audio(audio_path: str) -> str`
Transcribe un archivo de audio/video a texto.

#### `translate_transcription(text: str) -> str`
Traduce el texto transcrito al idioma deseado.

#### `save_transcription(text: str, path: str) -> None`
Guarda la transcripción en un archivo.

#### `save_translation(text: str, path: str) -> None`
Guarda la traducción en un archivo.

### tasks.py

#### `summarize_meeting(text: str) -> str`
Genera un resumen conciso de la reunión.

#### `get_actionable_items(text: str) -> str`
Extrae puntos clave y elementos accionables de la transcripción.

### audio_divide.py

Maneja el procesamiento y división de archivos de audio.

### llm.py

Gestiona la integración con los modelos de lenguaje de OpenAI.

### token_cost.py

Utilidades para calcular y gestionar el costo de tokens de la API.

## Uso del Script Principal

### Clase `MeetingAssistant`

El script principal `meeting_assistant.py` proporciona las siguientes funciones:

#### `setup_output_directory() -> Path`
Crea y retorna el directorio de salida para los archivos generados.

#### `process_meeting(audio_path: str, output_dir: Path, should_translate: bool = True) -> None`
Procesa un archivo de audio/video de una reunión.

Argumentos:
- `audio_path`: Ruta al archivo de audio/video
- `output_dir`: Directorio donde se guardarán los archivos generados
- `should_translate`: Si se debe traducir la transcripción

## Ejemplos de Uso

```python
from meeting_assistant import process_meeting
from pathlib import Path

# Configurar directorio de salida
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# Procesar una reunión
process_meeting("examples/audio/meeting.mp4", output_dir)

# Procesar sin traducción
process_meeting("examples/audio/meeting.mp4", output_dir, should_translate=False)
``` 