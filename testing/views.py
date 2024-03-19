from django.shortcuts import render
from django.views import View
from .models import Answer, Question
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

class TestsView(View):
    template_name = 'testing/testingList.html'

    def get(self, request):
        return render(request, self.template_name)


class TestDetailView(View):
    template_name = 'testing/testingDetails.html'


class GetQuestion(GenericAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def get(self, request):
        questions = Question.objects.filter(visible = True)
        last_point = QuestionSerializer(questions, many = True)
        return Response(last_point)

class QuestionAnwser(GenericAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def post(self, request):
        anwser = AnswerSerializer(data = request.data, context = request)
        if anwser.is_valid(raise_exception = True):
            anwser.save()
            return Response({'result' : 'OK'})