from django.contrib import admin

from . import models


class GolfClubAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'slug', 'phone', 'email')
    prepopulated_fields = {'slug': ('title_english',)}
    ordering = ['-created']


class LineUserAdmin(admin.ModelAdmin):
    list_display = ('line_user_id', 'line_display_name', 'golf_club', 'follow_status', 'fullname')
    list_filter = ('follow_status', 'golf_club__title_english')
    readonly_fields = ('line_user_id', 'line_display_name', 'golf_club', 'follow_status')
    ordering = ['-created']


admin.site.register(models.GolfClub, GolfClubAdmin)
admin.site.register(models.LineUser, LineUserAdmin)
