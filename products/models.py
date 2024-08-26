from django.db import models
from django.conf import settings


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

    def __str__(self):
        return self.title

    def update_counter(self):
        self.hit += 1
        self.save()
