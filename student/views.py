# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import *
# Create your views here.
def index_view(request):
    return render(request,'index.html')


def  register_view(request):
    if request.method == 'GET':
        clazzs = TClazz.objects.all()
        course = TCourse.objects.all()
        return render(request,'register.html',{'clazzs':clazzs,'course':course})
    else:
        sname = request.POST.get('name')
        clazz = request.POST.get('clazz')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        age = int(age)
        course = request.POST.getlist('course')
        # print course
        # print sname,clazz,gender,age
        try:
            cls = TClazz.objects.get(clazzname=clazz)
        except TClazz.DoesNotExist:
            cls = TClazz.objects.create(clazzname=clazz)
        cns = []
        for cn in course:
            try:
                cour = TCourse.objects.get(coursename=cn)
            except TCourse.DoesNotExist:
                cour = TCourse.objects.create(coursename=cn)
            cns.append(cour)
        try:
            stu = TStudent.objects.get(studentname=sname, clazz=cls, sex=gender, age=age)
        except TStudent.DoesNotExist:
            stu =  TStudent.objects.create(studentname=sname,clazz=cls,sex=gender,age=age)
        for c in cns:
            try:
                TStuentCourse.objects.get(student=stu, course=c)
            except TStuentCourse.DoesNotExist:
                TStuentCourse.objects.create(student=stu,course=c)

        return redirect('/student/show/1')


def get_page(num):
    num = int(num)
    per = 1
    pages = Paginator(TStudent.objects.order_by('-studentid'),per)
    if num <= 0:
        num = 1
    if num > pages.num_pages:
        num = pages.num_pages
    #生成页码数
    start = num
    end = num + 3
    #判断end是否越界
    if end > pages.num_pages:
        end = pages.num_pages+1
    return pages.page(num),range(start,end)



def show_view(request,num = '1'):
        # stus = TStudent.objects.all()
        stus,page_range = get_page(num)
        return render(request,'show.html',{'stus':stus,'page_range':page_range})




def operate_view(request):
    if request.method == 'GET':
        stus = TStudent.objects.all()
        return render(request, 'operate.html', {'stus': stus})
    else:
        key = request.POST.get('key')
        relation = request.POST.get('relation')
        value = request.POST.get('value')
        print key, relation, value
        if key == 'sid':
            if relation == '>=':
                stus = TStudent.objects.filter(studentid__gte=value)
                return render(request, 'operate.html', {'stus': stus})
            elif relation == '=':
                stus = TStudent.objects.filter(studentid=value)
                return render(request, 'operate.html', {'stus': stus})
            elif relation == '<=':
                stus = TStudent.objects.filter(studentid__lte=value)
                return render(request, 'operate.html', {'stus': stus})
            else:
                stus = TStudent.objects.filter(studentid__contains=value)
                return render(request, 'operate.html', {'stus': stus})
        elif key == 'sname':
            if relation == '>=':
                stus = TStudent.objects.all()
                return render(request, 'operate.html', {'stus': stus})
            elif relation == '=':
                stus = TStudent.objects.filter(studentname__contains=value)
                return render(request, 'operate.html', {'stus': stus})
            elif relation == '<=':
                stus = TStudent.objects.all()
                return render(request, 'operate.html', {'stus': stus})
            else:
                stus = TStudent.objects.filter(studentname__contains=value)
        elif key == 'sclazz':
            if relation == '>=':
                stus = TStudent.objects.all()
                return render(request, 'operate.html', {'stus': stus})
            elif relation == '=':
                stus = TStudent.objects.filter(clazz__clazzname__contains=value)
                return render(request, 'operate.html', {'stus': stus})
            elif relation == '<=':
                stus = TStudent.objects.all()
                return render(request, 'operate.html', {'stus': stus})
            else:
                stus = TStudent.objects.filter(clazz__clazzname__contains=value)
                return render(request, 'operate.html', {'stus': stus})
        elif key == 'ssex':
            if relation == '>=':
                stus = TStudent.objects.all()
                return render(request, 'operate.html', {'stus': stus})
            elif relation == '=':
                stus = TStudent.objects.filter(sex__contains=value)
                return render(request, 'operate.html', {'stus': stus})
            elif relation == '<=':
                stus = TStudent.objects.all()
                return render(request, 'operate.html', {'stus': stus})
            else:
                stus = TStudent.objects.filter(sex__contains=value)
                return render(request, 'operate.html', {'stus': stus})
        else:
            if relation == '>=':
                stus = TStudent.objects.filter(age__gte=value)
                return render(request, 'operate.html', {'stus': stus})
            elif relation == '=':
                stus = TStudent.objects.filter(age=value)
                return render(request, 'operate.html', {'stus': stus})
            elif relation == '<=':
                stus = TStudent.objects.filter(age__lte=value)
                return render(request, 'operate.html', {'stus': stus})
            else:
                stus = TStudent.objects.filter(age__contains=value)
                return render(request, 'operate.html', {'stus': stus})


def del1_view(request,delid):
    print delid
    try:
        stucour = TStuentCourse.objects.filter(student=delid)
        print stucour
        for sc in stucour:
            sc.delete()
    except TStuentCourse.DoesNotExist:
        pass
    stu = TStudent.objects.get(studentid=delid)
    stu.delete()
    return redirect('/student/operate/')



