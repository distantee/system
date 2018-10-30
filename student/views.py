# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import *
import jsonpickle
from django.core.serializers import serialize


# Create your views here.

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


def index_view(request):
    return render(request, 'index.html')


def all_meuns(request):
    return render(request, 'all_menus.html')


def getpage(num, size):
    posts = Paginator(Post.objects.order_by('-created'), size)
    if num <= 0:
        num = 1
    if num >= posts.num_pages:
        num = posts.num_pages
    start = num
    end = start + 3
    if end > posts.num_pages:
        end = posts.num_pages
    return posts.page(num), range(start, end)


def c_manage(request, num='1'):
    num = int(num)
    posts, page_range = getpage(num, 3)
    return render(request, 'c_manage.html', {'posts': posts, 'page_range': page_range})


def c_news(request):
    return render(request, 'c_news.html')


def c_simply(request):
    c_post = Post.objects.all()
    return render(request, 'c_simply.html', {'c_post': c_post})


def c_time(request):
    return render(request, 'c_time.html')


def post_view(request, postId):
    post = Post.objects.get(id=postId)
    return render(request, 'post.html', {'post': post})


def archive_view(request, year, month):
    # print year,month
    c_post = Post.objects.filter(created__year=year, created__month=month)
    # print c_post
    return render(request, 'archive.html', {'c_post': c_post})


# 成绩分页
def Pagecj(num, size):
    num = int(num)
    paginator = Paginator(Grade.objects.all().order_by('grade'), size)

    if num < 1:
        num = 1
    if num > paginator.num_pages:
        num = paginator.num_pages

    start = num
    end = start + 3

    if end > paginator.num_pages:
        end = paginator.num_pages + 1

    return paginator.page(num), range(start, end), paginator.num_pages


# 成绩查询
def gradecx_view(request, num='1'):
    if request.method == 'GET':
        size = 5
        gradelist, page_range, total_pages = Pagecj(num, size)
        return render(request, 'gradecx.html',
                      {'gradelist': gradelist, 'page_range': page_range, 'total_pages': total_pages})

    else:
        # 接受参数
        tiaojian = request.POST.get('tiaojian', '')
        # 判断
        if tiaojian == '学生姓名':
            content = request.POST.get('content', '')
            gradelist = Grade.objects.filter(studentid__studentname=content)
        elif tiaojian == '课程名称':
            content = request.POST.get('content', '')
            gradelist = Grade.objects.filter(courseid__coursename=content)
        else:
            content = request.POST.get('content', '')
            gradelist = Grade.objects.filter(studentid__clazz__clazzname=content)
        return render(request, 'gradecx.html', {'gradelist': gradelist})


# 成绩录入
def gradelr_view(request):
    if request.method == 'GET':
        stus = TStudent.objects.all()
        return render(request, 'gradelr.html', {'stus': stus})
    else:
        # 获取参数
        studentname = request.POST.get('studentname', '')

        #根据选中的学生名获取到班级
        student = TStudent.objects.get(studentname=studentname)  # student实例
        clazz = student.clazz  # clazz实例
        clazzname = clazz.clazzname

        # courseList = TStudent.objects.get(studentname=studentname).tstuentcourse_set.all()

        # 根据选中的学生名获取到课程
        tcList = TStuentCourse.objects.filter(student__studentname=studentname)
        # print tcList
        courseList = []
        for tc in tcList:
            tcc = TCourse.objects.get(coursename=tc.course.coursename)
            courname = tcc.coursename
            courseList.append(courname)
        # return JsonResponse({'clazz':jsonpickle.dumps(clazz,unpicklable=False),'courseList':serialize('json',courseList)})

        #获取更新后的参数
        coursename = request.POST.get('coursename', '')
        grade = request.POST.get('grade', '')
        claname = request.POST.get('clazzname', '')

        #判断四个属性是否为空
        if studentname and claname and coursename and grade:
            course = TCourse.objects.get(coursename=coursename)
            try:
                Grade.objects.get(studentid=student, courseid=course, grade=grade)
                return redirect('gradelr.html')
            except Grade.DoesNotExist:
                Grade.objects.create(studentid=student, courseid=course, grade=grade)
                return redirect('gradelr.html')

        #ajax传参
        return JsonResponse({'clazzname': clazzname, 'courseList': courseList})


