# coding=utf-8
from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^library/', views.library_view, name='library'),
    url(r'^addbook/', views.addbook_view, name='addbook'),
    url(r'^bookdata/',views.bookdata_view,name='bookdata'),
    url(r'^showbook/(.*)',views.showbook_view,name='showbook'),
    url(r'^delbook/',views.delbook_view,name='delbook'),
    url(r'^page/(\d+)',views.bookdata_view),
]


