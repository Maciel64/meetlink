class UserEmailOrPasswordIsInvalidException(Exception) :
    def __init__(self) :
        super().__init__("Email ou senha inválidos")


class LoginDataIsInvalidException(Exception) :
    def __init__(self, message = "Os dados de login passados são inválidos") :
        super().__init__(message)