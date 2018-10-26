#coding=utf-8
from django.db.models import Count, connection

from models import *
def rightInfo(request):
    #分类
    cate_post = Post.objects.values('category__cname', 'category').annotate(c=Count('*')).order_by('-c')

    #归档
    cursor = connection.cursor()
    cursor.execute("SELECT created,COUNT('*') AS c FROM blog_post GROUP BY DATE_FORMAT(created,'%Y%m') ORDER BY c DESC")
    archive = cursor.fetchall()

    return {'cate_post': cate_post,'archive':archive}