# 删除成绩
def delgrade_view(request, gradeid):
    grade = Grade.objects.get(gradeid=gradeid)
    grade.delete()
    return redirect('/student/gradecx/')


#学生信息的注册功能
def  register_view(request):
    if request.method == 'GET':
        clazzs = TClazz.objects.all()
        course = TCourse.objects.all()
        return render(request, 'register.html', {'clazzs': clazzs, 'course': course})
    else:
        stuid = request.POST.get('stuid')
        sname = request.POST.get('name')
        clazz = request.POST.get('clazz')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        age = int(age)
        #学生课程一对多关系，用getlist接受课程列表
        course = request.POST.getlist('course')
        #判断班级是否需要添加数据库
        try:
            cls = TClazz.objects.get(clazzname=clazz)
        except TClazz.DoesNotExist:
            cls = TClazz.objects.create(clazzname=clazz)
        cns = []
        #判断课程
        for cn in course:
            try:
                cour = TCourse.objects.get(coursename=cn)
            except TCourse.DoesNotExist:
                cour = TCourse.objects.create(coursename=cn)
            cns.append(cour)
            # print cns
        #判断学生
        try:
            TStudent.objects.filter(studentid=stuid).update(studentname=sname, clazz=cls, sex=gender, age=age)
            stu = TStudent.objects.get(studentid=stuid)
        except TStudent.DoesNotExist:
            stu =  TStudent.objects.create(studentname=sname,clazz=cls,sex=gender,age=age)
            #在学生课程中间表中添加关联数据，因为课程信息会根据修改操作有变动，所以判断是否添加或者创建之前先删除所有的关系
            TStuentCourse.objects.filter(student=stu).delete()
            #stu = TStudent.objects.create(studentname=sname, clazz=cls, sex=gender, age=age)
        for c in cns:
            try:
                TStuentCourse.objects.get(student=stu, course=c)
            except TStuentCourse.DoesNotExist:
                TStuentCourse.objects.create(student=stu, course=c)

        return redirect('/student/show/1')

#学生信息修改功能
def update_view(request,num = '1'):
    #修改单个学生信息，通过学生id获取参数，使用路由位置传参
    if request.method == 'GET':
        num = int(num)
        #通过num值从数据库获取单个学生对象
        msg = TStudent.objects.get(studentid=num)
        clazz = TClazz.objects.all()
        #从数据库课程表获取所有课程信息
        allcourse = TCourse.objects.all()
        #从学生课程关系上正向查询该学生所选的课程信息
        course = TCourse.objects.filter(tstuentcourse__student_id__exact=msg.studentid)
        # print course
        return render(request,'update.html',{'msg':msg,'clazz':clazz,'course':course,'allcourse':allcourse})
    else:
        pass
#学生信息分页功能函数封装
def get_page(num):
    num = int(num)
    per = 1
    pages = Paginator(TStudent.objects.order_by('-studentid'), per)
    pages = Paginator(TStudent.objects.order_by('-studentid'),per)
    #判断当前页码是否越界
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
    return pages.page(num), range(start, end)


#学生信息展示页面。为主页显示
def show_view(request,num = '1'):
    # stus = TStudent.objects.all()
    #实现分页功能
    stus,page_range = get_page(num)
    cour_list = []
    for sol in stus.object_list:
        course = TStuentCourse.objects.filter(student=sol.studentid)
        # print course

        for cour in course:
            c = cour.course_id
            ccc = TCourse.objects.get(courseid=c)
            cour_list.append(ccc)
    return render(request, 'show.html', {'stus': stus, 'page_range': page_range, 'cour_list': cour_list})


