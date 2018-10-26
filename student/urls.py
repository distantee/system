#coding=utf-8
from django.conf.urls import url

from student import views

urlpatterns = [
    url(r'^index/',views.index_view,name='index'),
    url(r'^all_menus/',views.all_meuns),
    url(r'^c_manage/', views.c_manage),
    # url(r'^page/(\d+)',views.c_manage),
    #详情页路由
    url(r'^post/(\d+)', views.post_view),
    url(r'^c_news/', views.c_news),
    url(r'^c_classify/', views.c_classify),
]