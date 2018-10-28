# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from student.models import Grade, TStudent, TCourse, TClazz


def index_view(request):
    return render(request,'index.html')


def grade_view(request):
    grades = Grade.objects.all()
    #print grades
    return render(request,'grade.html',{'grades':grades})


def gradecx_view(request):
    if request.method == 'GET':
        grades = Grade.objects.all()
        return render(request,'gradecx.html',{'grades':grades})
    else:
        #接受参数
        tiaojian = request.POST.get('tiaojian','')
        #判断
        if tiaojian == '学生姓名':
            content = request.POST.get('content','')
            grades = Grade.objects.filter(studentid__studentname=content)
        elif tiaojian == '课程名称':
            content = request.POST.get('content', '')
            grades = Grade.objects.filter(courseid__coursename=content)
        else:
            content = request.POST.get('content', '')
            grades = Grade.objects.filter(studentid__clazz__clazzname=content)
        return render(request, 'gradecx.html', {'grades': grades})

def gradelr_view(request):
    if request.method == 'GET':
        return render(request,'gradelr.html')
    else:
        #获取参数
        studentname = request.POST.get('studentname','')
        clazzname = request.POST.get('clazzname','')
        coursename = request.POST.get('coursename','')
        grade = request.POST.get('grade','')
        if studentname and clazzname and coursename and grade:
            student = TStudent.objects.get(studentname=studentname)
            course = TCourse.objects.get(coursename=coursename)
            clazz = TClazz.objects.get(clazzname=clazzname)
            try:
                Grade.objects.get(studentid=student, courseid=course,grade=grade)
                return HttpResponse('数据库已有该成绩')
            except Grade.DoesNotExist:
                Grade.objects.create(studentid=student, courseid=course, grade=grade)
                return render(request,'gradelr.html')

        return HttpResponse('添加数据不完整')

def deletegrade_view(request,gradeid):
    #print gradeid
    grade = Grade.objects.get(gradeid=gradeid)
    grade.delete()
    return HttpResponse('删除成功')