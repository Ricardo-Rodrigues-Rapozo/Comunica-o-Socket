import socket
import threading

class Servidor():
    """Classe servidor - calculadora remota API socket
    """
    def __init__(self, host, port):
        """Construtor da classe servidor 
        Args:
            host (_type_): _description_
            port (_type_): _description_
        """
        self._host = host # 
        self._port = port 
        self._tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #objeto tcp
    
    def start(self):
        """Inicia a execução do serviço
           Criar o socket e atender aos clientes
        """
        endpoint = (self._host,self._port) # uma tupla para que não seja modificado
        try:
            self._tcp.bind(endpoint)
            self._tcp.listen(1) #1 apenas para ativar o log do sistema
            print("O servidor foi iniciado",self._host,":",self._port)
            while True:
                con, client = self._tcp.accept()#esperando o cliente se conectar 
                
                self._service(con,client) #metodo service
        except Exception as e:
            print("Erro ao inicializar o servidor",e.args)# o args indica o erro que ira aparecer dentro do bloco try 
            
    def _service(self,con,client):
        """Implementa o serviço de calculadora remota

        Args:
            con (_type_): objeto socket utilizado para enviar e receber dados
            client (_type_):é o endereço e porta do cliente 
        """
        print("Atendendo cliente: ",client)
        # daqui para baixo é o que quero que seja feito
        operadores = ['+','-','/','*','%']
        
        while True: # loop infinito para possibilitar que o cliente faça varias operações 
            try:
                msg = con.recv(1024) # recebo os dados brutos em bytes
                #transformando o conjunto de bytes em strings
                msg_s = str(msg.decode('ascii')) # padrao é operando1 operação e operando2
                op = 'none'
                for x in operadores:
                    if msg_s.find(x) > 0:
                        op = x
                        msg_s = msg_s.split(op)# split retorna uma lista separa pelo op
                        break
                if op =='+':
                    resp = float(msg_s[0]) + float(msg_s[1])
                elif op =='-':
                    resp = float(msg_s[0]) - float(msg_s[1])
                elif op =='*':
                    resp = float(msg_s[0]) * float(msg_s[1])
                elif op == '/':
                    resp = float(msg_s[0]) / float(msg_s[1])
                elif op =='%':
                    resp = float(msg_s[0]) % float(msg_s[1])
                else:
                    print("Operação invalida")
                    
                con.send(bytes(str(resp),'ascii'))# converte para str antes de passar para bytes
                print(client," : Requisição atendida")
            except OSError as e: # USADO PARA ERROS DE I/O 
                print("Erro na conexão",client,":",e.args)
                return # este return serve para encerrar o metodo service 
            except Exception as e:
                print("Erro nos dados recebidos do cliente: ", client, e.args)
                
                    
class SERVIDORMT(Servidor):
    """ServidorMT que suporta multiplos clientes(multi thread)

    Args:
        Servidor (_type_): _description_
    """
    def __init__(self,host, port):
        """COnstrutor da classe servidormt

        Args:
            host (_type_): _description_
            port (_type_): _description_
        """
        super().__init__(host,port) # puxando da classe mae 
        self.__threadpool = {} # coleção de threads para novo cliente
        
        
    def start(self):
        """Inicia a execução do serviço
            Criar o socket e atender aos clientes
        """
        endpoint = (self._host,self._port) # uma tupla para que não seja modificado
        try:
            self._tcp.bind(endpoint)
            self._tcp.listen(1) #1 apenas para ativar o log do sistema
            print("O servidor foi iniciado",self._host,":",self._port)
            while True:
                con, client = self._tcp.accept()#esperando o cliente se conectar 
                
                self.__threadpool[client] = threading.Thread(target = self._service, args = (con,client))#utilizando o metodo service para cada nova linha 
                self.__threadpool[client].start()
        except Exception as e:
            print("Erro ao inicializar o servidor",e.args)# o args indica o erro que ira aparecer dentro do bloco try 
        