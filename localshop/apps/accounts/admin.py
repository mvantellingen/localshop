from django.contrib import admin

from localshop.apps.accounts import models


class AccessKeyAdmin(admin.ModelAdmin):
    model = models.AccessKey
    list_display = ['user', 'created', 'last_usage']


class TeamMemberInline(admin.TabularInline):
    model = models.TeamMember
    list_display = ['user', 'role']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [TeamMemberInline]


admin.site.register(models.AccessKey, AccessKeyAdmin)
admin.site.register(models.Team, TeamAdmin)
