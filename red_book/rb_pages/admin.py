from django.contrib import admin

from rb_pages.models import Favorite, Species

# Register your models here.
admin.site.register(Species)
admin.site.register(Favorite)