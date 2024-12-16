import os
import shutil
from pathlib import Path

# Crear directorios
directories = [
    'src',
    'tests',
    'examples/audio',
    'examples/transcriptions',
    'docs/api',
    'docs/usage'
]

for directory in directories:
    Path(directory).mkdir(parents=True, exist_ok=True)

# Mover archivos de código fuente a src/
source_files = [
    'audio_divide.py',
    'llm.py',
    'token_cost.py',
    'transcriptions.py',
    'tasks.py'
]

for file in source_files:
    if os.path.exists(file):
        shutil.move(file, f'src/{file}')

# Mover archivos de ejemplo
example_files = [
    'weekly_meeting_rust.mp4',
    'weekly_meeting_rust.txt',
    'translation.txt',
    'transcription.txt'
]

for file in example_files:
    if os.path.exists(file):
        if file.endswith(('.mp4', '.wav', '.m4a')):
            shutil.move(file, f'examples/audio/{file}')
        else:
            shutil.move(file, f'examples/transcriptions/{file}')

print("Estructura de archivos reorganizada correctamente.") 