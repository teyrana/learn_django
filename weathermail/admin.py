from django.contrib import admin

# Register your models here.

from .models import City, Recipient

admin.site.register(City)
admin.site.register(Recipient)
