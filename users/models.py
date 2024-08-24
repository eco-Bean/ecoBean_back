from django.db import models

# Create your models here.
class users(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.TextField(default="user")
    profile_image = models.TextField(null=True)
    point = models.IntegerField(default=0)
    social_type = models.CharField(max_length=50)
    class Meta:
        db_table = 'users'