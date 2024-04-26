import os
from collections import defaultdict
from datetime import timedelta

from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import QuestionForm
from .models import Question, Answer, QuestionFile, UserTest, UserScore


def upload_questions(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save()
            process_and_save_results(question.file,
                                     request.user)
            return redirect('test_list')
    else:
        form = QuestionForm()
    return render(request, 'polls/upload_questions.html', {'form': form})


def process_and_save_results(uploaded_file, user):
    try:
        file_content = uploaded_file.open().read().decode('windows-1251')
        lines = file_content.splitlines()
        current_question_file = QuestionFile.objects.get(file=uploaded_file)
        current_question = None
        user_answers = defaultdict(list)
        total_questions = 0
        for line in lines:
            line = line.strip()
            if line.startswith('-'):
                if current_question is not None and current_question.question_text.strip():
                    current_question.save()
                current_question = Question.objects.create(question_file=current_question_file,
                                                           question_text=line[1:].strip())
            elif line.startswith('/'):
                if current_question is not None:
                    answer_text = line[1:].strip()
                    is_correct = answer_text.endswith('*')
                    answer_text = answer_text[:-1].strip() if is_correct else answer_text.strip()
                    answer = Answer.objects.create(question=current_question, answer_text=answer_text,
                                                   is_correct=is_correct)
            elif current_question is not None and line.endswith('*'):
                user_answers[current_question.id].append(answer_text)
                total_questions += 1
        print("user_answers:", user_answers)
        user_score = 0
        for question_id, selected_answers in user_answers.items():
            question = Question.objects.get(id=question_id)
            correct_answers = question.answer_set.filter(is_correct=True).values_list('answer_text', flat=True)
            print("Выбранные ответы пользователя для вопроса", question_id, ":", selected_answers)
            print("Правильные ответы на вопрос", question_id, ":", correct_answers)
            if set(selected_answers) == set(correct_answers):
                user_score += 1
        UserScore.objects.create(user=user, score=user_score, total_questions=total_questions,
                                 question_file=current_question_file)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")


def test_list(request):
    tests = QuestionFile.objects.all()
    return render(request, 'polls/test_list.html', {'tests': tests})


def submit_test(request, question_file_id):
    if request.method == 'POST':
        user_answers = request.POST
        test = get_object_or_404(QuestionFile, pk=question_file_id)
        time_left = test.time_limit - (timezone.now() - test.start_time)
        if time_left <= timedelta(seconds=0):
            return HttpResponse("Time limit exceeded!")
        questions = Question.objects.filter(question_file=test)
        correct_answers_count = 0
        for question in questions:
            correct_answers = Answer.objects.filter(question=question, is_correct=True)
            correct = True
            user_answers_for_question = user_answers.getlist(f"question_{question.id}")

            for answer in correct_answers:
                if str(answer.id) not in user_answers_for_question:
                    correct = False
                    break
            if correct:
                correct_answers_count += 1
        user_score, created = UserScore.objects.get_or_create(user=request.user, question_file=test)
        user_score.score = correct_answers_count
        user_score.total_questions = questions.count()
        user_score.start_time = timezone.now()
        user_score.save()
        messages.success(request, 'Тест успешно отправлен!')
        return redirect('test_result', question_file_id=question_file_id)
    return redirect('test_detail', test_id=question_file_id)


def test_detail(request, test_id):
    test = get_object_or_404(QuestionFile, pk=test_id)
    questions = test.question_set.all()
    user_tests = UserTest.objects.filter(question_file=test, user=request.user)
    user_answers = {user_test.question_id: user_test.answer_id for user_test in user_tests}
    user_score = get_object_or_404(UserScore, user=request.user, question_file=test)
    if user_score.start_time:
        time_left = user_score.question_file.time_limit - (timezone.now() - user_score.start_time)
    else:
        time_left = None

    return render(request, 'polls/test_detail.html',
                  {'test': test, 'questions': questions, 'user_answers': user_answers, 'time_left': time_left})


def test_result(request, question_file_id):
    try:
        test = QuestionFile.objects.get(pk=question_file_id)
    except QuestionFile.DoesNotExist:
        raise Http404("Test does not exist")
    user_score = get_object_or_404(UserScore, user=request.user, question_file=test)
    percentage = (user_score.score / user_score.total_questions) * 100 if user_score.total_questions > 0 else 0
    current_time = timezone.now()
    if test.start_time:
        time_left = test.time_limit - (current_time - test.start_time)
        if time_left <= timedelta(seconds=0):
            messages.warning(request, 'Время на прохождение теста истекло.')
    else:
        time_left = None
    questions = test.question_set.all()
    user_tests = UserTest.objects.filter(question_file=test, user=request.user)
    user_answers = {}
    for user_test in user_tests:
        user_answers[user_test.question_id] = user_test.answer_id
    return render(request, 'polls/test_result.html', {
        'test': test,
        'user_score': user_score,
        'percentage': percentage,
        'questions': questions,
        'user_answers': user_answers,
        'current_time': current_time,
        'time_left': time_left,
    })

# TODO у каждого пользователя свой список тестирования
