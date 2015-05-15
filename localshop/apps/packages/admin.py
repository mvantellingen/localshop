from django.contrib import admin

from localshop.apps.packages import models


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


class ReleaseFileInline(admin.TabularInline):
    model = models.ReleaseFile


class PackageAdmin(admin.ModelAdmin):
    list_display = ['repository', '__unicode__', 'created', 'modified', 'is_local']
    list_filter = ['is_local', 'repository']
    search_fields = ['name']


class ReleaseAdmin(admin.ModelAdmin):
    inlines = [ReleaseFileInline]
    list_display = ['__unicode__', 'package', 'created', 'modified']
    list_filter = ['package__repository', 'package']
    search_fields = ['version', 'package__name']
    ordering = ['-created', 'version']


class ReleaseFileAdmin(admin.ModelAdmin):
    list_filter = ['user', 'release__package__repository']
    list_display = ['__unicode__', 'created', 'modified', 'md5_digest', 'url']


admin.site.register(models.Classifier)
admin.site.register(models.Repository, RepositoryAdmin)
admin.site.register(models.Package, PackageAdmin)
admin.site.register(models.Release, ReleaseAdmin)
admin.site.register(models.ReleaseFile, ReleaseFileAdmin)
