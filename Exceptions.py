class TipoInvalido(Exception):
    def __init__(self, mensagem):
        self.mensagem = mensagem

    def __str__(self):
        return f"{self.mensagem}"

class MuitasTentativas(Exception):
    def __init__(self, mensagem):
        self.mensagem = mensagem

    def __str__(self):
        return f"{self.mensagem}"