from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader

from taskManager.models import Task, Project, Notes


def note_create(request, project_id, task_id):
    if request.method == 'POST':

        parent_task = Task.objects.get(pk=task_id)

        note_title = request.POST.get('note_title', False)
        text = request.POST.get('text', False)

        note = Notes(
            title=note_title,
            text=text,
            user=request.user,
            task=parent_task)

        note.save()
        return redirect('/projects/' + project_id + '/tasks' +
                        task_id, {'new_note_added': True})
    else:
        template = loader.get_template('notes/note_create.html')
        context = {'task_id': task_id}
        return HttpResponse(template.render(context, request))

#! Insecure Direct Object Reference (IDOR)
def note_edit(request, project_id, task_id, note_id):

    proj = Project.objects.get(pk=project_id)
    task = Task.objects.get(pk=task_id)
    note = Notes.objects.get(pk=note_id)

    if request.method == 'POST':

        if task.project == proj:

            if note.task == task:

                text = request.POST.get('text', False)
                note_title = request.POST.get('note_title', False)

                note.title = note_title
                note.text = text
                note.save()

        return redirect('/projects/' + project_id + '/tasks/' + task_id)
    else:
        template = loader.get_template('notes/note_edit.html')
        context = {'note': note}
        return HttpResponse(template.render(context, request))

#! Insecure Direct Object Reference (IDOR)
def note_delete(request, project_id, task_id, note_id):
    proj = Project.objects.get(pk=project_id)
    task = Task.objects.get(pk=task_id)
    note = Notes.objects.get(pk=note_id)
    if proj is not None:
        if task is not None and task.project == proj:
            if note is not None and note.task == task:
                note.delete()

    return redirect('/projects/' + project_id + '/tasks/' + task_id)
