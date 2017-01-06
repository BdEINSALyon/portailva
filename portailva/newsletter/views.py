from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from portailva.association.mixins import AssociationMixin
from portailva.newsletter.models import Article


class AssociationArticleListView(AssociationMixin, ListView):
    model = Article
    template_name = 'newsletter/article/list.html'


class AssociationArticleNewView(AssociationMixin, CreateView):
    model = Article
    template_name = 'newsletter/article/new.html'


class AssociationArticleUpdateView(AssociationMixin, UpdateView):
    model = Article
    template_name = 'newsletter/article/update.html'


class AssociationArticleDetailView(AssociationMixin, DetailView):
    model = Article
    template_name = 'newsletter/article/detail.html'

    def get_context_data(self, **kwargs):
        context = super(AssociationArticleDetailView, self).get_context_data()
        context.update({
            'can_update': self.object.can_update(self.request.user),
            'can_delete': self.object.can_delete(self.request.user)
        })
        return context


class AssociationArticleDeleteView(AssociationMixin, DeleteView):
    model = Article
    template_name = 'newsletter/article/delete.html'
