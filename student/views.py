# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *

# Create your views here.
#展示多个课程的相关信息
def showAll(courses):
    # courses = TCourse.objects.all()
    #用来存放每个课程的相关信息
    messages = []
    #得到每门课程与其选课人数的相关信息
    set1 = TStuentCourse.objects.values('course_id').annotate(c=Count('*'))

    for course in courses:
        #获取该课程对应的所有教师信息，TTeacherCourse对象
        allteachers = TTeacherCourse.objects.filter(courseid=course.courseid)
        #存放所有教师信息，TTeacher对象
        teachers = []
        for teacher in allteachers:
            #转化TTeacherCourse对象为TTeacher对象
            teacher = TTeacher.objects.get(teacherid=teacher.teacherid_id)
            teachers.append(teacher)
        xkcourses = []
        for xkgx in set1:
            #得到课程id
            xkcourses.append(xkgx['course_id'])
            #得到选课人数
            c = xkgx['c']
            #所得课程与课程选课人数信息之间的相互匹配
            #匹配
            if xkgx['course_id'] == course.courseid:
                #将课程，对应教师，选课人数存入一个列表，再存入messages大列表
                mes = [course, teachers, c]
                messages.append(mes)
        #如果不匹配，则选课人数直接存为0
        if course.courseid not in xkcourses:
            mes = [course, teachers, 0]
            messages.append(mes)
    return messages


#展示首页相关的信息
def index_view(request):
    return render(request,'index.html')

#展示内容管理的相关信息
def getpage(num,size):
    #调用分页函数进行分页
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

#展示近期要闻的相关信息
def c_news(request):
    return render(request,'c_news.html')

#展示简要分类的相关信息
def c_simply(request):
    c_post=Post.objects.all()
    return render(request, 'c_simply.html',{'c_post':c_post})

#展示时间分类表的页面
def c_time(request):
    return render(request, 'c_time.html')

#展示详情页的信息
def post_view(request,postId):
    post=Post.objects.get(id=postId)
    return render(request,'post.html',{'post':post})

#按照时间分类表分类出来的表的相关信息
def archive_view(request,year,month):
    # print year,month
    c_post = Post.objects.filter(created__year=year, created__month=month)
    # print c_post
    return render(request,'archive.html',{'c_post':c_post})

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
        stus = TStudent.objects.all()
        clazz = TClazz.objects.all()
        cours_list = []
        for stu in stus:
            courses =TStuentCourse.objects.filter(student=stu.studentid)
            # print courses
            cour_list = []
            for cour in courses:
                cour_list.append(cour.course)
            print cour_list
            cours_list.append(cour_list)

        return render(request,'gradelr.html',{'stus':stus,'cour_list':cours_list,'clazz':clazz})
    else:
        #获取参数
        studentname = request.POST.get('studentname','')
        clazzname = request.POST.get('clazzname','')
        coursename = request.POST.get('coursename','')
        grade = request.POST.get('grade','')
        if studentname and clazzname and coursename and grade:
            student = TStudent.objects.get(studentname=studentname)
            course = TCourse.objects.get(coursename=coursename)
            try:
                Grade.objects.get(studentid=student, courseid=course,grade=grade)
                return HttpResponse('数据库已有该成绩')
            except Grade.DoesNotExist:
                Grade.objects.create(studentid=student, courseid=course, grade=grade)
                return redirect('/student/gradelr/')

        return HttpResponse('添加数据不完整')

def deletegrade_view(request,gradeid):
    #print gradeid
    grade = Grade.objects.get(gradeid=gradeid)
    grade.delete()
    return HttpResponse('删除成功')

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
        cour_list = []
        for sol in stus.object_list:
            course = TStuentCourse.objects.filter(student=sol.studentid)
            # print course

            for cour in course:
                c = cour.course_id
                ccc = TCourse.objects.get(courseid=c)
                cour_list.append(ccc)
        return render(request,'show.html',{'stus':stus,'page_range':page_range,'cour_list':cour_list})

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
                return render(request, 'operate.html', {'stus': stus})
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

#添加课程功能
def addCourse_view(request):
    #初次进入页面传入已有的教师信息
    if request.method=='GET':
        teachers = TTeacher.objects.all()
        return render(request,'addCourse.html',{'teachers':teachers})
    else:
        #获取参数
        name=request.POST.get('coursename','')
        #得到的教师列表第一项是输入框的内容，后面的是复选框中的内容
        reTnames=request.POST.getlist('rkTname','')
        #添加课程到课程表
        try:
            course=TCourse.objects.get(coursename=name)
        except TCourse.DoesNotExist:
            course=TCourse.objects.create(coursename=name)

        #存储所选的所有教师
        tnames=[]
        #如果有输入新教师，则遍历所有
        if reTnames[0]:
            for reTname in reTnames:
                #存储教师信息到教师表
                try:
                    tname=TTeacher.objects.get(teachername=reTname)
                except TTeacher.DoesNotExist:
                    tname=TTeacher.objects.create(teachername=reTname)
                tnames.append(tname)

            #存储课程信息和对应的教师信息到教师任课表中
            for tname in tnames:
                # print tname,course
                try:
                    TTeacherCourse.objects.get(teacherid=tname.teacherid,courseid=course.courseid)
                except TTeacherCourse.DoesNotExist:
                    TTeacherCourse.objects.create(teacherid=tname,courseid=course)
        # 如果没有输入新教师，则从教师列表第二项开始遍历所有
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
            #添加成功，跳转到课程展示页面
        return redirect('/student/showCourse/')
