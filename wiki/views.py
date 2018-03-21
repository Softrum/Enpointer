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
	categories = Category.objects.filter(project=project)
	other_pages = Page.objects.filter(project=project).filter(category=None).filter(published=True)
	return render(request, 'wiki/home.html', {'project':project, 'active':active, 'categories':categories, 'other_pages':other_pages})

def page(request, uid_page):
	page = Page.objects.get(uid=uid_page)
	project = page.project
	active = 'wiki_menu'
	return render(request, 'wiki/page.html', {'project':project, 'active':active, 'page':page})


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

	return render(request, 'wiki/edit.html', {'project':project, 'active':active, 'page':page})


def delete_page(request, uid_page):
	page = Page.objects.get(uid=uid_page)
	uid_project = str(page.project.uid)
	page.delete()
	return redirect('/wiki/home/'+uid_project)



def create_category(request, uid_project):
	project = Project.objects.get(uid=uid_project)
	c = Category.objects.create(project=project, title=request.POST['title'])
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def publish(request, uid_page):
	page = Page.objects.get(uid=uid_page)
	page.published=True
	page.current_version.title = request.POST['title']
	page.current_version.content = request.POST['content']
	page.category = Category.objects.get(uid=request.POST['category_uid'])
	print('page is published')
	print(page.current_version.title)

	page.save()
	page.current_version.save()
	return HttpResponse('done')



