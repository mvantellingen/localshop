from django.contrib import admin

from localshop.apps.permissions import models


class CidrAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.CIDR, CidrAdmin)

