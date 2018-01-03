import json
import logging

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic.detail import SingleObjectMixin

from todo.models import Todo, TodoState

logger = logging.getLogger(__name__)


class TodoViewMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['states'] = TodoState.objects.all()
        context['completed_json'] = json.dumps(list(TodoState.completed_in_last(days=7).values()))

        return context


class TodoListView(TodoViewMixin, ListView):
    model = Todo

    def get_queryset(self):
        allowed_states = TodoState.objects.filter(timer_running=True)

        state = self.kwargs.get('state')
        if state is not None:
            allowed_states = [TodoState.objects.get(computer_readable_text=state)]
        todos = TodoListView.model.objects. \
            filter(state__in=allowed_states). \
            order_by('created'). \
            select_related('state')

        logger.info('Retrieved {} todos'.format(len(todos)))
        return todos


class TodoCreateView(TodoViewMixin, CreateView):
    model = Todo
    fields = ['text', 'state']

    def get_success_url(self):
        return reverse('todo-list-view')


class TodoUpdateView(TodoViewMixin, UpdateView):
    model = Todo
    fields = ['text']

    def get_success_url(self):
        return reverse('todo-list-view')


class ChangeTodoStateView(SingleObjectMixin, View):
    """Records the current user's interest in an author."""
    model = Todo

    def get(self, request, *args, **kwargs):
        state_name = kwargs.get('state')
        todo = self.get_object()
        old_state = todo.state

        new_state = TodoState.objects.get(computer_readable_text=state_name)
        todo.set_state(new_state)

        logger.info("Changed todo {} from {} to {}".format(todo.id, old_state, new_state))

        return HttpResponseRedirect(reverse('todo-list-view'))
