from django.shortcuts import render

from dragonslayer.models import Project
from django.http import HttpResponse
import requests
import json

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter


from django.utils.safestring import mark_safe

import ast
from django.http import JsonResponse


def source(request, uid_project):
	project = Project.objects.get(uid=uid_project)
	return render(request, 'coda/home.html', {'project':project})

def commits(request, uid_project):
	project = Project.objects.get(uid=uid_project)
	return render(request, 'coda/commits.html', {'project':project})

def branches(request, uid_project):
	project = Project.objects.get(uid=uid_project)
	return render(request, 'coda/branches.html', {'project':project})

def pull_requests(request, uid_project):
	project = Project.objects.get(uid=uid_project)
	return render(request, 'coda/pull-requests.html', {'project':project})