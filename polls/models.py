from django.db import models
from django.contrib.auth.models import User


class QuestionFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='polls/quiz/', null=False, blank=False, default=None)

    class Meta:
        verbose_name = 'Файл с вопросами'
        verbose_name_plural = 'Файлы с вопросами'


class Question(models.Model):
    question_file = models.ForeignKey(QuestionFile, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class UserTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    correct_answers_count = models.IntegerField(default=0)
    question_file = models.ForeignKey(QuestionFile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Test Result"

    class Meta:
        verbose_name = 'Вариант ответа пользователя'
        verbose_name_plural = 'Варианты ответов пользователя'


class UserScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    question_file = models.ForeignKey(QuestionFile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Score"

    class Meta:
        verbose_name = 'Оценка пользователя'
        verbose_name_plural = 'Оценки пользователей'
