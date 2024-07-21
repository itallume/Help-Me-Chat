class User:
    def __init__(self, nickname, password):
        self.__nickname = nickname
        self.__password = password
        self.__numberOfNotes = 0
        self.__note = 10
        self.__status = "Offline"
        
        
    @property
    def nickname(self):
        return self.__nickname
    
    @property
    def note(self):
        return self.__note
    
    @property
    def chat(self):
        return self.__chat
    
    @property
    def status(self):
        return self.__status

    @chat.setter
    def chat(self, newchat):
        self.__chat = newchat
    
    def addnote(self, new_note):
        if self.__numberOfNotes == 0:
            self.__note = 0
        self.__note += new_note
        self.__numberOfNotes += 1
        self.__note = self.__note / self.__numberOfNotes 

    def confirmPassword(self, password:str) -> bool: 
        return password == self.__password 
        
    def ChangeStatus(self):
        if self.__status == "Online":
            self.__status = "Offline"
            return self.__status
        
        self.__status = "Online"
        return self.__status
        
    def __eq__(self, outroObjeto):
        '''Método que vai possibilitar comparar chaves quando a chave for um objeto de outra classe'''
        return self.note == outroObjeto.note

    def __lt__(self, outroObjeto):
        '''Método que vai possibilitar comparar chaves quando a chave for um objeto de outra classe'''
        return self.note < outroObjeto.note
    
    def __gt__(self, outro_objeto):
        '''Método que possibilita comparar chaves quando a chave for um objeto de outra classe'''
        return self.note > outro_objeto.note
