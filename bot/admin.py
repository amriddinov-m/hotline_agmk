from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html

from bot.models import EEUser, Category, Application


@admin.register(EEUser)
class EEUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = 'id', 'category', 'status_colored', 'comment', 'creator'

    def status_colored(self, obj):
        status_color_mapping = {
            'created': 'white',
            'progress': 'orange',
            'completed': 'green',
        }
        color = status_color_mapping.get(obj.status, 'black')
        return format_html(
            '<span style="color:{};">{}</span>',
            color,
            obj.get_status_display()
        )

    status_colored.short_description = 'Статус'


admin.site.unregister(User)
admin.site.unregister(Group)
