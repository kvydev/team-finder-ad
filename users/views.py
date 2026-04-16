from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from constants.limits import PaginationLimit
from users.models import User
from users.forms import (
    UserRegistrationForm,
    UserLoginForm,
    UserEditForm,
    UserChangePasswordForm,
)
from utils import paginate


@require_GET
def user_list(request: HttpRequest):
    users = User.objects.all()
    active_filter = None

    if request.user.is_authenticated:
        active_filter = request.GET.get("filter")
        me = request.user

        if active_filter == "owners-of-favorite-projects":
            users = users.filter(owned_projects__owner=me)
        elif active_filter == "owners-of-participating-projects":
            users = users.filter(owned_projects__in=me.participated_projects.all())
        elif active_filter == "interested-in-my-projects":
            users = users.filter(favorites__in=me.owned_projects.all())
        elif active_filter == "participants-of-my-projects":
            users = users.filter(participated_projects__in=me.owned_projects.all())

    return render(
        request,
        "users/participants.html",
        {
            "participants": paginate(request, users, PaginationLimit.USERS_PER_PAGE),
            "active_filter": active_filter,
            "active_skill": None,
        },
    )


@require_GET
def user_detail(request: HttpRequest, user_id: int):
    user = get_object_or_404(User, id=user_id)
    return render(request, "users/user-details.html", {"user": user})


def register(request: HttpRequest):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        auth_login(request, user)
        return redirect("users:user_detail", user.id)
    return render(request, "users/register.html", {"form": form})


def login(request: HttpRequest):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(request, email=email, password=password)
        if user:
            auth_login(request, user)
            return redirect("users:user_detail", user.id)
        form.add_error(None, "Неверный email или пароль")
    return render(request, "users/login.html", {"form": form})


@login_required
def edit_profile(request: HttpRequest):
    form = UserEditForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect("users:user_detail", request.user.id)

    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def change_password(request: HttpRequest):
    form = UserChangePasswordForm(request.POST or None)
    if form.is_valid():
        old_password = form.cleaned_data["old_password"]
        new_password = form.cleaned_data["new_password1"]

        if not request.user.check_password(old_password):
            form.add_error("old_password", "Неверный текущий пароль")
        else:
            request.user.set_password(new_password)
            request.user.save()
            auth_login(request, request.user)
            return redirect("users:user_detail", request.user.id)

    return render(request, "users/change_password.html", {"form": form})


def logout(request: HttpRequest):
    auth_logout(request)
    return redirect("projects:project_list")
