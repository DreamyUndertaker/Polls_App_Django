from django.shortcuts import render, redirect

from .forms import QuestionForm
from .models import Question, Answer, UserTest

from .models import QuestionFile


def upload_questions(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save()  # Сохраняем форму, это создаст объект Question с прикрепленным файлом
            process_file(question.file)  # Обрабатываем файл
            return redirect('test_list')  # Редирект на страницу списка тестов
    else:
        form = QuestionForm()
    return render(request, 'polls/upload_questions.html', {'form': form})


def process_file(uploaded_file):
    print("Reading file...")
    try:
        file_content = uploaded_file.open().read().decode('windows-1251')  # Чтение содержимого файла
        print("File content:", file_content)
        lines = file_content.splitlines()  # Разбиение содержимого файла на строки
        current_question = None
        for line in lines:
            line = line.strip()
            if line.startswith('-'):
                if current_question is not None and current_question.question_text.strip():
                    current_question.save()  # Сохраняем текущий вопрос, если он не пустой
                current_question = Question.objects.create(question_text=line[1:].strip())  # Создаем новый вопрос
            elif line.startswith('/'):
                if current_question is not None:
                    answer_text = line[1:].strip()  # Получаем текст ответа
                    is_correct = answer_text.endswith('*')  # Проверяем, является ли ответ правильным
                    answer_text = answer_text[
                                  :-1].strip() if is_correct else answer_text.strip()  # Удаляем звездочку из текста ответа, если есть
                    Answer.objects.create(question=current_question, answer_text=answer_text,
                                          is_correct=is_correct)  # Создаем ответ
        if current_question is not None and current_question.question_text.strip():
            current_question.save()  # Сохраняем последний вопрос, если он не пустой
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")


def test_list(request):
    tests = UserTest.objects.all()
    return render(request, 'polls/test_list.html', {'tests': tests})


def test_detail(request, test_id):
    test = UserTest.objects.get(pk=test_id)
    return render(request, 'polls/test_detail.html', {'test': test})