#学生信息操作功能，包括修改和删除
def operate_view(request):
    #以get进入操作页面时，通过if判断传参跳转到操作对应的html
    if request.method == 'GET':
        stus = TStudent.objects.all()
        #获取所有学生对象信息进行传参
        return render(request, 'operate.html', {'stus': stus})
    else:
        #operate页面操作提交后，以post方式提交到该函数，第一步先获取表单数据
        key = request.POST.get('key')
        relation = request.POST.get('relation')
        value = request.POST.get('value')
        # print key, relation, value
        #通过比较传来的参数信息进行判定比较
        #通过学号进行查询
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
        #通过学生姓名就行提交
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
        #通过班级进行查询
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
        #通过性别进行查询
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
        #通过年龄进行查询
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


#学生信息删除功能
def del1_view(request,delid):
    try:
        #首先查找外键关联，删除学生表和课程表中间表的信息
        stucour = TStuentCourse.objects.filter(student=delid)
        # print stucour
        for sc in stucour:
            sc.delete()
    except TStuentCourse.DoesNotExist:
        #如果数据库中没有，就可以跳过这一操作
        pass
    try:
        #同上处理，查找学生表和成绩表中是否有关联
        gradestu = Grade.objects.filter(studentid=delid)
        for sc in gradestu:
            sc.delete()
    except Grade.DoesNotExist:
        pass
    #删除所有外键信息后，就可以删除学生信息了
    stu = TStudent.objects.get(studentid=delid)
    stu.delete()
    #删除操作成功后重定向本操作页面
    return redirect('/student/operate/')


def course_view(request):
    return render(request, 'course.html')


def addCourse_view(request):
    if request.method == 'GET':
        teachers = TTeacher.objects.all()
        return render(request, 'addCourse.html', {'teachers': teachers})
    else:
        name = request.POST.get('coursename', '')
        reTnames = request.POST.getlist('rkTname', '')
        try:
            course = TCourse.objects.get(coursename=name)
        except TCourse.DoesNotExist:
            course = TCourse.objects.create(coursename=name)

        tnames = []
        if reTnames[0]:
            for reTname in reTnames:
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
    messages = showAll(courses)

    num = request.GET.get('num', 1)
    num = int(num)
    paginator = Paginator(messages, 3)
    try:
        t_pre_page = paginator.page(num)  # 获取当前页码的记录
    except PageNotAnInteger:  # 如果用户输入的页码不是整数时,显示第1页的内容
        t_pre_page = paginator.page(1)
    except EmptyPage:  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
        t_pre_page = paginator.page(paginator.num_pages)

    return render(request, 'showCourse.html', {'paginator': paginator, 't_pre_page': t_pre_page})


def operCourse_view(request):
    if request.method == 'GET':
        courses = TCourse.objects.all()
        messages = showAll(courses)
        return render(request, 'operCourse.html', {'messages': messages})
    else:
        key = request.POST.get('key', '')
        constraint = request.POST.get('constraint', '')
        val = request.POST.get('val', '')
        # print key,constraint,val
        if key == 'cid':
            if constraint == 'gt':
                courses = TCourse.objects.filter(courseid__gt=val)
                messages = showAll(courses)
            elif constraint == 'lt':
                courses = TCourse.objects.filter(courseid__lt=val)
                messages = showAll(courses)
            else:
                courses = TCourse.objects.filter(courseid=val)
                messages = showAll(courses)
        elif key == 'cname':
            course = TCourse.objects.get(coursename=val)
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
            all = TTeacherCourse.objects.filter(teacherid__teachername__contains=val)
            # print all
            courses = []
            for single in all:
                course = TCourse.objects.get(courseid=single.courseid_id)
                courses.append(course)
            messages = showAll(courses)
        return render(request, 'operCourse.html', {'messages': messages})


def delCourse_view(request, courseid):
    # print courseid
    TTeacherCourse.objects.filter(courseid=courseid).delete()
    Grade.objects.filter(courseid=courseid).delete()
    TStuentCourse.objects.filter(course=courseid).delete()
    TCourse.objects.get(courseid=courseid).delete()

    return redirect('/student/showCourse/')



