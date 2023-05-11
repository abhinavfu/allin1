from django.db import models

# Create your models here.


class Feedback(models.Model):
    name = models.CharField(max_length=20, default="", null=True, blank=True)
    email = models.CharField(max_length=50, default="", null=True, blank=True)
    subject = models.CharField(
        max_length=100, default="", null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name + ' ' + self.email
