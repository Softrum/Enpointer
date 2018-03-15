from django.shortcuts import render

from dragonslayer.models import Project
from django.http import HttpResponse


def qa(request, uid_project):
	project = Project.objects.get(uid=uid_project)

	return HttpResponse('hi new architecture')

# Create your views here.
