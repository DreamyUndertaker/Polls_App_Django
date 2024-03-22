from django.shortcuts import render, redirect
from django.views import generic
from .models import Lecture
from .forms import LectureForm

class LecturesList(generic.ListView):
    model = Lecture
    context_object_name = 'lectures'   # ваше собственное имя переменной контекста в шаблоне
    queryset = Lecture.objects.all() # Получение 5 книг, содержащих слово 'war' в заголовке
    template_name = 'articles/lectures_list.html'  # Определение имени вашего шаблона и его расположения
    

def upload_lecture(request):
    if request.method == 'POST':
        form = LectureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lecture_list')
    else:
        form = LectureForm()
    return render(request, 'articles/upload_lecture.html', {'form': form})

