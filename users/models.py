from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from uuid import uuid4
import random
import io

from users.managers import UserManager

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    phone = models.CharField(max_length=12)
    github_url = models.URLField(blank=True)
    about = models.TextField(max_length=256, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    favorites = models.ManyToManyField(settings.PROJECT_MODEL, related_name='interested_users', blank=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def _generate_avatar(self):
        GRADIENTS = [
            ((86, 156, 214), (180, 142, 173)),
            ((106, 153, 85), (156, 220, 254)),
            ((206, 145, 120), (180, 142, 173)),
            ((86, 156, 214), (106, 153, 85)),
            ((180, 142, 173), (206, 145, 120)),
        ]

        size = 256
        color_start, color_end = random.choice(GRADIENTS)
        letter = self.name[0].upper() if self.name else self.email[0].upper()

        img = Image.new('RGB', (size, size))

        for y in range(size):
            ratio = y / size
            r = int(color_start[0] + (color_end[0] - color_start[0]) * ratio)
            g = int(color_start[1] + (color_end[1] - color_start[1]) * ratio)
            b = int(color_start[2] + (color_end[2] - color_start[2]) * ratio)
            for x in range(size):
                img.putpixel((x, y), (r, g, b))

        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype('arial.ttf', size=160)
        except IOError:
            font = ImageFont.load_default(size=160)

        bbox = draw.textbbox((0, 0), letter, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (size - w) / 2 - bbox[0]
        y = (size - h) / 2 - bbox[1]
        draw.text((x, y), letter, fill=(255, 255, 255), font=font)

        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        self.avatar.save(
            f'avatar_{uuid4()}.png',
            ContentFile(buffer.getvalue()),
            save=False
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_avatar()
        super().save(*args, **kwargs)