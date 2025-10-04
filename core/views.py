from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from .models import Conversation, Message
from .chatbot import PazBotService

def dashboard(request):
    return render(request, 'dashboard.html')

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
        
        if not user_message:
            return JsonResponse({'error': 'Mensaje vacío'}, status=400)
        
        if not session_id:
            return JsonResponse({'error': 'Session ID requerido'}, status=400)
        
        # Obtener o crear conversación
        conversation, created = Conversation.objects.get_or_create(session_id=session_id)
        
        # Guardar mensaje del usuario
        Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )
        
        # Obtener historial para contexto
        history = list(conversation.messages.values('role', 'content'))
        history_for_bot = [
            {'role': msg['role'], 'content': msg['content']} 
            for msg in history[:-1]  # Excluir el último mensaje (ya lo enviamos)
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
        
        return JsonResponse({
            'success': True,
            'response': bot_response
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

def historias(request):
    return render(request, 'historias.html')
