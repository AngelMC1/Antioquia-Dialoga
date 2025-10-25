from django.contrib import admin
from .models import Conversation, Message, UserProfile, Activity, Achievement, UserAchievement, StoryRead, Quiz, Question, QuizAttempt

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'created_at', 'updated_at', 'message_count')
    list_filter = ('created_at',)
    search_fields = ('session_id',)
    readonly_fields = ('created_at', 'updated_at')
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Mensajes'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'role', 'content_preview', 'timestamp')
    list_filter = ('role', 'timestamp')
    search_fields = ('content',)
    readonly_fields = ('timestamp',)
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Contenido'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'level', 'total_points', 'daily_points', 'streak_days', 'messages_sent', 'created_at')
    list_filter = ('level', 'created_at', 'last_activity')
    search_fields = ('username',)
    readonly_fields = ('created_at', 'last_activity')
    ordering = ('-total_points',)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'activity_type', 'points_earned', 'description', 'timestamp')
    list_filter = ('activity_type', 'timestamp')
    search_fields = ('user_profile__username', 'description')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'points_required', 'code')
    search_fields = ('name', 'code')
    ordering = ('points_required',)

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'achievement', 'unlocked_at')
    list_filter = ('unlocked_at',)
    search_fields = ('user_profile__username', 'achievement__name')
    readonly_fields = ('unlocked_at',)
    ordering = ('-unlocked_at',)

@admin.register(StoryRead)
class StoryReadAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'story_id', 'read_at')
    list_filter = ('story_id', 'read_at')
    search_fields = ('user_profile__username', 'story_id')
    readonly_fields = ('read_at',)
    ordering = ('-read_at',)

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('order', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'points_reward', 'get_questions_count', 'is_active', 'created_at')
    list_filter = ('difficulty', 'category', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    inlines = [QuestionInline]
    ordering = ('-created_at',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question_text', 'correct_answer', 'order')
    list_filter = ('quiz', 'correct_answer')
    search_fields = ('question_text',)
    ordering = ('quiz', 'order')

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'quiz', 'score', 'total_questions', 'get_percentage', 'points_earned', 'completed_at')
    list_filter = ('quiz', 'completed_at')
    search_fields = ('user_profile__username', 'quiz__title')
    readonly_fields = ('completed_at',)
    ordering = ('-completed_at',)
