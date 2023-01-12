import datetime

from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils import timezone
from django.template import loader

from django.contrib import messages

from taskManager.models import Project


def project_create(request):

    if request.method == 'POST':

        title = request.POST.get('title', False)
        text = request.POST.get('text', False)
        project_priority = int(request.POST.get('project_priority', False))
        now = timezone.now()
        project_duedate = request.POST.get('project_duedate', False)

        if project_duedate is '':
            project_duedate = datetime.datetime.utcnow().strftime('%s')

        project_duedate = timezone.make_aware(datetime.datetime.fromtimestamp(
            int(project_duedate)))

        project = Project(title=title,
                          text=text,
                          priority=project_priority,
                          due_date=project_duedate,
                          start_date=now)
        project.save()
        project.users_assigned.set([request.user.id])

        return redirect('/dashboard', {'new_project_added': True})
    else:
        template = loader.get_template('projects/project_create.html')
        context = {}
        return HttpResponse(template.render(context, request))


#! Broken Acess Control - Insecure Direct Object Reference (IDOR)
def project_edit(request, project_id):

    proj = Project.objects.get(pk=project_id)

    if request.method == 'POST':

        title = request.POST.get('title', False)
        text = request.POST.get('text', False)
        project_priority = int(request.POST.get('project_priority', False))
        project_duedate = request.POST.get('project_duedate', False)

        if project_duedate is '':
            project_duedate = datetime.datetime.utcnow().strftime('%s')

        project_duedate = datetime.datetime.fromtimestamp(int(project_duedate))

        proj.title = title
        proj.text = text
        proj.priority = project_priority
        proj.due_date = project_duedate
        proj.save()

        return redirect('/projects/' + project_id + '/')
    else:
        template = loader.get_template('projects/project_edit.html')
        context = {'proj': proj}
        return HttpResponse(template.render(context, request))


#! Broken Acess Control - Insecure Direct Object Reference (IDOR)
def project_delete(request, project_id):
    # IDOR
    project = Project.objects.get(pk=project_id)
    project.delete()
    return redirect('/dashboard')


def project_details(request, project_id):
    proj = Project.objects.filter(
        users_assigned=request.user.id,
        pk=project_id)
    if not proj:
        messages.warning(
            request,
            'You are not authorized to view this project')
        return redirect('/dashboard')
    else:
        proj = Project.objects.get(pk=project_id)

        template = loader.get_template('projects/project_details.html')
        context = {'proj': proj}
        return HttpResponse(template.render(context, request))

#! Broken Acess Control - Insecure Direct Object Reference (IDOR)
def project_list(request):
    sorted_projects = Project.objects.filter(
        users_assigned=request.user.id).order_by('title')

    template = loader.get_template('projects/project_list.html')
    context = {'project_list': sorted_projects}
    return HttpResponse(template.render(context, request))
