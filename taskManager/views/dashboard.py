from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from taskManager.models import Task, Project


def index(request):
    sorted_projects = Project.objects.order_by('-start_date')

    admin_level = False

    if request.user.groups.filter(name='admin_g').exists():
        admin_level = True

    list_to_show = []
    for project in sorted_projects:
        if (project.users_assigned.filter(username=request.user.username)).exists():
            list_to_show.append(project)

    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        template = loader.get_template('index.html')
        context = {}
        return HttpResponse(template.render(context, request))


def dashboard(request):
    sorted_projects = Project.objects.filter(
        users_assigned=request.user.id).order_by('title')
    sorted_tasks = Task.objects.filter(
        users_assigned=request.user.id).order_by('title')
    return render(request,
                  'dashboard.html',
                  {'project_list': sorted_projects,
                   'user': request.user,
                   'task_list': sorted_tasks})


def search(request):
    query = request.GET.get('q', '')

    my_project_list = Project.objects.filter(
        users_assigned=request.user.id).filter(
            title__icontains=query).order_by('title')
    my_task_list = Task.objects.filter(
        users_assigned=request.user.id).filter(
            title__icontains=query).order_by('title')
    return render(request,
                  'search.html',
                  {'q': query,
                   'task_list': my_task_list,
                   'project_list': my_project_list,
                   'user': request.user})
