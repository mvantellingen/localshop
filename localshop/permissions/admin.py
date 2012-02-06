from django.contrib import admin

from localshop.permissions import models


class CidrAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.CIDR, CidrAdmin)

