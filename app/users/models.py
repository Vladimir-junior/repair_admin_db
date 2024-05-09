from datetime import datetime
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager as BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(_("username"), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True, blank=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    position = models.ForeignKey(
        'Position',
        related_name='position',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Position(models.Model):
    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class RepairOrder(models.Model):
    class Meta:
        verbose_name = 'Repair Order'
        verbose_name_plural = 'Repair Orders'

    user = models.ForeignKey(
        User,
        related_name='users',
        on_delete=models.CASCADE,
        null=True
    )
    Status_CHOICES = {
        "READY": "Готов",
        "IN_PROGRESS": "В работе",
        "ACCEPTED": "Принят",
    }
    status = models.CharField(max_length=70, choices=Status_CHOICES, default="")
    description_device = models.CharField(max_length=300, blank=True)
    price = models.IntegerField(blank=True, null=True)
    date_start = models.DateField(blank=True)
    date_end = models.DateField(blank=True, null=True)
    worker = models.ForeignKey(
        User,
        related_name='worker',
        on_delete=models.CASCADE,
        null=True
    )

class SpareParts(models.Model):
    class Meta:
        verbose_name = 'Spare Part'
        verbose_name_plural = 'Spare Parts'
    name = models.CharField(max_length=200, blank=True)
    count = models.IntegerField(blank=True)
    price_for_1 = models.FloatField(blank=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    class Meta:
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
    description_device_or_detail = models.CharField(max_length=300, blank=True)
    amount = models.IntegerField(blank=True)
    date_create = models.DateField(blank=True)
    date_supplies = models.DateField(blank=True)
    provider = models.CharField(max_length=100, blank=True)
    price = models.FloatField(blank=True)

    def __str__(self):
        return self.description_device_or_detail

class StorySpareParts(models.Model):
    class Meta:
        verbose_name = 'Story Spare Part'
        verbose_name_plural = 'Story Spare Parts'
    spare_parts = models.ForeignKey(
        SpareParts,
        related_name='spare_parts',
        on_delete=models.CASCADE,
        null=True
    )
    user = models.ForeignKey(
        User,
        related_name='users_Story_spare_parts_user',
        on_delete=models.CASCADE,
        null=True
    )
    EMERGENCE_CHOICES = {
        "SUPPLY": "Поставка",
        "REPAIR": "Ремонт",
        "MARRIAGE": "Брак",
    }
    emergence = models.CharField(max_length=70, choices=EMERGENCE_CHOICES, default="")
    count = models.IntegerField(blank=True)
    description = models.CharField(max_length=200, blank=True)
    timestamp = models.DateField(blank=True)
