from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class HomeTemplateView(TemplateView):
    template_name = 'homepage/home.html'

    def get_context_data(self, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)