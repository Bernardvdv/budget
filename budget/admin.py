from django.contrib import admin

from .models import Items, Income, BaseConfig


admin.site.register(Income)
admin.site.register(Items)
admin.site.register(BaseConfig)
