from django.shortcuts import render

from dragonslayer.models import Project
from django.http import HttpResponse


def qa(request, uid_project):
	project = Project.objects.get(uid=uid_project)
	active = 'qa_menu'

	return render(request, 'qa/home.html', {'project':project, 'active':active})

# Create your views here.
