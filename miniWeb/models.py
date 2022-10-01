from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class dataAtten(models.Model):
    username = models.CharField(max_length=100, null=True)
    dateUpdated = models.DateTimeField(auto_now=True, null=True)
    data = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return f'{self.username}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    webKioskPassword = models.CharField(null=True, max_length=100)
    lastUpdated = models.DateTimeField(blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    data = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f'{self.user}'

