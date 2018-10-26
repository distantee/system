#coding=utf-8
from django.db.models import Count

from models import *
def rightInfo(request):
    #分类
    cate_post = Post.objects.values('category__cname', 'category').annotate(c=Count('*')).order_by('-c')
    return {'cate_post':cate_post}