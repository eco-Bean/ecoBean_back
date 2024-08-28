from django.db import models
from users.models import users

class Challenge(models.Model):
    title = models.TextField()  # The title of the challenge

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'Challenge'

class User_Challenge_mapping(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    image = models.TextField(null=True, blank=True)  # URL to the image
    achieve_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.nickname}'s {self.challenge.title} Challenge"
    class Meta:
        db_table = 'User_Challenge_mapping'