from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic.detail import SingleObjectMixin

from todo.models import Todo


class TodoListView(ListView):
    model = Todo


class TodoDetailView(DetailView):
    model = Todo


class TodoCreateView(CreateView):
    model = Todo
    fields = ['text']

    def get_success_url(self):
        return reverse('todo-list-view')


class TodoUpdateView(UpdateView):
    model = Todo
    fields = ['text']

    def get_success_url(self):
        return reverse('todo-list-view')


class TodoActionView(SingleObjectMixin, View):
    """Records the current user's interest in an author."""
    model = Todo

    def get(self, request, *args, **kwargs):
        action = kwargs.get('action')
        object = self.get_object()

        if action == 'delete':
            object.delete()

        elif action == 'flip':
            object.flip()

        else:
            raise RuntimeWarning("Action %s is not known" % action)

        return HttpResponseRedirect(reverse('todo-list-view'))
