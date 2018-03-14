from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,  login 
from django.contrib.auth import logout
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Label, Blog, Password_change_request, Invite_user_request,  UserProfile,Swimlane,Task, Layout, Col_layout,  FileAttachment, CustomFieldValue,Event, Event_type_project, CustomField, Project_role,Screen, Project,Priority, Issue,Version,Workflow, Comment, Section, Org, Status, Backlog, Sprint, Transition, Column, IssueType, ProjectPermission, FieldConfig
from django.http import HttpResponseRedirect
from datetime import date, timedelta, datetime
from django.db.models import Q
from django.contrib import messages
import os.path
import uuid
import pytz
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password


from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives


from django.utils import timezone
now = timezone.now()
from django.conf import settings

import os




x ='testing123'

col_layout = """

<!-- column add column class and add column uid in column id and hide the edit buttons for starting -->



<div id=\""""+x+"""_0_1" class="block column" style="height: 92%; overflow-y: scroll; display: inline-block;margin-right: 10px;  width:360px" >





<!-- column header -->

<div contenteditable="true" class="well well-sm " align="center" style="margin: 0px 0px 0px 0px; height: 30px; font-weight: 150%; font-size: 110%;padding-top:5px;" >
<span data-toggle="tooltip" title="Move Column To Left" style="color:grey; display:none" onclick="move_left($(this))" class="edit_button glyphicon glyphicon-arrow-left pull-left"></span>Column_text

<span onclick="delete_column($(this))" data-toggle="tooltip" title="Delete Column"  style="color:grey; opacity: 0.5; display:none" class="edit_button glyphicon glyphicon-remove-circle"></span>
<span data-toggle="tooltip" title="Move Column To Right" style="color:grey; display:none" onclick="move_right($(this))" class=" edit_button glyphicon glyphicon-arrow-right pull-right"></span>



</div>


<!-- column header ends -->


<!-- block -->


<div id=\""""+x+"""_1_1" class="block connectedSortable" style="background-color: #f1f1f2; min-width: 360px; min-height: 250px; display: inline-block; vertical-align: top ;    -webkit-box-shadow:inset 0px 0px 0px 1px white;
	-moz-box-shadow:inset 0px 0px 0px 1px white;
	box-shadow:inset 0px 0px 0px 1px white; overflow-y: auto;  width:360px "  >


<!-- block  header -->

<div id="status_uid"  class="well well-sm " align="center" style="margin: 0px 0px 0px 0px; height: 30px; font-weight: 150%; font-size: 110%;padding-top:5px;  " >

<span class="block_title"  contenteditable="true"> Block_text</span>

 <a id="1" class="edit_button number_of_issues_in_row"  data-toggle="tooltip" title="Number of Issues in row"   style="cursor: pointer; color: grey; display: none" onclick="set_issues_in_row($(this) )" >N</a> 

 <a class="get_block_issues_button"  data-toggle="tooltip" title="Set number of issues in a row"   style="cursor: pointer; color: grey; display: none" onclick="get_block_issues($(this).parent() )" >i</a> 

 <a class="edit_button" data-toggle="tooltip" title="Split Vertically"   style="cursor: pointer; color: grey; display: none" onclick="split_vertically($(this).parent().parent())" >||</a> 

 <a class="edit_button" data-toggle="tooltip" title="Status for this block"   style="cursor: pointer; color: grey; display: none" onclick="set_block_status($(this).parent() )" >s</a> 


<a class="edit_button" data-toggle="tooltip" title="Split Horizontally"  style="cursor: pointer; color: grey; display: none" onclick="split_horizontally($(this).parent().parent())" >==</a> 



<a class="edit_button" data-toggle="tooltip" title="Increase Number of Last Split"  class="plus" style="cursor: pointer; color: grey; display: none" onclick="add_node($(this).parent().parent())" >+</a>


<a class="edit_button" data-toggle="tooltip" title="Increase With of Column"  class="plus" style="cursor: pointer; color: grey; display: none" onclick="increase_width($(this).parent().parent())" >W</a>

<a class="edit_button" data-toggle="tooltip" title="Delete"  class="pull-right" style="color: grey; opacity: 0.5; display: none" onclick="delete_node($(this).parent().parent())" style="margin-right: 0px;"><i class="glyphicon glyphicon-remove-circle"></i></a>


<a class="edit_button" data-toggle="tooltip" title="Auto Adjust Width"   style="color: grey; opacity: 0.5; display: none" onclick="adjust_width($(this).parent().parent())" style="margin-right: 0px;"><i class="glyphicon glyphicon-refresh"></i></a>

<a class="edit_button" data-toggle="tooltip" title="Hide This Panel Bar"  class="pull-right" style="color: grey; opacity: 0.5; display: none" onclick="hide_panel(this)" style="margin-right: 0px;"><i class="glyphicon glyphicon-eye-close"></i></a>



</div>

<!-- block header -->


</div>  <!-- for block -->




</div>   <!-- for column -->

"""






def register_event(request, uid_project, event_type_title, uid_issue):
	event_type = Event_type_project.objects.filter(title=event_type_title).filter(project=Project.objects.get(uid=uid_project))[0]
	issue = Issue.objects.get(uid=uid_issue)
	event = Event.objects.create(event_type_project=event_type, issue=issue, actor=request.user, action=event_type_title, org=get_org(request))
	event.listeners.add(*event_type.listeners.all())
	event.listener_groups.add(*event_type.listener_groups.all())
	event.save()
	print(event.action)

def release_detail(request, uid_release):
	release = Version.objects.get(uid=uid_release)
	project = release.project
	resolved_issues = Issue.objects.filter(fix_version=release).filter(resolved=True)
	remaining_issues = Issue.objects.filter(fix_version=release).filter(resolved=False)
	active = 'releases_menu'
	return render(request, 'release_detail.html', {'active':active, 'release':release, 'project':project, 'resolved_issues':resolved_issues, 'remaining_issues':remaining_issues})
"""
def services(request):
	return render(request, 'website/services.html')"""

def services_enquiry(request):
	name = request.POST['name']
	email = request.POST['email']
	requirement = request.POST['requirement']
	message = name+','+email+','+requirement
	send_mail('New Services Request', message , 'Enpointer', ['ishaan@enpointer.com']) 


	return redirect('/')

def support(request, slug):
	if slug == 'home':
		return render(request, 'support/home.html')
	if slug == '8200':
		from pygit2 import clone_repository
		repo_url = 'git://github.com/libgit2/pygit2.git'
		repo_path = '/users/ishaanbhola/genius'
		repo = clone_repository(repo_url, repo_path)
		return HttpResponse('cloned')



def knowledge(request, slug):
	if slug == 'home':
		return render(request, 'knowledge/home.html')


def why(request):
	return render(request, 'website/why.html')

def sitemap(request):
	k = os.path.join(os.path.dirname(os.path.dirname(__file__)),'media/sitemap.xml')
	p = open(k).read()
	return HttpResponse(p, content_type='text/xml')


def design_philosophy(request):
	return render(request, 'website/design_philosophy.html')

def product_philosophy(request):
	return render(request, 'website/product_philosophy.html')

def company_principles(request):
	return render(request, 'website/company_principles.html')

def blog(request):
	blogs = Blog.objects.all()
	return render(request, 'blog/blog_list.html', {'blogs':blogs})

def blog_detail(request, slug):
	blog= Blog.objects.get(slug=slug)
	return render(request, 'blog/blog_detail.html', {'blog':blog})	

def features(request):

	return render(request, 'website/features.html')

def pricing(request):
	return render(request, 'website/pricing.html')

def security(request):
	return render(request, 'website/security.html')


def about(request):
	return render(request, 'website/about.html')

def case_studies(request):
	return render(request, 'website/case_studies.html')

def privacy_policy(request):
	return render(request, 'website/privacy_policy.html')

def use_cases(request, use_type):
	if use_type == 'all':
		return render(request, 'website/use_cases/use_cases.html')
	if use_type == 'agile_development':
		return render(request, 'website/use_cases/agile_development.html')


def terms_of_use(request):
	return render(request, 'website/terms_of_use.html')


def invite_user(request):
	org = get_org(request)
	email = request.POST['email']
	guid = uuid.uuid4()
	guid = str(uuid.uuid4())
	hash_id = hash(guid)
	Invite_user_request.objects.create(org = org, hash_id=hash_id, email=email )


	if request.get_host() == '127.0.0.1:8000':
		message = 'http://127.0.0.1:8000/invited_user_page/'+ guid
	else:
		message = 'http://www.enpointer.com/invited_user_page/'+ guid

	send_mail('Enpointer Invite User', message , 'Enpointer', [email])

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def invited_user_page(request, guid):
	hash_id = hash(guid)
	if Invite_user_request.objects.filter(hash_id=hash_id).exists():
		i = Invite_user_request.objects.get(hash_id=hash_id).org
		return render(request, 'invited_user_page.html' , {'org':i })
	else:
		return HttpResponse('Error 404')

def invited_user_signup(request):
	user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
	org = Org.objects.get(uid=request.POST['uid_org'])
	profile = UserProfile.objects.create(user = user, org=org)
	login(request, user)
	return redirect('/')
	#create usr with email as email and password as password and orh as org
	#redirect him to the dashboard home


def send_reset_password_link(request):
	username = request.POST['username']
	if User.objects.filter(username=username).exists():
		user = User.objects.get(username=username)
		guid = uuid.uuid4()
		guid = str(uuid.uuid4())

		hash_id = hash(guid) #improve the type of hash .. use argon hash maybe ?
		print(guid)
		print(hash_id)
		pass_request = Password_change_request.objects.create(user=user, hash_id=hash_id )
		if request.get_host() == '127.0.0.1:8000':
			message = 'http://127.0.0.1:8000/reset_password_page/'+ guid 
		else:
			message = 'http://www.enpointer.com/reset_password_page/'+ guid 


		send_mail('Enpointer Password Reset', message , 'Enpointer', [username])
		
		return render(request, 'website/password_reset_email_sent.html')
	else:
		return redirect('/forgot_password/')



