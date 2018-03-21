from django.conf.urls import url

from . import views

urlpatterns = [
    
    
    url(r'^wiki/home/(?P<uid_project>[\w-]+)/$', views.home ),
    url(r'^wiki/page/(?P<uid_page>[\w-]+)/$', views.page ),
    url(r'^wiki/page/(?P<uid_page>[\w-]+)/history$', views.page_history ),
    url(r'^wiki/page/create/(?P<uid_project>[\w-]+)/$', views.create_page ),

    url(r'^wiki/page/edit/(?P<uid_page>[\w-]+)/$', views.edit_page ),
    url(r'^wiki/page/publish/(?P<uid_page>[\w-]+)/$', views.publish ),
    url(r'^wiki/category/create/(?P<uid_project>[\w-]+)/$', views.create_category ),

    


   ]