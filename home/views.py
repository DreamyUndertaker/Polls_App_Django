from django.shortcuts import render
from django.views.generic import ListView, DetailView

from home.models import Instructions


class HomeView(ListView):
    template_name = 'home/homePage.html'
    model = Instructions
    context_object_name = 'instruction'
    queryset = Instructions.objects.all()


# TODO def to parse file with instruction text

class InstructionDetail(DetailView):
    template_name = 'home/instructions_detail.html'
    model = Instructions

    def get_context_data(self, **kwargs):
        return super(InstructionDetail, self).get_context_data(**kwargs)

    context_object_name = 'instruction'
