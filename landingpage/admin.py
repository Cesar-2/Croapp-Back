from django.contrib import admin

# Register your models here.
from django.contrib import admin
from landingpage.models import LandingPage
# Register your models here.


@admin.register(LandingPage)
class FinanceAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')
    list_filter = ('email',)