def reset_password_page(request, guid):
	print(guid)
	hash_id = hash(guid)
	print(hash_id)
	
	if Password_change_request.objects.filter(hash_id=hash_id).exists(): #add a 24 hr time check as well
		user = Password_change_request.objects.get(hash_id = hash_id).user
		return render(request, 'website/reset_password.html', {'user':user})
	else:
		return HttpResponse('Error 404')



def reset_password(request):
	u = User.objects.get(username=request.POST['username'])
	u.set_password(request.POST['password'])
	u.save()
	return redirect('/login')



	
def edit_layout(request, uid_project):
	



	
	project = Project.objects.get(uid=uid_project)
	columns = Column.objects.filter(project=project)
	status = Status.objects.filter(project=project)
	"""
			x = ''
			for s in status:
				x += ('#'+str(s.uid)+',')

			index = len(x)
			x = x[:index-1]
			x = '"{}"'.format(x)
			print(x)
			#newstr = oldstr.replace("M", "")


			y = {}

			

			for s in status:
				issues_in_status = Issue.objects.filter(status=s).filter(sprint=current_sprint)
				key = s.title
				key = key.replace(" ", "")
				print(key)
				y[key] = issues_in_status
			print(y)
	"""

			#calculate column widths 
	board_layout = project.board_layout
	for c in columns:
		c.wid = 0
		for f in c.col_layout.all():
			if f.layout_type == 'vertical':
				c.wid = c.wid + 380*f.sections
				c.save()
				print('col_saved')
				print('helooooooooooooooo')


			#end csalculatung column widths 

			#layout = Layout.objects.filter(project=project).filter(root=True)[0]

	col_layouts = Col_layout.objects.filter(project=project).filter(parent=None)
	versions = Version.objects.filter(project=project)
	#issue_type_epic = IssueType.objects.filter(project=project).filter(title='epic')[0]
			
	#epics = Issue.objects.filter(project=project).filter(issue_type=issue_type_epic)	
	labels = Label.objects.filter(project=project)	
	active ='board_menu'	


	statuss = Status.objects.filter(project=project)
	workflows = Workflow.objects.filter(project=project)
			

	z = {'workflows':workflows, 'statuss':statuss, 'active':active, 'labels':labels,  'versions':versions, 'col_layouts':col_layouts, 'board_layout':board_layout, 'status':status, 'project':project,  'columns':columns}

	

			

			#what about distribution of issues in same status boxes. restriction could be this, thar one status, one box 


	

	return render(request, 'test8.html', z )
	

def default_settings(request, uid_project):
	#create default status types
	#create feault columns
	#create default workflow
	#create default transitions
	#create default issue_types
	#create default priority 
	#create default permissions 
	#create default backlog if required 
	#create default screens 
	return True 

def update_col_layout(request, uid_col):
	col = Column.objects.get(uid=uid_col)
	col.layout = request.POST['x']
	col.save()
	return HttpResponse('done')


def show_screen(request, uid_project, uid_screen):
	return True

def screen_settings(request, uid_project):
	issuetypes = IssueType.objects.filter(project=Project.objects.get(uid=uid_project))
	print(issuetypes)
	return render(request, 'screen_settings.html' , {'issuetypes':issuetypes})


def test(request):
	return HttpResponse('All tests passed. Ready to ship')


def swimlane(request, crud, uid_project):
	if crud == 'create':
		Swimlane.objects.create(title = request.POST['title'], project=Project.objects.get(uid=uid_project), org=get_org(request) )
		print('swimlane created')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def get_org(request):
	org = UserProfile.objects.get(user=request.user).org
	return org 


def create_custom_field(request,uid_project, uid_screen):
	project = Project.objects.get(uid=uid_project)
	title = request.POST['title']
	screen = Screen.objects.get(uid=uid_screen)
	field_type = request.POST['field_type']
	CustomField.objects.create(project=project, org=get_org(request), title=title, screen=screen, field_type=field_type)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def create_screen(request, uid_project):
	project=Project.objects.get(uid=uid_project)
	s = Screen.objects.create(title=request.POST['title'], project=Project.objects.get(uid=uid_project), org=get_org(request))
	FieldConfig.objects.create(project=project,screen=s, org=get_org(request))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

def issuetype(request,crud,  uid_project, uid_issuetype):
	if crud == 'create':
		IssueType.objects.create(icon=request.FILES['icon'],title = request.POST['title'], description = request.POST['description'], project=Project.objects.get(uid=request.POST['project']), org=get_org(request), workflow=Workflow.objects.get(uid=request.POST['workflow']),create_screen=Screen.objects.get(uid=request.POST['create_screen']), edit_screen=Screen.objects.get(uid=request.POST['edit_screen']),  view_screen=Screen.objects.get(uid=request.POST['view_screen']))
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	if crud == 'delete':
		i = IssueType.objects.get(uid=uid_issuetype)
		i.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def project_settings_normal(request, setting_type, uid_project):

	if setting_type == 'issuetype':
		project = Project.objects.get(uid=uid_project)
		issuetypes = IssueType.objects.filter(project=project)
		return render(request, 'project_settings_normal/project_settings_issuetype.html', {'project':project, 'issuetypes':issuetypes})
	if setting_type == 'workflow':

		project = Project.objects.get(uid=uid_project)
		statuss = Status.objects.filter(project=project)
		workflows = Workflow.objects.filter(project=project)
		return render(request, 'project_settings_normal/project_settings_workflow.html',  {'project':project, 'workflows':workflows, 'statuss':statuss})
	

	if setting_type == 'screen_detail' :
		uid_project, uid_screen = uid_project[:36], uid_project[36:]


		project = Project.objects.get(uid=uid_project)
		screen = Screen.objects.get(uid=uid_screen)
		custom_fields = CustomField.objects.filter(screen = screen)
		return render(request, 'project_settings_normal/project_settings_screen_detail.html', {'project':project, 'screen':screen, 'custom_fields':custom_fields})


	if setting_type == 'screen':

		project = Project.objects.get(uid=uid_project)
		screens= Screen.objects.filter(project=project)
		return render(request, 'project_settings_normal/project_settings_screen.html', {'project':project, 'screens':screens})
	
	if setting_type == 'columns_status':
		project = Project.objects.get(uid=uid_project)
		columns = Column.objects.filter(project=project)
		status = Status.objects.filter(project=project)
		return render(request, 'project_settings_normal/project_settings_columns_status.html', {'project':project, 'columns':columns})
	
	if setting_type == 'permissions':
		project = Project.objects.get(uid=uid_project)
		users = UserProfile.objects.filter(org=get_org(request))
		return render(request, 'project_settings_normal/project_settings_permissions.html', {'project':project, 'users':users})
	
	if setting_type == 'priority':
		project = Project.objects.get(uid=uid_project)
		prioritys = Priority.objects.filter(project=project)
		return render(request, 'project_settings_normal/project_settings_priority.html', {'project':project, 'prioritys':prioritys})
	
	if setting_type == 'field':
		project = Project.objects.get(uid=uid_project)
		custom_fields = CustomField.objects.filter(project=project)
		return render(request, 'project_settings_normal/project_settings_customfields.html', {'project':project, 'custom_fields':custom_fields})

	if setting_type == 'components':
		project = Project.objects.get(uid=uid_project)
		return render(request, 'project_settings_normal/project_settings_components.html', {'project':project})

	if setting_type == 'swimlane':
		project = Project.objects.get(uid=uid_project)
		return render(request, 'project_settings_normal/project_settings_swimlane.html', {'project':project})
	if setting_type == 'general':
		project = Project.objects.get(uid=uid_project)
		
		return render(request, 'project_settings_normal/project_settings_general.html', {'project':project})    



def update_issue_description(request, uid_project, uid_issue):
	project = Project.objects.get(uid=uid_project)
	issue = Issue.objects.get(uid=uid_issue)
	issue.description = request.POST['description']
	issue.save()
	return HttpResponse('done babes')



def project_settings(request, setting_type, uid_project):
	active = 'project_settings_menu'
	
	if setting_type == 'issuetype':
		project = Project.objects.get(uid=uid_project)
		issuetypes = IssueType.objects.filter(project=project)
		active2 = 'issue_type_settings'
		return render(request, 'project_settings_issuetype.html', {'active2':active2,'active':active, 'project':project, 'issuetypes':issuetypes})
	if setting_type == 'workflow':

		project = Project.objects.get(uid=uid_project)
		statuss = Status.objects.filter(project=project)
		workflows = Workflow.objects.filter(project=project)
		active2 = 'workflow_settings'
		return render(request, 'project_settings_workflow.html',  {'active2':active2, 'active':active,'project':project, 'workflows':workflows, 'statuss':statuss})
	


	if setting_type == 'screen_detail' :
		uid_project, uid_screen = uid_project[:36], uid_project[36:]


		project = Project.objects.get(uid=uid_project)
		screen = Screen.objects.get(uid=uid_screen)
		custom_fields = CustomField.objects.filter(screen = screen)
		active2 = 'screen_settings'
		return render(request, 'project_settings_screen_detail.html', {'active2':active2,'active':active,'project':project, 'screen':screen, 'custom_fields':custom_fields})


	if setting_type == 'screen':

		project = Project.objects.get(uid=uid_project)
		screens= Screen.objects.filter(project=project)
		active2 = 'screen_settings'
		return render(request, 'project_settings_screen.html', {'active2':active2,'active':active,'project':project, 'screens':screens})
	
	if setting_type == 'columns':
		project = Project.objects.get(uid=uid_project)
		columns = Column.objects.filter(project=project)
		statuss = Status.objects.filter(project=project)
		workflows = Workflow.objects.filter(project=project)
		active2 ='columns_settings'
		return render(request, 'project_settings_columns.html', {'active2':active2,'active':active,'project':project, 'columns':columns, 'statuss':statuss, 'workflows':workflows})
	

	if setting_type == 'status':
		project = Project.objects.get(uid=uid_project)
		columns = Column.objects.filter(project=project)
		statuss = Status.objects.filter(project=project)
		workflows = Workflow.objects.filter(project=project)
		active2 ='status_settings'
		return render(request, 'project_settings_status.html', {'active2':active2,'active':active,'project':project, 'columns':columns, 'statuss':statuss, 'workflows':workflows})
	
	if setting_type == 'permissions':
		project = Project.objects.get(uid=uid_project)
		users = UserProfile.objects.filter(org=get_org(request))
		active2 = 'permission_settings'
		return render(request, 'project_settings_permissions.html', {'active2':active2,'active':active,'project':project, 'users':users})
	
	if setting_type == 'priority':
		project = Project.objects.get(uid=uid_project)
		prioritys = Priority.objects.filter(project=project)
		active2 = 'priority_settings'
		return render(request, 'project_settings_priority.html', {'active2':active2,'active':active,'project':project, 'prioritys':prioritys})
	
	if setting_type == 'field':
		project = Project.objects.get(uid=uid_project)
		custom_fields = CustomField.objects.filter(project=project)
		active2 = 'custom_field_settings'
		return render(request, 'project_settings_customfields.html', {'active2':active2,'active':active,'project':project, 'custom_fields':custom_fields})

	if setting_type == 'components':
		project = Project.objects.get(uid=uid_project)
		active2 = 'components_settings'
		return render(request, 'project_settings_components.html', {'active2':active2, 'active':active,'project':project})

	if setting_type == 'swimlane':
		project = Project.objects.get(uid=uid_project)

		return render(request, 'project_settings_swimlane.html', {'active2':active2, 'active':active,'project':project})

	if setting_type == 'users':
		project = Project.objects.get(uid=uid_project)
		active2 = 'users_settings'
		org = get_org(request)
		iv = Invite_user_request.objects.filter(org=org)
		return render(request, 'project_settings_users.html', {'iv':iv,'active2':active2, 'active':active,'project':project, 'org':org})

	if setting_type == 'general':
		project = Project.objects.get(uid=uid_project)
		active2 = 'general_settings'
		org = get_org(request)
		
		
		return render(request, 'project_settings_general.html', { 'org':org, 'active2':active2, 'active':active,'project':project})    

