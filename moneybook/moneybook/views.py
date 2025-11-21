from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from config import settings


def home(request):
    return render(request, 'base.html')

def signup(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)

    return render(request, "registration/signup.html", {'form': form})