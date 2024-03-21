
from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    name = models.CharField(max_length=300)
    published = models.DateTimeField(auto_now_add=True)
    # input_file = models.FieldFile(upload_to = None, )

    def user_voted(self, user):
        user_votes = user.vote_set.all()
        done = user_votes.filter(question=self)
        if done.exists():
            return False
        return True

    def __str__(self):
        return self.name
    
    # def parse_questions(input_file):
    #     questions = []
    #     with open(input_file, 'r', encoding="windows-1251") as file:
    #         lines = file.readlines()
    #         current_question = None
    #     for line in lines:
    #         line = line.strip()
    #         if line.startswith('-'):
    #             if current_question is not None:
    #                 questions.append(current_question)
    #             current_question = {'question': line[1:], 'options': [], 'correct_answer': None}
    #         elif line.startswith('/'):
    #             current_question['options'].append(line[1:])    
    #         elif line.startswith('Ответ:'):
    #             current_question['correct_answer'] = str(line[7:-1])
    #     if current_question is not None:
    #         questions.append(current_question)
    #     return questions
    # questions = parse_questions(input_file)




class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.question.name[:15]} - {self.choice.name[:15]} - {self.user.username}'