def set_issue_bg(request, uid_issue):

	issue=Issue.objects.get(uid=uid_issue)
	issue.bg = request.POST['url2']
	issue.save()
	return HttpResponse('success')

def home(request):
	profile = UserProfile.objects.get(user=request.user)
	org = profile.org
	projects = Project.objects.filter(org=org)
	sections = Section.objects.filter(org=org)
	return render(request, 'home.html', {'profile':profile, 'projects':projects, 'sections':sections})

def find_current_sprint(uid):
	project = Project.objects.get(uid=uid)
	date_today = date.today()
	print(date_today)
	sprints = Sprint.objects.filter(project=project)
	for s in sprints:
		if s.start_date is not None and s.end_date is not None:
			if s.start_date <= date_today and date_today <= s.end_date:
				return s

def profile(request):
	return render(request,'profile.html')

def upload_attachment(request, uid_issue):
	issue = Issue.objects.get(uid=uid_issue)
	file = FileAttachment.objects.create(issue=issue, file = request.FILES["myfile"])
	file.filename =  os.path.basename(file.file.url)
	file.save()
	url = file.file.url

	if url.lower().endswith(('.png', '.jpg', '.jpeg')):
		file.mimetype = 'image'
	else:
		file.mimetype ='notimage'
	file.save()


	return HttpResponse(file.file.url)


def increase_column_order(request, col_uid):
	col = Column.objects.get(uid=col_uid)
	col.order = col.order+1
	col.save()
	return HttpResponse('done')

def decrease_column_order(request, col_uid):
	col = Column.objects.get(uid=col_uid)
	col.order = col.order-1
	col.save()
	return HttpResponse('done')


def create_task(request, uid_project, uid_issue):
	t= Task.objects.create(issue=Issue.objects.get(uid=uid_issue),project=Project.objects.get(uid=uid_project), title=request.POST['title'], created_by=request.user)
	return HttpResponse(t.uid)

def settings(request):
	return render(request, 'settings.html')


#username is basically userporfile's uid 

def assign_user(request, uid_issue, username):
	issue = Issue.objects.get(uid=uid_issue)
	userprofile = UserProfile.objects.get(uid=username)
	user = userprofile.user
	issue.assigned_to = user
	issue.save()
	return HttpResponse('success')

def add_due_date(request, uid_issue, date):
	issue = Issue.objects.get(uid=uid_issue)
	issue.due_date = date
	issue.save()
	print('ok')
	return HttpResponse('success')



def updates(request):
	return render(request, 'website/updates.html')


def create_issue_types(request, project):
	org = get_org(request)
	IssueType.objects.create(title='story', project=project, org=org, icon='issue_type_icons/story.png')
	IssueType.objects.create(title='bug', project=project, org=org, icon='issue_type_icons/bug.png')
	IssueType.objects.create(title='task', project=project, org=org, icon='issue_type_icons/task.png')
	#IssueType.objects.create(title='epic', project=project, org=org)

def create_default_prioritys(request, project):
	org = get_org(request)
	Priority.objects.create(title='high',org=org, project=project, color='#D32F2F')
	Priority.objects.create(title='mid',org=org, project=project, color='#FFC107')
	Priority.objects.create(title='low',org=org, project=project, color='#8BC34A')


def create_default_project_roles(request, project):
	org = get_org(request)
	p1= Project_role.objects.create(title='admin',org=org)


	p2= Project_role.objects.create(title='developer',org=org)
	project.project_roles.add(p1,p2)
	project.save()


def create_default_permissions(request, project):
	p1=ProjectPermission.objects.create(title='can_transition', org=get_org(request))
	p2=ProjectPermission.objects.create(title='can_resolve', org=get_org(request))
	p3=ProjectPermission.objects.create(title='can_create_issue', org=get_org(request))
	project.project_permissions.add(p1,p2,p3)
	project.save()
	# assign permissions to project roles
	admin = project.project_roles.filter(title='admin')[0]
	admin.project_permissions.add(p1,p2,p3)
	admin.save()

	developer = project.project_roles.filter(title='developer')[0]
	developer.project_permissions.add(p1)
	developer.save()



def link_issue_types_with_workflow(project):
	w = Workflow.objects.get(project=project, title='default')
	issue_types = IssueType.objects.filter(project=project)
	for i in issue_types:
		i.workflow = w
		i.save()


def link_issue_types_with_screens(project):
	screen = Screen.objects.get(project=project, title='default')
	print(screen.title)
	issue_types = IssueType.objects.filter(project=project)
	print('linking')
	for i in issue_types:
		i.create_screen = screen
		i.edit_screen = screen
		i.view_screen = screen 
		i.save()
		print(i.title)

def create_default_screens(request, project):   #this function creates screens and corresponding fieldconfigs 
	s1 = Screen.objects.create(title='default', project=project, org=get_org(request))
	FieldConfig.objects.create(screen=s1, project=project, org=get_org(request))
	s2 = Screen.objects.create(title='resolve issue screen', project=project, org=get_org(request))
	FieldConfig.objects.create(screen=s2, project=project, org=get_org(request))     
	s3 = Screen.objects.create(title='workflow', project=project, org=get_org(request))
	FieldConfig.objects.create(screen=s3, project=project, org=get_org(request))
	link_issue_types_with_screens(project)
	#rdfd



def create_default_status_columns(request, project):
	c1 = Column.objects.create(title='Open', project=project, org=get_org(request), order=1)
	c2 = Column.objects.create(title='In Progress', project=project, org=get_org(request), order=2)
	c3 = Column.objects.create(title='Resolved', project=project, org=get_org(request), order=3)

	





			
	s1= Status.objects.create(title='Open',project=project, org=get_org(request))
	s2 = Status.objects.create(title='In Progress',project=project, org=get_org(request))
	s3 = Status.objects.create(title='Resolved',project=project, org=get_org(request), resolution=True)
	
	c1.layout = col_layout.replace("testing123", str(c1.uid))
	c1.layout = c1.layout.replace("status_uid", str(s1.uid))
	c1.layout = c1.layout.replace("Column_text", 'Open Column')
	c1.layout = c1.layout.replace("Block_text", 'Open Block')
	c1.save()

	c2.layout = col_layout.replace("testing123", str(c2.uid))
	c2.layout = c2.layout.replace("status_uid", str(s2.uid))
	c2.layout = c2.layout.replace("Column_text", 'In Progress Column')
	c2.layout = c2.layout.replace("Block_text", 'In Progress Block')
	c2.save()

	c3.layout = col_layout.replace("testing123", str(c3.uid))
	c3.layout = c3.layout.replace("status_uid", str(s3.uid))
	c3.layout = c3.layout.replace("Column_text", 'Resolved Column')
	c3.layout = c3.layout.replace("Block_text", 'Resolved Block')
	c3.save()

	sortable_list_ids = '"'+'#'+str(c1.uid)+'_1_1,' + '#'+str(c2.uid) +'_1_1,'+'#'+str(c3.uid)+'_1_1' +'"'
	project.sortable_list_ids = sortable_list_ids
	print('here comes tthe  stuff')
	print(sortable_list_ids)
	project.save()


	col1 = Col_layout.objects.create(title="root", project=project, layout_type="vertical", sections=1, column=c1)
	col1_child = Col_layout.objects.create(title="root_child",parent=col1, project=project, layout_type="none", sections=0, status=s1)

	col2 = Col_layout.objects.create(title="root2", project=project, layout_type="vertical", sections=1, column=c2)
	col2_child = Col_layout.objects.create(title="root_child2",parent=col2, project=project, layout_type="none", sections=0, status=s2)

	col3 = Col_layout.objects.create(title="root3", project=project, layout_type="vertical", sections=1, column=c3)
	col3_child = Col_layout.objects.create(title="root3_child",parent=col3, project=project, layout_type="none", sections=0, status=s3)

def create_default_event_types(request, project):
	Event_type_project.objects.create(title='issue_created', project=project, org=get_org(request))
	Event_type_project.objects.create(title='issue_updated', project=project, org=get_org(request))

def create_default_workflow(request, project):
	w= Workflow.objects.create(title='default',project=project, org=get_org(request))
	s1 = Status.objects.get(project=project, title='Open')
	s2 = Status.objects.get(project=project, title='In Progress')
	s3 = Status.objects.get(project=project, title='Resolved')
	Transition.objects.create(project=project, org=get_org(request), workflow=w, start_status=s1, end_status=s2, title='In Progress' )
	Transition.objects.create(project=project, org=get_org(request), workflow=w, start_status=s2, end_status=s3, title='Resolve' )
	Transition.objects.create(project=project, org=get_org(request), workflow=w, start_status=s3, end_status=s1, title='Reopen' )
	link_issue_types_with_workflow(project)



