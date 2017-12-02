from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .models import Bookmark, Label


class BookmarkListView(ListView):
    model = Label

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['unlabelled_bookmarks'] = Bookmark.objects. \
            filter(label=None)

        return context


class BookmarkMixin(object):
    fields = ['url', 'name', 'label']

    def get_success_url(self):
        return reverse('bookmark-list-view')


class BookmarkCreateView(BookmarkMixin, CreateView):
    model = Bookmark


class BookmarkUpdateView(BookmarkMixin, UpdateView):
    model = Bookmark


class BookmarkDeleteView(DeleteView):
    model = Bookmark

    def get_success_url(self):
        return reverse('bookmark-list-view')


class LabelMixin(object):
    fields = ['name']

    def get_success_url(self):
        return reverse('bookmark-list-view')


class LabelCreateView(LabelMixin, CreateView):
    model = Label


class LabelUpdateView(LabelMixin, UpdateView):
    model = Label


class LabelDeleteView(DeleteView):
    model = Label

    def get_success_url(self):
        return reverse('bookmark-list-view')
