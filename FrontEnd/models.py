from django.db import models
# Create your models here.


from django.contrib.auth.models import User


class BlogUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='Profile', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Blog(models.Model):
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="image", null=True, blank=True)

    def __str__(self):
        return self.title