#def create_default_workflow(request, project):
	#dfsdfs

def forgot_password(request):
	return render(request, 'forgot_password.html')







def quick_create_issue_plan(request, uid):
	uid = uuid.UUID(uid).hex

	if Backlog.objects.filter(uid=uid).exists():
		backlog = Backlog.objects.get(uid=uid)
		sprint = None
		project = backlog.project
	else:
		backlog = None
		sprint = Sprint.objects.get(uid=uid)
		project = sprint.project


	issue = Issue.objects.create(title=request.POST['title'], project=project, org=get_org(request), sprint=sprint, backlog=backlog, points=request.POST['points'] )
	issue.issue_id = create_issue_id(request, project)
	issue.status = Status.objects.filter(project=project)[0]
	issue.created_by = request.user
	issue.issue_type = IssueType.objects.get(uid=request.POST['issuetype'])
	print('issue_type' + issue.issue_type.title)
	screen = issue.issue_type.create_screen
	issue.priority = Priority.objects.get(uid=request.POST['priority'])
	issue.save()

	





	print('done')
	k = str(issue.uid)



	
	return HttpResponse(k)








def quick_create_issue(request, uid_status):
	print('here hahahahah')
	print(uid_status)

	uid_status = uuid.UUID(uid_status).hex



	status=Status.objects.get( uid = uid_status)
	project = status.project
	issue = Issue.objects.create(title=request.POST['title'], status=status, project=project, org=get_org(request), sprint=get_active_sprint(request, project.uid), points=request.POST['points'] )
	issue.issue_id = create_issue_id(request, project)
	issue.created_by = request.user
	issue.issue_type = IssueType.objects.get(uid=request.POST['issuetype'])
	print('issue_type' + issue.issue_type.title)
	screen = issue.issue_type.create_screen
	issue.priority = Priority.objects.get(uid=request.POST['priority'])
	issue.save()

	p = {'priority' : issue.priority.title, 'uid': issue.uid, 'type':issue.issue_type.title, 'is':issue.issue_id}
	p=p.values()
	p=list(p)





	print('done')

	k = str(issue.uid)

	return JsonResponse({'p':p})



	
	


def start_time_log(request, uid_issue):
	issue = Issue.objects.get(uid=uid_issue)
	issue.time_started = datetime.utcnow().replace(tzinfo=pytz.UTC)


	issue.save()
	return HttpResponse('success')

def stop_time_log(request, uid_issue):
	issue = Issue.objects.get(uid=uid_issue)
	issue.time_ended = datetime.utcnow().replace(tzinfo=pytz.UTC)
	k = ((issue.time_ended - issue.time_started).total_seconds())/60
	

	
	k = int(round(k))
	issue.timespent2 = issue.timespent2 + k 
	print k
	issue.save()


	return HttpResponse(issue.timespent2)



def transition_issue_plan(request, uid_project, uid_issue, uid_backlog_or_sprint):
	issue = Issue.objects.get(uid=uid_issue)




	if Backlog.objects.filter(uid=uid_backlog_or_sprint).exists():
		print('1')

		b = Backlog.objects.get(uid=uid_backlog_or_sprint)
		issue.backlog = b
		issue.sprint = None
		issue.save()

	elif Sprint.objects.filter(uid=uid_backlog_or_sprint).exists():
		print('2')
		s = Sprint.objects.get(uid=uid_backlog_or_sprint)
		issue.sprint = s
		issue.backlog = None
		issue.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def project2(request, crud, uid_project, uid_issue):
	current_sprint = get_active_sprint(request, uid_project)
	if current_sprint is None:

		project = Project.objects.get(uid=uid_project)
		active ='board_menu'
		return render(request, 'project_scrum_board.html', {'active':active, 'project':project} )
	else:
		

		issues = Issue.objects.filter(sprint=current_sprint).order_by('created')
		project = Project.objects.get(uid=uid_project)
		columns = Column.objects.filter(project=project)
		status = Status.objects.filter(project=project)
		x = ''
		for s in status:
			x += ('#'+str(s.uid)+',')

		index = len(x)
		x = x[:index-1]
		x = '"{}"'.format(x)
		print(x)
		#newstr = oldstr.replace("M", "")

		y = {}

		board_layout = project.board_layout

		for s in status:
			issues_in_status = Issue.objects.filter(status=s).filter(sprint=current_sprint)
			key = s.title
			key = key.replace(" ", "")
			print(key)
			y[key] = issues_in_status
		print(y)

			#calculate column widths 
		for c in columns:
			c.wid = 0
			for f in c.col_layout.all():
				if f.layout_type == 'vertical':
					c.wid = c.wid + 380*f.sections
					c.save()
					print('col_saved')
					print('helooooooooooooooo')



			#end csalculatung column widths 

			#layout = Layout.objects.filter(project=project).filter(root=True)[0]

		col_layouts = Col_layout.objects.filter(project=project).filter(parent=None)
		versions = Version.objects.filter(project=project)

		open_issue_uid = Issue.objects.get(uid=uid_issue).uid
			#issue_type_epic = IssueType.objects.filter(project=project).filter(title='epic')[0]
			
			#epics = Issue.objects.filter(project=project).filter(issue_type=issue_type_epic)	
		labels = Label.objects.filter(project=project)	
		active ='board_menu'	



			

		z = {'quick_search':'visible', 'open_issue_uid':open_issue_uid, 'active':active, 'labels':labels,  'versions':versions, 'col_layouts':col_layouts, 'board_layout':board_layout,'issues':issues,'x':x, 'status':status, 'project':project, 'sprint':current_sprint, 'columns':columns}

		z.update(y)

			

			#what about distribution of issues in same status boxes. restriction could be this, thar one status, one box 




		return render(request, 'test3.html', z )

def set_sortable_list_ids(request, uid_project):
	project = Project.objects.get(uid=uid_project)
	project.sortable_list_ids = request.POST['x']
	project.save()
	return HttpResponse('done')

def edit_sprint(request, uid_sprint):
	sprint = Sprint.objects.get(uid=uid_sprint)
	sprint.title = request.POST.get('title')
	if request.POST.get('start_date') != None and request.POST.get('start_date') !=  "":
		sprint.start_date= request.POST['start_date']
	if request.POST.get('end_date') != None and request.POST.get('end_date') != "":
		sprint.end_date = request.POST['end_date']
	sprint.save()
	messages.add_message(request, messages.INFO, 'Sprint has been edited')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def project(request, crud, uid):
	if crud == 'update':
		project = Project.objects.get(uid=uid)
		project.title = request.POST['project_name']
		project.issue_id_prefix =request.POST['issue_id'] 
		project.description = request.POST['description']
		project.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


	if crud == 'delete':
		project = Project.objects.get(uid=uid)
		project.delete()
		return redirect('/')

	if crud == 'board':
		current_sprint = get_active_sprint(request, uid)
		if current_sprint is None:
			project = Project.objects.get(uid=uid)
			active ='board_menu'
			return render(request, 'project_scrum_board.html', {'active':active,'project':project} )
		else:

			issues = Issue.objects.filter(sprint=current_sprint).order_by('created')
			project = Project.objects.get(uid=uid)
			columns = Column.objects.filter(project=project)
			status = Status.objects.filter(project=project)
			x = ''
			for s in status:
				x += ('#'+str(s.uid)+',')

			index = len(x)
			x = x[:index-1]
			x = '"{}"'.format(x)
			print(x)
			#newstr = oldstr.replace("M", "")

			y = {}

			board_layout = project.board_layout

			for s in status:
				issues_in_status = Issue.objects.filter(status=s).filter(sprint=current_sprint)
				key = s.title
				key = key.replace(" ", "")
				print(key)
				y[key] = issues_in_status
			print(y)

			#calculate column widths 
			for c in columns:
				c.wid = 0
				for f in c.col_layout.all():
					if f.layout_type == 'vertical':
						c.wid = c.wid + 380*f.sections
						c.save()
						print('col_saved')
						print('helooooooooooooooo')


			#end csalculatung column widths 

			#layout = Layout.objects.filter(project=project).filter(root=True)[0]

			col_layouts = Col_layout.objects.filter(project=project).filter(parent=None)
			versions = Version.objects.filter(project=project)
			#issue_type_epic = IssueType.objects.filter(project=project).filter(title='epic')[0]
			
			#epics = Issue.objects.filter(project=project).filter(issue_type=issue_type_epic)	
			labels = Label.objects.filter(project=project)	
			active ='board_menu'

			x= project.sortable_list_ids	



			

			z = {'quick_search':'visible', 'active':active, 'labels':labels,  'versions':versions, 'col_layouts':col_layouts, 'board_layout':board_layout,'issues':issues,'x':x, 'status':status, 'project':project, 'sprint':current_sprint, 'columns':columns}

			z.update(y)

			

			#what about distribution of issues in same status boxes. restriction could be this, thar one status, one box 




			return render(request, 'board.html', z )


	if crud == 'read':

		project= Project.objects.get(uid=uid)
		status = Status.objects.filter(project=project)
		columns = Column.objects.filter(project=project)
		
		sprints = Sprint.objects.filter(project=project).order_by('-created')

			
		if project.project_type =='scrum':
			backlog = Backlog.objects.get(project=project)
			
			#issue_type_epic = IssueType.objects.filter(project=project).filter(title='epic')[0]
			issues = Issue.objects.filter(project=project)
			#print(issue_type_epic)
			versions = Version.objects.filter(project=project)
			backlog_issues = Issue.objects.filter(project=project).filter(backlog = backlog).order_by('-created')
			#epics = Issue.objects.filter(project=project).filter(issue_type=issue_type_epic)
			y = ""
			for s in sprints:
				y += ('#'+ str(s.uid) +',')

			
			y += ('#'+ str(backlog.uid) +',')
			index = len(y)
			y = y[:index-1]
			y = '"{}"'.format(y)

			labels = Label.objects.filter(project=project)
			active='plan_menu'
				


			return render(request, 'project_scrum_plan.html', {'quick_search':'visible', 'active':active,'project':project,'y':y, 'backlog':backlog,'labels':labels, 'issues':issues, 'status':status, 'sprints':sprints, 'backlog_issues':backlog_issues,  'versions':versions})
		else:
			x = ''
			for s in status:
				x += ('#'+str(s.uid)+',')

			index = len(x)
			x = x[:index-1]
			x = '"{}"'.format(x)
			print(x)			
			issues = Issue.objects.filter(project=project)
			return render(request, 'project_normal.html', {'x':x,'project':project, 'issues':issues, 'status':status, 'columns':columns})
	elif crud == 'releases':
		releases = Version.objects.filter(project=Project.objects.get(uid=uid))
		project=Project.objects.get(uid=uid)
		x={}
		y={}

		for r in releases:
			x.update({r.title:r.issues.filter(resolved=True).count()})
			y.update({r.title:r.issues.filter(resolved=False).count()})
			


		
		print(x,y)
		active = 'releases_menu'
		
		return render(request, 'releases.html', {'active':active, 'releases':releases, 'project':project, 'x':x, 'y':y})
	elif crud == 'create':
		messages.add_message(request, messages.INFO, 'New Scrum project has started')

		title=request.POST['title']
		description=request.POST['description']
		project = Project.objects.create(title=title, description=description)
		profile = UserProfile.objects.get(user=request.user)
		project.org = profile.org
		project.issue_id_prefix = request.POST['project_prefix'] 
		project.project_type = request.POST['project_type']
		section = Section.objects.get(uid=request.POST['section'])
		print(section.title)
		project.section = section
		project.save()
		
		create_issue_types(request, project)
		create_default_prioritys(request, project)
		create_default_project_roles(request, project)
		create_default_permissions(request, project)
		create_default_screens(request, project)
		create_default_event_types(request, project)

		create_default_status_columns(request, project)
		create_default_workflow(request, project)

		Backlog.objects.create(project=project,org=get_org(request))



		return redirect('/project/read/'+ str(project.uid) )

	elif crud == 'delete':
		project= Project.objects.get(uid=uid).delete()
		return redirect('/home/')


