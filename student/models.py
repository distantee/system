#coding=utf-8
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Grade(models.Model):
    gradeid = models.IntegerField(primary_key=True)
    studentid = models.ForeignKey('TStudent', models.DO_NOTHING, db_column='studentid', blank=True, null=True)
    courseid = models.ForeignKey('TCourse', models.DO_NOTHING, db_column='courseid', blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grade'


class TBook(models.Model):
    bookid = models.IntegerField(primary_key=True)
    bookname = models.CharField(max_length=20, blank=True, null=True)
    press = models.CharField(max_length=30, blank=True, null=True)
    author = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_book'


class TClazz(models.Model):
    clazzid = models.IntegerField(primary_key=True)
    clazzname = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_clazz'


class TCourse(models.Model):
    courseid = models.IntegerField(primary_key=True)
    coursename = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_course'


class TStudent(models.Model):
    studentid = models.IntegerField(primary_key=True)
    studentname = models.CharField(max_length=20, blank=True, null=True)
    clazz = models.ForeignKey(TClazz, models.DO_NOTHING, db_column='clazz', blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_student'


class TStuentCourse(models.Model):
    xkid = models.IntegerField(primary_key=True)
    student = models.ForeignKey(TStudent, models.DO_NOTHING, db_column='student', blank=True, null=True)
    course = models.ForeignKey(TCourse, models.DO_NOTHING, db_column='course', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_stuent_course'


class TTeacher(models.Model):
    teacherid = models.IntegerField(primary_key=True)
    teachername = models.CharField(max_length=20, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_teacher'


class TTeacherCourse(models.Model):
    rkid = models.IntegerField(primary_key=True)
    teacherid = models.ForeignKey(TTeacher, models.DO_NOTHING, db_column='teacherid', blank=True, null=True)
    courseid = models.ForeignKey(TCourse, models.DO_NOTHING, db_column='courseid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_teacher_course'



#栏目管理的具体内容
#分类表：分为三类-教师-学生-校园
class Category(models.Model):
    id=models.AutoField(primary_key=True,unique=True)
    cname=models.CharField(max_length=20,unique=True,verbose_name='分类名称')

    def __unicode__(self):
        return  u'Category:%s'%self.cname

    class Meta:
        db_table='blog_category'
        verbose_name_plural='分类管理表'

#标签表  标签分为三类：奖励、惩罚、飞跃进步
class Tag(models.Model):
    id=models.AutoField(primary_key=True,unique=True)
    tname=models.CharField(max_length=20,unique=True,verbose_name='标签名称')

    def __unicode__(self):
        return u'Tag:%s'%self.tname

    class Meta:
        db_table='blog_tag'
        verbose_name_plural = '标签管理表'

#帖子表
class Post(models.Model):
    id=models.AutoField(primary_key=True,unique=True)
    #标题
    title=models.CharField(max_length=20,verbose_name='标题')
    #简介
    desc=models.TextField(verbose_name='简介')
    #内容
    content=RichTextUploadingField(verbose_name='内容')
    #创建时间
    created=models.DateTimeField(verbose_name='创建时间')
    #修改时间
    modified=models.DateTimeField(auto_now_add=True,verbose_name='修改时间')
    #外键连接
    category=models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='分类详情')
    tag=models.ManyToManyField(Tag,verbose_name='可选标签')

    def __unicode__(self):
        return u'Post:%s'%self.title

    class Meta:
        db_table='blog_post'
        verbose_name_plural = '帖子管理表'

