from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class Contact_table(models.Model):
    user = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    problem = models.CharField(max_length = 200)
    desc = models.CharField(max_length = 400)

    def __str__(self):
        return self.user.username


    