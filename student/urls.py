from django.conf.urls import url

from student import views

urlpatterns = [
    url(r'^index/',views.index_view,name='index'),
    url(r'^all_menus/',views.all_meuns),
    url(r'^c_manage/', views.c_manage),
    url(r'^c_news/', views.c_news),
    url(r'^c_classify/', views.c_classify),
]