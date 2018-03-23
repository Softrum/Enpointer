from django.shortcuts import render, redirect

from dragonslayer.models import Project
from django.http import HttpResponse
import requests
import json

from .models import Category, Page, Version, History

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter


from django.utils.safestring import mark_safe

import ast
from django.http import HttpResponseRedirect
from django.http import JsonResponse


def home(request, uid_project):
	project = Project.objects.get(uid=uid_project)
	active = 'wiki_menu'
	pages_count = project.pages.all().count()
	categories = Category.objects.filter(project=project)
	other_pages = Page.objects.filter(project=project).filter(category=None).filter(published=True)
	drafts =  Page.objects.filter(project=project).filter(published=False)
	return render(request, 'wiki/home.html', {'project':project, 'active':active, 'categories':categories, 'other_pages':other_pages, 'pages_count':pages_count, 'drafts':drafts})

def page(request, uid_page):
	page = Page.objects.get(uid=uid_page)
	project = page.project
	active = 'wiki_menu'
	other_pages = Page.objects.filter(project=project).filter(category=None).filter(published=True)
	return render(request, 'wiki/page.html', {'project':project, 'active':active, 'page':page, 'other_pages':other_pages})


def page_history(request, uid_page):
	page = Page.objects.get(uid=uid_page)
	project = page.project
	active = 'wiki_menu'
	return render(request, 'wiki/page_history.html', {'project':project, 'active':active, 'page':page})


def create_page(request, uid_project):

	project = Project.objects.get(uid=uid_project)
	version = Version.objects.create(author=request.user)
	page = Page.objects.create(project=project,author=request.user, current_version=version)
	page.versions.add(version)
	page.save()
	history = History.objects.create(page=page, project=project, message='created new page', version=version)
	print('new page and version is created')
	active = 'wiki_menu'

	return render(request, 'wiki/create.html', {'project':project, 'active':active, 'page':page})


def edit_page(request, uid_page):
	page = Page.objects.get(uid=uid_page)
	project = page.project
	active = 'wiki_menu'
	version = page.current_version

	return render(request, 'wiki/edit.html', {'project':project, 'active':active, 'page':page, 'version':version})

def save_version(request, uid_page):
	page = Page.objects.get(uid=uid_page)	
	title = request.POST['title']
	content = request.POST['content']
	page.category = Category.objects.get(uid=request.POST['category_uid'])
	version = Version.objects.create(title=title, content=content, author=request.user)
	page.versions.add(version)
	page.save()
	return redirect('/wiki/page/versions/'+uid_page)



def draft(request, uid_page):
	page = Page.objects.get(uid=uid_page)
	project=page.project
	drafts = Page.objects.filter(project=project).filter(published=False)
	active = 'wiki_menu'
	return render(request, 'wiki/draft.html', {'active':active, 'project':project, 'drafts':drafts, 'page':page})



def commit_changes(request, uid_page):
	page = Page.objects.get(uid=uid_page)	
	title = request.POST['title']
	content = request.POST['content']
	page.category = Category.objects.get(uid=request.POST['category_uid'])
	version = Version.objects.create(title=title, content=content, author=request.user)
	page.versions.add(version)
	page.current_version = version
	history = History.objects.create(page=page, project=page.project, version=version, message='new commit added')
	page.save()
	return redirect('/wiki/page/'+ uid_page)


def delete_page(request, uid_page):
	page = Page.objects.get(uid=uid_page)
	uid_project = str(page.project.uid)
	project = page.project
	page.delete()
	#uid_draft =  Page.objects.filter(project=project).filter(published=False)[0].uid
	return redirect('/wiki/home/'+ uid_project)
	#return redirect('/wiki/home/'+uid_project)

def versions(request, uid_page):
	page = Page.objects.get(uid=uid_page)
	return render(request, 'wiki/versions.html', {'page':page})


def version(request, uid_version):
	version = Version.objects.get(uid=uid_version)
	page = version.version_page.all()[0]
	project = page.project
	active = 'wiki_menu'
	return render(request, 'wiki/version.html', {'active':active, 'version':version, 'project':project, 'page':page})


def history(request, uid_history):
	history = History.objects.get(uid=uid_history)
	page = history.page
	project = history.project
	active = 'wiki_menu'
	return render(request, 'wiki/history.html', {'project':project, 'active':active, 'page':page, 'project':project, 'history':history})



def create_category(request, uid_project):
	project = Project.objects.get(uid=uid_project)
	c = Category.objects.create(project=project, title=request.POST['title'])
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def publish(request, uid_page):
	page = Page.objects.get(uid=uid_page)
	page.published=True
	page.current_version.title = request.POST['title']
	page.current_version.content = request.POST['content']
	uid_category = request.POST.get('category_uid')
	if uid_category != "asdasd":
		page.category = Category.objects.get(uid=uid_category)

	
	print('page is published')
	print(page.current_version.title)

	page.save()
	page.current_version.save()
	return HttpResponse('done')



