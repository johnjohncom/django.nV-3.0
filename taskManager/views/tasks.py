import datetime
from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils import timezone
from django.template import loader

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User

from taskManager.models import Task, Project


def task_create(request, project_id):

    if request.method == 'POST':

        proj = Project.objects.get(pk=project_id)

        text = request.POST.get('text', False)
        task_title = request.POST.get('task_title', False)
        now = timezone.now()
        task_duedate = timezone.now() + datetime.timedelta(weeks=1)
        if request.POST.get('task_duedate') != '':
            task_duedate = datetime.datetime.fromtimestamp(
                int(request.POST.get('task_duedate', False)))

        task = Task(
            text=text,
            title=task_title,
            start_date=now,
            due_date=task_duedate,
            project=proj)

        task.save()
        task.users_assigned.set([request.user])

        return redirect('/projects/' + project_id +
                        '/', {'new_task_added': True})
    else:
        template = loader.get_template(
            'tasks/task_create.html')
        context = {'proj_id': project_id}
        return HttpResponse(template.render(context, request))

#! Broken Acess Control - Insecure Direct Object Reference (IDOR)
def task_edit(request, project_id, task_id):

    proj = Project.objects.get(pk=project_id)
    task = Task.objects.get(pk=task_id)

    if request.method == 'POST':

        if task.project == proj:

            text = request.POST.get('text', False)
            task_title = request.POST.get('task_title', False)
            task_completed = request.POST.get('task_completed', False)

            task.title = task_title
            task.text = text
            task.completed = True if task_completed == "1" else False
            task.save()

        return redirect('/projects/' + project_id + '/tasks/' + task_id)
    else:
        template = loader.get_template('tasks/task_edit.html')
        context = {'task': task}
        return HttpResponse(template.render(context, request))

#! Broken Acess Control - Insecure Direct Object Reference (IDOR)
def task_delete(request, project_id, task_id):
    proj = Project.objects.get(pk=project_id)
    task = Task.objects.get(pk=task_id)
    if proj is not None:
        if task is not None and task.project == proj:
            # TODO: 하위에 note 있으면 삭제 못하도록
            task.delete()

    return redirect('/projects/' + project_id + '/')

#! Broken Acess Control - Insecure Direct Object Reference (IDOR)
def task_complete(request, project_id, task_id):
    proj = Project.objects.get(pk=project_id)
    task = Task.objects.get(pk=task_id)
    if proj is not None:
        if task is not None and task.project == proj:
            task.completed = not task.completed
            task.save()

    return redirect('/projects/' + project_id + '/tasks/' + task_id)


def task_details(request, project_id, task_id):

    task = Task.objects.get(pk=task_id)

    logged_in = True

    if not request.user.is_authenticated:
        logged_in = False

    admin_level = False
    if request.user.groups.filter(name='admin_g').exists():
        admin_level = True

    pmanager_level = False
    if request.user.groups.filter(name='project_managers').exists():
        pmanager_level = True

    assigned_to = False
    if task.users_assigned.filter(username=request.user.username).exists():
        assigned_to = True
    elif admin_level:
        assigned_to = True
    elif pmanager_level:
        project_users = task.project.users_assigned
        if project_users.filter(username=request.user.username).exists():
            assigned_to = True

    template = loader.get_template('tasks/task_details.html')
    context = {'task': task,
               'assigned_to': assigned_to,
               'logged_in': logged_in,
               'completed_task': "Yes" if task.completed else "No"}
    return HttpResponse(template.render(context, request))


def task_list(request):
    my_task_list = Task.objects.filter(users_assigned=request.user.id)

    template = loader.get_template('tasks/task_list.html')
    context = {'task_list': my_task_list, 'user': request.user}
    return HttpResponse(template.render(context, request))


def manage_tasks(request, project_id):

    user = request.user
    project = Project.objects.get(pk=project_id)

    if user.is_authenticated:

        assigned_user_list = []
        for assigned_user in project.users_assigned.all():
            assigned_user_list.append(assigned_user.pk)

        if user.pk in assigned_user_list:

            if request.method == 'POST':

                userid = request.POST.get("userid")
                taskid = request.POST.get("taskid")

                user = User.objects.get(pk=userid)
                task = Task.objects.get(pk=taskid)

                task.users_assigned.add(user)

                return redirect('/')
            else:

                template = loader.get_template('tasks/manage_tasks.html')
                context = {'tasks': Task.objects.filter(project=project).order_by('title'),
                           'users': project.users_assigned.all()}
                return HttpResponse(template.render(context, request))
        else:
            return redirect('/projects/', {'permission': False})

    return redirect('/projects/', {'logged_in': False})
