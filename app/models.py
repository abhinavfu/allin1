from django.db import models

# Create your models here.


class AppCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    username = models.CharField(
        max_length=50, default=None, blank=True, null=True)
    name = models.CharField(max_length=50, default=None, blank=True, null=True)
    email = models.EmailField(default=None, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class App(models.Model):
    name = models.CharField(max_length=50, default=None, blank=True, null=True)
    link = models.URLField(default=None, blank=True, null=True)
    appCat = models.ForeignKey(AppCategory, on_delete=models.CASCADE)
    subCat = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    points = models.IntegerField()
    picapp = models.ImageField(upload_to="app/images/admin/",
                               default=None, blank=True, null=True)
    date = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.name


class UserPoints(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to="app/images/user/",
                                   default=None, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.name} | {self.app.name}'


class App_page_view_count(models.Model):
    app_home_view_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.app_home_view_count} views"
