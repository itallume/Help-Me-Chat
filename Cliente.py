import socket
import threading 
import socket
import threading
import sys
from Exceptions import *

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.CodesTranslate = None
        self.conected = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.setDict()

    def setDict(self):

        self.CodesTranslate = {
        "198": "Voltado ao menu de escolha de login",
        "200": "login efetuado",
        "201": "Usuário ou senha incorreto",
        "203": "Usuário já está online",
        "205": "Nome de usuário deve ser maior que 3 e menor que 20",
        "207": "Senha deve ter no minimo 6 caracteres",
        "210": "Cadastro efetuado",
        "211": "Nome de usuário já existente, tente outro",
        "220": "Tipo setado",
        "221": "Tipo inexistente",
        "222": "Escolha o chat que deseja entrar",
        "223": "O chat escolhido não está mais diponivel, escolha outro",
        "230": "Tema definido",
        "231": "Intensidade inexistente", 
        "233": "Assunto inválido",
        "240": "Comunicação feita",
        "250": "Conectado a um chat",
        "261": "Nota inválida",
        "270": "O chat foi encerrado",
        "299": "Muitas tentativas de login, tente mais tarde.",
        "301": "Opção inválida.",
        "555": "Erro no servidor"

    }
        
    def getTranslate(self, code:str) -> str:
        try:
            translate = self.CodesTranslate[code]
        except KeyError:
            return None
        return translate
    
    def Validate_login(self, userName:str, password:str):
        """ Parameters: userName:str, password:str
            Returns: server response code str
            codes that can be returned: "200", "201", "299"
            these codes can be translated into the .getTranslate(enterCodeHere) method 
        """    
        log = f"login {userName} {password}"
        self.sock.send(log.encode("utf-8"))
        serverResponse = self.sock.recv(1024).decode("utf-8")
        if serverResponse == "299":
            self.sock.close()
        return serverResponse

    def Validate_register(self, userName, password):
        
        signup = f"register {userName} {password}"
        self.sock.send(signup.encode("utf-8"))
        validate_signup = self.sock.recv(4096).decode("utf-8")
        return validate_signup
    
    def setTypeCounselor(self) -> str:
       
        self.sock.send(f"type&counselor".encode("utf-8"))
        response_server = self.sock.recv(4096).decode("utf-8")
        return response_server
    
    def setTypeUndecided(self, subject:str, intensity:str) -> str:

        self.sock.send(f"type&undecided&{subject}&{intensity}".encode("utf-8"))
        response_server = self.sock.recv(4096).decode("utf-8")
        return response_server

    def set_assunto(self):
        
        try:
            assert len(assunto) > 0
            if len(assunto) <= 3:
                self.set_assunto()
        except Exception:
            print("Escreva um assunto Válido!")
            self.set_assunto()
            
        print("Escolha a intensidade:\n1: Baixa\n2: Média\n3: Alta")
        self.set_intensity(assunto)
        return
        
    def waitingConnection(self, response_server):   

        if response_server[0] == "270":
            print(response_server[0], f"Assunto: {response_server[1]} Intensidade: {response_server[2]}")
            self.conected = True
            print("Chat iniciado!")
            threading.Thread(target=self.escutar, args=()).start()
            self.DigitOnchat()
            
    def escutar(self):
        while True:
            response_server = self.sock.recv(4096).decode("utf-8").split("&")
            if not response_server[0] == "270":
                  # Limpa a linha atual
                sys.stdout.write(f"\r{response_server}\n")  # Imprime a mensagem
                sys.stdout.write(">> ")  # Reposiciona o prompt de input
                sys.stdout.flush()
            else:
                print("VOCE FOI DESCONECTADO!!!")
                self.conected = False 
                break
            
    def DigitOnchat(self):
    
        while True: 
            if self.conected:
                break
            msg = input(">> ")
            self.sock.send(f"msg&{msg}".encode("utf-8"))

    def backToLoginChoice(self):
        self.sock.send("back".encode("utf-8"))
        self.sock.recv(4096).decode("utf-8")

client = Client("localhost", 12345)
print(f"Conectado ao servidor na porta {client.port}")
print("\n\n=============Bem-Vindo ao Conselheiro Virtual!=============\n")
try:
    while True:
        login = False
        while True:
            print("Escolha uma opção:")
            print("\n1 - login\n2 - signup\n")
            loginChoice = input("Opção: ")
            if loginChoice not in ["1", "2"]:  
                print("Digite uma opção válida (1 ou 2)" )
                continue
            
            while True:
                print("Digite 'Voltar' em qualquer campo para retornar ao menu anterior.")
                userName = input("\nUsuario: ")
                if userName.upper() == "VOLTAR":
                    client.backToLoginChoice()
                    break
                password = input("Senha: ")
                if password.upper() == "VOLTAR":
                    client.backToLoginChoice()
                    break
                if loginChoice == "1":
                    responseCode = client.Validate_login(userName, password)
                    msgTranslate = client.getTranslate(responseCode)
                    print(msgTranslate)
                    if responseCode == "200":
                        login = True
                        break
                    elif responseCode == "299":
                        raise MuitasTentativas(msgTranslate)
                    else:
                        continue
                else:
                    responseCode = client.Validate_register(userName, password)
                    msgTranslate = client.getTranslate(responseCode)
                    print(msgTranslate)
                    if responseCode == "210":
                        login = True
                        break
                    else: 
                        continue
            if login:
                break              
        if login:
            break
        
    print()

    while True:
        
        print("O que deseja ser? ")
        print("1. Indeciso(a)\n2. Conselheiro")
        type = input("Escolha (1/2): ")
        if type not in ["1", "2"]:  
            print("Digite uma opção válida (1 ou 2)" )
            continue

        if type == "1":   
            while True:
                assunto = input("Qual será o assunto? ")
                print("Escolha a intensidade:\n1: Baixa\n2: Média\n3: Alta")
                intensidade = input("Intensidade: ")
                if intensidade not in ["1", "2", "3"]:
                    print("Escolha uma opção válida (1, 2 ou 3)")
                    continue
                responseCode = client.setTypeUndecided(assunto, intensidade)
                if responseCode == "231" or responseCode == "233":
                    print(client.getTranslate(responseCode))
                    continue
                else:
                    print(responseCode)
                    threading.Thread(target=client.escutar, args=()).start()
                    client.DigitOnchat()
                    break
                #fazer parte de conectar no chat          
        else:
            response = client.setTypeCounselor().split("&")
            print(response)
            responseCode = response[0]
            print(client.getTranslate(responseCode))
            
            if responseCode == "222":
                for chat in response:
                    if chat == "222":
                        continue
                    print(chat)
            threading.Thread(target=client.escutar, args=()).start()
            client.DigitOnchat()
            break
except MuitasTentativas as e:
    print("")