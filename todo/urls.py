from django.conf.urls import url

from todo.views import TodoListView, TodoCreateView, ChangeTodoStateView, TodoUpdateView

urlpatterns = [
    url(r'^$', TodoListView.as_view(), name='todo-list-view'),
    url(r'^filtered/(?P<state>[a-zA-Z_]+)/$', TodoListView.as_view(), name='todo-list-view'),
    url(r'^new/$', TodoCreateView.as_view(), name='todo-create-view'),
    url(r'^(?P<pk>[0-9]+)/edit/$', TodoUpdateView.as_view(), name='todo-update-view'),
    url(r'^(?P<pk>[0-9]+)/state/(?P<state>[a-zA-Z_]+)/$', ChangeTodoStateView.as_view(), name='todo-action-view')
]
