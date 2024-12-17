from .models import Role


def sidebar_context(request):
    user = request.user

    return {"user": user, "SHOULD_VIEW_TOTEM_REDIRECT": (Role.SUPERADMIN, Role.TOTEM)}
