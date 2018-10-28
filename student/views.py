# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from models import *

# Create your views here.
def index_view(request):
    return render(request,'index.html')


def all_meuns(request):
    return render(request,'all_menus.html')


def getpage(num,size):
    posts=Paginator(Post.objects.order_by('-created'),size)
    if num<=0:
        num=1
    if num>=posts.num_pages:
        num=posts.num_pages
    start=num
    end=start+3
    if end>posts.num_pages:
        end=posts.num_pages
    return posts.page(num),range(start,end)
def c_manage(request,num='1'):
    num=int(num)
    posts,page_range=getpage(num,3)
    return render(request, 'c_manage.html', {'posts': posts,'page_range':page_range})




def c_news(request):
    return render(request,'c_news.html')


def c_simply(request):
    c_post=Post.objects.all()
    return render(request, 'c_simply.html',{'c_post':c_post})

def c_time(request):
    return render(request, 'c_time.html')


def post_view(request,postId):
    post=Post.objects.get(id=postId)
    return render(request,'post.html',{'post':post})


def archive_view(request,year,month):
    # print year,month
    c_post = Post.objects.filter(created__year=year, created__month=month)
    # print c_post
    return render(request,'archive.html',{'c_post':c_post})