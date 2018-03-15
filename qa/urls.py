from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^qa/(?P<uid_project>[\w-]+)/$', views.qa ),


   ]