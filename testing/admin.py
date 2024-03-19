from django.contrib import admin

from .models import Answer, Choice, Question

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'visible',
        'max_points',
    )

class ChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'question',
        'points',
        'lock_other',
    )

class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'question',
        'choice',
    )
    list_filter = ('user', )

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)