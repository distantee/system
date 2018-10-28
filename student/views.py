# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *

def showAll(courses):
    # courses = TCourse.objects.all()
    messages = []
    set1 = TStuentCourse.objects.values('course_id').annotate(c=Count('*'))
    for course in courses:
        allteachers = TTeacherCourse.objects.filter(courseid=course.courseid)
        teachers = []
        for teacher in allteachers:
            teacher = TTeacher.objects.get(teacherid=teacher.teacherid_id)
            teachers.append(teacher)
        xkcourses = []
        for xkgx in set1:
            xkcourses.append(xkgx['course_id'])
            c = xkgx['c']
            if xkgx['course_id'] == course.courseid:
                mes = [course, teachers, c]
                messages.append(mes)
        if course.courseid not in xkcourses:
            mes = [course, teachers, 0]
            messages.append(mes)
    return messages

# Create your views here.
def index_view(request):
    return render(request,'index.html')


def course_view(request):
    return render(request,'course.html')


def addCourse_view(request):
    if request.method=='GET':
        teachers = TTeacher.objects.all()
        return render(request,'addCourse.html',{'teachers':teachers})
    else:
        name=request.POST.get('coursename','')
        reTnames=request.POST.getlist('rkTname','')
        try:
            course=TCourse.objects.get(coursename=name)
        except TCourse.DoesNotExist:
            course=TCourse.objects.create(coursename=name)

        tnames=[]
        if reTnames[0]:
            for reTname in reTnames:
                try:
                    tname=TTeacher.objects.get(teachername=reTname)
                except TTeacher.DoesNotExist:
                    tname=TTeacher.objects.create(teachername=reTname)
                tnames.append(tname)

            for tname in tnames:
                # print tname,course
                try:
                    TTeacherCourse.objects.get(teacherid=tname.teacherid,courseid=course.courseid)
                except TTeacherCourse.DoesNotExist:
                    TTeacherCourse.objects.create(teacherid=tname,courseid=course)
        else:
            for reTname in reTnames[1:]:
                try:
                    tname = TTeacher.objects.get(teachername=reTname)
                except TTeacher.DoesNotExist:
                    tname = TTeacher.objects.create(teachername=reTname)
                tnames.append(tname)

            for tname in tnames:
                # print tname,course
                try:
                    TTeacherCourse.objects.get(teacherid=tname.teacherid, courseid=course.courseid)
                except TTeacherCourse.DoesNotExist:
                    TTeacherCourse.objects.create(teacherid=tname, courseid=course)
        return redirect('/student/showCourse/')


def showCourse_view(request):
    courses = TCourse.objects.all()
    messages=showAll(courses)

    num = request.GET.get('num', 1)
    num = int(num)
    paginator = Paginator(messages,3)
    try:
        t_pre_page = paginator.page(num)  # 获取当前页码的记录
    except PageNotAnInteger:  # 如果用户输入的页码不是整数时,显示第1页的内容
        t_pre_page = paginator.page(1)
    except EmptyPage:  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
        t_pre_page = paginator.page(paginator.num_pages)

    return render(request,'showCourse.html',{'paginator':paginator,'t_pre_page':t_pre_page})


def operCourse_view(request):
    if request.method=='GET':
        courses = TCourse.objects.all()
        messages = showAll(courses)
        return render(request, 'operCourse.html',{'messages':messages})
    else:
        key=request.POST.get('key','')
        constraint=request.POST.get('constraint','')
        val=request.POST.get('val','')
        # print key,constraint,val
        if key=='cid':
            if constraint=='gt':
                courses=TCourse.objects.filter(courseid__gt=val)
                messages=showAll(courses)
            elif constraint=='lt':
                courses = TCourse.objects.filter(courseid__lt=val)
                messages = showAll(courses)
            else:
                courses = TCourse.objects.filter(courseid=val)
                messages = showAll(courses)
        elif key=='cname':
            course=TCourse.objects.get(coursename=val)
            messages = []
            set1 = TStuentCourse.objects.values('course_id').annotate(c=Count('*'))
            allteachers = TTeacherCourse.objects.filter(courseid=course.courseid)
            teachers = []
            for teacher in allteachers:
                teacher = TTeacher.objects.get(teacherid=teacher.teacherid_id)
                teachers.append(teacher)
            xkcourses = []
            for xkgx in set1:
                xkcourses.append(xkgx['course_id'])
                c = xkgx['c']
                if xkgx['course_id'] == course.courseid:
                    mes = [course, teachers, c]
                    messages.append(mes)
            if course.courseid not in xkcourses:
                mes = [course, teachers, 0]
                messages.append(mes)
        else:
            all=TTeacherCourse.objects.filter(teacherid__teachername__contains=val)
            # print all
            courses=[]
            for single in all:
                course=TCourse.objects.get(courseid=single.courseid_id)
                courses.append(course)
            messages = showAll(courses)
        return render(request, 'operCourse.html', {'messages': messages})


def delCourse_view(request,courseid):
    # print courseid
    TTeacherCourse.objects.filter(courseid=courseid).delete()
    TStuentCourse.objects.filter(course=courseid).delete()
    TCourse.objects.get(courseid=courseid).delete()

    return redirect('/student/showCourse/')