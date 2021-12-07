from django.contrib import admin
from finance.models import Finance
# Register your models here.


@admin.register(Finance)
class FinanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('name',)
