from django.conf.urls import url

from student import views

urlpatterns = [
    url(r'^index/',views.index_view,name='index'),
    url(r'^grade/',views.grade_view,name='grade'),
    url(r'^gradecx/',views.gradecx_view),
    url(r'^gradelr/',views.gradelr_view),
    url(r'^delete/(\d+)',views.delete_view),
]