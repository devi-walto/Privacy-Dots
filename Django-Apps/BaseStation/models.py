from django.db import models

# Create your models here.
class Device(models.Model):
    push_token = models.CharField(max_length=255)
    user = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.user if self.user else self.push_token
