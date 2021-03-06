# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-29 19:14
# Generated by Django 1.11.6 on 2018-10-30 14:21
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'blog_category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('desc', models.TextField()),
                ('content', models.TextField()),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
            ],
            options={
                'db_table': 'blog_post',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BlogPostTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'blog_post_tag',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BlogTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tname', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'blog_tag',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('gradeid', models.AutoField(primary_key=True, serialize=False)),
                ('grade', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'grade',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TClazz',
            fields=[
                ('clazzid', models.AutoField(primary_key=True, serialize=False)),
                ('clazzname', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 't_clazz',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TCourse',
            fields=[
                ('courseid', models.AutoField(primary_key=True, serialize=False)),
                ('coursename', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 't_course',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TStudent',
            fields=[
                ('studentid', models.AutoField(primary_key=True, serialize=False)),
                ('studentname', models.CharField(blank=True, max_length=20, null=True)),
                ('sex', models.CharField(blank=True, max_length=10, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 't_student',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TStuentCourse',
            fields=[
                ('xkid', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 't_stuent_course',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TTeacher',
            fields=[
                ('teacherid', models.AutoField(primary_key=True, serialize=False)),
                ('teachername', models.CharField(blank=True, max_length=20, null=True)),
                ('sex', models.CharField(blank=True, max_length=10, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 't_teacher',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TTeacherCourse',
            fields=[
                ('rkid', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 't_teacher_course',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('cname', models.CharField(max_length=20, unique=True, verbose_name='\u5206\u7c7b\u540d\u79f0')),
            ],
            options={
                'db_table': 'blog_category',
                'verbose_name_plural': '\u5206\u7c7b\u8868',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=20, verbose_name='\u6807\u9898')),
                ('desc', models.TextField(verbose_name='\u7b80\u4ecb')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('created', models.DateTimeField(verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('modified', models.DateTimeField(auto_now_add=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Category', verbose_name='\u5206\u7c7b\u8be6\u60c5')),
            ],
            options={
                'db_table': 'blog_post',
                'verbose_name_plural': '\u5e16\u5b50\u8868',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('tname', models.CharField(max_length=20, unique=True, verbose_name='\u6807\u7b7e\u540d\u79f0')),
            ],
            options={
                'db_table': 'blog_tag',
                'verbose_name_plural': '\u6807\u7b7e\u8868',
            },
        ),
        migrations.CreateModel(
            name='TBook',
            fields=[
                ('bookid', models.IntegerField(primary_key=True, serialize=False)),
                ('bookname', models.CharField(blank=True, max_length=20, null=True)),
                ('press', models.CharField(blank=True, max_length=30, null=True)),
                ('author', models.CharField(blank=True, max_length=20, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('time', models.CharField(blank=True, max_length=20, null=True)),
                ('introduce', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 't_book',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(to='student.Tag', verbose_name='\u53ef\u9009\u6807\u7b7e'),
        ),
    ]
