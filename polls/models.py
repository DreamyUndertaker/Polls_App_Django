from django.db import models
from django.contrib.auth.models import User


class QuestionFile(models.Model):  # Исправлено на QuestionFile
    title = models.CharField(max_length=255, default='')
    file = models.FileField(upload_to='polls/quiz/', default='default_file', null=True, blank=True)


class Question(models.Model):
    title = models.CharField(max_length=255, default='')
    file = models.ForeignKey(QuestionFile, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.question_text or ''


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text


class UserTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Test Result"
