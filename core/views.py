from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from .models import Conversation, Message, UserProfile, Activity, Achievement, UserAchievement, StoryRead, Quiz, Question, QuizAttempt
from .chatbot import PazBotService


def get_or_create_profile(request):
    """Obtener o crear perfil de usuario basado en sesión"""
    username = request.session.get('username')
    
    if not username:
        return None
    
    profile, created = UserProfile.objects.get_or_create(
        username=username,
        defaults={'session_key': request.session.session_key}
    )
    
    return profile


def dashboard(request):
    """Vista principal del dashboard con gamificación"""
    profile = get_or_create_profile(request)
    
    if not profile:
        # Redirigir al login si no hay sesión
        return redirect('login')
    
    # Calcular progreso al siguiente nivel
    points_for_next = ((profile.level) * 200) - profile.total_points
    progress_percent = (profile.total_points % 200) / 200 * 100
    
    # Obtener ranking
    ranking = UserProfile.objects.all()[:10]
    
    # Actividades recientes
    recent_activities = profile.activities.all()[:5]
    
    # Logros del usuario
    user_achievements = profile.achievements.all()
    
    context = {
        'profile': profile,
        'progress_percent': progress_percent,
        'points_for_next': points_for_next,
        'ranking': ranking,
        'recent_activities': recent_activities,
        'user_achievements': user_achievements,
    }
    
    return render(request, 'dashboard.html', context)


