from django.db.models import Count
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .models import Page, Label


class PageListView(ListView):
    model = Page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['label_list'] = Label.objects. \
            annotate(num_bookmarks=Count('page')). \
            order_by('-num_bookmarks')

        return context


class PageMixin(object):
    fields = ['url', 'name', 'description', 'labels']

    def get_success_url(self):
        return reverse('page-list-view')


class PageCreateView(PageMixin, CreateView):
    model = Page


class PageEditView(PageMixin, UpdateView):
    model = Page


class PageDeleteView(DeleteView):
    model = Page

    def get_success_url(self):
        return reverse('page-list-view')


class LabelMixin(object):
    fields = ['name']

    def get_success_url(self):
        return reverse('page-list-view')


class LabelCreateView(LabelMixin, CreateView):
    model = Label


class LabelEditView(LabelMixin, UpdateView):
    model = Label


class LabelDeleteView(DeleteView):
    model = Label

    def get_success_url(self):
        return reverse('page-list-view')