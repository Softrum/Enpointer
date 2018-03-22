from django.conf.urls import url

from . import views

urlpatterns = [
    
    
    url(r'^wiki/home/(?P<uid_project>[\w-]+)/$', views.home ),
    url(r'^wiki/page/(?P<uid_page>[\w-]+)/$', views.page ),
    url(r'^wiki/page/(?P<uid_page>[\w-]+)/history$', views.page_history ),
    url(r'^wiki/page/create/(?P<uid_project>[\w-]+)/$', views.create_page ),

    url(r'^wiki/page/delete/(?P<uid_page>[\w-]+)/$', views.delete_page ),


    url(r'^wiki/page/versions/(?P<uid_page>[\w-]+)/$', views.versions ),

    url(r'^wiki/page/version/(?P<uid_version>[\w-]+)/$', views.version ),

    url(r'^wiki/page/history/(?P<uid_history>[\w-]+)/$', views.history ),

    url(r'^wiki/page/save_version/(?P<uid_page>[\w-]+)/$', views.save_version ),

    url(r'^wiki/page/commit_changes/(?P<uid_page>[\w-]+)/$', views.commit_changes ),

    


    url(r'^wiki/page/edit/(?P<uid_page>[\w-]+)/$', views.edit_page ),
    url(r'^wiki/page/publish/(?P<uid_page>[\w-]+)/$', views.publish ),
    url(r'^wiki/category/create/(?P<uid_project>[\w-]+)/$', views.create_category ),

    


   ]