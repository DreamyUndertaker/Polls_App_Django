from django.shortcuts import render
from django.views.generic import ListView, DetailView

from home.models import Instructions


class HomeView(ListView):
    template_name = 'home/homePage.html'
    model = Instructions
    context_object_name = 'instruction'
    queryset = Instructions.objects.all()


# TODO def to parse file with instruction text

