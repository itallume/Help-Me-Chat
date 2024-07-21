class TipoInvalido(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"{self.msg}"

class MuitasTentativas(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"{self.msg}"
    
class InvalidIntensity(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return f"{self.msg}"
    
class InvalidChat(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return f"{self.msg}"