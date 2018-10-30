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
    return render(request, 'index.html')

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

#展示近期要闻的相关信息

def c_news(request):
    return render(request, 'c_news.html')

#展示简要分类的相关信息
def c_simply(request):
    c_post = Post.objects.all()
    return render(request, 'c_simply.html', {'c_post': c_post})

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

#添加课程功能
def addCourse_view(request):
    #初次进入页面传入已有的教师信息
    if request.method=='GET':
        teachers = TTeacher.objects.all()
        return render(request, 'addCourse.html', {'teachers': teachers})
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
                    tname = TTeacher.objects.get(teachername=reTname)
                except TTeacher.DoesNotExist:
                    tname = TTeacher.objects.create(teachername=reTname)
                tnames.append(tname)

            #存储课程信息和对应的教师信息到教师任课表中
            for tname in tnames:
                # print tname,course
                try:
                    TTeacherCourse.objects.get(teacherid=tname.teacherid, courseid=course.courseid)
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
        return render(request, 'operCourse.html', {'messages': messages})
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
                course = TCourse.objects.get(courseid=single.courseid_id)
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

    return redirect('/student/operCourse/')
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



