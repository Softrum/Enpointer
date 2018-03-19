from django.conf.urls import url

from . import views

urlpatterns = [
    
    
    url(r'^wiki/home/(?P<uid_project>[\w-]+)/$', views.home ),

   ]