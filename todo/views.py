
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic import ListView

from todo.models import Todo


class TodoListView(ListView):
    model = Todo


class TodoDetailView(DetailView):
    model = Todo


def flip_done(request, pk):
    todo = Todo.objects.get(id=pk)
    if todo.done:
        todo.finished = None
    else:
        todo.finished = timezone.now()
    todo.save()

    return redirect(reverse('todo-list-view'))