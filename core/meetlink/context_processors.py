from .models import Role


def sidebar_context(request) :
    user = request.user
    
    return {
        "user": user,
        "roles": Role.__dict__
    }