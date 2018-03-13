# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import uuid

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from datetime import datetime
from django.conf import settings

from django.contrib.auth.hashers import make_password
from ckeditor.fields import RichTextField



#sample models ---------------------------------------------------------------------
#org > sections > projects >issues 
#org > profiles 



# The three classes which served as the base of the future universe upon which kingdoms were built, battles were fought and civilizations lost
#invest in classes and architecture early on 
#sample models ---------------------------------------------------------------------
#org > sections > projects >issues 
#org > profiles 








#org, group, project_role, profile, section , project, backlog, sprint, column, status, isuetype, priority, version, issue, transition - consditions, validators, postfunctions, fieldtype, screen, schemes/templates, component, filters
#dashboards






# The three classes which served as the base of the future universe upon which kingdoms were built, battles were fought and civilizations lost
#invest in classes and architecture early on 


# User management 
class Org(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	created = models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
		if self.title != None:
			return self.title
		else:
			return 'org'
		









class GlobalPermission(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	org = models.ForeignKey(Org)

class ProjectPermission(models.Model):  #this will be divided into project permissions and global permissions 
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	org = models.ForeignKey(Org)
	


#permission , role and groups can come below project and fk to project 






class UserProfile(models.Model):  #global
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) # showing some error about uniqyeness , hipefuly it will reoslve 
	user = models.ForeignKey(User, related_name='userprofile')
	title = models.CharField(max_length=100, null = True, blank = True)
	created = models.DateTimeField(default=datetime.now, blank=True)
	updated = models.DateTimeField(default=datetime.now, blank=True)
	
	active = models.BooleanField(default=True)
	project_permissions = models.ManyToManyField(ProjectPermission)
	global_permissions = models.ManyToManyField(GlobalPermission) # project wise differentiation ?,,,it has to be directed via project role only 
	#project_roles = models.ManyToManyField(Project_roles)
	org = models.ForeignKey(Org, null=True, related_name="org_members")

	def __str__(self):
		k = self.user.username
		return k or ''

class Project_role(models.Model):  # link between group of users in project and project permissions 
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	members = models.ManyToManyField(User) #not reuiqred 
	project_permissions = models.ManyToManyField(ProjectPermission)
	org = models.ForeignKey(Org)


class Group(models.Model):   #link between group of users and global permissions ...dont give it addtional functionality of containing project wise permissions as project_roles is already there. 
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	description = models.CharField(max_length=100, null = True, blank = True)
	members = models.ManyToManyField(UserProfile)
	global_permissions = models.ManyToManyField(GlobalPermission)
	org = models.ForeignKey(Org, null=True)	


class Blog(models.Model):
	title = models.CharField(max_length=200, null=True, blank=True)
	content = RichTextField(null=True, blank=True)
	author = models.CharField(max_length=100, null = True, blank = True)
	category = models.CharField(max_length=100, null=True, blank=True )
	slug = models.SlugField(null=True, blank=True, max_length=200)
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	created = models.DateTimeField(default=datetime.now, blank=True)
	featured_image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.title or ''

	def save(self, *args, **kwargs):
		if not self.id:
			# Newly created object, so set slug
			self.slug = slugify(self.title)

		super(Blog, self).save(*args, **kwargs)

#Project and stuff 

class Section(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	description = models.CharField(max_length=100, null = True, blank = True)
	created = models.DateTimeField(default=datetime.now, blank=True)
	org = models.ForeignKey(Org , null=True)

	def __str__(self):
		return self.title or ''



class Invite_user_request(models.Model):
	org = models.ForeignKey(Org)
	hash_id = models.CharField(max_length=200)



class Project(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	description = models.CharField(max_length=100, null = True, blank = True)
	project_type = models.CharField(max_length=100, null = True, blank = True)
	admin = models.ManyToManyField(User)
	project_lead = models.ManyToManyField(User, related_name='projects')

	#workflow = simple where issue can be placed anywhere or it can be customized 
	created = models.DateTimeField(default=datetime.now, blank=True)
	section = models.ForeignKey(Section, null=True)
	org = models.ForeignKey(Org, null=True, related_name='projects')
	board_layout = models.TextField(null=True, blank=True)
	bg = models.TextField(null=True, blank=True)

	sortable_list_ids = models.TextField(null=True, blank=True)


	
	members = models.ManyToManyField(UserProfile, related_name='members')
	project_permissions = models.ManyToManyField(ProjectPermission)
	project_roles = models.ManyToManyField(Project_role)
	issue_id_prefix = models.CharField(max_length=100, null = True, blank = True)

	def __str__(self):
		return self.title or ''








class Backlog(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	project = models.ForeignKey(Project)
	org = models.ForeignKey(Org)
	created = models.DateTimeField(default=datetime.now, blank=True)


class Sprint(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	org = models.ForeignKey(Org)
	duration = models.IntegerField(null=True, blank=True)
	goal = models.CharField(max_length=100, null = True, blank = True)
	created = models.DateTimeField(default=datetime.now, blank=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	description = models.CharField(max_length=100, null = True, blank = True)
	project = models.ForeignKey(Project, related_name='sprints')
	start_date = models.DateField( null = True, blank = True)
	end_date =  models.DateField( null = True, blank = True)
	is_Active = models.BooleanField(default=False)
	complete =  models.BooleanField(default=False)

	def __str__(self):
		return self.title or ''




class Column(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	min_issues = models.IntegerField( null = True, blank = True)
	max_issues = models.IntegerField( null = True, blank = True)
	order = models.IntegerField(null=True, blank=True)
	bg_url = models.TextField(null=True, blank=True)
	project = models.ForeignKey(Project, related_name="columns")
	layout = models.TextField(null=True, blank=True)
	wid = models.IntegerField(null=True, blank=True, default=0)
	org = models.ForeignKey(Org)
	

	def __str__(self):
		k = self.project.title + ':'+self.title
		return k

class Status_type(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	project = models.ForeignKey(Project)
	org = models.ForeignKey(Org)

class Status(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	description = models.CharField(max_length=100, null = True, blank = True)
	#column = models.ForeignKey(Column,  null=True, blank=True, related_name='status')
	project = models.ForeignKey(Project, related_name="statuss")
	order = models.TextField(null=True, blank=True)
	status_type = models.ForeignKey(Status_type, null=True, blank=True)
	resolution = models.BooleanField(default=False)
	org = models.ForeignKey(Org)


	def __str__(self):
		k = self.title + self.project.title
		return k


class Col_layout(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	parent = models.ForeignKey("self", null=True, blank=True, related_name="children")
	title = models.CharField(max_length=100, null=True, blank=True)
	sections = models.IntegerField()
	width=models.CharField(max_length=100, null=True, blank=True)
	layout_type = models.CharField(max_length=100)
	column = models.ForeignKey(Column, null=True, blank=True, related_name="col_layout")
	status = models.ForeignKey(Status, null=True, blank=True)
	project = models.ForeignKey(Project, null=True, blank=True)


	def __str__(self):
		return self.title



class Layout(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	parent = models.ForeignKey("self", null=True,blank=True, related_name="children")
	
	divisions = models.IntegerField(null=True, blank=True)
	status = models.ForeignKey(Status, null=True, blank=True)
	layout_type = models.CharField(max_length=100, null=True, blank=True)
	project = models.ForeignKey(Project)
	title = models.CharField(max_length=100, null=True, blank=True)
	root = models.BooleanField(default=False)
	n =  models.IntegerField(null=True, blank=True)

	def __str__(self):
		k = str(self.title)
		return k

	def save(self, *args, **kw):
		if self.layout_type == 'vertical':
			self.n = 12/self.divisions
		super(Layout, self).save(*args, **kw)


"""
class Board(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	project = models.ForeignKey(Project)
	org = models.ForeignKey(Org) 

"""

class Component(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	description = models.CharField(max_length=100, null = True, blank = True)
	lead = models.ForeignKey(UserProfile, null=True)
	project = models.ForeignKey(Project)
	org = models.ForeignKey(Org)





class Label(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	description = models.CharField(max_length=100, null = True, blank = True)
	project = models.ForeignKey(Project)
	org = models.ForeignKey(Org)




class Screen(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	project = models.ForeignKey(Project, related_name='screens')
	org = models.ForeignKey(Org)

	def __str__(self):
		k = self.project.title + self.title
		return k






class Workflow(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	project = models.ForeignKey(Project, related_name='workflows')
	org = models.ForeignKey(Org)

	def __str__(self):
		k = self.project.title + self.title
		return k
	#belongs to project


class Transition(models.Model):
	uid= models.UUIDField(default=uuid.uuid4, editable=False, null=True, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	start_status = models.ForeignKey(Status, related_name='transitions', null=True, blank=True)
	end_status = models.ForeignKey(Status, null=True, blank=True)
	screen = models.ForeignKey(Screen, null=True, blank=True)
	workflow = models.ForeignKey(Workflow, null=True, blank=True, related_name='transitions')
	project = models.ForeignKey(Project)
	org = models.ForeignKey(Org, null=True, blank=True)

	def __str__(self):
		k = self.project.title + self.title 
		return k



class IssueType(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	description = models.CharField(max_length=100, null = True, blank = True)
	icon = models.ImageField(null=True, blank=True, upload_to='issue_type_icons')
	create_screen = models.ForeignKey(Screen, null = True, blank = True, related_name='a')
	edit_screen =  models.ForeignKey(Screen, null = True, blank = True, related_name='b')
	view_screen =  models.ForeignKey(Screen, null = True, blank = True, related_name='c')
	workflow = models.ForeignKey(Workflow, null=True, blank=True, related_name='workflow_issuetypes')
	project = models.ForeignKey(Project, related_name='issuetypes')
	org = models.ForeignKey(Org)

	def __str__(self):
		return self.title or ''

class Priority(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	description = models.CharField(max_length=100, null = True, blank = True)
	color = models.CharField(max_length=100, null = True, blank = True)
	project = models.ForeignKey(Project, related_name='project_prioritys')
	org = models.ForeignKey(Org)

	def __str__(self):
		return self.project.title or ''

class Version(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	description = models.CharField(max_length=100, null = True, blank = True)
	start_date = models.DateField( null = True, blank = True)
	release_date = models.DateField( null = True, blank = True)
	released = models.BooleanField(default=False)
	project = models.ForeignKey(Project, related_name='versions')
	org = models.ForeignKey(Org)


class Swimlane(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	description = models.CharField(max_length=100, null = True, blank = True)
	project = models.ForeignKey(Project)
	org = models.ForeignKey(Org)

"""
fieldconfigtable:
uid
project
org
screen= fk (Screen)


fieldconfig:
field = char ( for bult in title, and for customfield can be the uid )
visible = bool
required = bool
text = char 
fielfshchme = fk (fielfschem)
project
org



screen.fildconfigtable.fildconfig.ge...

better way would to be process these things at backend and send it along..




"""
class Resolution(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	models.CharField(max_length=100, null = True, blank = True)
	project = models.ForeignKey(Project)
	org = models.ForeignKey(Org)
	is_default = models.BooleanField(default=False, blank=True)

class Password_change_request(models.Model):
	user = models.ForeignKey(User)
	time = models.DateTimeField(default=datetime.now, blank=True)
	hash_id = models.CharField(max_length=200, null=True, blank=True)

class Issue(models.Model):
	issue_id = models.CharField(max_length=100, null = True, blank = True)
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=200, null = True, blank = True)
	description = models.TextField( null = True, blank = True, default=' ')

	created = models.DateTimeField(default=datetime.now, blank=True)
	last_updated = models.DateTimeField(default=datetime.now, blank=True)
	end_date = models.DateTimeField(null=True,  blank=True)
	start_date = models.DateTimeField(null=True,  blank=True)
	due_date = models.DateField(null=True,  blank=True)

	assigned_to = models.ForeignKey(User, related_name='issues_assigned' , null=True, blank=True)
	created_by = models.ForeignKey(User, related_name='issues_created', null=True, blank=True)


	priority =  models.ForeignKey(Priority,  null=True, blank=True)
	
	fix_version = models.ForeignKey(Version, related_name='issues', null=True, blank=True)
	affected_version = models.ManyToManyField(Version,  null=True, blank=True)
	issue_type = models.ForeignKey(IssueType, null=True) #low, mid, high
	#status =  models.CharField(max_length=100, null = True, blank = True, default='open') #open, resolved
	component = models.ForeignKey(Component, null=True, blank=True)
	related_issues = models.ManyToManyField("self" , null=True, blank=True)
	epic = models.ForeignKey("self", null=True, blank=True, related_name="issues")
	label = models.ManyToManyField(Label, null=True, blank=True, related_name='issues')
	status = models.ForeignKey(Status, null=True, blank=True, related_name='issues')
	bg = models.TextField(null=True, blank=True)

	original_time_estimate = models.TimeField(null=True, blank=True)
	current_time_estimate = models.TimeField(null=True, blank=True)
	timespent = models.TimeField(null=True, blank=True)
	timespent2 = models.IntegerField(null=True, blank=True, default=0) #should this also be date time field ?
	time_started = models.DateTimeField(default=datetime.now, blank=True)
	time_ended =  models.DateTimeField(default=datetime.now, blank=True)

	points = models.IntegerField(null=True, blank=True)


	
	
	project = models.ForeignKey(Project, null=True, related_name='issues')
	backlog = models.ForeignKey(Backlog, null=True, blank=True)
	sprint = models.ForeignKey(Sprint, null=True, blank=True, related_name='issues')
	org = models.ForeignKey(Org, null=True)

	resolved = models.BooleanField(default=False)
	resolution = models.ForeignKey(Resolution, null=True, blank=True)


	def __str__(self):
		if self.title != None:
			k = self.title
		else:
			k = 'issue'
		return k

class Task(models.Model):
	uid=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	issue = models.ForeignKey(Issue, related_name='tasks')
	project = models.ForeignKey(Project)
	title = models.CharField(max_length=100, null = True, blank = True)
	checked = models.BooleanField(default=False)
	created_by = models.ForeignKey(User, related_name='x')
	checked_by = models.ForeignKey(User, null=True, blank=True)
	created_date = models.DateTimeField(default=datetime.now, null=True, blank=True)
	checked_date = models.DateTimeField(null=True,  blank=True)


class FieldConfig(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	project = models.ForeignKey(Project)
	screen = models.ForeignKey(Screen, related_name='field_config')
	org = models.ForeignKey(Org)
	title_required = models.BooleanField(default=False)
	title_visible = models.BooleanField(default=True)
	title_text = models.CharField(max_length=100, null = True, blank = True)
	description_required = models.BooleanField(default=False)
	description_visible = models.BooleanField(default=True)
	description_text = models.CharField(max_length=100, null = True, blank = True)
	
	tasks_visible = models.BooleanField(default=True)
	
	
	comment_visible = models.BooleanField(default=True)
	priority_required = models.BooleanField(default=False)
	priority_visible = models.BooleanField(default=True)
	priority_text = models.CharField(max_length=100, null = True, blank = True)
	fix_version_required = models.BooleanField(default=False)
	fix_version_visible = models.BooleanField(default=True)
	fix_version_text = models.CharField(max_length=100, null = True, blank = True)	

	points_visible = models.BooleanField(default=True)
	points_required = models.BooleanField(default=False)
	points_text = models.CharField(max_length=100, null = True, blank = True)

	label_visible = models.BooleanField(default=True)

	subscribers = models.ManyToManyField(User)

	epic_visible = models.BooleanField(default=True)
	epic_text = models.CharField(max_length=100, null = True, blank = True)

		

class Event_type_org(models.Model):
	title= models.CharField(max_length=100, null = True, blank = True)
	org = models.ForeignKey(Org)
	active = models.BooleanField(default=True)
	listeners = models.ManyToManyField(User)
	listener_groups = models.ManyToManyField(Group)


class Event_type_project(models.Model):
	title= models.CharField(max_length=100, null = True, blank = True)
	project = models.ForeignKey(Project)
	org = models.ForeignKey(Org)
	active = models.BooleanField(default=True)
	listeners = models.ManyToManyField(User)
	listener_groups = models.ManyToManyField(Group)


class Event(models.Model):
	event_type_project = models.ForeignKey(Event_type_project, null=True, blank=True)
	event_type_org = models.ForeignKey(Event_type_org, null=True, blank=True)
	created = models.DateTimeField(default=datetime.now, blank=True)
	issue = models.ForeignKey(Issue, related_name='events')
	actor = models.ForeignKey(User)
	action = models.CharField(max_length=100, null = True, blank = True)
	listeners = models.ManyToManyField(User, related_name='events')
	listener_groups = models.ManyToManyField(Group)
	org = models.ForeignKey(Org, related_name='events')




class CustomField(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	field_type = models.CharField(max_length=100, null = True, blank = True)
	screen = models.ForeignKey(Screen, related_name='custom_fields') #m2m ?
	title = models.CharField(max_length=100, null = True, blank = True)
	project = models.ForeignKey(Project)
	org = models.ForeignKey(Org)
	required = models.BooleanField(default=False)
	visible = models.BooleanField(default=True)
	text =  models.CharField(max_length=100, null = True, blank = True)

	def __str__(self):
		return self.title or ''

class Option(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	titile =  models.CharField(max_length=100, null = True, blank = True)
	value=  models.CharField(max_length=100, null = True, blank = True)
	default = models.BooleanField(default=False, blank=True)
	project = models.ForeignKey(Project)
	org = models.ForeignKey(Org)
	custom_field = models.ForeignKey(CustomField, null=True, related_name='options')

class CustomFieldValue(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	issue = models.ForeignKey(Issue, related_name='custom_field_values')
	custom_field = models.ForeignKey(CustomField, related_name='custom_field_value' )
	title = models.CharField(max_length=100, null = True, blank = True)
	val_char = models.CharField(max_length=100, null = True, blank = True)
	val_int = models.IntegerField(null=True, blank=True)
	val_boolean = models.BooleanField(default=False, blank=True)
	val_options = models.ManyToManyField(Option)


class FileAttachment(models.Model):
	issue= models.ForeignKey(Issue, related_name='file_attachments')
	file = models.FileField(null=True, blank=True, upload_to='attachments')
	mimetype = models.CharField(max_length=500, null = True, blank = True)
	filename = models.CharField(max_length=500, null = True, blank = True)
	created = models.DateTimeField(default=datetime.now, blank=True)
	filesize = models.IntegerField(null=True, blank=True)
	author = models.ForeignKey(UserProfile, null=True, blank=True)


# ? to keep or not 
class IssueAction(models.Model):
	issue = models.ForeignKey(Issue)
	author = models.ForeignKey(UserProfile)
	created = models.DateTimeField(default=datetime.now, blank=True)
	updated = models.DateTimeField(default=datetime.now, blank=True)
	actiontype = models.CharField(max_length=500, null = True, blank = True)
	screen = models.ForeignKey(Screen)



class Worklog(models.Model):
	issue = models.ForeignKey(Issue)
	author = models.ForeignKey(UserProfile)
	description = models.CharField(max_length=500, null = True, blank = True)
	time_Spent = models.TimeField()
	start_date = models.DateTimeField(default=datetime.now, blank=True)
	updated = models.DateTimeField(default=datetime.now, blank=True)




class Comment(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	content = models.CharField(max_length=500, null = True, blank = True)
	created =  models.DateTimeField(default=datetime.now, blank=True)
	commentor = models.ForeignKey(User)
	issue = models.ForeignKey(Issue, null=True)

	def __str__(self):
		return self.content













# Create your models here.
