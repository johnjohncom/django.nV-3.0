import datetime
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.template import RequestContext
from django.db import connection
from django.template import loader

from django.views.decorators.csrf import csrf_exempt

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import logout

from taskManager.models import Project, UserProfile
from taskManager.utils import store_uploaded_file
from taskManager.forms import UserForm, ProfileForm


def login(request):
    template = loader.get_template('accounts/login.html')

    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)

        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    # Redirect to a success page.
                    return redirect('/dashboard/')
                else:
                    # Return a 'disabled account' error message
                    return redirect('/dashboard/', {'disabled_user': True})
            else:
                # Return an 'invalid login' error message.
                context = {'failed_login': False}
                return HttpResponse(template.render(context, request))
        else:
            context = {'invalid_username': False}
            return HttpResponse(template.render(context, request))
    else:
        return HttpResponse(template.render({}, request))


def register(request):

    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            user.set_password(user.password)

            # add user to lowest permission group

            # grp = Group.objects.get(name='team_member')
            # user.groups.add(grp)

            user.userProfile = UserProfile.objects.create(user=user)
            user.userProfile.save()
            user.save()

            # Update our variable to tell the template registration was
            # successful.
            registered = True

        else:
            print(user_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.

    template = loader.get_template('accounts/register.html')
    context = {'user_form': user_form, 'registered': registered}
    return HttpResponse(template.render(context, request))


def profile(request):
    return render(request, 'profile.html', {'user': request.user})

#! Insecure Direct Object Reference (IDOR)
def profile_view(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect("/dashboard")

    if request.user.groups.filter(name='admin_g').exists():
        role = "Admin"
    elif request.user.groups.filter(name='project_managers').exists():
        role = "Project Manager"
    else:
        role = "Team Member"

    sorted_projects = Project.objects.filter(
        users_assigned=request.user.id).order_by('title')

    return render(request, 'accounts/profile_view.html',
                  {'user': user, 'role': role, 'project_list': sorted_projects})


#! Security Misconfiguration - Cross Site Request Forgery (CSRF)
@csrf_exempt
def profile_by_id(request, user_id):
    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print("made it!")
            if request.POST.get('username') != user.username:
                user.username = request.POST.get('username')
            if request.POST.get('first_name') != user.first_name:
                user.first_name = request.POST.get('first_name')
            if request.POST.get('last_name') != user.last_name:
                user.last_name = request.POST.get('last_name')
            if request.POST.get('email') != user.email:
                user.email = request.POST.get('email')
            if request.POST.get('password'):
                user.set_password(request.POST.get('password'))
            if request.FILES:
                user.userprofile.image = store_uploaded_file(user.username
                                                             + "." + request.FILES['picture'].name.split(".")[-1], request.FILES['picture'])
                user.userprofile.save()
            user.save()
            messages.info(request, "User Updated")

    return render(request, 'profile.html', {'user': user})


def reset_password(request):

    if request.method == 'POST':

        reset_token = request.POST.get('reset_token')

        try:
            userprofile = UserProfile.objects.get(reset_token=reset_token)
            if timezone.now() > userprofile.reset_token_expiration:
                # Reset the token and move on
                userprofile.reset_token_expiration = timezone.now()
                userprofile.reset_token = ''
                userprofile.save()
                return redirect('/')

        except UserProfile.DoesNotExist:
            messages.warning(request, 'Invalid password reset token')
            return render(request, 'accounts/reset_password.html')

        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password != confirm_password:
            messages.warning(request, 'Passwords do not match')
            return render(request, 'accounts/reset_password.html')

        # Reset the user's password + remove the tokens
        userprofile.user.set_password(new_password)
        userprofile.reset_token = ''
        userprofile.reset_token_expiration = timezone.now()
        userprofile.user.save()
        userprofile.save()

        messages.success(request, 'Password has been successfully reset')
        return redirect('/login')

    return render(request, 'accounts/reset_password.html')


def forgot_password(request):

    if request.method == 'POST':
        t_email = request.POST.get('email')

        try:
            reset_user = User.objects.get(email=t_email)

            # Generate secure random 6 digit number
            res = ""
            nums = [x for x in os.urandom(6)]
            for x in nums:
                res = res + str(x)

            reset_token = res[:6]
            reset_user.userprofile.reset_token = reset_token
            reset_user.userprofile.reset_token_expiration = timezone.now() + \
                datetime.timedelta(minutes=10)
            reset_user.userprofile.save()
            reset_user.save()

            messages.success(
                request, 'Check your email(dosen\'t support) for a reset token. reset_token:' + reset_token)
            return redirect('/reset_password')
        except User.DoesNotExist:
            messages.warning(request, 'Check your email for a reset token')

    return render(request, 'accounts/forgot_password.html')


def change_password(request):

    if request.method == 'POST':
        user = request.user
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if authenticate(username=user.username, password=old_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password Updated')
            else:
                messages.warning(request, 'Passwords do not match')
        else:
            messages.warning(request, 'Invalid Password')

    return render(request,
                  'accounts/change_password.html',
                  {'user': request.user})


#! Open Redirect
def logout_view(request):
    logout(request)
    return redirect(request.GET.get('redirect', '/'))
