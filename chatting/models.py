from django.db import models
from users.models import users

# Create your models here.

class chatting(models.Model):
    question = models.TextField()
    answer = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    file = models.TextField(blank=True)
    class Meta:
        db_table = 'chatting'