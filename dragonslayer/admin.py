# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


from .models import Col_layout,Blog, UserProfile,FileAttachment,Layout,  Option, FieldConfig, Project, Issue, Section, Org, Transition, Workflow, GlobalPermission, Screen, Version, Label, Priority, Component, Status, Column,  CustomField, IssueType,Version,  Swimlane, Backlog, Sprint, Project_role 

admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Project_role)
admin.site.register(Issue)
admin.site.register(Section)
admin.site.register(Org)
admin.site.register(Workflow)
admin.site.register(Transition)
admin.site.register(GlobalPermission)
admin.site.register(Screen)
admin.site.register(CustomField)
admin.site.register(IssueType)

admin.site.register(Version)
admin.site.register(Label)
admin.site.register(Priority)
admin.site.register(Status)
admin.site.register(Column)
admin.site.register(Swimlane)

admin.site.register(Backlog)
admin.site.register(Sprint)

admin.site.register(Option)
admin.site.register(FieldConfig)
admin.site.register(FileAttachment)

admin.site.register(Layout)
admin.site.register(Blog)


admin.site.register(Col_layout)

