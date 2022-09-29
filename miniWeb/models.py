from django.db import models

# Create your models here.
class dataAtten(models.Model):
    username = models.CharField(max_length=100, null=True)
    dateUpdated = models.DateTimeField(auto_now=True, null=True)
    data = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return f'{self.username}'


