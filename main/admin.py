from django.contrib import admin
from .models import CustomUser,Profile,Post,Like,Comment,Follow
Like
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)