from django.contrib import admin

# Register your models here.

from accounts.models import PendingRegistration

admin.site.register([PendingRegistration])