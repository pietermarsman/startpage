from django.conf.urls import url
from views import TodoListView, TodoDetailView

urlpatterns = [
    url(r'^$', TodoListView.as_view(), name='todo-list-view'),
    url(r'^(?P<pk>[0-9]+)/$', TodoDetailView.as_view(), name='todo-detail-view')
]
