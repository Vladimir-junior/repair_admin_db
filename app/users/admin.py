from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import User, Position, Repair_order, Spare_parts, Purchase_order, Story_spare_parts




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


class PositionAdmin(admin.ModelAdmin):
    list_display = ["name"]

    @admin.display(empty_value="-")
    def num_users(self, obj: Position):
        return obj.num_users


class Repair_orderAdmin(admin.ModelAdmin):
    list_display = ["user_full_name", "status", "description_device", "date_start", "date_end", "worker"]

    @admin.display(empty_value="-")
    def user_full_name(self, obj: User):
        return f'{obj.user.last_name} {obj.user.first_name}'

class Spare_partsAdmin(admin.ModelAdmin):
    list_display = ["name", "count", "price_for_1", "description"]

class Purchase_orderAdmin(admin.ModelAdmin):
    list_display = ["description_device_or_detail", "amount", "date_create", "date_supplies", "provider", "price"]

class Story_spare_partsAdmin(admin.ModelAdmin):
    list_display = ["spare_parts", "user_full_name", "purchase_order", "count", "description", "timestamp"]

    @admin.display(empty_value="-")
    def user_full_name(self, obj: User):
        return f'{obj.user.last_name} {obj.user.first_name}'

admin.site.register(Story_spare_parts, Story_spare_partsAdmin)
admin.site.register(Purchase_order, Purchase_orderAdmin)
admin.site.register(Spare_parts, Spare_partsAdmin)
admin.site.register(Repair_order, Repair_orderAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)