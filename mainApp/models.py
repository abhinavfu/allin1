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


class Portfolio_page_view_count(models.Model):
    portfolio_view_count = models.IntegerField(default=0)
    about_view_count = models.IntegerField(default=0)
    contact_view_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.portfolio_view_count} views"
