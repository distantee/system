#coding=utf-8
from django.conf.global_settings import MEDIA_ROOT
from django.conf.urls import url
from django.views.static import serve

from student import views

urlpatterns = [
    url(r'^index/',views.index_view,name='index'),
    url(r'^all_menus/',views.all_meuns),

    url(r'^c_manage/(\d+)', views.c_manage,name='c_manage'),
    #详情页路由
    url(r'^post/(\d+)', views.post_view,name='post'),
    url(r'^c_news/', views.c_news),
    url(r'^c_simply/', views.c_simply),
    url(r'^c_time/', views.c_time),
    url(r'^archive/(\d+)/(\d+)', views.archive_view),
    # url(r'^media/(?P<path>.*)/$', serve, {"document_root": MEDIA_ROOT})

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