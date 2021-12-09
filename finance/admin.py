from django.contrib import admin
from finance.models import Finance, Cost
# Register your models here.


@admin.register(Finance)
class FinanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('name',)


@admin.register(Cost)
class FinanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'finance', "amount_cost")
    list_filter = ('name',)
