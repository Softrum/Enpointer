# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import uuid

from django.contrib.auth.models import User

from datetime import datetime



#sample models ---------------------------------------------------------------------
#org > sections > projects >issues 
#org > profiles 



# The three classes which served as the base of the future universe upon which kingdoms were built, battles were fought and civilizations lost
#invest in classes and architecture early on 
#sample models ---------------------------------------------------------------------
#org > sections > projects >issues 
#org > profiles 














# The three classes which served as the base of the future universe upon which kingdoms were built, battles were fought and civilizations lost
#invest in classes and architecture early on 
class Org(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	created = models.DateTimeField(default=datetime.now, blank=True)


class UserProfile(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=100, null = True, blank = True)
	created = models.DateTimeField(default=datetime.now, blank=True)
	org = models.ForeignKey(Org)



class Section(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	description = models.CharField(max_length=100, null = True, blank = True)
	created = models.DateTimeField(default=datetime.now, blank=True)
	org = models.ForeignKey(Org)

class Project(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	description = models.CharField(max_length=100, null = True, blank = True)
	created = models.DateTimeField(default=datetime.now, blank=True)
	section = models.ForeignKey(Section)
	org = models.ForeignKey(Org)

	def __str__(self):
		return self.title


class Issue(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	description = models.CharField(max_length=100, null = True, blank = True)
	created = models.DateTimeField(default=datetime.now, blank=True)
	last_updated = models.DateTimeField(default=datetime.now, blank=True)
	assigned_to = models.ForeignKey(User, related_name='issues_assigned' , null=True)
	created_by = models.ForeignKey(User, related_name='issues_created', null=True)
	priority =  models.CharField(max_length=100, null = True, blank = True, default='mid') #low, mid, high
	status =  models.CharField(max_length=100, null = True, blank = True, default='open') #open, resolved
	due_date = models.DateTimeField(default=datetime.now, blank=True)
	project = models.ForeignKey(Project)
	org = models.ForeignKey(Org)


	def __str__(self):
		return self.title


class Comment(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	content = models.CharField(max_length=500, null = True, blank = True)
	created =  models.DateTimeField(default=datetime.now, blank=True)
	commentor = models.ForeignKey(User)
	issue = models.ForeignKey(Issue)

	def __str__(self):
		return self.content













# Create your models here.
