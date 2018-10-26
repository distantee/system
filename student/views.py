# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from models import *

# Create your views here.
def index_view(request):
    return render(request,'index.html')


def all_meuns(request):
    return render(request,'all_menus.html')


# def page(num,size):
#     # print num,size
#     num=int(num)
#     paginator=Paginator(Post.objects.all().order_by('-created'),size)
#     # print paginator.count 总的记录条数
#     # print paginator.num_pages 总的分页数
#     # print paginator.page(num) 显示当前页所包含的对象
#     if num<1:
#         num=1
#     if num>paginator.num_pages:
#         num=paginator.num_pages
#     start=((num-1)/2)*2+1
#     end=start+2
#     if end>paginator.num_pages:
#         end=paginator.num_pages+1
#     # print(range(start,end))
#     return paginator.page(num),range(start,end)
def c_manage(request,num='1'):
    # # print num
    # size=2
    # posts,page_range=page(num,size)
    # # print posts
    # # cate_post=Post.objects.values('category__cname','category').annotate(c=Count('*')).order_by('-c')
    posts=Post.objects.all().order_by('-created')
    return render(request,'c_manage.html',{'posts':posts})




def c_news(request):
    return render(request,'c_news.html')


def c_classify(request):
    return render(request,'c_classify.html')


def post_view(request,postId):
    # post=Post.objects.get(id=postId)
    print postId
    # return render(request,'post.html',{'post':post})
    return HttpResponse('123')