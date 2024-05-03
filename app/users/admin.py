from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import User




class UserAdmin(admin.ModelAdmin):
    list_display = ["user_full_name"]

    search_fields = ["first_name", "last_name"]

    fields = [
        "first_name",
        "last_name",
        "email",

    ]

    @admin.display(empty_value="-")
    def user_full_name(self, obj: User):
        return f'{obj.last_name} {obj.first_name}'


admin.site.register(User, UserAdmin)


admin.site.unregister(Group)