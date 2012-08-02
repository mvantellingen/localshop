from django.contrib import admin

from localshop.apps.packages.models import Classifier, Package, Release, ReleaseFile


class ReleaseFileInline(admin.TabularInline):
    model = ReleaseFile


class PackageAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'created', 'modified', 'is_local']
    list_filter = ['is_local']
    search_fields = ['name']


class ReleaseAdmin(admin.ModelAdmin):
    inlines = [ReleaseFileInline]
    list_display = ['__unicode__', 'package', 'created', 'modified']
    list_filter = ['package']
    search_fields = ['version', 'package__name']
    ordering = ['-created', 'version']


class ReleaseFileAdmin(admin.ModelAdmin):
    list_filter = ['user', 'release__package']
    list_display = ['__unicode__', 'created', 'modified', 'md5_digest', 'url']


admin.site.register(Classifier)
admin.site.register(Package, PackageAdmin)
admin.site.register(Release, ReleaseAdmin)
admin.site.register(ReleaseFile, ReleaseFileAdmin)
