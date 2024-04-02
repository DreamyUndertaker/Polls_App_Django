from django.shortcuts import render, redirect
from django.views import generic

from .forms import LectureForm
from .models import Lecture
from weasypdf.views import WeasypdfView


class LecturesList(generic.ListView):
    model = Lecture
    context_object_name = 'lectures'
    queryset = Lecture.objects.all()
    template_name = 'articles/lectures_list.html'


def upload_lecture(request):
    if request.method == 'POST':
        form = LectureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lecture_list')
    else:
        form = LectureForm()
    return render(request, 'articles/upload_lecture.html', {'form': form})



