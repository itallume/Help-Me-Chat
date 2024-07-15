class Chat:
    def __init__(self, assunto:str, intensidade:int):
        self.assunto = assunto
        self.intensidade = intensidade
        self.status = "desconected"
        self.__undecided = None
        self.__Conseheiro = None


    @property
    def undecided(self):
        return self.__undecided
    
    @undecided.setter
    def undecided (self, undecided):
        self.__undecided = undecided

    @property
    def Conselheiro(self):
        return self.__Conseheiro

    @Conselheiro.setter
    def Conselheiro(self, Conselheiro):
        self.__Conseheiro = Conselheiro


    # def addOnChat(self, nickname, socket):
    #     "O método `addOnChat` adiciona um novo participante à lista de clientes de um chat."
    #     self.clients.append([nickname, socket])
        
    def getClients(self):
        "O método `getClients` retorna a lista de clientes atualmente presentes no chat."
        usersOnChat = []
        for user in self.clients:
            usersOnChat.append(user)
        return usersOnChat
    
    def changeStatus(self):
        "O método `changeStatus` altera o status do chat entre desconectado e ativo. muda o status atual do chat e retorna o novo status."
        
        if self.status == "desconected":
            self.status = "active"
        else:
            self.status = "desconected"
            
        return self.status