from django.db import models

# Create your models here.
# Creates a Device (Node) and stores the push token
class Device(models.Model):
    location = models.CharField(max_length=255, null=True, blank=True)  # Location of the Dots, connected to the Rpi
    node_id = models.CharField(max_length=255, unique=True)    # Name of Node connected to the Rpi


    def __str__(self):
        return self.user if self.user else self.push_token