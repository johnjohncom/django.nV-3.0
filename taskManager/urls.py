#     _  _                        __   __
#  __| |(_)__ _ _ _  __ _ ___   _ \ \ / /
# / _` || / _` | ' \/ _` / _ \_| ' \ V /
# \__,_|/ \__,_|_||_\__, \___(_)_||_\_/
#     |__/          |___/
#
# INSECURE APPLICATION WARNING
#
# django.nV is a PURPOSELY INSECURE web-application
# meant to demonstrate Django security problems
# UNDER NO CIRCUMSTANCES should you take any code
# from django.nV for use in another web application!
#

from django.urls import re_path

from taskManager.views import (
    accounts,
    files,
    projects,
    tasks,
    notes,
    dashboard,
    index
)

from taskManager.views.apis import (
    ogtag
)


app_name = 'taskManager'

urlpatterns = [
    re_path(r'^$', index.index, name='index'),

    # Common
    re_path(r'^dashboard/$', dashboard.dashboard, name='dashboard'),
    re_path(r'^search/$', dashboard.search, name='search'),


    # File
    re_path(r'^files/(?P<file_id>\d+)/$', files.download, name='download'),
    re_path(r'^projects/(?P<project_id>\d+)/files/$',
            files.upload, name='upload'),
    re_path(r'^downloadprofilepic/(?P<user_id>\d+)/$',
            files.download_profile_pic, name='download_profile_pic'),

    # Authentication & Authorization
    re_path(r'^register/$', accounts.register, name='register'),
    re_path(r'^login/$', accounts.login, name='login'),
    re_path(r'^logout/$', accounts.logout_view, name='logout'),
    re_path(r'^profile/$', accounts.profile, name='profile'),
    re_path(r'^change_password/$', accounts.change_password,
            name='change_password'),
    re_path(r'^forgot_password/$', accounts.forgot_password,
            name='forgot_password'),
    re_path(r'^reset_password/$', accounts.reset_password,
            name='reset_password'),
    re_path(r'^profile/(?P<user_id>\d+)$',
            accounts.profile_by_id, name='profile_by_id'),
    re_path(r'^profile_view/(?P<user_id>\d+)$',
            accounts.profile_view, name='profile_view'),

    # Projects
    re_path(r'^projects/create$', projects.project_create,
            name='project_create'),
    re_path(r'^projects/(?P<project_id>\d+)/delete/$',
            projects.project_delete, name='project_delete'),
    re_path(r'^projects/(?P<project_id>\d+)/edit/$',
            projects.project_edit, name='project_edit'),
    re_path(r'^projects/(?P<project_id>\d+)/$',
            projects.project_details, name='project_details'),
    re_path(r'^projects/$', projects.project_list, name='project_list'),

    # Tasks
    re_path(r'^projects/(?P<project_id>\d+)/create/$',
            tasks.task_create, name='task_create'),
    re_path(r'^projects/(?P<project_id>\d+)/tasks/(?P<task_id>\d+)/$',
            tasks.task_details, name='task_details'),
    re_path(r'^projects/(?P<project_id>\d+)/tasks(?P<task_id>\d+)/edit$',
            tasks.task_edit, name='task_edit'),
    re_path(r'^projects/(?P<project_id>\d+)/tasks/(?P<task_id>\d+)/delete$',
            tasks.task_delete, name='task_delete'),
    re_path(r'^projects/(?P<project_id>\d+)/tasks/(?P<task_id>\d+)/complete$',
            tasks.task_complete, name='task_complete'),
    re_path(r'^tasks$', tasks.task_list, name='task_list'),
    re_path(r'^projects/(?P<project_id>\d+)/manage_tasks/$',
            tasks.manage_tasks, name='manage_tasks'),


    # Notes
    re_path(r'^projects/(?P<project_id>\d+)/notes/(?P<task_id>\d+)/notes/create/$',
            notes.note_create, name='note_create'),
    re_path(r'^projects/(?P<project_id>\d+)/notes/(?P<task_id>\d+)/notes/(?P<note_id>\d+)/edit$',
            notes.note_edit, name='note_edit'),
    re_path(r'^projects/(?P<project_id>\d+)/notes/(?P<task_id>\d+)/notes/(?P<note_id>\d+)/delete$',
            notes.note_delete, name='note_delete'),

    # Settings - DEBUG
    re_path(r'^settings/$', index.settings, name='settings'),

    # ogtag api
    re_path(r'^ogtag/$', ogtag.retrive, name='ogtag'),

    # secret page
    re_path(r'^superadmin/$', index.superadmin, name='superadmin'),

    # Admin
    # re_path(r'^admin/', admin.site.urls),
]
