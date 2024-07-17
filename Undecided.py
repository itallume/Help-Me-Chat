class Undecided:
    def __init__(self, username, socket) -> None:
        self.__username = username
        self.__socket = socket
    
    @property
    def username(self) -> str:
        return self.__username
    
    @username.setter
    def username(self, username):
        self.__username = username
        
    @property
    def socket(self):
        return self.__socket
    
    @socket.setter
    def socket(self, socket):
        self.__socket = socket