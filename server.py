import socket
import threading
from ChainingHashTableProblema import ChainingHashTable
from BinarySearchTree import BinarySearchTree
from User import User
from Chat import Chat
import time
from Undecided import Undecided
from Counselor import Counselor

class Server:
    def __init__(self, adress:str , porta:int):
        self.adress = adress
        self.port = porta
        self.usersHashTable = ChainingHashTable(20)
        self.AllChats = ChainingHashTable(20)
        self.arvore = BinarySearchTree()
        self.MinNote = self.setDictionary()
        self.Lock = threading.Lock()
        self.OnlineUsers = ChainingHashTable(20)
        self.chats = []

    def setDictionary(self):
        """ Atribui ao atributo MinNote da classe o dicionário que
            contém a nota minima para entrar em um chat
            com base nas intensidades 1, 2 e 3.
            Onde:
                1 = Intensidade baixa
                2 = Intensidade média
                3 = Intendsidade alta
        """
        return {
            1: 0,
            2: 3,
            3: 6
        }

    def start_server(self):
        """
        `start_server` é um método responsável por iniciar o servidor. Ele configura o dicionário de notas mínimas chamando o método `setDictionary,
        cria um socket para o servidor usando `socket.socket`, faz o bind do socket, e então inicia o modo de escuta do socket usando `listen()`.

        Após essas configurações, o método entra em um loop infinito (`while True`) onde aguarda novas conexões de clientes chamando `aceitar_clientes` e passando o socket do servidor como argumento.
        Esse método é responsável por aceitar novas conexões de clientes e iniciar uma nova thread para lidar com a comunicação com cada cliente. O loop continua indefinidamente para aceitar várias conexões consecutivas.
        """
        UserObject1 = User("itallo", "123456")
        self.usersHashTable.put(UserObject1.nickname, UserObject1) # abre o server
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.bind(("0.0.0.0", self.port))
        clientSocket.listen()
        print(f"Servidor aguardando conexao na porta {self.port}")

        while True:
            self.aceitar_clientes(clientSocket)


    def aceitar_clientes(self, clientSocket):
        """
        `aceitar_clientes` é responsável por aceitar a conexão de um cliente.
        Ele cria uma nova thread para lidar com a comunicação com esse cliente, chamando o método `clientComunication` e
        passando a conexão como argumento. Essa abordagem permite que o servidor aceite múltiplas conexões simultaneamente.
        """

        connection, end_client = clientSocket.accept()
        print(f"Conexão estabelecida com {end_client}")

        threading.Thread(target=self.clientComunication, args=(connection,)).start()


    def clientComunication(self, connection):
        """
        O método gerencia a comunicação entre servidor e cliente.
        Ele trata os comandos de login e registro, autenticando as credenciais do cliente.
        Mmonitora o envio e recebimento de mensagens no chat, lidando com eventos como desconexões e comandos específicos que levam a ações como encerrar a comunicação. """
        while True:
            try:
                msg_client = connection.recv(4096).decode("utf-8").split(" ")
                if msg_client == "back":
                    connection.send("198".encode('utf-8'))
                    continue
                # criar um while para o login e cadastro
                if msg_client[0] == "login":   # fazer a tentativa maxima de 10 login por nome de usuário
                    userObject = None
                    login = self.handleLogin(connection, msg_client, userObject)
                    if login:
                        break
                    elif login is None:
                        continue
                    else:
                        return
                    
                if msg_client[0] == "register":
                    with self.Lock:
                        if self.usersHashTable.contains(msg_client[1]): 
                            connection.send("211".encode('utf-8'))
                            continue
                        userObject = User(msg_client[1], msg_client[2])
                        self.usersHashTable.put(msg_client[1], userObject) # abre o server
                        self.OnlineUsers.put(msg_client[1], msg_client[1])
                    connection.send("210".encode('utf-8'))
                    self.usersHashTable.displayTable()
                    print()
                    break
            except ConnectionResetError as e:
                print("Erro de conexão:", connection)
                connection.close()
            except OSError:
                print("Erro de conexão: ", connection)
                connection.close()
                
        while True:
            try:
                msg_client = connection.recv(4096).decode("utf-8").split("&")
                if msg_client[0] == "type":
                    if msg_client[1] == "undecided":                      
                        if msg_client[3] not in ["1","2","3"]:
                            connection.send("231".encode('utf-8'))
                            continue
                        if len(msg_client[2]) < 2:
                            connection.send("233".encode('utf-8'))
                            continue
                        chat = Chat(msg_client[2], int(msg_client[3]))# cria um objeto chat com o assunto e a intensidad
                        chat.undecided = Undecided(userObject.nickname, connection)
                        with self.Lock:
                            self.chats.append(chat)
                        while chat.counselor is None:
                            time.sleep(0.2)    
                        self.undecidedChat(chat, connection)
                        break
                    
                    if msg_client[1] == "counselor":
                        # fazer as de solicitações de escolha de chat para o conselheiro
                        chat = self.enterOnChat(connection, userObject)
                        self.councelorChat(chat, connection)
                        
                        break
            except ConnectionResetError:
                print("Erro de conexão: ", connection)
                connection.close()
            except OSError:
                print("Erro de conexão: ", connection)
                connection.close()
                
    def enterOnChat(self, connection, userObject):
       
        while True:
            with self.Lock:
                if len(self.chats) == 0:           
                    time.sleep(0.2)
                else:
                    for chat in self.chats:
                        if userObject.nota >= self.MinNote[chat.intensity]:
                            chat.counselor = Counselor(userObject.nickname, connection)
                            print("antes de remover: ", len(self.chats))
                            self.chats.remove(chat)
                            print("dps de remover: ", len(self.chats))
                            return chat
                    
    def loginVerification(self, username:str, password:str) -> str:
        with self.Lock:
            try:
                user = self.usersHashTable.get(username) 
            except Exception:
                return "201"
            if not user.confirmPassword(password):
                return "201"
            if self.OnlineUsers.contains(user.nickname):
                return "203"
        return "200"
        
    def handleLogin(self, connection, msg_client, userObject):
        
        username = msg_client[1]
        password = msg_client[2]
        loginAttempts = 6
        for i in range(loginAttempts):
            code = self.loginVerification(username, password)
            connection.send(code.encode('utf-8'))
            if code == "200":
                self.OnlineUsers.put(username, username)
                userObject = self.usersHashTable.get(username)
                return True
            else:
                msg_client = connection.recv(4096).decode("utf-8").split(" ")
                if msg_client == "back":
                    connection.send("198".encode('utf-8'))
                    return None
                username = msg_client[1]
                password = msg_client[2]
        connection.send("299".encode('utf-8'))
        connection.close()
        return False   
                
    def councelorChat(self, chat, connection):
        try:
            undecidedSocket = chat.undecided.socket
            undecidedSocket.send(f"250&{chat.subject}&{chat.intensity}".encode('utf-8'))

            while True:
                msg_client = connection.recv(4096).decode("utf-8").split("&")
                if msg_client[0] == "msg":
                    undecidedSocket.send(f"240&{chat.undecided.username}&{msg_client[1]}".encode('utf-8'))
        except ConnectionResetError:
            print("Erro de conexão, finalizando o chat: ", chat)
            connection.close()
            undecidedSocket.send(f"270".encode('utf-8'))
                #adicionar uma opção de saida do chat para um conselheiro
            
    def undecidedChat(self, chat, connection):
        try:
            counselorSocket = chat.counselor.socket
            counselorSocket.send(f"250&{chat.subject}&{chat.intensity}".encode('utf-8'))

            while True:
                msg_client = connection.recv(4096).decode("utf-8").split("&")
                if msg_client[0] == "msg":
                    counselorSocket.send(f"240&{chat.counselor.username}&{msg_client[1]}".encode('utf-8'))
                else:
                    counselorSocket.send(f"250".encode('utf-8'))
        except ConnectionResetError:
            print("Erro de conexão, finalizando o chat: ", chat)
            connection.close()
            counselorSocket.send(f"270".encode('utf-8'))
            #adicionar uma opção de saida do chat
        
servidor = Server("0.0.0.0", 12345)
servidor.start_server()
