from django.urls import path

from projects.views import (
    project_list, project_details, create_project, edit_project,
    toggle_favorite, favorite_projects, project_complete, toggle_participate
)

app_name = 'projects'
urlpatterns = [
    path('list/', project_list, name='project_list'),
    path('favorites/', favorite_projects, name='favorite_projects'),
    path('<int:project_id>/toggle-favorite/', toggle_favorite, name='toggle-favorite'),
    path('<int:project_id>/', project_details, name='details'),
    path('<int:project_id>/complete/', project_complete, name='complete'),
    path('<int:project_id>/toggle-participate/', toggle_participate, name='toggle-participate'),
    path('create-project/', create_project, name='create'),
    path('<int:project_id>/edit/', edit_project, name='edit')
]
