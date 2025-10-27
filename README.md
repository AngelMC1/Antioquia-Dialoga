# Antioquia Dialoga 🌿

Plataforma web interactiva (Django) para promover cultura de paz en Antioquia, Colombia.

## ✨ Características

### 🤖 Chat Inteligente con IA
- Chatbot **PazBot** potenciado por Google Gemini AI
- Conversaciones contextuales sobre paz, reconciliación y convivencia
- Reconocimiento de voz en español (Web Speech API)
- Historial de conversaciones persistente

### 📚 Historias Interactivas
- Narrativas educativas sobre construcción de paz
- Modal de lectura inmersiva
- Contenido adaptado al contexto de Antioquia

### 🎮 Sistema de Gamificación FUNCIONAL
- ✅ **Perfiles de usuario** sin necesidad de contraseña
- ✅ **Sistema de puntos** automático (+10 pts por mensaje)
- ✅ **Niveles** progresivos (cada 200 puntos = 1 nivel)
- ✅ **Rachas diarias** para mantener motivación
- ✅ **Ranking en tiempo real** entre usuarios
- ✅ **6 logros** desbloqueables
- ✅ **Dashboard dinámico** con estadísticas reales

## 🚀 Inicio Rápido

### Requisitos
- Python 3.11+ (probado en 3.12 y 3.13)
- pip y venv

### Instalación

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar API Key de Gemini
# Crea un archivo .env en la raíz con:
# GEMINI_API_KEY=tu_api_key_aqui

# 5. Ejecutar migraciones (ya están hechas)
python manage.py migrate

# 6. Crear superusuario para admin (opcional)
python manage.py createsuperuser

# 7. Ejecutar servidor
python manage.py runserver
```

### Primera Vez Usando la App

1. Abre tu navegador en `http://localhost:8000/`
2. Aparecerá un modal pidiendo tu nombre/nickname
3. Ingresa un nombre único (mínimo 2 caracteres)
4. ¡Listo! Ya puedes empezar a ganar puntos 🌿

## 📖 Cómo Usar

### Ganar Puntos

1. **Chatear con PazBot** (`/chat/`)
   - Escribe mensajes de más de 10 caracteres
   - Ganas **+10 puntos** por cada mensaje
   - Verás una notificación flotante con tus puntos

2. **Leer Historias** (`/historias/`)
   - Explora historias sobre paz
   - anas **+30 puntos** por cada mensaje

3. **Completar Desafíos** (`/`)
   - (Próximamente: sistema de desafíos diarios)

### Ver tu Progreso

- **Dashboard** (`/`): Nivel, puntos, racha, ranking
- **Panel Admin** (`/admin/`): Estadísticas detalladas

## 🏆 Sistema de Logros

| Logro | Cómo Desbloquearlo |
|-------|-------------------|
| 🌟 Primer Conversador | Envía tu primer mensaje |
| 🧭 Mediador en práctica | Envía 20 mensajes (200 pts) |
| 📖 Narrador de Paz | Lee tu primera historia |
| 🔥 Racha x5 | 5 días consecutivos de actividad |
| 🏗️ Constructor de Paz | Alcanza nivel 5 (800 pts) |
| 🕊️ Pacificador | Acumula 1000 puntos |

## 🛠️ Tecnologías

- **Backend**: Django 5.1.4
- **IA**: Google Gemini API (gemini-2.0-flash-exp)
- **Frontend**: TailwindCSS, JavaScript Vanilla
- **Base de Datos**: SQLite (desarrollo)
- **Voz**: Web Speech API (Chrome/Edge)

## 📁 Estructura del Proyecto

```
Antioquia-Dialoga/
├── core/                # App principal
│   ├── models.py       # Modelos (Conversation, Message, UserProfile, etc.)
│   ├── views.py        # Vistas y lógica de negocio
│   ├── chatbot.py      # Servicio de IA con Gemini
│   └── admin.py        # Configuración del admin
├── templates/          # HTML templates
│   ├── base.html
│   ├── dashboard.html  # Dashboard con gamificación
│   ├── chat.html       # Interfaz del chat
│   └── historias.html  # Historias interactivas
├── static/             # Archivos estáticos
│   ├── css/
│   └── js/chat.js      # Lógica del chat + notificaciones
├── config/             # Configuración Django
└── db.sqlite3          # Base de datos
```

## 🔐 Variables de Entorno

Crea un archivo `.env` en la raíz:

```env
GEMINI_API_KEY=tu_api_key_de_google_gemini
SECRET_KEY=tu_secret_key_de_django
```

> **Obtener API Key**: https://ai.google.dev/


## 📝 Licencia

Este proyecto es de código abierto para fines educativos.

## 🌟 Créditos

Desarrollado para promover la cultura de paz en Antioquia, Colombia 🇨🇴

---