def chat(request):
    """Vista principal del chat"""
    # Generar o recuperar session_id
    session_id = request.session.get('chat_session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['chat_session_id'] = session_id
    
    # Obtener o crear conversación
    conversation, created = Conversation.objects.get_or_create(session_id=session_id)
    
    # Cargar historial de mensajes
    messages = conversation.messages.all().values('role', 'content', 'timestamp')
    
    temas = [
        "Construcción de paz",
        "Reconciliación",
        "Víctimas y memoria",
        "Juventud y paz",
        "Territorios de paz",
        "Comunicación no violenta",
    ]
    
    context = {
        "temas": temas,
        "session_id": session_id,
        "messages": list(messages)
    }
    
    return render(request, 'chat.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def chat_message(request):
    """API endpoint para enviar/recibir mensajes del chatbot"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')
        
        if not user_message or not session_id:
            return JsonResponse({'error': 'Datos incompletos'}, status=400)
        
        # Obtener conversación
        conversation, created = Conversation.objects.get_or_create(session_id=session_id)
        
        # Guardar mensaje del usuario
        Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )
        
        # Obtener historial
        history = list(conversation.messages.values('role', 'content'))
        history_for_bot = [
            {'role': msg['role'], 'content': msg['content']} 
            for msg in history[:-1]
        ]
        
        # Generar respuesta del bot
        bot_service = PazBotService()
        bot_response = bot_service.get_response(user_message, history_for_bot)
        
        # Guardar respuesta del bot
        Message.objects.create(
            conversation=conversation,
            role='bot',
            content=bot_response
        )
        
        # Otorgar puntos al usuario
        profile = get_or_create_profile(request)
        points_earned = 0
        
        if profile:
            # 10 puntos por mensaje significativo (más de 10 caracteres)
            if len(user_message) > 10:
                profile.add_points(10, 'message')
                profile.messages_sent += 1
                profile.save()
                points_earned = 10
        
        return JsonResponse({
            'success': True,
            'response': bot_response,
            'points_earned': points_earned
        })
    
    except Exception as e:
        print(f"Error en chat_message: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'error': 'Error procesando mensaje',
            'details': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def new_chat(request):
    """Inicia una nueva conversación"""
    new_session_id = str(uuid.uuid4())
    request.session['chat_session_id'] = new_session_id
    
    return JsonResponse({
        'success': True,
        'session_id': new_session_id
    })


@csrf_exempt
@require_http_methods(["POST"])
def set_username(request):
    """Establecer username en sesión"""
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        
        if not username or len(username) < 2:
            return JsonResponse({'error': 'Nombre muy corto (mínimo 2 caracteres)'}, status=400)
        
        # Verificar si ya existe
        if UserProfile.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Ese nombre ya está en uso'}, status=400)
        
        # Guardar en sesión
        request.session['username'] = username
        
        # Crear perfil
        profile = UserProfile.objects.create(
            username=username,
            session_key=request.session.session_key
        )
        
        return JsonResponse({
            'success': True,
            'username': username
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def historias(request):
    """Vista de historias interactivas"""
    profile = get_or_create_profile(request)
    
    # Obtener historias ya leídas por el usuario
    stories_read_ids = []
    if profile:
        stories_read_ids = list(profile.stories_read_list.values_list('story_id', flat=True))
    
    context = {
        'profile': profile,
        'stories_read_ids': stories_read_ids,
    }
    
    return render(request, 'historias.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def mark_story_read(request):
    """Marcar una historia como leída y otorgar puntos"""
    try:
        data = json.loads(request.body)
        story_id = data.get('story_id', '').strip()
        
        if not story_id:
            return JsonResponse({'error': 'ID de historia requerido'}, status=400)
        
        # Validar que el story_id sea válido
        valid_stories = ['parque', 'puente', 'semillas']
        if story_id not in valid_stories:
            return JsonResponse({'error': 'Historia no válida'}, status=400)
        
        # Obtener perfil del usuario
        profile = get_or_create_profile(request)
        
        if not profile:
            return JsonResponse({'error': 'Debes registrarte primero'}, status=400)
        
        # Verificar si ya leyó esta historia
        already_read = StoryRead.objects.filter(
            user_profile=profile,
            story_id=story_id
        ).exists()
        
        if already_read:
            return JsonResponse({
                'success': False,
                'message': 'Ya leíste esta historia anteriormente',
                'points_earned': 0
            })
        
        # Marcar historia como leída
        StoryRead.objects.create(
            user_profile=profile,
            story_id=story_id
        )
        
        # Otorgar puntos (+30 puntos por historia)
        points = 30
        profile.add_points(points, 'story')
        profile.stories_read += 1
        profile.save()
        
        return JsonResponse({
            'success': True,
            'message': '¡Historia completada! 🎉',
            'points_earned': points,
            'total_stories': profile.stories_read
        })
    
    except Exception as e:
        print(f"Error en mark_story_read: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'error': 'Error procesando la historia',
            'details': str(e)
        }, status=500)


def trivias(request):
    """Vista principal de trivias"""
    profile = get_or_create_profile(request)
    
    # Obtener todas las trivias activas
    quizzes = Quiz.objects.filter(is_active=True).prefetch_related('questions')
    
    # Si hay perfil, obtener intentos previos
    user_attempts = {}
    if profile:
        attempts = QuizAttempt.objects.filter(user_profile=profile).order_by('-completed_at')
        # Agrupar por quiz (solo el último intento)
        for attempt in attempts:
            if attempt.quiz_id not in user_attempts:
                user_attempts[attempt.quiz_id] = attempt
    
    context = {
        'profile': profile,
        'quizzes': quizzes,
        'user_attempts': user_attempts,
    }
    
    return render(request, 'trivias.html', context)


def quiz_detail(request, quiz_id):
    """Vista para tomar una trivia específica"""
    profile = get_or_create_profile(request)
    
    if not profile:
        return render(request, 'trivias.html', {'needs_username': True})
    
    try:
        quiz = Quiz.objects.prefetch_related('questions').get(id=quiz_id, is_active=True)
    except Quiz.DoesNotExist:
        return render(request, 'trivias.html', {'error': 'Trivia no encontrada'})
    
    # Obtener preguntas
    questions = quiz.questions.all()
    
    # Obtener intentos previos del usuario
    previous_attempts = QuizAttempt.objects.filter(
        user_profile=profile,
        quiz=quiz
    ).order_by('-completed_at')[:5]  # Últimos 5 intentos
    
    context = {
        'profile': profile,
        'quiz': quiz,
        'questions': questions,
        'previous_attempts': previous_attempts,
    }
    
    return render(request, 'quiz_detail.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def submit_quiz(request):
    """Procesar respuestas de una trivia y otorgar puntos"""
    try:
        data = json.loads(request.body)
        quiz_id = data.get('quiz_id')
        answers = data.get('answers', {})  # {question_id: 'A', ...}
        time_taken = data.get('time_taken', 0)
        
        if not quiz_id:
            return JsonResponse({'error': 'ID de trivia requerido'}, status=400)
        
        # Obtener perfil del usuario
        profile = get_or_create_profile(request)
        
        if not profile:
            return JsonResponse({'error': 'Debes registrarte primero'}, status=400)
        
        # Obtener trivia y preguntas
        try:
            quiz = Quiz.objects.prefetch_related('questions').get(id=quiz_id, is_active=True)
        except Quiz.DoesNotExist:
            return JsonResponse({'error': 'Trivia no encontrada'}, status=400)
        
        questions = quiz.questions.all()
        
        # Calcular puntaje
        score = 0
        total_questions = questions.count()
        results = []
        
        for question in questions:
            user_answer = answers.get(str(question.id), '').upper()
            is_correct = (user_answer == question.correct_answer)
            
            if is_correct:
                score += 1
            
            results.append({
                'question_id': question.id,
                'question_text': question.question_text,
                'user_answer': user_answer,
                'correct_answer': question.correct_answer,
                'is_correct': is_correct,
                'explanation': question.explanation
            })
        
        # Calcular puntos otorgados (proporcional al puntaje)
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        
        if percentage == 100:
            # Trivia perfecta: puntos completos
            points_earned = quiz.points_reward
        elif percentage >= 80:
            # Muy bien: 80% de los puntos
            points_earned = int(quiz.points_reward * 0.8)
        elif percentage >= 60:
            # Bien: 60% de los puntos
            points_earned = int(quiz.points_reward * 0.6)
        elif percentage >= 40:
            # Regular: 40% de los puntos
            points_earned = int(quiz.points_reward * 0.4)
        else:
            # Menos del 40%: 20% de los puntos (consolación)
            points_earned = int(quiz.points_reward * 0.2)
        
        # Guardar intento
        attempt = QuizAttempt.objects.create(
            user_profile=profile,
            quiz=quiz,
            score=score,
            total_questions=total_questions,
            points_earned=points_earned,
            time_taken=time_taken
        )
        
        # Otorgar puntos al perfil
        if points_earned > 0:
            profile.add_points(points_earned, 'quiz')
            profile.quizzes_completed += 1
            profile.save()
        
        return JsonResponse({
            'success': True,
            'score': score,
            'total_questions': total_questions,
            'percentage': percentage,
            'points_earned': points_earned,
            'is_perfect': percentage == 100,
            'results': results,
            'attempt_id': attempt.id
        })
    
    except Exception as e:
        print(f"Error en submit_quiz: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'error': 'Error procesando la trivia',
            'details': str(e)
        }, status=500)


def login_view(request):
    """Vista de login - permite ingresar o registrarse"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        action = request.POST.get('action', 'login')  # 'login' o 'register'
        
        if not username or len(username) < 2:
            return render(request, 'login.html', {
                'error': 'El nombre debe tener al menos 2 caracteres'
            })
        
        if action == 'register':
            # Crear nuevo usuario
            if UserProfile.objects.filter(username=username).exists():
                return render(request, 'login.html', {
                    'error': 'Ese nombre ya está en uso. Intenta con otro o inicia sesión.'
                })
            
            # Crear perfil
            UserProfile.objects.create(
                username=username,
                session_key=request.session.session_key
            )
            
            # Guardar en sesión
            request.session['username'] = username
            
            return redirect('desafios')
        
        else:  # action == 'login'
            # Iniciar sesión con usuario existente
            try:
                profile = UserProfile.objects.get(username=username)
                
                # Guardar en sesión
                request.session['username'] = username
                
                return redirect('desafios')
                
            except UserProfile.DoesNotExist:
                return render(request, 'login.html', {
                    'error': 'Usuario no encontrado. ¿Quieres registrarte?',
                    'suggested_username': username
                })
    
    # GET request
    # Si ya tiene sesión activa, redirigir al dashboard
    if request.session.get('username'):
        return redirect('desafios')
    
    return render(request, 'login.html')


def logout_view(request):
    """Vista de logout - cierra la sesión actual"""
    # Limpiar la sesión
    if 'username' in request.session:
        del request.session['username']
    
    if 'chat_session_id' in request.session:
        del request.session['chat_session_id']
    
    # Limpiar toda la sesión
    request.session.flush()
    
    return redirect('login')
