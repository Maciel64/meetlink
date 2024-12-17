class CallNotFoundException(Exception):
    def __init__(self):
        super().__init__("Chamada solicitada não encontrada")


class CallIdNotPassedException(Exception):
    def __init__(self):
        super().__init__("O Id da chamada não foi passado")


class EditCallFormException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
