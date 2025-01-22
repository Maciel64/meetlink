from django.contrib import admin
from django.http import Http404

from .models import Call, Role, Subject, User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)

    def has_permission(self, request):
        if not request.user.is_authenticated or request.user.role != Role.SUPERADMIN:
            raise Http404("Página não encontrada.")
        return super().has_permission(request)


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ("responsible", "interpreter", "subject", "created_at")
    search_fields = ("responsible__username", "subject__name", "description")
    list_filter = ("created_at",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
