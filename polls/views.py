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
            process_and_save_results(question.file,
                                     request.user)  # Обрабатываем файл и сохраняем результаты тестирования
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
        total_questions = 0

        # Чтение и обработка файла
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
                user_answers[current_question.id].append(answer_text)  # Сохраняем выбранные ответы пользователя
                total_questions += 1

        # Вычисление оценки пользователя
        print("user_answers:", user_answers)
        user_score = 0
        for question_id, selected_answers in user_answers.items():
            question = Question.objects.get(id=question_id)
            correct_answers = question.answer_set.filter(is_correct=True).values_list('answer_text', flat=True)
            print("Выбранные ответы пользователя для вопроса", question_id, ":", selected_answers)
            print("Правильные ответы на вопрос", question_id, ":", correct_answers)
            if set(selected_answers) == set(correct_answers):  # Если все правильные ответы были выбраны
                user_score += 1

        # Сохранение оценки пользователя
        UserScore.objects.create(user=user, score=user_score, total_questions=total_questions,
                                 question_file=current_question_file)

        # Отладочный вывод
        print("Оценка пользователя:", user_score)
        print("Количество вопросов:", total_questions)

    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")


def test_list(request):
    tests = QuestionFile.objects.all()
    return render(request, 'polls/test_list.html', {'tests': tests})


def submit_test(request, question_file_id):
    if request.method == 'POST':
        # Получаем данные из POST-запроса
        user_answers = request.POST

        # Получаем объект теста
        test = get_object_or_404(QuestionFile, pk=question_file_id)

        # Получаем все вопросы для этого теста
        questions = Question.objects.filter(question_file=test)

        # Счетчик правильных ответов
        correct_answers_count = 0

        # Проходим по всем вопросам
        for question in questions:
            # Получаем список правильных ответов для текущего вопроса
            correct_answers = Answer.objects.filter(question=question, is_correct=True)

            # Флаг правильных ответов на текущий вопрос
            correct = True

            # Проверяем, есть ли каждый из правильных ответов пользователя среди правильных ответов на вопрос
            for answer in correct_answers:
                if user_answers.get(f"question_{question.id}") != str(answer.id):
                    correct = False
                    break

            # Если все правильные ответы были выбраны, увеличиваем счетчик правильных ответов
            if correct:
                correct_answers_count += 1

        # Создаем или обновляем запись об оценке пользователя
        user_score, created = UserScore.objects.get_or_create(user=request.user, question_file=test)
        user_score.score = correct_answers_count
        user_score.total_questions = questions.count()
        user_score.save()

        # Выводим сообщение об успешной отправке теста
        messages.success(request, 'Тест успешно отправлен!')

        # Перенаправляем пользователя на страницу с результатами
        return redirect('test_result', question_file_id=question_file_id)

    # Если запрос не POST, возвращаемся на страницу с деталями теста
    return redirect('test_detail', test_id=question_file_id)


def test_detail(request, test_id):
    test = get_object_or_404(QuestionFile, pk=test_id)
    questions = test.question_set.all()  # Получаем все вопросы из файла
    user_tests = UserTest.objects.filter(question_file=test,
                                         user=request.user)  # Получаем ответы пользователя для данного теста
    user_answers = {user_test.question_id: user_test.answer_id for user_test in
                    user_tests}  # Создаем словарь ответов пользователя
    return render(request, 'polls/test_detail.html',
                  {'test': test, 'questions': questions, 'user_answers': user_answers})


def test_result(request, question_file_id):
    # Получаем объект теста
    test = get_object_or_404(QuestionFile, pk=question_file_id)

    # Получаем оценку пользователя для данного теста
    user_score = get_object_or_404(UserScore, user=request.user, question_file=test)

    # Получаем все вопросы для данного теста
    questions = test.question_set.all()

    # Получаем ответы пользователя для данного теста
    user_tests = UserTest.objects.filter(question_file=test, user=request.user)

    # Создаем словарь для хранения неправильных ответов
    incorrect_answers = {}

    # Проходим по всем вопросам
    for question in questions:
        # Получаем список правильных ответов на текущий вопрос
        correct_answers = list(Answer.objects.filter(question=question, is_correct=True).values_list('id', flat=True))

        # Получаем ответы пользователя на текущий вопрос
        user_answer = user_tests.filter(question=question).first()

        # Проверяем, является ли ответ пользователя правильным
        if user_answer:
            user_selected_answer = user_answer.answer_id
            if user_selected_answer != correct_answers:
                # Если ответ пользователя неправильный, добавляем его в словарь неправильных ответов
                incorrect_answers[question] = user_selected_answer

    # Рассчитываем процент правильных ответов
    percentage = (user_score.score / user_score.total_questions) * 100 if user_score.total_questions > 0 else 0

    # Передаем данные в шаблон для отображения
    return render(request, 'polls/test_result.html', {'test': test, 'user_score': user_score,
                                                       'percentage': percentage, 'incorrect_answers': incorrect_answers})





# TODO у каждого пользователя свой список тестирования