def create_release(request, uid_project):
	project = Project.objects.get(uid=uid_project)
	if request.POST.get('start_date') == "":
		start_date=None
	else:
		start_date = request.POST.get('start_date')
	if request.POST.get('release_date') == "":
		release_date=None
	else:
		release_date = request.POST.get('release_date')

	release = Version.objects.create(project=project, title=request.POST['title'], org=get_org(request), description=request.POST.get('description'), start_date=start_date, release_date=release_date)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def releases(request, uid_project):
	project = Project.objects.get(uid=uid_project)
	releases =project.versions.all()
	x={}
	y={}

	for r in releases:
		x.update({r.title:r.issues.filter(resolved=True).count()})
		y.update({r.title:r.issues.filter(resolved=False).count()})
	active = 'releases_menu'
	return render(request, 'releases.html', {'releases':releases, 'active':active, 'project':project, 'x':x, 'y':y})


def get_block_issues(request, uid_status):

	status = Status.objects.get(uid=uid_status)
	sprint = get_active_sprint(request, status.project.uid )
	#issues = Issue.objects.filter(sprint=sprint, status=status).values()
	issues = Issue.objects.filter(sprint=sprint, status=status)

	data = [] #list which will be sent . should have issues as items with key values 

	for i in issues:
		a = {}
		a['uid'] = i.uid
		a['title'] = i.title
		a['issue_id'] = i.issue_id
		a['issue_type'] = i.issue_type.title
		a['priority_color'] = i.priority.color
		a['priority_title'] = i.priority.title
		a['icon_url'] = i.issue_type.icon.url
		data.append(a)





	#issues = list(issues)
	print(issues)



	x =  JsonResponse({'issues': data})
	#print(x)
	

	return x

	


def create_workflow(request, uid_project):
	Workflow.objects.create(title=request.POST['title'],project=Project.objects.get(uid=uid_project), org=get_org(request))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_user_to_project(request, uid_project):
	user = request.POST['user']
	project

def workflow(request, uid_project):
	org = get_org(request)
	project = Project.objects.get(uid=uid_project)
	transitions = Transition.objects.filter(project=project)
	statuss = Status.objects.filter(project=project)
	workflows = Workflow.objects.filter(project=project)
	return render(request, 'workflow.html', {'transitions':transitions, 'project':project, 'statuss':statuss, 'workflows':workflows})


def column(request,crud, uid_project, uid_column):
	if crud == 'editpage':
		project = Project.objects.get(uid=uid_project)
		columns = Column.objects.filter(project=project)
		statuss = Status.objects.filter(project=project)
		return render(request, 'columns.html', {'columns':columns, 'project':project, 'statuss':statuss})

	elif crud == 'create':
		Column.objects.create(title=request.POST['title'],project=Project.objects.get(uid=uid_project), org = get_org(request))
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	elif crud == 'add_a_column':# this is for adding a column from editor
		c = Column.objects.create(title='new_column',project=Project.objects.get(uid=uid_project), org = get_org(request))
		c.layout = col_layout.replace("testing123", str(c.uid))
		c.layout = col_layout.replace("status_uid", "")
		c.order=Column.objects.filter(project=Project.objects.get(uid=uid_project)).count()
		#c.layout = c1.layout.replace("status_uid", str(s1.uid))
		#c.layout = c.layout.replace("Column_text", 'Open Column')
		#c.layout = c.layout.replace("Block_text", 'Open Block')
		c.save()
		return HttpResponse(str(c.uid))

	elif crud == 'delete_column':
		c = Column.objects.get(uid=uid_column)
		c.delete()
		return HttpResponse('done')
	elif crud == 'delete':
		c = Column.objects.get(uid=uid_column)
		c.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def transition(request, crud, uid_project, uid_transition):
	if crud=="create":
		t = Transition.objects.create(title=request.POST['title'], start_status=Status.objects.get(uid=request.POST['start_status']), end_status=Status.objects.get(uid=request.POST['end_status']), project=Project.objects.get(uid=uid_project), org=get_org(request), workflow=Workflow.objects.get(uid=request.POST['workflow']))
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	if crud == 'delete':
		t = Transition.objects.get(uid=uid_transition)
		t.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def sprint(request, crud, uid_project, uid_sprint):
	if crud == 'create':
		org = get_org(request)

		project = Project.objects.get(uid=uid_project)
		s = Sprint.objects.create(org=org, project=project)
		if request.POST.get('start_date') != None and request.POST.get('start_date') !=  "":
			s.start_date= request.POST['start_date']
		if request.POST.get('end_date') != None and request.POST.get('end_date') != "":
			s.end_date = request.POST['end_date']

		s.title = request.POST['title']
		
		
		s.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	elif crud== 'read':
		sprint = Sprint.objects.get(uid=uid_sprint)

		issues = Issue.objects.filter(sprint=sprint)
		project = Project.objects.get(uid=uid_project)
		status = Status.objects.filter(project=project)
		columns = Column.objects.filter(project=project)
		return render(request, 'sprint_detail.html', {'sprint':sprint, 'issues':issues, 'status':status,'columns':columns, 'project':project})



def create_label(request, uid_project):
	Label.objects.create(title=request.POST['title'], project=Project.objects.get(uid=uid_project), org=get_org(request))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def version(request, crud, uid_project):
	project = Project.objects.get(uid=uid_project)
	Version.objects.create(title=request.POST['title'], description=request.POST['description'], release_date=request.POST['release_date'], project=project, org=get_org(request))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def notifications(request):
	user=request.user
	subscribed_issues = user.subscribed_issues.all()

	for s in subscribed_issues:
		s.events.all()
	events = user.events.all()
	return render(request, 'notifications.html', {'events':events})


def analytics(request, uid_project):
	startdate = date.today()
	enddate = startdate + timedelta(days=1)
	org = get_org(request)
	project = Project.objects.get(uid=uid_project)



	issues_added_today = Issue.objects.filter(created__range=[startdate, enddate]).filter(org=org)

	return render(request, 'analytics.html', {'issues_added_today':issues_added_today, 'project':project})


