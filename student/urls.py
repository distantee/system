from django.conf.urls import url

from student import views

urlpatterns = [
    url(r'^index/',views.index_view,name='index'),
    url(r'^show/(\d+)',views.show_view,name='show'),
    url(r'^register/',views.register_view,name='register'),
    url(r'^operate/',views.operate_view,name='operate'),
    url(r'^del1/(\d+)',views.del1_view,name='del1'),

]
