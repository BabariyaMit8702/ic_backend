from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15,null=True,blank=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    Profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    bio = models.CharField(max_length=50,default="")
    profile_pic = models.ImageField(upload_to='',default='profile.jpg')
    hobbie = models.CharField(max_length=30,default='')
    website = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=30,default='')
    location = models.CharField(max_length=15,default='')
    image = models.ImageField(upload_to='posts/',null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_like')
        ]


    def __str__(self):
        return self.user.username
    
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    body = models.CharField(max_length=100,default="empty")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username