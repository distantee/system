# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from student.models import *
# Create your views here.
#进入图书模块首页，与addbook相同
def library_view(request):
    return render(request, 'addbook.html')

# 进入添加图书功能，添加图书
def addbook_view(request):
    # 通过get进入html页面
    if request.method == 'GET':
        return render(request,'addbook.html')
    # 提交form表单后，运用post方法获取相关数据
    else :
        bookid = request.POST.get('bookid','')
        bookname = request.POST.get('bookname','')
        author = request.POST.get('author','')
        price = request.POST.get('price')
        press = request.POST.get('press','')
        time = request.POST.get('time','')
        introduce = request.POST.get('introduce','')
        # 将获取到的数据添加到数据库中
        TBook.objects.create(bookname=bookname,author=author,bookid=bookid,price=price,press=press,time=time,introduce=introduce)
        # 完成图书添加后，重定向进入所有图书信息页面中，进行展示
        return redirect('/library/bookdata/')


# 封装分页功能
def Page(num,size):
    # 运用分页器，将图书表中的所有信息进行分页
    paginator = Paginator(TBook.objects.all(),size)
    # 如果当前页数小于1，让页数等于1
    if num < 1 :
        num = 1
    # 如果当前页数大于总页数，让页数等于最大页数
    elif num > paginator.num_pages :
        num = paginator.num_pages
    # 添加页码数，设置起始页
    start = ((num-1)/2)*2+1
    # 设置终止页
    end = start + 2
    # 当终止页数大于总页数时，令它等于总页数+1
    if end > paginator.num_pages :
        end = paginator.num_pages + 1
    # 返回所有页数以及起始，终止页
    return paginator.page(num),range(start,end)


# 进入所有图书数据页面，默认当前页数为第一页
def bookdata_view(request,num='1'):
    # 通过get进入html页面
    if request.method == 'GET':
        # 设置每页图书显示数量
        size = 2
        # 将页数转为int型，不然会报错
        num = int(num)
        # 调用分页函数，进行分页
        books,page_range = Page(num,size)
        # 进入html页面，并传参
        return render(request,'bookdata.html',{'books':books,'page_range':page_range})
    # 添加查询功能
    else :
        # 从html里边，获取下拉框的name属性以及文本框中的name属性
        key = request.POST.get('key','')
        test = request.POST.get('test', '')
        # 判断查询的是什么
        if key == 'bid':
            # 通过图书id获取具体图书信息
            books = TBook.objects.filter(bookid=test)
            return render(request,'bookdata.html',{'books':books})
        elif key == 'bname':
            # 通过图书name获取与之对应的图书信息
            books = TBook.objects.filter(bookname = test)
            return render(request,'bookdata.html',{'books':books})
        elif key == 'press':
            # 通过图书press获取与之对应的图书信息
            books = TBook.objects.filter(press = test)
            return render(request,'bookdata.html',{'books':books})
        elif key == 'gt_price':
            #通过图书price获取与之对应的图书信息
            books = TBook.objects.filter(price__gt=test)
            return render(request, 'bookdata.html', {'books': books})
        elif key == 'eq_price':
            #通过图书price获取与之对应的图书信息
            books = TBook.objects.filter(price=test)
            return render(request, 'bookdata.html', {'books': books})
        elif key == 'lt_price':
            #通过图书price获取与之对应的图书信息
            books = TBook.objects.filter(price__lt=test)
            return render(request, 'bookdata.html', {'books': books})


# 进入图书详情页面
def showbook_view(request,id):
    # 直接从页面获取要展示的图书id，进入html页面
    if request.method == 'GET':
        # 利用图书id获取该图书的详细信息
        bookIntro = TBook.objects.get(bookid=id)
        return render(request, 'showbook.html', {'bi':bookIntro})
    # 当页面有更改时，利用post获取相关信息
    else :
        bookid = request.POST.get('bookid','')
        bookname = request.POST.get('bookname','')
        author = request.POST.get('author','')
        price = request.POST.get('price','')
        press = request.POST.get('press','')
        time = request.POST.get('time','')
        introduce = request.POST.get('introduce','')
        # 如果存在图书id时，对数据库中的信息进行修改
        try :
            TBook.objects.filter(bookid=bookid).update(bookname=bookname,author=author,price=price,press=press,time=time,introduce=introduce)
        except TBook.DoesNotExist:
            TBook.objects.create(bookname=bookname, author=author, bookid=bookid, price=price, press=press, time=time,introduce=introduce)
        # 修改后直接进入所有图书页面进行展示
        return redirect('/library/bookdata/')


# 添加删除图书功能
def delbook_view(request):
    # 通过get获取要删除图书的id
    id = request.GET.get('id','')
    # 从图书表中获得相关信息，并删除
    TBook.objects.get(bookid=id).delete()
    return redirect('/library/bookdata/')


