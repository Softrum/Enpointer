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


def home(request, uid_project):
	project = Project.objects.get(uid=uid_project)
	return render(request, 'coda/home.html', {'project':project})