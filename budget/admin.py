from django.contrib import admin
from datetime import timedelta

from .models import BaseConfig, Category, Income, Items, Period


class ItemsAdmin(admin.ModelAdmin):
    list_filter = ('month',)
    save_as = True


class PeriodAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date']
    actions = ['duplicate_selected_periods']

    def duplicate_selected_periods(self, request, queryset):
        for period in queryset:
            new_period = period.duplicate()
            # self.message_user(request, f"Successfully duplicated {period.name} to {new_period.name}.")
    duplicate_selected_periods.short_description = "Duplicate selected periods"


admin.site.register(Income)
admin.site.register(Items, ItemsAdmin)
admin.site.register(BaseConfig)
admin.site.register(Period, PeriodAdmin)
admin.site.register(Category)
