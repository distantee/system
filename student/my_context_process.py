#coding=utf-8
from django.db import connection

from models import *
def rightInfo(request):
    #分类
    # cate_post = Post.objects.values('category__cname', 'category').annotate(c=Count('*')).order_by('-c')

    #按时间归档
    cursor = connection.cursor()
    cursor.execute("SELECT created,COUNT('*') AS c FROM blog_post GROUP BY DATE_FORMAT(created,'%Y%m') ORDER BY c DESC")
    archive = cursor.fetchall()

    # 近期yaowen
    recent = Post.objects.all().order_by('-created')[:5]
    return {'archive':archive,'recent':recent}