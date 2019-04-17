from django.contrib import admin

from localshop.permissions import models


@admin.register(models.CIDR)
class CidrAdmin(admin.ModelAdmin):
    list_display = ['cidr', 'label']


@admin.register(models.Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = [
        'repository', 'access_key', 'created', 'comment', 'allow_upload']
    list_filter = ['repository', 'allow_upload']
