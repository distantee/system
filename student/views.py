# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index_view(request):
    return render(request,'index.html')


def all_meuns(request):
    return render(request,'all_menus.html')


def c_manage(request):
    return render(request,'c_manage.html')

def c_add(request):
    return render(request,'c_add.html')


def c_classify(request):
    return render(request,'c_classify.html')