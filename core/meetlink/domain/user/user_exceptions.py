from meetlink.models import Role
from rest_framework.exceptions import NotFound, ValidationError


class UserEmailOrPasswordIsInvalidException(Exception):
    def __init__(self):
        super().__init__("Email ou senha inválidos")


class LoginDataIsInvalidException(Exception):
    def __init__(self, message="Os dados de login passados são inválidos"):
        super().__init__(message)


class InvalidUserRoleException(Exception):
    def __init__(self, user_name: str, user_role: Role):
        super().__init__(
            (
                f"O usuário {user_name} com o cargo de {user_role} não pode"
                "ser atribuído a essa operação"
            )
        )


class ManagerIdNotPassedException(ValidationError):
    def __init__(self):
        super().__init__("O Id do gestor não foi passado")


class ManagerNotFoundException(NotFound):
    def __init__(self):
        super().__init__("O gestor solicitado não foi encontrado")
