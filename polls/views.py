from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, UserTest

def upload_questions(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        process_file(uploaded_file)
        return HttpResponseRedirect('/polls/display/')
    return render(request, 'polls/upload_questions.html')

def process_file(uploaded_file):
    file_content = uploaded_file.read().decode('windows-1251')
    lines = file_content.split('\n')
    current_question = None
    for line in lines:
        line = line.strip()
        if line.startswith('-'):
            if current_question is not None:
                current_question.save()  # Сохраняем текущий вопрос
            current_question = Question(question_text=line[1:])
            current_question.save()  # Сохраняем новый вопрос
        elif line.startswith('/'):
            answer_text = line[1:]
            is_correct = False
            if answer_text.startswith('*'):
                answer_text = answer_text[1:]
                is_correct = True
            answer = Answer(question=current_question, answer_text=answer_text, is_correct=is_correct)
            answer.save()  # Сохраняем ответ
    if current_question is not None:
        current_question.save()

def display_questions(request):
    questions = Question.objects.all()
    return render(request, 'polls/display_questions.html', {'questions': questions})


@login_required
def take_test(request):
    questions = Question.objects.all()
    if request.method == 'POST':
        user = request.user
        for question in questions:
            selected_answers = request.POST.getlist(f'answers_{question.id}')
            for answer_id in selected_answers:
                answer = Answer.objects.get(id=answer_id)
                is_correct = answer.is_correct
                UserTest.objects.create(user=user, question=question, answer=answer, is_correct=is_correct)
        return redirect('test_result')
    return render(request, 'polls/take_test.html', {'questions': questions})


@login_required
def test_result(request):
    user_tests = UserTest.objects.filter(user=request.user)
    return render(request, 'polls/test_result.html', {'user_tests': user_tests})
