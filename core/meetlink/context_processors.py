from .models import Role


def view_context(request):
    user = request.user

    return {
        "user": user,
        "SHOULD_VIEW_TOTEM_REDIRECT": user.role in (Role.SUPERADMIN, Role.TOTEM),
        "SHOULD_VIEW_FINISH_CALL_BUTTON": user.role in (Role.SUPERADMIN, Role.MANAGER),
    }
