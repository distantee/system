from django.conf.urls import url

from student import views

urlpatterns = [
    url(r'^index/',views.index_view,name='index'),
    url(r'^grade/',views.grade_view,name='grade'),
    url(r'^gradecx/',views.gradecx_view),
    url(r'^gradelr/',views.gradelr_view),
    url(r'^delete/(\d+)',views.deletegrade_view),
    url(r'^course/',views.course_view,name='course'),
    url(r'^addCourse/',views.addCourse_view,name='addCourse'),
    url(r'^showCourse/',views.showCourse_view,name='showCourse'),
    url(r'^operCourse/',views.operCourse_view,name='operCourse'),
    url(r'^delCourse/(\d+)',views.delCourse_view,name='delCourse'),
    url(r'^show/(\d+)',views.show_view,name='show'),
    url(r'^register/',views.register_view,name='register'),
    url(r'^operate/',views.operate_view,name='operate'),
    url(r'^del1/(\d+)',views.del1_view,name='del1'),

]