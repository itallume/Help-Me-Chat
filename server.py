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
                    # criar um while para o login e cadastro
                    if msg_client[0] == "login":   # fazer a tentativa maxima de 10 login por nome de usuário
                        login = False
                        for i in range(6):
                            try:
                                with self.Lock:
                                    assert self.usersHashTable.get(msg_client[1]).confirmPassword(msg_client[2])  # com o metodo confirmPassword da classe User, faz a confirmação da senha
                                    #assert not self.OnlineUsers.contains(msg_client[1])  #LANÇAR EXCEÇÃO

                                    userObject = self.usersHashTable.get(msg_client[1])
                                    self.OnlineUsers.put(msg_client[1], msg_client[1])
                                connection.send("200".encode('utf-8'))
                                login = True
                                break
                            except Exception as e:
                                    connection.send("201".encode('utf-8'))
                                    msg_client = connection.recv(4096).decode("utf-8").split(" ")
                                    continue
                        if login == False:
                            connection.send("299".encode('utf-8'))
                            connection.close()
                            return
                        break

                 #Enviar codigo
                    if msg_client[0] == "register":

                        if self.usersHashTable.contains(msg_client[1]): # verifica se já existe algum usuário com o nome de usuário desejado
                            connection.send("211".encode('utf-8'))
                            continue

                        userObject = User(msg_client[1], msg_client[2])
                        with self.Lock:
                            self.usersHashTable.put(msg_client[1], userObject) # abre o server
                            self.OnlineUsers.put(msg_client[1], msg_client[1])
                        connection.send("210".encode('utf-8'))
                        self.usersHashTable.displayTable()
                        print()
                        break
                except ConnectionResetError as e:
                    print(f"Erro de conexão: {e}")
                    connection.send("555".encode('utf-8')) #Enviar codigo

        while True:
            
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
                        # usar lock
                        #threading.Thread(target= self.matchClients, args=(chat, userObject)).start()
                        break
                    
                    if msg_client[1] == "counselor":
                        # fazer as de solicitações de escolha de chat para o conselheiro
                        chat = self.enterOnChat(connection, userObject)
                        self.councelorChat(chat, connection)
                        
                        break
            
        # while True:
        #     try:
        #         msg_client = connection.recv(4096).decode("utf-8").split("&") # receber a mensagem do cliente e separar o comando do texto
        #         print(msg_client)
        #      #Enviar codigo

        #         if msg_client[0] == "msg":
        #             if msg_client[1].lower() == 'exit': #subtituir por uma forma de que venha no cabeçalho, não é trabalho do usuário digitar isso, e sim do cliente achar uma maneira de notificar
        #                 print(f"Desconectado: {userObject.nickname}")
        #                 response = '250'
        #                 for participants in chat.getClients():
        #                     with self.Lock:
        #                         self.OnlineUsers.remove(participants[0])
        #                     participants[1].send(f"{response}".encode('utf-8')) #talvez cause bug
        #                     connection.close()
        #                 break

        #             else:
        #                 for participants in chat.getClients():

        #                     participants[1].send(f"240&{userObject.nickname}: {msg_client[1]}".encode('utf-8'))

        #     except ConnectionResetError as e:
        #         print("Ouve um erro na conexão!")

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
