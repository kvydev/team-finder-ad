from django import forms

from constants.validators import validate_phone, validate_github_url
from users.models import User


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "surname", "email", "password"]
        widgets = {"password": forms.PasswordInput}

    def save(self, commit=True):
        user: User = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "surname", "phone", "github_url", "about", "avatar"]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        return validate_phone(phone, current_user_pk=self.instance.pk)

    def clean_github_url(self):
        url = self.cleaned_data.get("github_url")
        return validate_github_url(url)


class UserChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Текущий пароль")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Новый пароль")
    new_password2 = forms.CharField(
        widget=forms.PasswordInput, label="Подтверждение пароля"
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Новый пароль и его подтверждение не совпадают")
