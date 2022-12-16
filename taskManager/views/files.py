import os
import mimetypes

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db import connection

from taskManager.models import Project, File
from taskManager.forms import ProjectFileForm
from taskManager.utils import store_uploaded_file


def upload(request, project_id):

    if request.method == 'POST':

        proj = Project.objects.get(pk=project_id)
        form = ProjectFileForm(request.POST, request.FILES)

        if form.is_valid():
            name = request.POST.get('name', False)
            upload_path = store_uploaded_file(name, request.FILES['file'])

            #! Injection (SQL Injection)
            curs = connection.cursor()
            curs.execute(
                "insert into taskManager_file ('name','path','project_id') values ('%s','%s',%s)" %
                (name, upload_path, project_id))

            # file = File(
            # name = name,
            # path = upload_path,
            # project = proj)

            # file.save()

            return redirect('/' + project_id +
                            '/', {'new_file_added': True})
        else:
            form = ProjectFileForm()
    else:
        form = ProjectFileForm()

    template = loader.get_template('files/upload.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))


def download(request, file_id):

    file = File.objects.get(pk=file_id)
    abspath = open(
        os.path.dirname(
            os.path.realpath(__file__)) +
        file.path,
        'rb')
    response = HttpResponse(content=abspath.read())
    response['Content-Type'] = mimetypes.guess_type(file.path)[0]
    response['Content-Disposition'] = 'attachment; filename=%s' % file.name
    return response


def download_profile_pic(request, user_id):

    user = User.objects.get(pk=user_id)
    filepath = user.userprofile.image
    if len(filepath) > 1:
        return redirect(filepath)
    else:
        return redirect('/static/uploads/default.png')
    # filename = user.get_full_name()+"."+filepath.split(".")[-1]
    # try:
    # abspath = open(filepath, 'rb')
    # except:
    # abspath = open("./taskmanager"+filepath, 'rb')
    # response = HttpResponse(content=abspath.read())
    # response['Content-Type']= mimetypes.guess_type(filepath)[0]
    # return response
