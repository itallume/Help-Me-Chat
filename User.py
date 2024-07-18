class User:
    def __init__(self, nickname, password):
        self.__nickname = nickname
        self.__password = password
        self.__quantidade_de_notas = 0
        self.__nota = 10
        self.__status = "Offline"
        
        
    @property
    def nickname(self):
        return self.__nickname
    
    @property
    def nota(self):
        return self.__nota
    
    @property
    def chat(self):
        return self.__chat
    
    @property
    def status(self):
        return self.__status

    @chat.setter
    def chat(self, newchat):
        self.__chat = newchat
    
    def addNota(self, new_nota):
        if self.__quantidade_de_notas == 0:
            self.__nota = 0
        self.__nota += new_nota
        self.__quantidade_de_notas += 1
        self.__nota = self.__nota / self.__quantidade_de_notas 

    def confirmPassword(self, password):
        return password == self.__password 
        
    def ChangeStatus(self):
        if self.__status == "Online":
            self.__status = "Offline"
            return self.__status
        
        self.__status = "Online"
        return self.__status
        
    def __eq__(self, outroObjeto):
        '''Método que vai possibilitar comparar chaves quando a chave for um objeto de outra classe'''
        return self.nota == outroObjeto.nota

    def __lt__(self, outroObjeto):
        '''Método que vai possibilitar comparar chaves quando a chave for um objeto de outra classe'''
        return self.nota < outroObjeto.nota
    
    def __gt__(self, outro_objeto):
        '''Método que possibilita comparar chaves quando a chave for um objeto de outra classe'''
        return self.nota > outro_objeto.nota
