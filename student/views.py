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



def c_manage(request):
    posts=Post.objects.all().order_by('-created')
    return render(request, 'c_manage.html', {'posts': posts})




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