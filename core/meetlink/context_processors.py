from .models import Role


def view_context(request):
    user = request.user

    return {
        "user": user,
        "SHOULD_VIEW_TOTEM_REDIRECT": (Role.SUPERADMIN, Role.TOTEM),
        "SHOULD_VIEW_FINISH_CALL_BUTTON": (Role.SUPERADMIN, Role.MANAGER),
    }
