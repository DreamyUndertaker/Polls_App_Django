import os
from collections import defaultdict
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuestionForm
from .models import Question, Answer, QuestionFile, UserTest, UserScore


def upload_questions(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save()  # Сохраняем форму, это создаст объект Question с прикрепленным файлом
            process_and_save_results(question.file, request.user)  # Обрабатываем файл и сохраняем результаты тестирования
            return redirect('test_list')  # Редирект на страницу списка тестов
    else:
        form = QuestionForm()
    return render(request, 'polls/upload_questions.html', {'form': form})


def process_and_save_results(uploaded_file, user):
    try:
        file_content = uploaded_file.open().read().decode('windows-1251')
        lines = file_content.splitlines()
        current_question_file = QuestionFile.objects.get(file=uploaded_file)
        current_question = None
        user_answers = defaultdict(list)  # Словарь для хранения ответов пользователя
        for line in lines:
            line = line.strip()
            if line.startswith('-'):
                if current_question is not None and current_question.question_text.strip():
                    current_question.save()
                current_question = Question.objects.create(question_file=current_question_file, question_text=line[1:].strip())
            elif line.startswith('/'):
                if current_question is not None:
                    answer_text = line[1:].strip()
                    is_correct = answer_text.endswith('*')
                    answer_text = answer_text[:-1].strip() if is_correct else answer_text.strip()
                    answer = Answer.objects.create(question=current_question, answer_text=answer_text, is_correct=is_correct)
                    user_answers[current_question.id].append(is_correct)  # Сохраняем ответ пользователя
        if current_question is not None and current_question.question_text.strip():
            current_question.save()

        # Вычисление оценки пользователя
        user_score = 0
        total_questions = 0
        for question_id, answers in user_answers.items():
            total_questions += 1
            if all(answers):  # Если все ответы на вопрос правильные
                user_score += 1

        # Сохранение оценки пользователя
        UserScore.objects.create(user=user, score=user_score, total_questions=total_questions, question_file=current_question_file)

        # Перезаписываем загруженный файл обработанным содержимым
        new_file_path = os.path.join('media', str(current_question_file.file))
        with open(new_file_path, 'w') as new_file:
            new_file.write(file_content)

    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")


def test_list(request):
    tests = QuestionFile.objects.all()
    return render(request, 'polls/test_list.html', {'tests': tests})


def submit_test(request, question_file_id):
    question_file = get_object_or_404(QuestionFile, pk=question_file_id)
    if request.method == 'POST':
        # Получаем отправленные ответы
        submitted_answers = {}
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                submitted_answers[question_id] = int(value)

        # Сохраняем результаты тестирования
        user = request.user  # Получаем пользователя
        for question_id, answer_id in submitted_answers.items():
            question = get_object_or_404(Question, pk=question_id)
            answer = get_object_or_404(Answer, pk=answer_id)
            is_correct = answer.is_correct
            UserTest.objects.create(user=user, question=question, answer=answer, is_correct=is_correct, question_file=question_file)

        # Выводим сообщение об успешном завершении теста
        messages.success(request, f'Test submitted successfully!')

        return redirect('test_list')  # Перенаправление на страницу списка тестов
    else:
        return redirect('test_list')  # Перенаправление на страницу списка тестов в случае GET-запроса


def test_detail(request, test_id):
    test = get_object_or_404(QuestionFile, pk=test_id)
    questions = Question.objects.filter(question_file=test)
    return render(request, 'polls/test_detail.html', {'test': test, 'questions': questions})
