# coding=utf-8
from django.conf.urls import url
from . import views
urlpatterns=[
    #添加图书管理路由
    url(r'^library/', views.library_view, name='library'),
    # 添加图书的路由
    url(r'^addbook/', views.addbook_view, name='addbook'),
    # 展示所有图书的数据的路由
    url(r'^bookdata/',views.bookdata_view,name='bookdata'),
    # 单个图书详情的路由
    url(r'^showbook/(.*)',views.showbook_view,name='showbook'),
    # 删除图书的路由
    url(r'^delbook/',views.delbook_view,name='delbook'),
    # 添加分页路由
    url(r'^page/(\d+)',views.bookdata_view),
]


