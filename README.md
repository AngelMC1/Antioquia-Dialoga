# Antioquia Dialoga 🌿

Prototipo web (Django) para promover cultura de paz:
- **Chat ciudadano** con voz (Web Speech API) y respuestas simuladas.
- **Historias interactivas** con modal de lectura.
- **Desafíos y gamificación** (progreso, puntos, logros).

## Requisitos
- Python 3.11+ (probado en 3.13)
- pip, venv

## Instalación
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
