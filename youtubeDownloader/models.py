from django.db import models

# Create your models here.


class Youtube_page_view_count(models.Model):
    home_view_count = models.IntegerField(default=0)
    yt_download_view_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.home_view_count} views"
