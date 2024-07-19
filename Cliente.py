import socket
import threading 
import socket
import threading
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
    
        # if validate_login[0] == "200": 
        #     print(validate_login) #Login efetuado com Sucesso!
        
        # if validate_login[0] == "299": 
        #     print(validate_login)
        #     self.Validate_login()

        # while validate_login[0] == "201":
        #      #translate bug 
        #     print(self.CodesTranslate[validate_login[0]]) #Login nao efetuado, Usuário ou Senha incorretos!
        #     self.Validate_login()
        
        # print(f"Servidor: {validate_login}")
        # print("1. Indeciso(a)\n2. Conselheiro")
        # self.set_type()

    def Validate_register(self, userName, password):
        """
        `Validate_register` inicia o processo de registro, envia as informações ao servidor, trata diferentes códigos de resposta e,
          em caso de sucesso, permite ao usuário escolher entre ser um Indeciso(a) ou Conselheiro(a), chamando `set_type`. 
          Em caso de falha (nome de usuário já existente), solicita novas informações de registro.
        """
        signup = f"register {userName} {password}"
        self.sock.send(signup.encode("utf-8"))
        validate_signup = self.sock.recv(4096).decode("utf-8")
        return validate_signup
    
        # if validate_signup[0] == "210":
        #     print("\n",self.CodesTranslate[validate_signup[0]]) #Cadastro efetuado com Sucesso!
            
        # while validate_signup[0] == "211": 
        #     print("\n",self.CodesTranslate[validate_signup[0]])
        #     print("Tente Novamente\n") #Nome de Usuario ja Existente, tente novamente!
        #     self.Validate_register()
        
        # print(f"Servidor: {validate_signup}")
        # print("1. Indeciso(a)\n2. Conselheiro(a)")
        # self.set_type(validate_signup)
        
    def setTypeCounselor(self) -> str:
        """
        `set_type` permite ao usuário escolher entre ser Indeciso(a) ou Conselheiro(a). 
        Em seguida, solicita informações adicionais conforme a escolha do usuário (assunto ou espera por um(a) Indeciso(a)), 
        chamando métodos apropriados como `set_assunto` ou `waitingConnection`.
        """
        self.sock.send(f"type&counselor".encode("utf-8"))
        response_server = self.sock.recv(4096).decode("utf-8")
        return response_server
    
    def setTypeUndecided(self, subject:str, intensity:str) -> str:

        self.sock.send(f"type&undecided&{subject}&{intensity}".encode("utf-8"))
        response_server = self.sock.recv(4096).decode("utf-8")
        return response_server
        
        if response_server[0] == "231":
            print(self.CodesTranslate[response_server[0]])
            self.set_intensity(assunto, self.sock)
        else:
            print("\nProcurando por um(a) Indeciso(a)...\n")
            self.waitingConnection(response_server)
            return


        
    def set_assunto(self):
        """
        `set_assunto` solicita ao usuário que forneça um assunto. 
        Verifica se o assunto tem mais de 3 caracteres e, se não, solicita novamente. 
        Em seguida, pede ao usuário que escolha a intensidade do assunto e chama o método `set_intensity` passando o assunto como argumento.
        """
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
        """
        `waitingConnection` é responsável por lidar com a resposta do servidor após solicitar a criação de um chat ou ao entrar em um chat existente. 
        Se o código da resposta for "270" (indicação de sucesso na criação ou entrada no chat), imprime informações sobre o chat (assunto e intensidade), 
        define `conected` como True (indicando que o cliente está conectado ao chat) e inicia uma nova thread para escutar mensagens do chat (`escutar`). 
        Em seguida, chama o método `DigitOnchat` para permitir que o usuário envie mensagens para o chat.
        """

        if response_server[0] == "270":
            print(response_server[0], f"Assunto: {response_server[1]} Intensidade: {response_server[2]}")
            self.conected = True
            print("Chat iniciado!")
            threading.Thread(target=self.escutar, args=()).start()
            self.DigitOnchat()
            
    def escutar(self):
        """
        `escutar` é um método responsável por ouvir as mensagens do servidor. 
        Ele executa em um loop infinito, recebendo mensagens do servidor, as dividindo usando "&" como delimitador e, em seguida, 
        verificando o código da mensagem. Se o código não for "250" (indicando que a mensagem não é uma indicação de desconexão), imprime o conteúdo da mensagem. 
        Se o código for "250", significa que o cliente foi desconectado do chat, então o método imprime a mensagem correspondente e define `conected` como False, encerrando o loop.
        """
        while True:
            response_server = self.sock.recv(4096).decode("utf-8").split("&")
            if not response_server[0] == "270":
                print(response_server)
            else:
                print("VOCE FOI DESCONECTADO!!!")
                self.conected = False 
                break
            
    def DigitOnchat(self):
        """
        `DigitOnchat` é um método responsável por permitir que o usuário envie mensagens para o servidor enquanto estiver conectado ao chat. 
        Ele permanece em um loop enquanto `conected` for verdadeiro, aguardando a entrada do usuário e enviando a mensagem para o servidor formatada com o código "msg". 
        Este método é interrompido quando o usuário decide encerrar o chat ou é desconectado do servidor.
        """
        while True: 
            if self.conected:
                break
            msg = input(">> ")
            self.sock.send(f"msg&{msg}".encode("utf-8"))

    def login(self): 
        """
        `login` é um método responsável por coletar as credenciais do usuário (nome de usuário e senha) e formar uma mensagem de login que será enviada ao servidor. 
        Ele fica em um loop até que as credenciais sejam fornecidas corretamente, ou o usuário decida voltar ao menu anterior digitando "Voltar". 
        O método retorna a mensagem de login formatada.
        """

    def signin(self):
        """
        `signin` é um método responsável por coletar informações do usuário durante o processo de registro (nome de usuário e senha). 
        Ele valida se o nome de usuário e a senha atendem aos critérios especificados (comprimento mínimo) e retorna a mensagem de registro formatada para ser enviada ao servidor. 
        O método permite que o usuário digite "Voltar" para retornar ao menu anterior durante a entrada de informações.
        """
        try:
           # print("Digite 'Voltar' para retornar ao menu anterior.")
            user = input("\nUsuario: ")
           # if user.upper() == "VOLTAR":
            #    self.validate_choice()
                
            password = input("Senha: ")
            #if password.upper == "VOLTAR":
            #    self.validate_choice()
                
            assert len(password) >= 6
            assert len(user) > 0 and len(user) <= 20
        except Exception:
            #print("\nA senha deve conter 6 ou mais caracteres e o Usuario deve conter 1 ou mais caracteres!\n")
            return self.signin()
        response = f"register {user} {password}"
        return response

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
            responseCode = client.setTypeCounselor()
            print(responseCode)
            threading.Thread(target=client.escutar, args=()).start()
            client.DigitOnchat()
            break
except MuitasTentativas as e:
    print("")