def reports(request, report_type, uid_project, uid_sprint):

	project = Project.objects.get(uid=uid_project)
	active ='reports_menu'

	if report_type == 'home':
		
		sprint = get_active_sprint(request, uid_project)
		issues = Issue.objects.filter(sprint=sprint)
		total_issues = issues.count()
		completed_sprints = Sprint.objects.filter(project=project).filter(complete=True).count()
		upcoming_sprints = Sprint.objects.filter(project=project).filter(complete=False).filter(is_Active=False).count()

		statuss = []
		issuetypes = []

		statuss_count = []
		issuetypes_count = []

		for s in project.statuss.all():
			y = s.title
			y='{}'.format(y)
			statuss.append(y)

		for it in project.issuetypes.all():
			y = it.title
			y='{}'.format(y)
			issuetypes.append(y)




		for s in project.statuss.all():
			issues= Issue.objects.filter(status=s).filter(sprint=sprint)
			y=issues.count()
			statuss_count.append(y)

		for it in project.issuetypes.all():
			issues= Issue.objects.filter(issue_type=it).filter(sprint=sprint)
			y=issues.count()
			issuetypes_count.append(y)


		# for sprint velocity 
		sprints = Sprint.objects.filter(project=project)

		labels = []
		for s in sprints:
			y= s.title
			y='{}'.format(y)
			labels.append(y)

		data = []

		for s in sprints :
			issues = Issue.objects.filter(sprint=s).filter(resolved=True)
			points = 0
			for i in issues:
				if i.points != None:
					points = points + i.points
			data.append(points)

		
	






		return render(request, 'report_home.html', {'upcoming_sprints':upcoming_sprints,'completed_sprints':completed_sprints,'total_issues':total_issues,'project':project, 'active':active, 'statuss':statuss, 'statuss_count':statuss_count, 'sprint':sprint, 'issuetypes':issuetypes, 'issuetypes_count':issuetypes_count, 'sprints':sprints, 'labels':labels, 'data':data,})

	if report_type == 'sprints':
		if uid_sprint == '100' :

			sprint = get_active_sprint(request, uid_project)
		else:
			sprint = Sprint.objects.get(uid=uid_sprint)
		sprints = Sprint.objects.filter(project=project)

		d1 = sprint.start_date
		d2 = sprint.end_date

		delta = d2-d1

		labels = []

		for i in range(delta.days + 1):
			labels.append(str(d1 + timedelta(days=i)))

		data = []



		issues = Issue.objects.filter(sprint=sprint)
		total_sprint_points = 0
		for i in issues:
			if i.points != None:
				total_sprint_points = total_sprint_points + i.points
		print(total_sprint_points)
		
		points_resolved_in_day = []

		for i in range(delta.days + 1):
			
			issues_resolved_on_day = Issue.objects.filter(end_date__range=[d1+timedelta(days=i),d1+timedelta(days=i+1)]).filter(sprint=sprint).filter(resolved=True)


			if issues_resolved_on_day.count() == 0:
				print('no issues resolved today')
				points_resolved_in_day.append(total_sprint_points - 0)
			else:
				print('issues_resolved_in a day ')
				print(issues_resolved_on_day.count())
				points=0
				for k in issues_resolved_on_day:
					
					
					if k.points != None:
						points = points + k.points
				points_resolved_in_day.append(total_sprint_points - points)
				total_sprint_points = total_sprint_points - points


		data = points_resolved_in_day



		
		



		



		#calculate story points reolved everday ..keep  subtracting it from total sprint points



		progress_status = Status.objects.filter(project=project).filter(title='In Progress')[0]
		issues_progress = Issue.objects.filter(project=project).filter(status=progress_status).filter(sprint=sprint)
		open_status = Status.objects.filter(project=project).filter(title='Open')[0]
		issues_open = Issue.objects.filter(project=project).filter(status=open_status).filter(sprint=sprint)
		resolved_status = Status.objects.filter(project=project).filter(title='Resolved')[0] 
		issues_resolved = Issue.objects.filter(project=project).filter(status=resolved_status).filter(sprint=sprint)
		return render(request, 'report_sprints.html', {'active':active, 'data':data, 'labels':labels, 'project':project, 'issues_resolved':issues_resolved, 'sprints':sprints, 'issues_progress':issues_progress, 'issues_open':issues_open, 'sprint':sprint})

	elif report_type == 'velocity_chart':
		project = Project.objects.get(uid=uid_project)
		sprint = get_active_sprint(request, uid_project)
		sprints = Sprint.objects.filter(project=project)
		labels = []
		for s in sprints:
			y= s.title
			y='{}'.format(y)
			labels.append(y)

		data = []

		for s in sprints :
			issues = Issue.objects.filter(sprint=s).filter(resolved=True)
			points = 0
			for i in issues:
				if i.points != None:
					points = points + i.points
			data.append(points)


					

			
			
		print(labels)
		print(data)

		return render(request, 'report_velocity_chart.html', {'active':active, 'project':project, 'sprints':sprints, 'labels':labels, 'data':data, 'sprint':sprint})

	






	elif report_type == 'burndown_chart':
		sprints = Sprint.objects.filter(project=project)
		project = Project.objects.get(uid=uid_project)



		#sprint = Sprint.objects.get(uid=uid_sprint)
		sprint = get_active_sprint(request, uid_project)

		sprints = Sprint.objects.filter(project=project)

		d1 = sprint.start_date
		d2 = sprint.end_date

		delta = d2-d1

		labels = []

		for i in range(delta.days + 1):
			labels.append(str(d1 + timedelta(days=i)))

		data = []



		issues = Issue.objects.filter(sprint=sprint)
		total_sprint_points = 0
		for i in issues:
			if i.points != None:
				total_sprint_points = total_sprint_points + i.points
		print(total_sprint_points)
		
		points_resolved_in_day = []

		for i in range(delta.days + 1):
			
			issues_resolved_on_day = Issue.objects.filter(end_date__range=[d1+timedelta(days=i),d1+timedelta(days=i+1)]).filter(sprint=sprint).filter(resolved=True)


			if issues_resolved_on_day.count() == 0:
				print('no issues resolved today')
				points_resolved_in_day.append(total_sprint_points - 0)
			else:
				print('issues_resolved_in a day ')
				print(issues_resolved_on_day.count())
				points=0
				for k in issues_resolved_on_day:
					
					
					if k.points != None:
						points = points + k.points
				points_resolved_in_day.append(total_sprint_points - points)
				total_sprint_points = total_sprint_points - points


		data = points_resolved_in_day

		return render(request, 'report_burndown_chart.html', {'active':active, 'sprints':sprints, 'project':project, 'data':data, 'labels':labels, 'sprint':sprint})

	






	elif report_type == 'cummulative_flow':

		project = Project.objects.get(uid=uid_project)

		sprint = Sprint.objects.get(uid=uid_sprint)

		sprints = Sprint.objects.filter(project=project)

		d1 = sprint.start_date
		d2 = sprint.end_date

		delta = d2-d1

		labels = []

		for i in range(delta.days + 1):
			labels.append(str(d1 + timedelta(days=i)))


		progress_count = []

		for i in range(delta.days + 1):

			progress_status = Status.objects.filter(title='In Progress').filter(project=project)[0]
			
			issues = Issue.objects.filter(e__range=[d1+timedelta(days=i),d1+timedelta(days=i+1)]).filter(sprint=sprint).filter(status=progress_status)

			progress_count.append(issues.count())

		print(progress_count)
			
		
		return render(request, 'report_cummulative_flow.html', {'sprints':sprints, 'active':active,  'project':project, 'sprint':sprint, 'labels':labels})

def has_perm(request, perm):
	profile = UserProfile.objects.get(user=request.user)
	perms = profile.permissions.all()
	for p in perms:
		if p.title == perm:
			return True
	return False


def activity_audit(request):
	org=get_org(request)
	events = org.events.all()
	return render(request, 'settings_activity_audit.html', {'events':events})

def search(request, query):
	
	org = get_org(request)

	results = Issue.objects.filter(title__contains=query).filter(org=org).values()

	results = list(results)
	j = JsonResponse({"results":results})
	print j 
	return JsonResponse({"results":results})


def search2(request):

	q=request.POST['query']
	org = get_org(request)
	results = Issue.objects.filter(title__contains=q).filter(org=org)
	return render(request, 'search.html', {'results':results})	


"""
def search(request):
	if has_perm(request, 'can_search'):
		q=request.POST['query']
		org = get_org(request)
		results = Issue.objects.filter(title__contains=q).filter(org=org)
		return render(request, 'search.html', {'results':results})
	else:
		return HttpResponse('You do not have permission')

		"""

def start_sprint(request, uid_sprint):
	sprint = Sprint.objects.get(uid=uid_sprint)
	project = sprint.project
	active_sprint = get_active_sprint(request, project.uid)

	if active_sprint == None:
		sprint.is_Active = True
		sprint.save()
		messages.add_message(request, messages.INFO, 'Sprint has started')
		return redirect('/project/board/'+ str(project.uid))

	else:
		messages.add_message(request, messages.INFO, 'This sprint is active currently, complete it first')
		return redirect('/project/board/'+str(project.uid))



	#check for project ..if any dprint is active ..return error ...

def get_active_sprint(request, uid_project):
	project=Project.objects.get(uid=uid_project)
	for s in project.sprints.all():
		if s.is_Active == True:
			return s 



def complete_sprint(request, uid_sprint):
	sprint = Sprint.objects.get(uid=uid_sprint)
	sprint.is_Active = False
	sprint.complete = True
	sprint.save()
	return redirect('/project/read/'+str(sprint.project.uid))

def section(request, crud, uid_section):
	if crud == 'create':
		s = Section.objects.create(title=request.POST['title'], description=request.POST['description'])
		s.org = UserProfile.objects.get(user=request.user).org
		s.save()
		return redirect('/')

	if crud =='delete':
		
		Section.objects.get(uid=uid_section).delete()
		return redirect('/')
		
		

def show_edit_issue_screen(request, uid_project, uid_issue):
	issue= Issue.objects.get(uid=uid_issue)
	issue_type = issue.issue_type
	screen = issue_type.edit_screen
	field_config = screen.field_config.all()[0]
	comments = Comment.objects.filter(issue=issue)
	project = Project.objects.get(uid=uid_project)
	versions = Version.objects.filter(project=project)
	#issue_type_epic = IssueType.objects.get(project=project, title='epic')
	#epics = Issue.objects.filter(project=project).filter(issue_type=issue_type_epic)
	labels = Label.objects.filter(project=project)

	#custom_fields = Screen.cutomfields.all()
	
	transitions = Transition.objects.filter(start_status=issue.status)
	return render(request, 'issue_edit.html', {'issue':issue, 'labels':labels, 'project':project, 'comments':comments, 'transitions':transitions, 'versions':versions})

def show_view_issue_screen(request, uid_project, uid_issue):
	if request.is_ajax():

		issue= Issue.objects.get(uid=uid_issue)
		issue_type = issue.issue_type
	
		screen = issue_type.edit_screen
		field_config = screen.field_config.all()
		print(field_config)
		comments = Comment.objects.filter(issue=issue).order_by('-created')
		project = issue.project
		print('view screen is here bitch')
		tasks = issue.tasks.all()
		field_config = screen.field_config.all()[0]

		cfvs = issue.custom_field_values.all()
		events = issue.events.all()



		uid=issue.project.uid

		current_sprint = get_active_sprint(request, uid)


	
	
		transitions = Transition.objects.filter(start_status=issue.status)
		return render(request, 'issue.html', { 'current_sprint': current_sprint,'events':events,'field_config':field_config, 'issue':issue,'tasks':tasks, 'cfvs':cfvs, 'project':project, 'comments':comments, 'transitions':transitions})
	else:
		issue= Issue.objects.get(uid=uid_issue)
		project = issue.project
		return redirect('/project/board/'+str(project.uid)+'/'+str(issue.uid))


