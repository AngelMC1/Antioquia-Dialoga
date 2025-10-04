from django.db import models
from django.utils import timezone

class Conversation(models.Model):
    """Sesión de conversación única"""
    session_id = models.CharField(max_length=100, unique=True, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Conversación {self.session_id[:8]}... - {self.created_at.strftime('%d/%m/%Y %H:%M')}"

class Message(models.Model):
    """Mensaje individual en una conversación"""
    ROLE_CHOICES = [
        ('user', 'Usuario'),
        ('bot', 'Bot'),
    ]
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
