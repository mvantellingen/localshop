from django.contrib import admin

from localshop.packages import models


@admin.register(models.Classifier)
class ClassifierAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


class ReleaseFileInline(admin.TabularInline):
    model = models.ReleaseFile


@admin.register(models.Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['repository', '__str__', 'created', 'modified', 'is_local']
    list_filter = ['is_local', 'repository']
    search_fields = ['name']


@admin.register(models.Release)
class ReleaseAdmin(admin.ModelAdmin):
    inlines = [ReleaseFileInline]
    list_display = ['__str__', 'package', 'created', 'modified']
    list_filter = ['package__repository', 'package']
    search_fields = ['version', 'package__name']
    ordering = ['-created', 'version']


@admin.register(models.ReleaseFile)
class ReleaseFileAdmin(admin.ModelAdmin):
    list_filter = ['user', 'release__package__repository']
    list_display = ['__str__', 'created', 'modified', 'md5_digest', 'url']
