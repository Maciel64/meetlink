class CallNotFoundException(Exception) :
    def __init__(self):
        super().__init__("Chamada solicitada não encontrada")