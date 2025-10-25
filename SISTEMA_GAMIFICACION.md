# 🎮 Sistema de Gamificación - Antioquia Dialoga

## ✅ Cambios Implementados

### 1. **Nuevos Modelos de Base de Datos**

Se agregaron 4 nuevos modelos en `core/models.py`:

- **`UserProfile`**: Perfil de usuario simple (sin contraseñas)
  - Campos: username, level, total_points, daily_points, streak_days
  - Contadores: messages_sent, stories_read, quizzes_completed
  
- **`Activity`**: Registro de actividades del usuario
  - Tipos: message, story, quiz, challenge
  - Tracking de puntos ganados por actividad
  
- **`Achievement`**: Logros desbloqueables
  - 6 logros iniciales creados (🌟 Primer Conversador, 🧭 Mediador, etc.)
  
- **`UserAchievement`**: Relación entre usuarios y logros desbloqueados

### 2. **Sistema de Puntos Automático**

- **10 puntos** por cada mensaje significativo (>10 caracteres) enviado al chat
- Los puntos se otorgan automáticamente al enviar mensajes
- Notificación visual flotante cuando ganas puntos (+10 puntos 🌿)

### 3. **Sistema de Niveles**

- **Fórmula**: Nivel = (total_points / 200) + 1
- Cada 200 puntos subes un nivel
- Barra de progreso visual en el dashboard

### 4. **Sistema de Rachas**

- Se actualiza automáticamente cada día que participas
- Si participas días consecutivos, la racha aumenta
- Si faltas un día, la racha se reinicia a 1

### 5. **Dashboard Funcional**

Ahora muestra datos **reales** en lugar de mockups:

- ✅ Nivel actual del usuario
- ✅ Puntos totales y puntos del día
- ✅ Racha de días consecutivos
- ✅ Número de mensajes enviados
- ✅ Actividad reciente con puntos ganados
- ✅ Ranking real de usuarios ordenados por puntos
- ✅ Logros desbloqueados

### 6. **Modal de Bienvenida**

- Primera vez que visitas el dashboard → modal pide tu nombre
- Nombre único (no se puede repetir)
- Se guarda en sesión de navegador
- Crea automáticamente tu perfil

## 🚀 Cómo Usar el Sistema

### Primera Vez

1. Abre el navegador en `http://localhost:8000/`
2. Aparecerá un modal pidiendo tu nombre
3. Ingresa tu nombre/nickname (mínimo 2 caracteres)
4. Haz clic en "Comenzar mi viaje 🌿"
5. ¡Listo! Ya tienes tu perfil creado

### Ganar Puntos

1. Ve al **Chat** (`http://localhost:8000/chat/`)
2. Escribe mensajes a PazBot (mínimo 11 caracteres)
3. Por cada mensaje recibes **+10 puntos**
4. Verás una notificación flotante: "+10 puntos 🌿"
5. Los puntos se acumulan automáticamente

### Ver tu Progreso

1. Ve al **Dashboard** (`http://localhost:8000/`)
2. Verás:
   - Tu nivel y progreso al siguiente nivel
   - Puntos totales y del día
   - Tu racha actual
   - Actividades recientes
   - Tu posición en el ranking

## 📊 Panel de Administración

Accede a `http://localhost:8000/admin/` para gestionar:

- **UserProfiles**: Ver usuarios, puntos, niveles
- **Activities**: Historial de actividades
- **Achievements**: Crear/editar logros
- **UserAchievements**: Ver logros desbloqueados

## 🏆 Logros Disponibles

| Icono | Nombre | Descripción | Puntos Requeridos |
|-------|--------|-------------|-------------------|
| 🌟 | Primer Conversador | Enviaste tu primer mensaje | 0 |
| 🧭 | Mediador en práctica | Enviaste 20 mensajes | 200 |
| 📖 | Narrador de Paz | Leíste tu primera historia | 0 |
| 🔥 | Racha x5 | 5 días consecutivos | 0 |
| 🏗️ | Constructor de Paz | Alcanzaste nivel 5 | 800 |
| 🕊️ | Pacificador | 1000 puntos totales | 1000 |

> **Nota**: El sistema de logros está implementado en los modelos, pero aún no se desbloquean automáticamente. Esto se puede agregar como mejora futura.

## 🔧 Archivos Modificados

```
core/
├── models.py          ← Agregados 4 nuevos modelos
├── views.py           ← Lógica de perfiles y puntos
├── admin.py           ← Registro de nuevos modelos
└── urls.py            ← Nueva ruta /set-username/

templates/
└── dashboard.html     ← Modal y datos dinámicos

static/js/
└── chat.js            ← Notificación de puntos
```

## 📝 Comandos Ejecutados

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear logros iniciales (ya ejecutado)
# Los logros ya están en la base de datos
```

## 🎯 Próximos Pasos Sugeridos

### Corto Plazo
1. ✅ Sistema de usuarios básico ← **COMPLETADO**
2. ✅ Sistema de puntos automático ← **COMPLETADO**
3. ✅ Dashboard funcional ← **COMPLETADO**
4. ⏳ Desbloqueo automático de logros
5. ⏳ Puntos por leer historias
6. ⏳ Sistema de trivias funcional

### Mediano Plazo
7. ⏳ Desafíos diarios con progreso real
8. ⏳ Notificaciones de logros desbloqueados
9. ⏳ Perfil de usuario con historial
10. ⏳ Sistema de badges visuales

### Largo Plazo
11. ⏳ Autenticación real (opcional)
12. ⏳ Ranking por categorías (semanal, mensual)
13. ⏳ Exportar progreso/certificados
14. ⏳ Competencias entre usuarios

## 🐛 Solución de Problemas

### No aparece el modal de nombre
- Borra las cookies del navegador
- O abre en modo incógnito

### No se guardan los puntos
- Verifica que tengas un nombre registrado
- Verifica en admin que existe tu UserProfile

### Error al crear usuario
- El nombre probablemente ya existe
- Prueba con otro nombre diferente

## 💡 Tips de Uso

1. **Nombre único**: Elige un nombre que nadie más haya usado
2. **Mensajes largos**: Escribe mensajes de más de 10 caracteres para ganar puntos
3. **Racha diaria**: Entra cada día para mantener tu racha
4. **Ranking**: Compite con otros usuarios por el primer lugar
5. **Nivel 5**: Necesitas 800 puntos = 80 mensajes aproximadamente

## 🌿 ¡Disfruta construyendo paz en Antioquia!

