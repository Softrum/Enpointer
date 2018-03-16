from django.shortcuts import render

from dragonslayer.models import Project
from django.http import HttpResponse
import requests



# Create your views here.

def api(request, uid_project):
	#r = requests.get('https://dog.ceo/api/breeds/list')
	#print(r.status_code, r.reason, r.text)
	project = Project.objects.get(uid=uid_project)
	active = 'api_menu'

	return render(request, 'api/home.html', {'project':project, 'active':active})
