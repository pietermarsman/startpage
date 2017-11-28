from django.conf.urls import url
from todo.views import TodoListView, TodoDetailView, flip_done

urlpatterns = [
    url(r'^$', TodoListView.as_view(), name='todo-list-view'),
    url(r'^(?P<pk>[0-9]+)/$', TodoDetailView.as_view(), name='todo-detail-view'),
    url(r'^(?P<pk>[0-9]+)/flip_done$', flip_done, name='todo-flip-done')
]