#展示课程功能
def showCourse_view(request):
    #获取所有课程
    courses = TCourse.objects.all()
    #调用展示函数
    messages=showAll(courses)
    #分页操作
    num = request.GET.get('num', 1)
    num = int(num)
    per = 3
    pages = Paginator(messages,per)
    if num <= 0:
        num = 1
    if num > pages.num_pages:
        num = pages.num_pages
    # 生成页码数
    start = num
    end = num + 3
    # 判断end是否越界
    if end > pages.num_pages:
        end = pages.num_pages + 1
    messages=pages.page(num)
    page_range=range(start, end)

    return render(request,'showCourse.html',{'messages':messages,'page_range':page_range})
#课程操作功能
def operCourse_view(request):
    if request.method=='GET':
        #初次进入该页面传入所有信息，与展示页面相同
        courses = TCourse.objects.all()
        messages = showAll(courses)
        return render(request, 'operCourse.html',{'messages':messages})
    else:
        #得到查询条件
        key=request.POST.get('key','')
        #约束条件
        constraint=request.POST.get('constraint','')
        #值
        val=request.POST.get('val','')
        # print key,constraint,val
        #课程编号
        if key=='cid':
            #大于
            if constraint=='gt':
                #得到大于值的所有课程信息
                courses=TCourse.objects.filter(courseid__gt=val)
                # 调用展示函数
                messages=showAll(courses)
            elif constraint=='lt':
                courses = TCourse.objects.filter(courseid__lt=val)
                messages = showAll(courses)
            else:
                courses = TCourse.objects.filter(courseid=val)
                messages = showAll(courses)
        #课程名称
        elif key=='cname':
            # 可模糊查询，有关键字即可找到
            course=TCourse.objects.get(coursename__contains=val)
            # 展示
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
        #教师名称
        else:
            all=TTeacherCourse.objects.filter(teacherid__teachername=val)
            # print all
            courses=[]
            #获取该教师所授的所有课程
            for single in all:
                course=TCourse.objects.get(courseid=single.courseid_id)
                courses.append(course)
            messages = showAll(courses)
        return render(request, 'operCourse.html', {'messages': messages})
#删除课程功能
def delCourse_view(request,courseid):
    # print courseid
    #首先删除教师任课中间表中的该课程相关记录
    TTeacherCourse.objects.filter(courseid=courseid).delete()
    #删除创建表中与该课程相关的记录
    Grade.objects.filter(courseid=courseid).delete()
    #删除学生选课表中与该课程相关的记录
    TStuentCourse.objects.filter(course=courseid).delete()
    #删除课程表中该课程信息
    TCourse.objects.get(courseid=courseid).delete()

    return redirect('/student/showCourse/')
#修改课程功能
def modifCourse_view(request,courseid):
    if request.method=='GET':
        #初次进入页面，默认展示该课程的所有信息
        course = TCourse.objects.get(courseid=courseid)
        messages = []
        set1 = TStuentCourse.objects.values('course_id').annotate(c=Count('*'))
        allteachers = TTeacherCourse.objects.filter(courseid=course.courseid)
        teachers = []
        exceptTeacher=TTeacher.objects.all()
        for teacher in allteachers:
            teacher = TTeacher.objects.get(teacherid=teacher.teacherid_id)
            teachers.append(teacher)
            #获取所有除了该课程原来任教的教师的教师信息
            exceptTeacher=exceptTeacher.exclude(teacherid=teacher.teacherid)
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
        courses=TCourse.objects.all()

        return render(request,'modifCourse.html',{'messages':messages,'courses':courses,'exceptTeacher':exceptTeacher})
    else:
        # print courseid
        #先删除教师任课表中原有的该课程相关数据
        TTeacherCourse.objects.filter(courseid=courseid).delete()
        #接收参数
        coursename=request.POST.get('coursename','')
        rkTeachers=request.POST.getlist('rkTeacher','')
        # print coursename,rkTeacher,xknum
        #修改课程名称并存储
        cour=TCourse.objects.get(courseid=courseid)
        cour.coursename=coursename
        cour.save()
        for rkTeacher in rkTeachers:
            # 若任课教师非空
            if rkTeacher:
                try:
                    teac=TTeacher.objects.get(teachername=rkTeacher)
                except TTeacher.DoesNotExist:
                    teac=TTeacher.objects.create(teachername=rkTeacher)
                #将课程与教师的相关信息存入教师任课表
                TTeacherCourse.objects.create(courseid=cour,teacherid=teac)
        return redirect('/student/showCourse/')