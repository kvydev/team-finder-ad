import io
import random
from uuid import uuid4

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from constants.avatars import Color, AVATAR_SIZE, AVATAR_GRADIENTS, FONT_SIZE, BBOX
from constants.limits import UserLimit
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        help_text="Введите адрес электронной почты",
    )
    name = models.CharField(
        max_length=UserLimit.MAX_NAME_LENGTH,
        verbose_name="Имя",
        help_text=f"Введите имя (до {UserLimit.MAX_NAME_LENGTH} символов)",
    )
    surname = models.CharField(
        max_length=UserLimit.MAX_SURNAME_LENGTH,
        verbose_name="Фамилия",
        help_text=f"Введите фамилию (до {UserLimit.MAX_SURNAME_LENGTH} символов)",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        verbose_name="Аватар",
        help_text="Загрузите изображение профиля (необязательно)",
    )
    phone = models.CharField(
        max_length=UserLimit.MAX_PHONE_LENGTH,
        blank=True,
        verbose_name="Номер телефона",
        help_text=f"Введите номер телефона (необязательно, до {UserLimit.MAX_PHONE_LENGTH} символов)",
    )
    github_url = models.URLField(
        blank=True,
        verbose_name="GitHub URL",
        help_text="Введите URL вашего профиля на GitHub (необязательно)",
    )
    about = models.TextField(
        max_length=UserLimit.MAX_ABOUT_LENGTH,
        blank=True,
        verbose_name="О себе",
        help_text=f"Введите информацию о себе (необязательно, до {UserLimit.MAX_ABOUT_LENGTH} символов)",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активный",
        help_text="Указывает, активен ли пользователь",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Сотрудник",
        help_text="Указывает, является ли пользователь сотрудником",
    )

    favorites = models.ManyToManyField(
        settings.PROJECT_MODEL, related_name="interested_users", blank=True
    )

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-id"]

    def _generate_avatar(self):
        size = AVATAR_SIZE
        color_start, color_end = random.choice(AVATAR_GRADIENTS)
        letter = self.name[0].upper() if self.name else self.email[0].upper()

        img = Image.new("RGB", (size, size))

        for y in range(size):
            ratio = y / size
            r = int(color_start[0] + (color_end[0] - color_start[0]) * ratio)
            g = int(color_start[1] + (color_end[1] - color_start[1]) * ratio)
            b = int(color_start[2] + (color_end[2] - color_start[2]) * ratio)
            for x in range(size):
                img.putpixel((x, y), (r, g, b))

        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default(size=FONT_SIZE)

        bbox = draw.textbbox(BBOX, letter, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (size - w) / 2 - bbox[0]
        y = (size - h) / 2 - bbox[1]
        draw.text((x, y), letter, fill=Color.WHITE, font=font)

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        self.avatar.save(
            f"avatar_{uuid4()}.png", ContentFile(buffer.getvalue()), save=False
        )

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_avatar()
        super().save(*args, **kwargs)
