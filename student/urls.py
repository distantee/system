from django.conf.urls import url

from student import views

urlpatterns = [
    url(r'^index/',views.index_view,name='index'),
]