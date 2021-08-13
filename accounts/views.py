from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import SignUpForm

# Create your views here.


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("tasks:list_projects")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})
