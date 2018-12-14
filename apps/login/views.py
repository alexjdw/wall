from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

FORM_ERROR = 21


# Create your views here.
def login(request):
    return render(request, 'login/login.html')


def login_submit(request):
    if request.method != "POST":
        return redirect(login)

    # validate
    if 'username' not in request.POST:
        messages.add_message(
                request, FORM_ERROR,
                "Please enter a username or email.",
                tags="login-username")
        return redirect(login)

    if 'password' not in request.POST:
        messages.add_message(
                request, FORM_ERROR,
                "Please enter a password.",
                tags="login-password")
        return redirect(login)

    # get user
    uname = request.POST.get('username')
    if '@' in request.POST.get('username'):
        user = User.objects.filter(email=uname).first()
        if not user:
            messages.add_message(
                    request, FORM_ERROR,
                    "Email not registered.",
                    tags="login-username")
    else:
        user = User.objects.filter(username=uname).first()
        if not user:
            messages.add_message(
                    request, FORM_ERROR,
                    "Username not registered.",
                    tags="login-username")

    if not bcrypt.checkpw(request.POST['password'].encode('utf-8'),
                          user.pw_hash.encode('utf-8')):
        messages.add_message(
                request, FORM_ERROR,
                "Password is not correct.",
                tags="login-password")
        return redirect(login)

    request.session['username'] = user.username
    messages.add_message(request, messages.INFO, "Logged in!")

    return redirect('/')


def create(request):
    if request.method != "POST":
        return redirect(login)

    errors = User.objects.validate_user(request.POST)
    if errors != {}:
        for elem, err in errors.items():
            print(errors)
            messages.add_message(request, FORM_ERROR, err, extra_tags=elem)
        return redirect(login)

    hashed_pw = bcrypt.hashpw(request.POST['password'].encode('utf-8'),
                              bcrypt.gensalt())

    user = User(username=request.POST.get('username'),
                pw_hash=hashed_pw,
                email=request.POST.get('email'))
    user.save()
    request.session['username'] = user.username
    request.session['user_id'] = user.id
    messages.add_message(request, messages.INFO, "Logged in!")
    return redirect('/')


# def profile(request):
#     if not request.session.get('username') and not request.session.get('user_id'):
#         request.session.flush()
#         return redirect(login)

#     Posts.objects.filter(username=request.session['user_id'])

#     return render(request, 'login/profile.html')


def logout(request):
    request.session.flush()
    return redirect(login)
