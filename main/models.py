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
    profile_pic = models.ImageField(upload_to='profile_pics/',default='default.png')
    hobbie = models.CharField(max_length=30,default='')
    website = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.user.username
    
# class post(models.Model):
#     user = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=30,default='')
#     location = models.CharField(max_length=15,default='')
#     image = models.ImageField(upload_to='posts/',null=True,blank=True)
#     created_at = models.DateField(auto_now_add=True)

