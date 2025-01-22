from django.contrib.admin import AdminSite
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from meetlink.admin import CallAdmin, SubjectAdmin, UserAdmin
from meetlink.models import Call, Role, Subject, User


class CustomAdminSite(AdminSite):
    site_title = _("Administração do Sistema")
    site_header = _("Administração")
    index_title = _("Painel Administrativo")

    def has_permission(self, request):
        if not request.user.is_authenticated or request.user.role != Role.SUPERADMIN:
            raise Http404("Página não encontrada.")
        return super().has_permission(request)


admin_site = CustomAdminSite()
admin_site.register(User, UserAdmin)
admin_site.register(Call, CallAdmin)
admin_site.register(Subject, SubjectAdmin)
