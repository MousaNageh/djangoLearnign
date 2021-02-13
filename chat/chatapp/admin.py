from django.contrib import admin
from chatapp.models import AuthUser, Post, Comment
# Register your models here.
admin.site.register(AuthUser)
admin.site.register(Post)
admin.site.register(Comment)
