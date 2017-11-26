from django.contrib import admin
from .models import Room
# Register your models here.

admin.site.register(
    Room,
    list_display=["id", "name", ],
    list_display_links=["id", "name"],
)
