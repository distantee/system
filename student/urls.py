#coding=utf-8
from django.conf.urls import url

from student import views

urlpatterns = [
    url(r'^index/',views.index_view,name='index'),
    url(r'^all_menus/',views.all_meuns),
    url(r'^c_manage/', views.c_manage,name='c_manage'),
    #详情页路由
    url(r'^post/(\d+)', views.post_view,name='post'),
    url(r'^c_news/', views.c_news),
    url(r'^c_simply/', views.c_simply),
    url(r'^c_time/', views.c_time),
]