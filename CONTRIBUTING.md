# Guía de Contribución

¡Gracias por tu interés en contribuir a Meeting Assistant! 

## Preparación del Entorno de Desarrollo

1. Fork y clona el repositorio
2. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Instala las dependencias de desarrollo:
```bash
pip install -r requirements.txt
```
4. Configura el pre-commit:
```bash
pre-commit install
```

## Estándares de Código

- Usamos [Black](https://github.com/psf/black) para formateo de código
- Seguimos las guías de estilo PEP 8
- Usamos type hints de Python
- Todos los módulos, clases y funciones deben tener docstrings

## Tests

- Escribe tests para cada nueva funcionalidad
- Mantén la cobertura de código >80%
- Ejecuta los tests antes de hacer commit:
```bash
pytest
```

## Proceso de Pull Request

1. Crea una rama para tu feature:
```bash
git checkout -b feature/nombre-feature
```
2. Haz commits de tus cambios:
```bash
git commit -m "Descripción clara del cambio"
```
3. Asegúrate de que los tests pasan
4. Actualiza la documentación si es necesario
5. Push a tu fork y crea un Pull Request

## Reportar Bugs

- Usa el sistema de issues de GitHub
- Incluye pasos detallados para reproducir el error
- Menciona tu sistema operativo y versión de Python

## Sugerir Mejoras

- Abre un issue con la etiqueta "enhancement"
- Explica el caso de uso y beneficios
- Si es posible, incluye ejemplos de implementación 