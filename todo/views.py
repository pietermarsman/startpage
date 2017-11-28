from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic.detail import SingleObjectMixin

from todo.models import Todo, TodoState


class TodoListView(ListView):
    model = Todo

    def get_queryset(self):
        allowed_states = TodoState.objects.filter(timer_running=True)

        state = self.kwargs.get('state')
        if state is not None:
            allowed_states = [TodoState.objects.get(computer_readable_text=state)]

        return TodoListView.model.objects. \
            filter(state__in=allowed_states). \
            order_by('created')


class TodoDetailView(DetailView):
    model = Todo


class TodoCreateView(CreateView):
    model = Todo
    fields = ['text', 'state']

    def get_success_url(self):
        return reverse('todo-list-view')


class TodoUpdateView(UpdateView):
    model = Todo
    fields = ['text']

    def get_success_url(self):
        return reverse('todo-list-view')


class ChangeTodoStateView(SingleObjectMixin, View):
    """Records the current user's interest in an author."""
    model = Todo

    def get(self, request, *args, **kwargs):
        state = kwargs.get('state')
        todo = self.get_object()

        new_state = TodoState.objects.get(computer_readable_text=state)
        todo.set_state(new_state)

        return HttpResponseRedirect(reverse('todo-list-view'))
