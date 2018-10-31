#coding=utf-8
from django.conf.global_settings import MEDIA_ROOT
from django.conf.urls import url
from django.views.static import serve

from student import views

urlpatterns = [
    #首页路由
    url(r'^index/',views.index_view,name='index'),
   #内容管理路由
    url(r'^c_manage/(\d+)', views.c_manage,name='c_manage'),
    #页面详情信息的路由
    url(r'^post/(\d+)', views.post_view,name='post'),
    #近期要闻路由
    url(r'^c_news/', views.c_news),
    #简要分类的路由
    url(r'^c_simply/', views.c_simply),
    #时间分类的主页面路由
    url(r'^c_time/', views.c_time),
    #时间详情页表路由
    url(r'^archive/(\d+)/(\d+)', views.archive_view),
    # url(r'^media/(?P<path>.*)/$', serve, {"document_root": MEDIA_ROOT})
    #成绩分页
    url(r'^pagegrade/(\d+)', views.gradecx_view),
    #成绩查询
    url(r'^gradecx/',views.gradecx_view),
    #成绩录入
    url(r'^gradelr/',views.gradelr_view),
    #删除成绩
    url(r'^delgrade/(\d+)',views.delgrade_view),
    #添加课程信息
    url(r'^addCourse/',views.addCourse_view,name='addCourse'),
    #展示课程信息
    url(r'^showCourse/',views.showCourse_view,name='showCourse'),
    #课程操作
    url(r'^operCourse/',views.operCourse_view,name='operCourse'),
    #修改课程信息
    url(r'^modifCourse/(\d+)',views.modifCourse_view,name='modifCourse'),
    #删除课程信息
    url(r'^delCourse/(\d+)',views.delCourse_view,name='delCourse'),
    #学生信息展示
    url(r'^show/(\d+)',views.show_view,name='show'),
    #学生信息注册
    url(r'^register/',views.register_view,name='register'),
    #学生信息操作，包括删除与修改
    url(r'^operate/',views.operate_view,name='operate'),
    url(r'^del1/(\d+)',views.del1_view,name='del1'),
    url(r'^update/(\d+)',views.update_view,name='update'),

]