from django.conf.urls import url

from todo.views import TodoListView, TodoDetailView, TodoCreateView, ChangeTodoStateView, TodoUpdateView

urlpatterns = [
    url(r'^$', TodoListView.as_view(), name='todo-list-view'),
    url(r'^new/$', TodoCreateView.as_view(), name='todo-create-view'),
    url(r'^(?P<pk>[0-9]+)/$', TodoDetailView.as_view(), name='todo-detail-view'),
    url(r'^(?P<pk>[0-9]+)/edit/$', TodoUpdateView.as_view(), name='todo-update-view'),
    url(r'^(?P<pk>[0-9]+)/state/(?P<action>[a-zA-Z_]+)/$', ChangeTodoStateView.as_view(), name='todo-action-view')
]
