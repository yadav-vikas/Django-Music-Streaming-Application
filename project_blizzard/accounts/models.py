from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.text import slugify 

from .manager import CustomAccountManager

from PIL import Image
from django.conf import settings


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, null=True, blank=True)
    last_login = models.DateTimeField(default=timezone.now, null=True, blank=True)
    # username_slug = models.SlugField(max_length=255, unique=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email',]

    def get_user_name(self):
        return self.username

    def __str__(self):
        return self.email
    
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.username)
    #     super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class EmailVerification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_query_name="verification", related_name='verify')
    verified = models.BooleanField(default=False)