def save_edit_issue_screen(request, uid_project, uid_issue):
	issue = Issue.objects.get(uid=uid_issue)
	issue.title = request.POST['title']
	issue.priority = Priority.objects.get(uid=request.POST['priority'])
	issue.description = request.POST['description']
	issue.points = request.POST['story_points']
	issue.issue_type = IssueType.objects.get(uid=request.POST['uid_issuetype'])

	if request.POST['epic'] != 'None':

		issue.epic = Issue.objects.get(uid=request.POST['epic'])


	if request.POST['version'] != 'None':

		issue.fix_version = Version.objects.get(uid=request.POST['version'])

	labels = request.POST.getlist('labels')

	for l in labels:
		l = l.encode("utf-8")
		label = Label.objects.get(uid=l)
		issue.label.add(label)

	issue.save()
	register_event(request, uid_project, 'issue_updated', uid_issue)
	return redirect('/show_view_issue_screen/'+uid_project+'/'+uid_issue)


	#take out fieldconfi associated with screen
	#show hide , required , text build in fields basis fieldconfig
	#renders issue html...all the processing hhappens there ...issue.html is basically screen
	#fetch custom fields associated with that screen and display them basis their respective settings
	#on submit screen either of the actions are taken
def show_create_issue_screen(request, uid_project, uid_issue_type):
	issue_type = IssueType.objects.get(uid=uid_issue_type)
	screen = issue_type.create_screen
	field_config = screen.field_config.all()[0]
	project = Project.objects.get(uid=uid_project)
	versions = Version.objects.filter(project=project)
	#issue_type_epic = IssueType.objects.get(project=project, title='epic')
	#epics = Issue.objects.filter(project=project).filter(issue_type=issue_type_epic)
	labels = Label.objects.filter(project=project)
	customfields = CustomField.objects.filter(screen=screen)
	users = UserProfile.objects.filter(org=get_org(request))
	sprints = Sprint.objects.filter(project=project)
	backlog = Backlog.objects.filter(project=project)[0]
	uid= project.uid
	current_sprint = get_active_sprint(request,uid)

	active = request.GET.get('q', '')
	#custom_fields = Screen.cutomfields.all()
	return render(request, 'issue_create.html', {'active':active, 'current_sprint':current_sprint, 'backlog':backlog,'sprints':sprints, 'users':users,'field_config':field_config,'customfields':customfields,'project':project, 'issue_type':issue_type, 'versions':versions, 'labels':labels})


def create_issue_id(request, project):
	count = Issue.objects.filter(project=project).count() + 1
	issue_id = project.issue_id_prefix+ '-' + str(count)
	print(issue_id)
	return issue_id

def test(request):

	return render(request, 'test.html')

def complete_task(request, uid_project, uid_task):
	task = Task.objects.get(uid=uid_task)
	task.checked = not task.checked
	checked_by = request.user
	checked_date = datetime.now()
	task.save()
	return HttpResponse('task completed')

def save_create_issue_screen(request, uid_project):
	title=request.POST['title']
	description=request.POST['description']
	project = Project.objects.get(uid=uid_project)
	issue= Issue.objects.create(title=title, description=description, org=get_org(request), project=project)
	add_to_uid = request.POST['add_to']

	if Backlog.objects.filter(uid=add_to_uid).count() != 0 :
		print('comes here 1........................................... ')
		issue.backlog = Backlog.objects.get(uid=add_to_uid)
	else:
		print('comes here 2')
		issue.sprint = Sprint.objects.get(uid=add_to_uid)

	if request.FILES.get('myfile') != None:

		file = request.FILES['myfile']

		f = FileAttachment.objects.create(file=file, issue=issue)
		print(f.created)

	labels = request.POST.getlist('labels')

	issue.issue_id = create_issue_id(request, project)






	





	for l in labels:
		l = l.encode("utf-8")
		label = Label.objects.get(uid=l)
		issue.label.add(label)

		
	
	

	#issue.label.add()


	if request.POST.get('version') != None and request.POST.get('version') != 'None':
		issue.fix_version = Version.objects.get(uid=request.POST['version'])


		

	issue.issue_type = IssueType.objects.get(uid=request.POST['issue_type'])
	issue.created_by = request.user

	screen = issue.issue_type.create_screen

	uid_issue = issue.uid


	cfs = CustomField.objects.filter(screen=screen)

	for cf in cfs:
		save_custom_field_value(request, cf, uid_issue)
		print('cf saved')

	issue.status=Status.objects.filter(project=project)[0]

	if request.POST.get('priority') != None and request.POST.get('priority') != 'None':
		issue.priority = Priority.objects.get(uid=request.POST['priority'])
		

	


		

	if request.POST.get('epic') != None and request.POST.get('epic') != 'None':
		e = Issue.objects.get(uid=request.POST['epic'])
		issue.epic = e

	if request.POST.get('points') != None and request.POST.get('points') != 'None':
		issue.points = request.POST['points']
		
	issue.save()
	
	register_event(request, uid_project, 'issue_created', uid_issue)
	print(issue.points)
	messages.add_message(request, messages.INFO, 'New issue has been created in Backlog')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def transition_issue_status(request, uid_project, uid_issue, uid_end_status):
	issue = Issue.objects.get(uid=uid_issue)
	end_status = Status.objects.get(uid=uid_end_status)
	issue.status = end_status
	
	issue.resolved = issue.status.resolution

	if end_status.resolution == True:
		issue.end_date= datetime.today()
		print('resolved')
	issue.save()
	return redirect('/project/board/'+uid_project)



#check transition screen 
#show_transition_Screen
#transition 



def check_transition_screen(request, uid_project, uid_issue, uid_end_status):
	issue = Issue.objects.get(uid=uid_issue)
	start_status = issue.status 
	#end_status = Status.objects.get(uid=request.POST['status'])
	end_status = Status.objects.get(uid=uid_end_status)
	project = Project.objects.get(uid=uid_project)
	transition = Transition.objects.filter(start_status=start_status, end_status=end_status)[0]
	

	if transition.screen == None:
		return HttpResponse('No Screen')
	else:
		return HttpResponse('Screen exists')






def show_transition_screen(request, uid_project, uid_issue, uid_end_status):  #gets called from scrum board 
	print('1')
	issue = Issue.objects.get(uid=uid_issue)
	start_status = issue.status 
	#end_status = Status.objects.get(uid=request.POST['status'])
	end_status = Status.objects.get(uid=uid_end_status)
	project = Project.objects.get(uid=uid_project)
	transition = Transition.objects.filter(start_status=start_status, end_status=end_status)[0]
	

	if transition.screen == None:
		print('5')
		return transition_issue_status(request,uid_project, uid_issue, uid_end_status)
	else:
		print('2')
		issue= Issue.objects.get(uid=uid_issue)
		issue_type = issue.issue_type
		screen = transition.screen
		field_config = screen.field_config.all()[0]
		custom_fields = screen.custom_fields.all()


		
		return render(request, 'transition_screen.html', {'field_config':field_config, 'custom_fields':custom_fields,'issue':issue,'project':project, 'screen':screen, 'end_status': end_status})
		

		
		
		
		




def save_custom_field_value(request, cf, uid_issue):
	if cf.field_type == 'text_field':
		cfv = CustomFieldValue.objects.create(custom_field=cf, issue=Issue.objects.get(uid=uid_issue), val_char=request.POST[cf.title], title=cf.title)


def save_transition_screen(request, uid_project, uid_issue, uid_screen):   # this gets alled from show_transition_screen
	issue = Issue.objects.get(uid=uid_issue)
	print('3')
	screen = Screen.objects.get(uid=uid_screen)
	end_status = Status.objects.get(uid=request.POST['uid_end_status'])
	uid_end_status = end_status.uid
	custom_fields = screen.custom_fields.all()
	return transition_issue_status(request,uid_project, uid_issue, uid_end_status)


"""
	 _.-(_)._     ."          ".      .--""--.          _.-{__}-._
   .'________'.   | .--------. |    .'        '.      .:-'`____`'-:.
  [____________] /` |________| `\  /   .'``'.   \    /_.-"`_  _`"-._\
  /  / .\/. \  \|  / / .\/. \ \  ||  .'/.\/.\'.  |  /`   / .\/. \   `\
  |  \__/\__/  |\_/  \__/\__/  \_/|  : |_/\_| ;  |  |    \__/\__/    |
  \            /  \            /   \ '.\    /.' / .-\                >/-.
  /'._  --  _.'\  /'._  --  _.'\   /'. `'--'` .'\/   '._-.__--__.-_.'
\/_   `"`   _\/_   ``   _\ /_  `-./\.-'  _\'.    `'`\
(__/    '|    \ _)_|           |_)_/            \__)|        '        
  |_____'|_____|   \__________/|;                  `_________'________`;-'
  s'----------'    '----------'   '--------------'`--------------------`
	 S T A N          K Y L E        K E N N Y         C A R T M A N

"""

"""
	for cf in custom_fields:
		if cf.field_type =='text_field':
			cfv = CustomFieldValue.objects.create(issue=issue,custom_field=cf, val_char=request.POST[cf.title])"""







	#save form of transition_screen and then transtion_issue_status
	
# issue function can be renamed as issue_action ...issue_Action and issue_type combination results in type of screen. 
#also need to think how does create issue shows screen 
#issue_Action can be abstracted out 

#submit_screen function which is post of show screen ?

#all issue_actions : create, view , edit, transition_status, transition_backlog_to_sprint, reosolve, 
#can granular permissions such editing the individual fields of issue...define an issuesecurity tabel per project which can be associted to issuetype, or it cn be part of project_permissions.. 
#break down edit into firther permissions called issue_security table 
#user has ability to restrit which user can edit which fields pf particular issue type 
#

#tansition ...check if tansition has a screen ...then show screen..then submit it ...then transition ...
#action ...find screen ...show screen...submit screen..create, edit , view

#show_screen 



#submit_screen - accept values for issue and then figure out next action..., transition screen, action screen 

