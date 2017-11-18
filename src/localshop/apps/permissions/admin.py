from django.contrib import admin

from localshop.apps.permissions import models


class CidrAdmin(admin.ModelAdmin):
    list_display = ['cidr', 'label']


class CredentialAdmin(admin.ModelAdmin):
    list_display = [
        'repository', 'access_key', 'created', 'comment', 'allow_upload']
    list_filter = ['repository', 'allow_upload']


admin.site.register(models.CIDR, CidrAdmin)
admin.site.register(models.Credential, CredentialAdmin)
