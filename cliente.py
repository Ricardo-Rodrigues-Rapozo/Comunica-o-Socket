import socket

class Cliente():
    """Classe cliente - calculadora remota - API socket
    """
    def __init__(self,server_ip, port):
        """construtor da classe cliente

        Args:
            server_ip (_type_): endereço IP do servidor 
            port (_type_): Porta para serviço
        """
        self.__server_ip = server_ip
        self.__port = port 
        self.__tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
    
    def start(self):
        """
        Método que inicializa a execução do cliente
        """
        endpoint = (self.__server_ip, self.__port)
        try:
            self.__tcp.connect(endpoint)
            print("conexao realizada com sucesso")
            self.__method() ## cria uma IHM 
        except Exception as e:
            print("Erro na conexao com o servidor", e.args)
            
       
       ##     
    def __method(self):
        """Método que implementa as requisições do cliente e a IHM
        """
        try:
            msg = ''
            while msg != 'x':   
                msg = input("Digite a operação desejada (digite 'x' para sair):")
                if msg == '':
                    continue
                elif msg =='x':
                    break
                self.__tcp.send(bytes(msg,'ascii'))
                resp = self.__tcp.recv(1024)
                print(" = ",resp.decode('ascii')) 
            self.__tcp.close()
        except Exception as e:
            print("Erro na comunicação com o servidor",e.args)