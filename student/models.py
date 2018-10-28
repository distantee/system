# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

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
    price = models.FloatField(blank=True, null=True)
    time = models.CharField(max_length=20, blank=True, null=True)
    introduce = models.CharField(max_length=500, blank=True, null=True)

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
