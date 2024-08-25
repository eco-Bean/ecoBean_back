# main/models.py

from django.db import models

class Mission(models.Model):
    content = models.TextField()  # Description of the mission
    point = models.IntegerField()  # Points awarded for completing the mission

    def __str__(self):
        return self.content
    class Meta:
        db_table = 'Mission'

from django.db import models
from users.models import users  # Import the Users model from the users app

class Mission_User_mapping(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)  # User associated with the mission
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)  # Mission associated with the user
    date = models.DateField()  # Date when the mission was assigned
    achieve = models.BooleanField(default=False)  # Whether the mission was achieved

    def __str__(self):
        return f"{self.user.nickname} - {self.mission.content}"
    class Meta:
        db_table = 'Mission_User_mapping'
