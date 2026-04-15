from django.contrib import admin

from accounts.models import OTPCode, Profile, User


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(OTPCode)
