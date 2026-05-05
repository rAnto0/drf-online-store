from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Profile, Address


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Профили"


class CustomUserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Address)
