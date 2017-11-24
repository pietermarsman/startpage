from django.views.generic import DetailView
from django.views.generic import ListView

from todo.models import Todo


class TodoListView(ListView):
    model = Todo


class TodoDetailView(DetailView):
    model = Todo