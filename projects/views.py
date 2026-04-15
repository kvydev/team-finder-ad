from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET

from constants.projects import ProjectStatus
from constants.limits import PaginationLimit
from projects.forms import ProjectForm
from projects.models import Project


@require_GET
def project_list(request: HttpRequest):
    projects = Project.objects.annotate(
        participants_count=Count("participants")
    ).select_related("owner")

    paginator = Paginator(projects, PaginationLimit.PROJECTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "projects/project_list.html", {"projects": page_obj})


@require_GET
def favorite_projects(request: HttpRequest):
    projects = []
    if request.user.is_authenticated:
        projects = request.user.favorites.all()

    return render(request, "projects/favorite_projects.html", {"projects": projects})


@require_POST
@login_required
def toggle_favorite(request: HttpRequest, project_id: int):
    project = get_object_or_404(Project, id=project_id)
    if request.user.favorites.filter(pk=project.pk).exists():
        request.user.favorites.remove(project)
    else:
        request.user.favorites.add(project)
    request.user.save()
    return JsonResponse({"status": "ok"})


@require_GET
def project_details(request: HttpRequest, project_id: int):
    project = get_object_or_404(Project, id=project_id)
    return render(request, "projects/project-details.html", {"project": project})


@require_POST
def project_complete(request: HttpRequest, project_id: int):
    project = get_object_or_404(Project, id=project_id)
    if request.user.is_authenticated:
        if project.owner.id == request.user.id:
            if project.status == ProjectStatus.OPEN:
                project.status = ProjectStatus.CLOSED
                project.save()
                return JsonResponse({"status": "ok", "project_status": project.status})


@require_POST
@login_required
def toggle_participate(request: HttpRequest, project_id: int):
    project = get_object_or_404(Project, id=project_id)
    if project.owner.id != request.user.id:
        if was_participant := project.participants.filter(pk=request.user.pk).exists():
            project.participants.remove(request.user)
        else:
            project.participants.add(request.user)
        project.save()
        return JsonResponse({"status": "ok", "participant": not was_participant})


@login_required
def create_project(request: HttpRequest):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project: Project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect("projects:details", project.id)

    return render(
        request, "projects/create-project.html", {"form": form, "is_edit": False}
    )


@login_required
def edit_project(request: HttpRequest, project_id: int):
    project = get_object_or_404(Project, id=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        project: Project = form.instance
        project.id = project_id
        project.owner = request.user
        project.save()
        return redirect("projects:details", project.id)

    return render(
        request, "projects/create-project.html", {"form": form, "is_edit": True}
    )
