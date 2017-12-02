from django.conf.urls import url

from .views import BookmarkListView, BookmarkCreateView, LabelCreateView, BookmarkDeleteView, LabelDeleteView, \
    BookmarkUpdateView, LabelUpdateView

urlpatterns = [
    url(r'^$', BookmarkListView.as_view(), name='bookmark-list-view'),
    url(r'^new', BookmarkCreateView.as_view(), name='bookmark-create-view'),
    url(r'^(?P<pk>[0-9]+)/delete/$', BookmarkDeleteView.as_view(), name='bookmark-delete-view'),
    url(r'^(?P<pk>[0-9]+)/edit/$', BookmarkUpdateView.as_view(), name='bookmark-update-view'),
    url(r'^label/(?P<pk>[0-9]+)/delete/$', LabelDeleteView.as_view(), name='label-delete-view'),
    url(r'^label/(?P<pk>[0-9]+)/edit/$', LabelUpdateView.as_view(), name='label-update-view'),
    url(r'^label/new', LabelCreateView.as_view(), name='label-create-view'),
]
