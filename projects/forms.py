from django import forms

from constants.validators import validate_github_url
from projects.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]
        widgets = {"status": forms.Select(choices=Project.Status)}

    def clean_github_url(self):
        url = self.cleaned_data.get("github_url")
        return validate_github_url(url)
