from django.conf.urls import url

from .views import PageListView, PageCreateView, PageDeleteView, PageEditView, LabelCreateView, LabelDeleteView, \
    LabelEditView

urlpatterns = [
    url(r'^$', PageListView.as_view(), name='page-list-view'),
    url(r'^new$', PageCreateView.as_view(), name='page-create-view'),
    url(r'^(?P<pk>[0-9]+)/delete/$', PageDeleteView.as_view(), name='page-delete-view'),
    url(r'^(?P<pk>[0-9]+)/edit/$', PageEditView.as_view(), name='page-edit-view'),

    url(r'^label/new$', LabelCreateView.as_view(), name='label-create-view'),
    url(r'^label/(?P<pk>[0-9]+)/delete/$', LabelDeleteView.as_view(), name='label-delete-view'),
    url(r'^label/(?P<pk>[0-9]+)/edit/$', LabelEditView.as_view(), name='label-edit-view'),
]
