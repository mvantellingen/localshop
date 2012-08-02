from django.contrib import admin

from localshop.apps.permissions import models


class CidrAdmin(admin.ModelAdmin):
    list_display = ['cidr', 'label']

admin.site.register(models.CIDR, CidrAdmin)
