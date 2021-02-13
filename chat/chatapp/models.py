from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class AuthUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    user_img = models.ImageField(upload_to='users')

    def __str__(self):
        return 'user image'


class Post(models.Model):
    author = models.ForeignKey(
        AuthUser, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    img = models.ImageField(upload_to='posts')
    created_date = models.DateTimeField(default=timezone.now())
    published_at = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def appproved_comments(self):
        return self.comments.filter(approved_comments=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("chatapp:post", kwargs={"pk": self.pk})


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    approved = models.BooleanField(default=False)

    def approve_comment(self):
        self.approved = True
        self.save

    def __str__(self):
        return self.content
    # get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})
