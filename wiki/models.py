from __future__ import unicode_literals

from django.db import models
import uuid
from dragonslayer.models import Project
from datetime import datetime

# Create your models here.


class Category(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	project = models.ForeignKey(Project , null=True)



class Page(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	poject = models.ForeignKey(Project , null=True)
	category = models.ForeignKey(Category, null=True)
	published = models.BooleanField(default=False)


	content = models.TextField(null=True, blank=True)
	created = models.DateTimeField(default=datetime.now, blank=True)
	updated = models.DateTimeField(null=True, blank=True)






