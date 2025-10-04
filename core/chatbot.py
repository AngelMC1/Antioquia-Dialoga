from google import genai
from google.genai import types
import os
from typing import List, Dict

class PazBotService:
    """Servicio de chatbot para Antioquia Dialoga usando Gemini AI"""
    
    SYSTEM_PROMPT = """Eres PazBot, un asistente virtual especializado en construcción de paz, 
    reconciliación y convivencia en Antioquia, Colombia. Tu objetivo es:

    1. Guiar conversaciones sobre paz, reconciliación y derechos de víctimas
    2. Proporcionar información práctica y pedagógica sobre construcción de paz
    3. Sugerir actividades concretas para colegios, comunidades y territorios
    4. Promover la comunicación no violenta (CNV) y el diálogo
    5. Ser empático, respetuoso y enfocado en soluciones constructivas

    Contexto regional: Antioquia ha vivido décadas de conflicto armado. Enfócate en:
    - Reconciliación comunitaria
    - Memoria histórica y víctimas
    - Participación juvenil en construcción de paz
    - Territorios de paz (comunas, veredas, barrios)
    - Mediación escolar y resolución de conflictos

    Mantén un tono cercano, usa emojis ocasionalmente (🌿💚✨) y ofrece ejemplos prácticos."""

    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        
        # Debug: verificar si se carga la API key
        if not api_key:
            print(f"DEBUG: GEMINI_API_KEY no encontrada")
            print(f"DEBUG: Variables de entorno disponibles: {list(os.environ.keys())}")
            raise ValueError("GEMINI_API_KEY no configurada en variables de entorno")
        
        print(f"DEBUG: API Key cargada correctamente (primeros 10 chars): {api_key[:10]}...")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash-exp"
    
    def format_history(self, messages: List[Dict[str, str]]) -> List[types.Content]:
        """Convierte el historial de mensajes al formato de Gemini"""
        history = []
        
        for msg in messages:
            role = "user" if msg['role'] == 'user' else "model"
            history.append(types.Content(
                role=role,
                parts=[types.Part(text=msg['content'])]
            ))
        
        return history
    
    def get_response(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """Genera respuesta del chatbot basada en el mensaje del usuario y el historial"""
        try:
            # Preparar el historial
            history = []
            if conversation_history:
                history = self.format_history(conversation_history)
            
            # Configurar el chat
            chat = self.client.chats.create(
                model=self.model,
                config=types.GenerateContentConfig(
                    system_instruction=self.SYSTEM_PROMPT,
                    temperature=0.7,
                    max_output_tokens=800,
                )
            )
            
            # Restaurar historial si existe
            if history:
                for msg in history:
                    if msg.role == "user":
                        chat.send_message(msg.parts[0].text)
            
            # Enviar mensaje actual
            response = chat.send_message(user_message)
            
            return response.text
        
        except Exception as e:
            print(f"Error en PazBotService.get_response: {str(e)}")
            import traceback
            traceback.print_exc()
            return "Lo siento, hubo un error procesando tu mensaje. Por favor, intenta nuevamente. 🌿"