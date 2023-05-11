from django.db import models

# Create your models here.


class Bloger(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, default="", blank=True, null=True)
    email_verified = models.BooleanField(default=False, null=False)
    pic = models.ImageField(upload_to="blogprofile/",
                            default=None, blank=True, null=True)
    bio = models.TextField(default="", blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class CreatePost(models.Model):
    bloger = models.ForeignKey(Bloger, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(default=True, blank=True, null=True)

    pic1 = models.ImageField(upload_to="blogimages/",
                             default=None, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bloger.username

# models.ForeignKey(Bloger, on_delete=models.CASCADE)


class Following(models.Model):
    username = models.CharField(max_length=50)
    follows = models.ForeignKey(Bloger, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username} --> {self.follows.username}'


class Follower(models.Model):
    username = models.CharField(max_length=50)
    follower = models.ForeignKey(Bloger, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username} <-- {self.follower.username}'


class Like(models.Model):
    bloger = models.ForeignKey(Bloger, on_delete=models.CASCADE)
    post = models.ForeignKey(CreatePost, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False, null=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.bloger.username} --> post id : {self.post.id}'


class Comment(models.Model):
    bloger = models.ForeignKey(Bloger, on_delete=models.CASCADE)
    post = models.ForeignKey(CreatePost, on_delete=models.CASCADE)
    Commented = models.CharField(
        max_length=200, default="", blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bloger.username
