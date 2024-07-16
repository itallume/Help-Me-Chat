class Counselor:
    def __init__(self) -> None:
        self.__username
        self.__socket
    
    @property
    def username(self):
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