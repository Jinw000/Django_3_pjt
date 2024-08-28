from django.db import models
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
class Hashtag(models.Model):
    tag = models.TextField(unique=True)

    def __str__(self):
        return self.tag

class Product(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(default='product.png',upload_to='images/prodcuts', blank=True)
    image2 = models.ImageField(upload_to='images/prodcuts', blank=True)
    image3 = models.ImageField(upload_to='images/prodcuts', blank=True)
    image4 = models.ImageField(upload_to='images/prodcuts', blank=True)
    image5 = models.ImageField(upload_to='images/prodcuts', blank=True)
    mark_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="mark_product")
    hit = models.PositiveIntegerField(default=0)
    hashtags = models.ManyToManyField(Hashtag, blank=True)

    def __str__(self):
        return self.title

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return False

    def update_counter(self):
        self.hit += 1
        self.save()