def issue(request, crud, uid_project, uid_issue):
	if crud == 'move':
		issue= Issue.objects.get(uid=uid_issue)
		add_to_project = Project.objects.get(uid=request.POST['add_to_project'])
		
		issue.project = add_to_project
		issue.backlog = Backlog.objects.get(project=add_to_project)
		issue.sprint = None
		issue.save()
		messages.add_message(request, messages.INFO, 'Issue '+issue.issue_id+ ' has been moved to backlog of project '+issue.project.title)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


	if crud == 'view': #this should be view and there should be an edit action as well...
		#fetch issuetype ion take out screen corresponding to that and send it to showscreen function 
		issue= Issue.objects.get(uid=uid_issue)
		issue_type = issue.issue_type
		screen = issue_type.view_screen
		#field_config = screen.field_config.all()[0]

		return show_issue_view_screen(request, screen,uid_project, issue)
		#comments = Comment.objects.filter(issue=issue)
		#transitions = Transition.objects.filter(start_status=issue.status)
		#return render(request, 'issue.html', {'issue':issue, 'uid_project':uid_project, 'comments':comments, 'transitions':transitions, 'field_config':field_config})
	
	elif crud=='edit':
		issue= Issue.objects.get(uid=uid_issue)
		issue_type = issue.issue_type
		screen = issue_type.edit_screen
		return show_edit_issue_screen(request, screen, uid_project, issue)



	elif crud == 'delete':
		
		issue= Issue.objects.get(uid=uid_issue)
		issue.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


	elif crud == 'create': #basis issue type and action ...take out screen and send it to show screen 
		issue_type = IssueType.objects.get(uid=request.POST['issue_type'])
		screen = issue_type.create_screen
		return show_create_issue_screen(request, screen, uid_project, issue)



		title=request.POST['title']
		description=request.POST['description']
		project = Project.objects.get(uid=uid_project)
		org = UserProfile.objects.get(user=request.user).org
		issue= Issue.objects.create(title=title, description=description)
		issue.org = org
		
		issue.project = project

		if request.POST['version'] != 'None':
			issue.fix_version = Version.objects.get(uid=request.POST['version'])


		

		issue.issue_type = IssueType.objects.get(uid=request.POST['issue_type'])




		issue.status=Status.objects.filter(project=project)[0]

		issue.priority = Priority.objects.get(uid=request.POST['priority'])

		if project.project_type =='scrum':
			issue.backlog = Backlog.objects.get(project=project)
		

		if request.POST['epic'] != 'None':
			e = Issue.objects.get(uid=request.POST['epic'])
			issue.epic = e
		issue.save()


		string_uid_issue = str(issue.uid)
		#added to userprofile it belongs to
		#return redirect('/issue/read/'+ uid_project +'/'+ string_uid_issue )
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	

	elif crud=="create_epic" :
		title=request.POST['title']
		description=request.POST['description']
		project = Project.objects.get(uid=uid_project)
		org = UserProfile.objects.get(user=request.user).org
		issue= Issue.objects.create(title=title, description=description)
		issue.org = org
		issue.issue_type = IssueType.objects.filter(project=project).filter(title="epic")[0]
		
		issue.project = project
		issue.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))       

	elif crud == 'create_in_backlog':
		title=request.POST['title']
		description=request.POST['description']
		project = Project.objects.get(uid=uid_project)  
		org = get_org(request)
		backlog = Backlog.objects.filter(project=project)[0]
		issue= Issue.objects.create(title=title, description=description, project=project, org=org, backlog=backlog)
		issue.status=Status.objects.filter(project=project)[0]
		issue.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	elif crud == 'shift_issue': # from backlog to sprint on project page
		issue = Issue.objects.get(uid=uid_issue)
		project = Project.objects.get(uid=uid_project)
		issue.sprint = Sprint.objects.get(uid=request.POST['sprint'])
		issue.backlog = None
		issue.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#based on issuetype and transition ...take out screen and send it to show screen 


#this is from one status to another either on issue detail page or project sprint page 
	

	elif crud == 'shift_issue_status':
		issue = Issue.objects.get(uid=uid_issue)
		new_status = Status.objects.get(uid=request.POST['status'])
		print(issue.status)
		print(new_status)
		transition = Transition.objects.filter(start_status=issue.status).filter(end_status=new_status)[0]
		if transition.screen != None :
			print(transition.screen.title)
			print('screen came')

		issue.status = new_status
		issue.save()

		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	elif crud == 'transition_issue_status2': # this is when clicking on button from issue detail 
		issue = Issue.objects.get(uid=uid_issue)
		current_status = issue.status
		#if transition.screen == True then snow screen
		new_status = Status.objects.get(uid=uid_project) # here uid_project is actually uid of 
		transition = Transition.objects.filter(start_status=current_status, end_status=new_status)[0]
		if transition.screen != None :
			print(screen.title)
			print('screen came')

		issue.status = new_status
		issue.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	 


	 






	elif crud == 'resolve':
		issue = Issue.objects.get(uid=uid_issue)
		project = Project.objects.get(uid=uid_project)
		issue.status = Status.objects.filter(project=project).filter(title='Resolved')[0]
		issue.last_updated = datetime.now()
		issue.save()
		return redirect('/issue/read/' + uid_project + '/' + uid_issue)

#   elif crud == 'update':




def comment(request, crud, uid_issue):
	if crud=='create':
		issue=Issue.objects.get(uid=uid_issue)
		comment = Comment.objects.create(issue=issue,content=request.POST['content'],commentor=request.user)
		return HttpResponse('comment added')
	



def create_priority(request, uid_project):
	Priority.objects.create(title= request.POST['title'], project=Project.objects.get(uid=uid_project), org=get_org(request), color=request.POST['color'])
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def logout_view(request):
	user=request.user
	logout(request)
	return redirect('/')

def login_view(request):
	print(request.get_host())
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']

		user = authenticate( username = username, password = password)
		if user is not None:
			login(request, user)
			return redirect('/home')        
		else:
			return render(request, 'login.html' , {'message':'Email and Password didnt match'})

	else:
		return render(request, 'login.html')


def status(request, crud, uid_project, uid_status):
	if crud == 'create':
		project = Project.objects.get(uid=uid_project)
		org = get_org(request)
		#column = Column.objects.get(uid=request.POST['column'])
		title = request.POST['title']
		new_status = Status.objects.create(title=title, project=project,org = org)
		workflow = Workflow.objects.get(uid=request.POST['workflow'])


		#col3 = Col_layout.objects.create(title=title, project=project, layout_type="vertical", sections=1, column=column)
		#col3_child = Col_layout.objects.create(title=title+'_child' ,parent=col3, project=project, layout_type="none", sections=0, status=new_status)

		#create associated transitions:
		#similarly do it for the end_statuses : with for every status in end statuses create a transition wth start status as and end status as new created status and workflow as workflow 
		# for every start status create a transition with start status as start status and end status as the newly created status and workflow as workflow

		start_statuses = request.POST.getlist('start_statuses')
		for s in start_statuses:
			start_status = Status.objects.get(uid=s)
			end_status = new_status
			t= Transition.objects.create(title=start_status.title +'->'+ end_status.title, start_status=Status.objects.get(uid=s), end_status=Status.objects.get(uid=new_status.uid), project=Project.objects.get(uid=uid_project), org=get_org(request), workflow=workflow)
			print(t.title)



		end_statuses = request.POST.getlist('end_statuses')	

		for s in end_statuses:
			start_status = new_status
			end_status = Status.objects.get(uid=s)
			t= Transition.objects.create(title=start_status.title +'->'+ end_status.title, start_status=new_status, end_status=end_status, project=Project.objects.get(uid=uid_project), org=get_org(request), workflow=workflow)
			print(t.title)



		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	elif crud == 'delete':
		status = Status.objects.get(uid=uid_status)
		Issue.objects.filter(status=status).delete()
		status.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


"""


:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::-'    `-::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::-'          `::::::::::::::::
:::::::::::::::::::::::::::::::::::::::-  '   /(_M_)\  `:::::::::::::::
:::::::::::::::::::::::::::::::::::-'        |       |  :::::::::::::::
::::::::::::::::::::::::::::::::-         .   \/~V~\/  ,:::::::::::::::
::::::::::::::::::::::::::::-'             .          ,::::::::::::::::
:::::::::::::::::::::::::-'                 `-.    .-::::::::::::::::::
:::::::::::::::::::::-'                  _,,-::::::::::::::::::::::::::
::::::::::::::::::-'                _,--:::::::::::::::::::::::::::::::
::::::::::::::-'               _.--::::::::::::::::::::::#####:::::::::
:::::::::::-'             _.--:::::::::::::::::::::::::::#####:::::####
::::::::'    ##     ###.-::::::###:::::::::::::::::::::::#####:::::####
::::-'       ###_.::######:::::###::::::::::::::#####:##########:::####
:'         .:###::########:::::###::::::::::::::#####:##########:::####
	 ...--:::###::########:::::###:::::######:::#####:##########:::####
 _.--:::##:::###:#########:::::###:::::######:::#####:#################
'#########:::###:#########::#########::######:::#####:#################
:#########:::#############::#########::######:::#######################
##########:::########################::################################
##########:::##########################################################
##########:::##########################################################
#######################################################################
#######################################################################
################################################################# dp ##
#######################################################################


"""


""" Young rogue, your destiny depends upon this crystal portal"""

def index(request):
	if request.user.is_authenticated:
		print('here')
		profile= UserProfile.objects.get(user=request.user)
		org = profile.org
		projects = Project.objects.filter(org=org)
		sections = Section.objects.filter(org=org)
		return render(request, 'home.html', {'profile':profile, 'projects':projects, 'sections':sections})
		
	else:
		print('what')

	

		
		
		

		from django.conf import settings

		if settings.OPEN == True:
			return redirect('/signup')
			
		else:
			return render(request, 'website/index.html')


def signup_view(request):
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		user = User.objects.create_user(username = username, password = password)
		user.save()
		print(user.username)
		profile = UserProfile.objects.create(user=user)
		org = Org.objects.create()

		profile.org = org 

		profile.save()

		#send_mail('Welcome to Enpointer', 'Thanks for signing up for Enpointer - issue tracker and project manager for software teams. ', 'Enpointer', [username])

		# at the time of signup a user, a profile and an org is created 

		print(profile.created)
		login(request, user)

		if request.user.is_authenticated:
			print('user is logged in here')
		# Add template
		


		section = Section.objects.create(title='My Projects', org=get_org(request))
		print('king has entered the kingdom')
		return HttpResponseRedirect('/')
		
	else:
		return render(request, 'signup.html')

