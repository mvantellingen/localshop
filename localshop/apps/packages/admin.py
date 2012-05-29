from django.contrib import admin

from localshop.apps.packages.models import Classifier, Package, Release, ReleaseFile

admin.site.register(Classifier)
admin.site.register(Package)
admin.site.register(Release)
admin.site.register(ReleaseFile)
