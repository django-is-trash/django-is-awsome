from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from core import settings


def home(request):
    return render(request, 'base.html')
