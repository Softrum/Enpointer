from django.conf.urls import url

from . import views
from . import views2


"""

   /\/\/\/\/\/\  
  <            >
   |          |
   |          |
   |   _  _   |
  -|_ / \/ \_ |-
 |I|  \_/\_/  |I|
  -|   /  \   |-
   |   \__/   |
   |          |
   |          |
   |__________|
  /___/\__/\___\
 /     | \|     \
   /\  |\ | _@|#_
  / /\ | \| |   |
  \/  / \ / |   |
   \_/___/   \_/ 

"""

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.login_view ),
    url(r'^sitemap', views.sitemap ),
    url(r'^home', views.home ),
    url(r'^logout', views.logout_view ),
    url(r'^signup/$', views.signup_view ),

    url(r'^services/$', views2.services, name='services' ),

    url(r'^services_enquiry/$', views.services_enquiry ),



    url(r'^updates/$', views.updates ),

    url(r'^case_studies', views.case_studies ),

    url(r'^use_cases/(?P<use_type>[\w-]+)/$', views.use_cases ),


    url(r'^test', views.test ),

    url(r'^increase_column_order/(?P<col_uid>[\w-]+)/$', views.increase_column_order ),
    url(r'^decrease_column_order/(?P<col_uid>[\w-]+)/$', views.decrease_column_order ),

    url(r'^add_user_to_project/$', views.add_user_to_project ),

    url(r'^why', views.why ),
    url(r'^design_philosophy', views.design_philosophy ),
    url(r'^company_principles', views.company_principles ),
    url(r'^product_philosophy', views.product_philosophy ),

    url(r'^support/(?P<slug>[\w-]+)/$', views.support ),
    url(r'^knowledge/(?P<slug>[\w-]+)/$', views.knowledge ),

    url(r'^blog/$', views.blog ),
    url(r'^blog/(?P<slug>[\w-]+)/$', views.blog_detail ),

    url(r'^about', views.about ),

    url(r'^security', views.security ),

    url(r'^privacy_policy', views.privacy_policy ),
    url(r'^terms_of_use', views.terms_of_use ),


     url(r'^settings', views.settings ),


     url(r'^send_reset_password_link/$', views.send_reset_password_link ),
     url(r'^reset_password_page/(?P<guid>[\w-]+)/$', views.reset_password_page ),
      url(r'^reset_password/$', views.reset_password ),

     url(r'^features/$', views.features ),

     url(r'^update_col_layout/(?P<uid_col>[\w-]+)/$', views.update_col_layout),
     url(r'^pricing', views.pricing ),

     url(r'^edit_layout/(?P<uid_project>[\w-]+)/$', views.edit_layout ),

    url(r'^forgot_password', views.forgot_password ),

     url(r'^start_time_log/(?P<uid_issue>[\w-]+)/$', views.start_time_log ),
     url(r'^stop_time_log/(?P<uid_issue>[\w-]+)/$', views.stop_time_log ),

     url(r'^quick_create_issue/(?P<uid_status>[\w-]+)/$', views.quick_create_issue ),
     url(r'^quick_create_issue_plan/(?P<uid>[\w-]+)/$', views.quick_create_issue_plan ),

     url(r'^release_detail/(?P<uid_release>[\w-]+)/$', views.release_detail ),

      url(r'^releases/(?P<uid_project>[\w-]+)/$', views.releases ),



    url(r'^project/(?P<crud>[\w-]+)/(?P<uid_project>[\w-]+)/(?P<uid_issue>[\w-]+)/$', views.project2),
    url(r'^project/(?P<crud>[\w-]+)/(?P<uid>[\w-]+)/$', views.project ),
    url(r'^issue/(?P<crud>[\w-]+)/(?P<uid_project>[\w-]+)/(?P<uid_issue>[\w-]+)/$', views.issue ),

    url(r'^issuetype/(?P<crud>[\w-]+)/(?P<uid_project>[\w-]+)/(?P<uid_issuetype>[\w-]+)/$', views.issuetype ),


    url(r'^analytics/(?P<uid_project>[\w-]+)/$', views.analytics),

    url(r'^reports/(?P<report_type>[\w-]+)/(?P<uid_project>[\w-]+)/(?P<uid_sprint>[\w-]+)/$', views.reports),

    url(r'^comment/(?P<crud>[\w-]+)/(?P<uid_issue>[\w-]+)/$', views.comment),
    url(r'^search/(?P<query>[\w ]+)', views.search),


    url(r'^invite_user/$', views.invite_user),
    url(r'^invited_user_page/(?P<guid>[\w-]+)$', views.invited_user_page),
    url(r'^invited_user_signup/$', views.invited_user_signup),

    url(r'^set_issue_bg/(?P<uid_issue>[\w-]+)', views.set_issue_bg),

    url(r'^assign_user/(?P<uid_issue>[\w-]+)/(?P<username>[\w-]+)/$', views.assign_user),

    url(r'^add_due_date/(?P<uid_issue>[\w-]+)/(?P<date>[\w-]+)/$', views.add_due_date),

    url(r'^search2/$', views.search2), 

    url(r'^edit_sprint/(?P<uid_sprint>[\w-]+)/$', views.edit_sprint), 

    url(r'^section/(?P<crud>[\w-]+)/(?P<uid_section>[\w-]+)/$', views.section ),
    url(r'^version/(?P<crud>[\w-]+)/(?P<uid_project>[\w-]+)/$', views.version ),
    url(r'^status/(?P<crud>[\w-]+)/(?P<uid_project>[\w-]+)/(?P<uid_status>[\w-]+)/$', views.status ),
    url(r'^sprint/(?P<crud>[\w-]+)/(?P<uid_project>[\w-]+)/(?P<uid_sprint>[\w-]+)/$', views.sprint ),

    url(r'^transition/(?P<crud>[\w-]+)/(?P<uid_project>[\w-]+)/(?P<uid_transition>[\w-]+)/$', views.transition ),

    url(r'^test', views.test),
    url(r'^create_workflow/(?P<uid_project>[\w-]+)', views.create_workflow),

    url(r'^create_priority/(?P<uid_project>[\w-]+)', views.create_priority),

    url(r'^create_screen/(?P<uid_project>[\w-]+)', views.create_screen),


    url(r'^get_block_issues/(?P<uid_status>[\w-]+)/', views.get_block_issues),


    url(r'^create_label/(?P<uid_project>[\w-]+)/$', views.create_label),

    url(r'^activity_audit/$', views.activity_audit),
    url(r'^notifications/$', views.notifications),




    url(r'^workflow/(?P<uid_project>[\w-]+)', views.workflow),
    url(r'^column/(?P<crud>[\w-]+)/(?P<uid_project>[\w-]+)/(?P<uid_column>[\w-]+)/', views.column),

    url(r'^screen_settings/(?P<uid_project>[\w-]+)', views.screen_settings),

    url(r'^create_custom_field/(?P<uid_project>[\w-]+)/(?P<uid_screen>[\w-]+)/', views.create_custom_field),

    url(r'^swimlane/(?P<crud>[\w-]+)/(?P<uid_project>[\w-]+)', views.swimlane),

    url(r'^start_sprint/(?P<uid_sprint>[\w-]+)/$', views.start_sprint),

    url(r'^set_sortable_list_ids/(?P<uid_project>[\w-]+)/$', views.set_sortable_list_ids),

    url(r'^complete_sprint/(?P<uid_sprint>[\w-]+)/$', views.complete_sprint),

    url(r'^show_view_issue_screen/(?P<uid_project>[\w-]+)/(?P<uid_issue>[\w-]+)/$', views.show_view_issue_screen),
    url(r'^show_edit_issue_screen/(?P<uid_project>[\w-]+)/(?P<uid_issue>[\w-]+)/$', views.show_edit_issue_screen),
    url(r'^save_edit_issue_screen/(?P<uid_project>[\w-]+)/(?P<uid_issue>[\w-]+)/$', views.save_edit_issue_screen),

    url(r'^show_create_issue_screen/(?P<uid_project>[\w-]+)/(?P<uid_issue_type>[\w-]+)/$', views.show_create_issue_screen),

    url(r'^save_create_issue_screen/(?P<uid_project>[\w-]+)/', views.save_create_issue_screen),
    url(r'^show_transition_screen/(?P<uid_project>[\w-]+)/(?P<uid_issue>[\w-]+)/(?P<uid_end_status>[\w-]+)/$', views.show_transition_screen),

    url(r'^check_transition_screen/(?P<uid_project>[\w-]+)/(?P<uid_issue>[\w-]+)/(?P<uid_end_status>[\w-]+)/$', views.check_transition_screen),
    url(r'^save_transition_screen/(?P<uid_project>[\w-]+)/(?P<uid_issue>[\w-]+)/(?P<uid_screen>[\w-]+)/$', views.save_transition_screen),
    
    url(r'^transition_issue_plan/(?P<uid_project>[\w-]+)/(?P<uid_issue>[\w-]+)/(?P<uid_backlog_or_sprint>[\w-]+)/$', views.transition_issue_plan),

    url(r'^update_issue_description/(?P<uid_project>[\w-]+)/(?P<uid_issue>[\w-]+)/$', views.update_issue_description),
    
    url(r'^create_task/(?P<uid_project>[\w-]+)/(?P<uid_issue>[\w-]+)/$', views.create_task),
    url(r'^complete_task/(?P<uid_project>[\w-]+)/(?P<uid_task>[\w-]+)/$', views.complete_task),

    url(r'^upload_attachment/(?P<uid_issue>[\w-]+)/$', views.upload_attachment),

    url(r'^transition_issue_status/(?P<uid_project>[\w-]+)/(?P<uid_issue>[\w-]+)/(?P<uid_end_status>[\w-]+)/$', views.transition_issue_status ),
    url(r'^project_settings/(?P<setting_type>[\w-]+)/(?P<uid_project>[\w-]+)/', views.project_settings ),
    url(r'^project_settings_normal/(?P<setting_type>[\w-]+)/(?P<uid_project>[\w-]+)/', views.project_settings_normal ),
    
    



    #swimlanes


]