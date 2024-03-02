from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Todo, CustomUser


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)


"""class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date']
"""

admin.site.register(Todo, TodoAdmin)
admin.site.register(CustomUser, UserAdmin)
