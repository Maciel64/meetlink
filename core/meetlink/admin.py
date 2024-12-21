from django.contrib import admin

from .models import Call, Subject, User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ("responsible", "subject", "created_at")
    search_fields = ("responsible__username", "subject__name", "description")
    list_filter = ("created_at",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
