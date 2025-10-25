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

class UserProfile(models.Model):
    """Perfil simple de usuario - sin autenticación compleja"""
    username = models.CharField(max_length=50, unique=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Stats de gamificación
    level = models.IntegerField(default=1)
    total_points = models.IntegerField(default=0)
    daily_points = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    last_activity = models.DateField(default=timezone.now)
    
    # Contadores
    conversations_count = models.IntegerField(default=0)
    messages_sent = models.IntegerField(default=0)
    stories_read = models.IntegerField(default=0)
    quizzes_completed = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-total_points']
    
    def __str__(self):
        return f"{self.username} (Nivel {self.level})"
    
    def add_points(self, points, activity_type):
        """Agregar puntos y actualizar nivel"""
        self.total_points += points
        self.daily_points += points
        
        # Sistema de niveles simple: cada 200 puntos = 1 nivel
        self.level = (self.total_points // 200) + 1
        
        # Actualizar racha
        today = timezone.now().date()
        if self.last_activity == today - timezone.timedelta(days=1):
            self.streak_days += 1
        elif self.last_activity != today:
            self.streak_days = 1
        
        self.last_activity = today
        self.save()
        
        # Crear registro de actividad
        Activity.objects.create(
            user_profile=self,
            activity_type=activity_type,
            points_earned=points
        )

class Activity(models.Model):
    """Registro de actividades del usuario"""
    ACTIVITY_TYPES = [
        ('message', 'Mensaje enviado'),
        ('story', 'Historia leída'),
        ('quiz', 'Trivia completada'),
        ('challenge', 'Desafío completado'),
    ]
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    points_earned = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        return f"{self.user_profile.username} - {self.get_activity_type_display()} (+{self.points_earned}pts)"

class Achievement(models.Model):
    """Logros desbloqueables"""
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='🏆')
    points_required = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.icon} {self.name}"

class UserAchievement(models.Model):
    """Logros del usuario"""
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['user_profile', 'achievement']
    
    def __str__(self):
        return f"{self.user_profile.username} - {self.achievement.name}"

class StoryRead(models.Model):
    """Registro de historias leídas por usuario"""
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='stories_read_list')
    story_id = models.CharField(max_length=50)  # ID de la historia (parque, puente, semillas)
    read_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['user_profile', 'story_id']
        ordering = ['-read_at']
    
    def __str__(self):
        return f"{self.user_profile.username} - Historia: {self.story_id}"

class Quiz(models.Model):
    """Trivia/Quiz sobre temas de paz"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, default='Cultura de Paz')
    difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Fácil'),
        ('medium', 'Medio'),
        ('hard', 'Difícil')
    ], default='medium')
    points_reward = models.IntegerField(default=50)  # Puntos por completar perfectamente
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Quizzes'
    
    def __str__(self):
        return f"{self.title} ({self.get_difficulty_display()})"
    
    def get_questions_count(self):
        return self.questions.count()

class Question(models.Model):
    """Pregunta de una trivia"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'Opción A'),
        ('B', 'Opción B'),
        ('C', 'Opción C'),
        ('D', 'Opción D')
    ])
    explanation = models.TextField(blank=True, help_text="Explicación de la respuesta correcta")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.quiz.title} - Pregunta {self.order}"

class QuizAttempt(models.Model):
    """Intento de completar una trivia por un usuario"""
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0)  # Respuestas correctas
    total_questions = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)
    completed_at = models.DateTimeField(default=timezone.now)
    time_taken = models.IntegerField(default=0, help_text="Segundos tomados")
    
    class Meta:
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.user_profile.username} - {self.quiz.title}: {self.score}/{self.total_questions}"
    
    def get_percentage(self):
        if self.total_questions == 0:
            return 0
        return int((self.score / self.total_questions) * 100)
    
    def is_perfect(self):
        return self.score == self.total_questions and self.total_questions > 0