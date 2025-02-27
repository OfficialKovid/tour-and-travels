from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,"index.html")
def about(request):
    return render(request,"about.html")
def services(request):
    return render(request,"services.html")