from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from projects.views import project_list

urlpatterns = [
    path('', project_list, name='project_list'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('projects/', include('projects.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)