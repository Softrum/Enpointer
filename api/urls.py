from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^api/(?P<uid_project>[\w-]+)/$', views.api ),

   ]