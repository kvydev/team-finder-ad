import re

from django import forms

from constants.patterns import PHONE_REGEX
from constants.vars import GITHUB_URL
from users.models import User


def validate_phone(phone: str, current_user_pk=None):
    if not phone:
        return phone
    
    if not re.match(PHONE_REGEX, phone):
        raise forms.ValidationError(
            "Номер должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX"
        )

    if phone.startswith("8"):
        phone = "+7" + phone[1:]

    alt_phone = "8" + phone[1:]
    users_with_same_phone = User.objects.filter(phone__in=[phone, alt_phone])

    if current_user_pk:
        users_with_same_phone = users_with_same_phone.exclude(pk=current_user_pk)

    if users_with_same_phone.exists():
        raise forms.ValidationError("Этот номер телефона уже используется")

    return phone


def validate_github_url(url: str):
    if url and GITHUB_URL not in url:
        raise forms.ValidationError(f"Ссылка должна вести на {GITHUB_URL}")
    return url
