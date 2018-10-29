# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from student.models import *
# Create your views here.

def library_view(request):
    return render(request, 'addbook.html')


def addbook_view(request):
    if request.method == 'GET':
        return render(request,'addbook.html')
    else :
        bookid = request.POST.get('bookid','')
        bookname = request.POST.get('bookname','')
        author = request.POST.get('author','')
        price = request.POST.get('price')
        press = request.POST.get('press','')
        time = request.POST.get('time','')
        introduce = request.POST.get('introduce','')
        TBook.objects.create(bookname=bookname,author=author,bookid=bookid,price=price,press=press,time=time,introduce=introduce)
        return redirect('/library/bookdata/')

def Page(num,size):
    paginator = Paginator(TBook.objects.all(),size)
    if num < 1 :
        num = 1
    elif num > paginator.num_pages :
        num = paginator.num_pages
    start = ((num-1)/2)*2+1
    end = start + 2
    if end > paginator.num_pages :
        end = paginator.num_pages + 1
    return paginator.page(num),range(start,end)

def bookdata_view(request,num='1'):
    if request.method == 'GET':
        size = 2
        num = int(num)
        books,page_range = Page(num,size)
        return render(request,'bookdata.html',{'books':books,'page_range':page_range})
    else :
        key = request.POST.get('key','')
        test = request.POST.get('test', '')
        if key == 'bid':
            books = TBook.objects.filter(bookid=test)
            return render(request,'bookdata.html',{'books':books})
        elif key == 'bname':
            books = TBook.objects.filter(bookname = test)
            return render(request,'bookdata.html',{'books':books})


def showbook_view(request,id):
    if request.method == 'GET':
        bookIntro = TBook.objects.get(bookid=id)
        return render(request, 'showbook.html', {'bi':bookIntro})
    else :
        bookid = request.POST.get('bookid','')
        bookname = request.POST.get('bookname','')
        author = request.POST.get('author','')
        price = request.POST.get('price','')
        press = request.POST.get('press','')
        time = request.POST.get('time','')
        introduce = request.POST.get('introduce','')
        try :
            TBook.objects.filter(bookid=bookid).update(bookname=bookname,author=author,price=price,press=press,time=time,introduce=introduce)
        except TBook.DoesNotExist:
            TBook.objects.create(bookname=bookname, author=author, bookid=bookid, price=price, press=press, time=time,introduce=introduce)
        return redirect('/library/bookdata/')

def delbook_view(request):
    id = request.GET.get('id','')
    TBook.objects.get(bookid=id).delete()
    return redirect('/library/bookdata/')


