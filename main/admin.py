# main/admin.py

from django.contrib import admin
from .models import Mission, Mission_User_mapping

admin.site.register(Mission)
admin.site.register(Mission_User_mapping)
