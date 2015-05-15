from django.contrib import admin

from localshop.apps.permissions import models


class TeamMemberInline(admin.TabularInline):
    model = models.TeamMember
    list_display = ['user', 'role']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [TeamMemberInline]


class CidrAdmin(admin.ModelAdmin):
    list_display = ['cidr', 'label']


class CredentialAdmin(admin.ModelAdmin):
    list_display = ['creator', 'access_key', 'created', 'comment']


admin.site.register(models.Team, TeamAdmin)
admin.site.register(models.CIDR, CidrAdmin)
admin.site.register(models.Credential, CredentialAdmin)
