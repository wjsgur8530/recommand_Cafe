from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Cafe(models.Model):
    name = models.TextField(max_length=40, null=True)
    tel1 = models.TextField(max_length=40, null=True)
    add1 = models.TextField(max_length=255, null=True)
    add2 = models.TextField(max_length=255, null=True)
    opening = models.TextField(max_length=40, null=True)
    off = models.TextField(max_length=40, null=True)
    sit = models.TextField(max_length=40, null=True)
    alcohol = models.TextField(max_length=40, null=True)
    smoke = models.TextField(max_length=40, null=True)
    reservation = models.TextField(max_length=40, null=True)
    restroom = models.TextField(max_length=40, null=True)
    delivery = models.TextField(max_length=40, null=True)
    ballet = models.TextField(max_length=40, null=True)
    introduce = models.TextField(max_length=255, null=True)
    hit = models.PositiveIntegerField(default=0)

    @property
    def update_counter(self):
        self.hit = self.hit + 1
        self.save()

class CafeImage(models.Model):
    image_id = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='image_id')
    image_url = models.URLField(max_length=2000, null=True)

class CafeType(models.Model):
    type_id = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='type_id')
    type = models.CharField(max_length=45, null=True)

class CafeTheme(models.Model):
    theme_id = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='theme_id')
    theme = models.TextField(max_length=255, null=True)

class CafeScore(models.Model):
    score_id = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='score_id')
    score = models.CharField(max_length=40, null=True)

class CafeOrder(models.Model):
    order_id = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='order_id')
    order = models.CharField(max_length=40, null=True)
