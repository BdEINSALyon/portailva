from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from portailva.association.mixins import AssociationMixin
from portailva.newsletter.forms import ArticleForm, NewsletterForm
from portailva.newsletter.models import Article, Newsletter


class AssociationArticleListView(AssociationMixin, ListView):
    model = Article
    template_name = 'newsletter/article/list.html'


class AssociationArticleNewView(AssociationMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'newsletter/article/new.html'

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse('association-article-list', kwargs={
            'association_pk': kwargs.get('association_pk')
        })
        return super(AssociationArticleNewView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AssociationArticleNewView, self).get_form_kwargs()
        kwargs.update({
            'association': self.association
        })

        return kwargs


class AssociationArticleUpdateView(AssociationMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'newsletter/article/update.html'

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse('association-article-detail', kwargs={
            'association_pk': kwargs.get('association_pk'),
            'pk': kwargs.get('pk'),
        })
        return super(AssociationArticleUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AssociationArticleUpdateView, self).get_form_kwargs()
        kwargs.update({
            'association': self.association
        })

        return kwargs


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

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if not object.can_delete(request.user):
            raise PermissionDenied
        self.success_url = reverse('association-article-list', kwargs={
            'association_pk': kwargs.get('association_pk')
        })
        return super(AssociationArticleDeleteView, self).dispatch(request, *args, **kwargs)


class NewsletterListView(ListView):
    model = Newsletter
    template_name = 'newsletter/newsletter/list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('newsletter.admin_newsletter'):
            raise PermissionDenied
        return super(NewsletterListView, self).dispatch(request, *args, **kwargs)


class NewsletterNewView(CreateView):
    model = Newsletter
    template_name = 'newsletter/newsletter/new.html'
    form_class = NewsletterForm

    def get_success_url(self):
        return reverse('newsletter-detail', kwargs={'pk': self.object.id})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('newsletter.admin_newsletter'):
            raise PermissionDenied
        return super(NewsletterNewView, self).dispatch(request, *args, **kwargs)


class NewsletterUpdateView(CreateView):
    model = Newsletter
    template_name = 'newsletter/newsletter/update.html'
    form_class = NewsletterForm
    object = None

    def get_success_url(self):
        return reverse('newsletter-detail', kwargs={'pk': self.object.id})

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.has_perm('newsletter.admin_newsletter'):
            raise PermissionDenied
        return super(NewsletterUpdateView, self).dispatch(request, *args, **kwargs)


class NewsletterDetailView(DetailView):
    model = Newsletter
    template_name = 'newsletter/newsletter/detail.html'

    def get_context_data(self, **kwargs):
        context = super(NewsletterDetailView, self).get_context_data()
        context.update({
            'can_update': self.request.user.has_perm('newsletter.admin_newsletter'),
            'can_delete': self.request.user.has_perm('newsletter.admin_newsletter')
        })
        return context


class NewsletterOnlineView(DetailView):
    model = Newsletter
    template_name = 'newsletter/email/template.html'

    def get_context_data(self, **kwargs):
        context = super(NewsletterOnlineView, self).get_context_data()
        context.update({
            'articles': kwargs['object'].articles,
            'events': kwargs['object'].events,
            'top_articles': kwargs['object'].articles.filter(type='FEATURED'),
            'classic_articles': kwargs['object'].articles.filter(type='CLASSIC')
        })
        return context


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    template_name = 'newsletter/newsletter/delete.html'

    def get_success_url(self):
        return reverse('newsletter-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('newsletter.admin_newsletter'):
            raise PermissionDenied
        return super(NewsletterDeleteView, self).dispatch(request, *args, **kwargs)
