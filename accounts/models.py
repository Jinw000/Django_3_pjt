from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='images/users', blank=True)
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )