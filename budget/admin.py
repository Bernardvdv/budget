from django.contrib import admin

from .models import Items, Income, BaseConfig, Period


class ItemsAdmin(admin.ModelAdmin):
    list_filter = ('month',)


admin.site.register(Income)
admin.site.register(Items, ItemsAdmin)
admin.site.register(BaseConfig)
admin.site.register(Period)
