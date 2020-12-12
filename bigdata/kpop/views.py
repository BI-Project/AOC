from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Article
from django.views.generic import ListView, TemplateView, RedirectView
# Create your views here.
from django.conf import settings

class NewsListView(ListView):
    model = Article
    template_name = 'news_list.html'

class GraphView(TemplateView):
    template_name = 'graph.html'


class ResultView(TemplateView):
    template_name = 'result.html'