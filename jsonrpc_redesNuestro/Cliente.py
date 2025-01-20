import socket
import json

def connect(address,port):
    return conCliente(address,port)

class conCliente:
    def __init__(self,address,port):
        self.id = 0 #inicializa id de peticiones
        self.address = address
        self.port = port
        try: 
            self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.con.connect((self.address,self. port))
        except:
            raise Exception("Error al conectar con el servidor")

    def testError(self,mensaje):
        try:
            self.con.sendall(mensaje)
        except:
            try: 
                self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.con.connect((self.address,self.port))
                return self.testError(mensaje)
            except:
                raise Exception("Error al conectar con el servidor")
        
        respuesta = self.con.recv(4096)
        if respuesta == b'':
            try: 
                self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.con.connect((self.address,self.port))
                return self.testError(mensaje)
            except:
                raise Exception("Error al conectar con el servidor")
        else:
            respuesta = respuesta.decode()
            respuesta = json.loads(respuesta)
            if 'error' in respuesta:
                raise Error(respuesta["error"]["message"],respuesta["error"]["code"])
            else:
                return respuesta["result"]


    def llamarMetodo(self,metodo,parametros,notify):
        llamada = {}
        llamada["jsonrpc"] = "2.0"
        llamada["method"] = metodo
        if parametros:
            llamada["params"] = parametros
        if(not notify):
            llamada["id"] = self.id
            self.id += 1
        try:
            self.con.sendall(json.dumps(llamada).encode())
        except:
            try: 
                self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.con.connect((self.address,self.port))
                return self.llamarMetodo(metodo,parametros,notify)
            except:
                raise Exception("Error al conectar con el servidor")
            
        if(not notify):
            res = self.con.recv(4096)
            if res == b'':
                try: 
                    self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.con.connect((self.address,self.port))
                    return self.llamarMetodo(metodo,parametros,notify)
                except Error as e:
                    raise e
                except Exception as er:
                    raise Exception("Error al conectar con el servidor")
            else:
                res = res.decode()
                res = json.loads(res)
                if 'error' in res:
                    raise Error(res["error"]["message"],res["error"]["code"])
                else:
                    return res["result"]
                
        else:
            return None


    def __getattr__(self,metodo):        
        def noImplementado(*params, **parClave): # *params son argumentos y **parClave son argumentos de palabras clave
            noti = parClave.pop('notify', None)
            if(noti != True):
                if(parClave):
                    res = self.llamarMetodo(metodo,parClave,False)
                else:
                    res = self.llamarMetodo(metodo,list(params),False)
            else:
                if(parClave):
                    res = self.llamarMetodo(metodo,parClave,True)
                else:
                    res = self.llamarMetodo(metodo,list(params),True)
            return res
        return noImplementado
    
    def close(self):
        self.con.close()

class Error(Exception):
    def __init__(self, message, code):
        self.message = message 
        self.code = code