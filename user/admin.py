from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

User = get_user_model()
# Register your models here.


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = ["username", "first_name", "amount_expense",
                    'last_name', 'email', "is_superuser"]
    search_fields = ["first_name", 'last_name', 'email', 'username']
    list_editable = ["amount_expense", ]
