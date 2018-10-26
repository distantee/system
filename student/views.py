# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from models import *

# Create your views here.
def index_view(request):
    return render(request,'index.html')


def all_meuns(request):
    return render(request,'all_menus.html')


def c_news(request):
    posts=Post.objects.all()
    return render(request,'c_news.html',{'posts':posts})

def c_manage(request):
    return render(request,'c_manage.html')


def c_classify(request):
    return render(request,'c_classify.html')