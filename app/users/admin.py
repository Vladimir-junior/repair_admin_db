from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.admin.sites import AdminSite
from django.db.models.functions import Trunc
from django.db.models import Avg, Count, Min, Sum, F, DateField

from users.models import (
    User,
    Position,
    SpareParts,
    RepairOrder,
    PurchaseOrder,
    StorySpareParts
)


class MyAdminSite(AdminSite):

    def index(self, request, extra_context=None):
        outcome_history = (StorySpareParts.objects.annotate(
            period=Trunc("timestamp", "month", output_field=DateField())
        ).values('period').annotate(
            total_price=Sum(F('spare_parts__price_for_1') * F('count')),
        ).all())
        income_history = (RepairOrder.objects.annotate(
            period=Trunc("date_start", "month", output_field=DateField())
        ).values('period').annotate(
            total_price=Sum('price'),
        ).all())


        extra_context = extra_context or {}
        extra_context['outcome'] = outcome_history
        extra_context['income'] = income_history
        return super().index(request, extra_context=extra_context)


site = MyAdminSite()


class UserAdmin(admin.ModelAdmin):
    list_display = ["user_full_name", "position"]

    search_fields = ["first_name", "last_name"]

    fields = [
        "first_name",
        "last_name",
        "email",
        "position",
    ]

    @admin.display(empty_value="-")
    def user_full_name(self, obj: User):
        return f'{obj.last_name} {obj.first_name}'


class PositionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

    @admin.display(empty_value="-")
    def num_users(self, obj: Position):
        return obj.num_users


class RepairOrderAdmin(admin.ModelAdmin):
    list_display = ["user_full_name", "status", "description_device", "date_start", "date_end", "worker", "price"]
    search_fields = ["user__first_name", "user__last_name", "description_device"]

    @admin.display(empty_value="-")
    def user_full_name(self, obj: User):
        return f'{obj.user.last_name} {obj.user.first_name}'


class SparePartsAdmin(admin.ModelAdmin):
    list_display = ["name", "count", "price_for_1", "description"]
    search_fields = ["name"]


class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ["description_device_or_detail", "amount", "date_create", "date_supplies", "provider", "price"]
    search_fields = ["description_device_or_detail"]


class StorySparePartsAdmin(admin.ModelAdmin):
    list_display = ["spare_parts", "user_full_name", "emergence", "count", "description", "timestamp"]
    search_fields = ["spare_parts__name", "user__first_name", "user__last_name"]


    @admin.display(empty_value="-")
    def user_full_name(self, obj: User):
        return f'{obj.user.last_name} {obj.user.first_name}'

site.register(StorySpareParts, StorySparePartsAdmin)
site.register(PurchaseOrder, PurchaseOrderAdmin)
site.register(SpareParts, SparePartsAdmin)
site.register(RepairOrder, RepairOrderAdmin)
site.register(Position, PositionAdmin)
site.register(User, UserAdmin)


