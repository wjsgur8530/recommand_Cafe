from django.contrib import admin

# Register your models here.
from CafeApp.models import *

admin.site.register(Cafe)
admin.site.register(CafeImage)
admin.site.register(CafeType)
admin.site.register(CafeTheme)
admin.site.register(CafeScore)
admin.site.register(CafeOrder)
