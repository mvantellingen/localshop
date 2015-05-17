from django.contrib import admin

from localshop.apps.accounts import models


class TeamMemberInline(admin.TabularInline):
    model = models.TeamMember
    list_display = ['user', 'role']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [TeamMemberInline]


admin.site.register(models.Team, TeamAdmin)
