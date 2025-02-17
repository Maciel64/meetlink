from django.contrib.auth.models import AnonymousUser

from .models import Role


def view_context(request):
    user = request.user

    if isinstance(user, AnonymousUser):
        return {"user": user}

    return {
        "SHOULD_VIEW_TOTEM_REDIRECT": user.role in (Role.SUPERADMIN, Role.TOTEM),
        "SHOULD_VIEW_FINISH_CALL_BUTTON": user.role in (Role.SUPERADMIN, Role.MANAGER),
        "CANNOT_EDIT_CALL": user.role not in (Role.SUPERADMIN, Role.MANAGER),
        "SHOUD_VIEW_SUPERADMIN_REDIRECT": user.role in (Role.SUPERADMIN),
    }
