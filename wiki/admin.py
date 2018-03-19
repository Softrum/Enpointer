
# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin

# Register your models here.






from .models import Category, Version, Page, History 

admin.site.register(Category)
admin.site.register(Version)
admin.site.register(Page)
admin.site.register(History)