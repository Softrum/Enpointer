from __future__ import unicode_literals

from django.db import models
import uuid
from dragonslayer.models import Project
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	project = models.ForeignKey(Project , null=True)

	def __str__(self):
		return self.title or ''


class Version(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	content = models.TextField(null=True, blank=True)
	author = models.ForeignKey(User)
	created = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.title or ''

class Page(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	project = models.ForeignKey(Project , null=True, related_name='pages')
	category = models.ForeignKey(Category, null=True, related_name='pages')
	published = models.BooleanField(default=False)
	current_version = models.ForeignKey(Version, null=True)
	versions = models.ManyToManyField(Version, related_name='versions')
	author = models.ForeignKey(User, related_name='pages')
	created = models.DateTimeField(default=datetime.now, blank=True)
	updated = models.DateTimeField(null=True, blank=True)






class History(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	message = models.CharField(max_length=500, null=True, blank=True)
	page = models.ForeignKey(Page, related_name='history')
	created =models.DateTimeField(default=datetime.now, blank=True)
	version = models.ForeignKey(Version, null=True)
	project =  models.ForeignKey(Project , null=True, related_name='history')
		
	def __str__(self):
		return self.message or ''





