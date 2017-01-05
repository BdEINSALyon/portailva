from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from portailva.association.mixins import AssociationMixin
from portailva.newsletter.models import Article


class AssociationArticleListArticleView(AssociationMixin, ListView):
    model = Article
    template_name = 'newsletter/article/.html'


class AssociationArticleNewArticleView(AssociationMixin, CreateView):
    model = Article
    template_name = 'newsletter/article/.html'


class AssociationArticleUpdateArticleView(AssociationMixin, UpdateView):
    model = Article
    template_name = 'newsletter/article/.html'


class AssociationArticleDetailedView(AssociationMixin, DetailView):
    model = Article
    template_name = 'newsletter/article/.html'


class AssociationArticleDeleteView(AssociationMixin, DeleteView):
    model = Article
