from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, folders
from django.http import JsonResponse
import json

@login_required
def home_view(req):
    folders.populate_folders()
    context = list_folders(req)
    return render(req, "home.html", context)

def list_folders(req):
    all_folders = folders.objects.all()
    context = {'folders': all_folders}
    return context

def get_features(request, folder_id):
    folder = folders.objects.get(id=folder_id)
    feature_names = folder.get_feature_names()
    context = {'features': feature_names}
    return JsonResponse(context)

def login_view(req):  
    """view for login page."""
    if req.method == "POST":
        email = req.POST.get("email")
        password = req.POST.get("password")
        user = User.get_user(email, password)
        if user:
            login(req, user)
            return redirect("/home")
        else:
            return render(
                req, "login.html", {"error_message": "Invalid credentials. Try again."})
    if req.method == "GET":
        if hasattr(req, "user"):
            if isinstance(req.user, User):
                logout(req) 
        return render(req, "login.html")       

def error_handler(response, exception=None):
    context = {"user": response.user}
    return render(response, "login.html", context)

# view to deal with server errors
def server_error_handler(response):
    context = {"user": response.user}
    return render(response, "login.html", context)