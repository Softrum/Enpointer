from django.shortcuts import render

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
	return render(request, 'wiki/home.html', {'project':project, 'active':active, 'categories':categories})

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
	active = 'wiki_menu'

	return render(request, 'wiki/create.html', {'project':project, 'active':active})


def edit_page(request, uid_page):
	page = Page.objects.get(uid=uid_page)
	project = page.project
	active = 'wiki_menu'

	return render(request, 'wiki/edit.html', {'project':project, 'active':active, 'page':page})



def create_category(request, uid_project):
	project = Project.objects.get(uid=uid_project)
	c = Category.objects.create(project=project, title=request.POST['title'])
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



