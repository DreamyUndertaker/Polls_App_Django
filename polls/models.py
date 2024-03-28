from django.db import models
from django.contrib.auth.models import User


class QuestionFile(models.Model):
    title = models.CharField(max_length=255, default='1')
    file = models.FileField(upload_to='polls/quiz/', null=False, blank=False, default=None)


class Question(models.Model):
    question_file = models.ForeignKey(QuestionFile, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255, null=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text


class UserTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    question_file = models.ForeignKey(QuestionFile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Test Result"
