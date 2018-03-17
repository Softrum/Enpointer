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

	return render(request, 'api/requests.html', {'project':project, 'active':active})


def api_request(request):

	uid_project = request.POST['uid_project']

	request_type = request.POST['request_type']
	project = Project.objects.get(uid=uid_project)

	endpoint = request.POST['endpoint']

	

	if request_type == 'GET':
		r = requests.get(endpoint)
	    
	if request_type == 'POST':
		r = requests.post(endpoint)
		print('post')

	if request_type == 'PUT':
		r = requests.put(endpoint)

	if request_type == 'DELET':
		r = requests.delete(endpoint)

	if request_type == 'HEAD':
		r = requests.head(endpoint)

	if request_type == 'OPTIONS':
		r = requests.options(endpoint)

	active = 'api_menu'

	#print(r.status_code, r.reason, r.text)

	response = r.text
	status_code = r.status_code
	reason = r.reason
	headers = r.headers
	cookies = r.cookies

	return render(request, 'api/requests.html', {'cookies':cookies, 'headers':headers, 'project':project, 'active':active, 'response':response, 'status_code':status_code, 'reason':reason})
