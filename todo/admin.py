from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    # ModelAdmin используется для кастомизации интерфейса администратора
    # Для отображения даты создания записи
    readonly_fields = ('date_created',)


admin.site.register(Todo, TodoAdmin)
