from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login as auth_login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.urls import reverse_lazy

# Create your views here.


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("tasks:list_project")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = (
        "first_name",
        "last_name",
        "email",
    )
    template_name = "my_account.html"
    success_url = reverse_lazy("my_account")

    def get_object(self):
        return self.request.user
