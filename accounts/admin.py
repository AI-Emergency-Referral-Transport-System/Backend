from django.contrib import admin

from accounts.models import OTPCode, User


admin.site.register(User)
admin.site.register(OTPCode)
