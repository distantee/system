# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

# Register your models here.
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('id','title','created')
    list_filter = ('title','created')
    search_fields = ('title', )

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post,PostModelAdmin)
