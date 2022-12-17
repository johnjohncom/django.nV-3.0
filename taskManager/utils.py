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

import os
import base64

""" Stores a temporary uploaded file on disk """
upload_dir_path = '%s/static/uploads' % (
    os.path.dirname(os.path.realpath(__file__)))


def store_uploaded_file(title, uploaded_file):
    if not os.path.exists(upload_dir_path):
        os.makedirs(upload_dir_path)

    #! Injection (command)
    os.system(
        "mv " +
        uploaded_file.temporary_file_path() +
        " " +
        "%s/%s" %
        (upload_dir_path,
         title))

    return '/static/uploads/%s' % (title)


def store_uploaded_base64_file(title, uploaded_file):

    f = open("%s/%s" % (upload_dir_path, title), 'wb')
    f.write(base64.b64decode(uploaded_file))
    f.close()

    return '/static/uploads/%s' % (title)
