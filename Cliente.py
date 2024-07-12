import socket
import threading 
import socket
import threading


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.CodesTranslate = None
        self.conected = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def setDict(self):

        self.CodesTranslate = {
        "200": "login efetuado",
        "201": "Usuário ou senha incorreto",
        "210": "Cadastro efetuado",
        "211": "Nome de usuário já existente",
        "220": "Tipo setado",
        "221": "Tipo inexistente",
        "230": "Tema definido",
        "231": "Intensidade inexistente", 
        "240": "Comunicação feita",
        "250": "Desconectado",
        "260": "Nota apurada",
        "261": "Nota inválida",
        "270": "Conectado a um chat",
        "299": "Muitas tentativas de login, tente mais tarde.",
        "301": "Opção inválida.",
        "555": "Erro no servidor"

    }

    def start_client(self):
        """
        `É responsável por iniciar a conexão do cliente com o servidor, exibindo uma mensagem de boas-vindas e 
        opções de login e cadastro. 
        Após isso, solicita a escolha do usuário entre login e cadastro e chama o método `validate_choice` para prosseguir.
        """
        self.sock.connect((self.host, self.port))
        #print(f"Conectado ao servidor na porta {self.port}")
        #print("\n\n=============Bem-Vindo ao Conselheiro Virtual!=============\n")
        self.validate_choice()
        #print("Conexão encerrada.")
        return
    
    def validate_choice(self):
        """
        validate_choice recebe a escolha do usuário (login ou cadastro) e, em caso de entrada inválida, solicita novamente. 
        Se a escolha for login, chama Validate_login.
        Se for cadastro, chama Validate_register.
        """
        
        #print("Escolha uma opção:")
        #print("\n1 - login\n2 - signup\n")

        try:
            loginChoice = int(input("Opção: "))
        except Exception:
            print("Não foi possivel Logar, tente novamente")
            return self.validate_choice()

        if loginChoice == 1:
            self.Validate_login()
        elif loginChoice == 2:
            self.Validate_register()

    def Validate_login(self):
        """
        `Validate_login` inicia o processo de login, envia as credenciais ao servidor, trata diferentes códigos de resposta, 
        e, em caso de sucesso, permite ao usuário escolher entre ser um Indeciso(a) ou Conselheiro(a), chamando `set_type`. 
        Em caso de falha, solicita novas credenciais.
        """
        
        log = self.login()
        self.sock.send(log.encode("utf-8"))
        validate_login = self.sock.recv(1024).decode("utf-8").split(" ")
        if validate_login[0] == "200": 
            print(validate_login) #Login efetuado com Sucesso!
        
        if validate_login[0] == "299": 
            print(validate_login)
            self.Validate_login()

        while validate_login[0] == "201":
             #translate bug 
            print(self.CodesTranslate[validate_login[0]]) #Login nao efetuado, Usuário ou Senha incorretos!
            self.Validate_login()
        
        print(f"Servidor: {validate_login}")
        print("1. Indeciso(a)\n2. Conselheiro")
        self.set_type()

    def Validate_register(self):
        """
        `Validate_register` inicia o processo de registro, envia as informações ao servidor, trata diferentes códigos de resposta e,
          em caso de sucesso, permite ao usuário escolher entre ser um Indeciso(a) ou Conselheiro(a), chamando `set_type`. 
          Em caso de falha (nome de usuário já existente), solicita novas informações de registro.
        """
        signup = self.signin()
        self.sock.send(signup.encode("utf-8"))
        validate_signup = self.sock.recv(4096).decode("utf-8").split(" ")
        if validate_signup[0] == "210":
            print("\n",self.CodesTranslate[validate_signup[0]]) #Cadastro efetuado com Sucesso!
            
        while validate_signup[0] == "211": 
            print("\n",self.CodesTranslate[validate_signup[0]])
            print("Tente Novamente\n") #Nome de Usuario ja Existente, tente novamente!
            self.Validate_register()
        
        print(f"Servidor: {validate_signup}")
        print("1. Indeciso(a)\n2. Conselheiro(a)")
        self.set_type(validate_signup)
        
    def set_type(self):
        """
        `set_type` permite ao usuário escolher entre ser Indeciso(a) ou Conselheiro(a). 
        Em seguida, solicita informações adicionais conforme a escolha do usuário (assunto ou espera por um(a) Indeciso(a)), 
        chamando métodos apropriados como `set_assunto` ou `waitingConnection`.
        """
        try:
            type = int(input("Escolha: "))
            if type not in [1,2]:
                self.set_type()
        except Exception:
            print("\nTente novamente, escolha uma opção válida\n")
            self.set_type()

        if type == 1:   
            print("Qual será o assunto? ")
            self.set_assunto()
            return
        
        if type == 2:
            print("\nEsperando por um(a) Indeciso(a)...\n")
            self.sock.send(f"type&counselor".encode("utf-8"))
            response_server = self.sock.recv(4096).decode("utf-8").split("&")
            self.waitingConnection(response_server)
            return
        
    def set_assunto(self):
        """
        `set_assunto` solicita ao usuário que forneça um assunto. 
        Verifica se o assunto tem mais de 3 caracteres e, se não, solicita novamente. 
        Em seguida, pede ao usuário que escolha a intensidade do assunto e chama o método `set_intensity` passando o assunto como argumento.
        """
        try:
            assunto = input()
            assert len(assunto) > 0
            if len(assunto) <= 3:
                self.set_assunto()
        except Exception:
            print("Escreva um assunto Válido!")
            self.set_assunto()
            
        print("Escolha a intensidade:\n1: Baixa\n2: Média\n3: Alta")
        self.set_intensity(assunto)
        return

    def set_intensity(self, assunto):
        """
        `set_intensity` solicita ao usuário que forneça a intensidade do assunto. 
        Usa um loop para garantir que a entrada seja válida (1, 2 ou 3) e, em seguida, envia a informação para o servidor, esperando uma resposta. 
        Se a resposta indicar que a intensidade escolhida não é aceitável (código 231), solicita novamente a intensidade. 
        Se for uma resposta válida, chama o método `waitingConnection` passando a resposta do servidor como argumento.
        """   
        while True:
            try:
                intensidade = int(input("Intensidade: "))
                
                self.sock.send(f"type&undecided&{assunto}&{intensidade}".encode("utf-8"))
                response_server = self.sock.recv(4096).decode("utf-8").split("&")
                print("linha 132", response_server)
                if response_server[0] == "231":
                    print(self.CodesTranslate[response_server[0]])
                    self.set_intensity(assunto, self.sock)
                else:
                    print("\nProcurando por um(a) Indeciso(a)...\n")
                    self.waitingConnection(response_server)
                    return
            except Exception:
                print("\nEscolha uma intensidade válida (1, 2 ou 3)!\n")

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
            if not response_server[0] == "250":
                print(response_server[1])
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
        while self.conected: 
                msg = input(">> ")
                self.sock.send(f"msg&{msg}".encode("utf-8"))

    def login(self): 
        """
        `login` é um método responsável por coletar as credenciais do usuário (nome de usuário e senha) e formar uma mensagem de login que será enviada ao servidor. 
        Ele fica em um loop até que as credenciais sejam fornecidas corretamente, ou o usuário decida voltar ao menu anterior digitando "Voltar". 
        O método retorna a mensagem de login formatada.
        """
        while True:
            try:
                #print("Digite 'Voltar' para retornar ao menu anterior.")
                user = input("\nUsuario: ")
                #if user.upper() == "VOLTAR":
               #     self.validate_choice()
                password = input("Senha: ")
                
                #if password.upper == "VOLTAR":
                #    self.validate_choice()
                response = f"login {user} {password}"
                return response
            except Exception:
                
                break

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


client = Client("localhost", 12345)
client.setDict() 
client.start_client()
