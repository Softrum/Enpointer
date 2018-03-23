from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^code/source/(?P<uid_project>[\w-]+)/$', views.source ),
    url(r'^code/commits/(?P<uid_project>[\w-]+)/$', views.commits ),
    url(r'^code/branches/(?P<uid_project>[\w-]+)/$', views.branches ),
    url(r'^code/pull-requests/(?P<uid_project>[\w-]+)/$', views.pull_requests ),
    

   ]