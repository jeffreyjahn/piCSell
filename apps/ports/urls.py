from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index),
    url(r'^start$', views.start),
    url(r'^process/(?P<action>\w+)$', views.process),
    url(r'^main$', views.main),
    url(r'^logout$', views.log_out),
    url(r'^edit_user/$', views.edit_user),
    url(r'^edit_user/process$', views.edit_user_process),
    url(r'^edit_pw/process$', views.edit_pw_process),
    url(r'^edit_profile_pic/process$', views.edit_profile_pic_process),
    url(r'^edit_admin/(?P<id>\d+)$', views.admin_edit),
    url(r'^edit_admin/(?P<id>\d+)/process$', views.admin_edit_process),
    url(r'^delete_user/(?P<id>\d+)$', views.delete_user),
    url(r'^manage_users$', views.manage_users),
    url(r'^portfolio/(?P<id>\d+)$', views.portfolio),
    url(r'^users/(?P<id>\d+)$', views.users),
    url(r'^add_photo/(?P<id>\d+)$', views.add_photo_process),
    url(r'^add_profile_pic/(?P<id>\d+)$', views.add_profile_pic_process),
    url(r'^photo/(?P<id>\d+)$', views.photo),
    url(r'^plans/new$', views.new_plan),
    url(r'^plans/(?P<id>\d+)$', views.show_plan),
    url(r'^plans/(?P<id>\d+)/edit$', views.edit_plan_process),
    url(r'^plans/add/(?P<id>\d+)$', views.add_to_plan_process),
    url(r'^plans/remove/(?P<id>\d+)$', views.remove_from_plan_process),
    url(r'^groups/new$', views.new_group),
    url(r'^groups/(?P<id>\d+)$', views.show_group),
    url(r'^groups/(?P<id>\d+)/edit$', views.edit_group_process),
    url(r'^groups/join/(?P<id>\d+)$', views.join_group),
    url(r'^groups/leave/(?P<id>\d+)$', views.leave_group),
    url(r'^groups/remove/(?P<group_id>/d+)/(?P<user_id>/d+)$', views.remove_groupmember)
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
