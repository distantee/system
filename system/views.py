#coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        name = request.POST.get('name')
        pwd = request.POST.get('password')
        # print name,pwd
        if name == 'admin' and pwd == '123':
            # return render(request,'index.html',{'name':name})
            return redirect(to='/student/index')
        else:
            return HttpResponse('登陆失败')
