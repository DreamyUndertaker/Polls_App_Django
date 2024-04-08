from django.contrib import admin
from .models import Question, Answer, QuestionFile, UserTest, UserScore

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionFile)
admin.site.register(UserTest)
admin.site.register(UserScore)
