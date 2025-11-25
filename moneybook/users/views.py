from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login

from users.forms import CustomUserCreationForm


def signup(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)

    context = {'form':form}

    return render(request,'registration/signup.html',context)

def login(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        django_login(request, form.get_user())

        next = request.GET.get('next')
        if next:
            return redirect(next)

        return redirect('/')
    context = {'form':form}

    return render(request, 'registration/login.html', context)


@login_required
def profile_view(request):
    user = request.user
    return render(request, "users/profile.html", {"user_obj": user})


