import threading
import socket
import json
import sys


##############SERVIDOR######################
class Server:
    def __init__(self, address):
        self.address,self.port = address
        self.metodos = {}
        self.server = None

    def add_method(self, proc,nombre = None):
        if not callable(proc):
            raise Exception("Se debe agregar una funcion")
        if nombre != None:
            nombreFuncion = nombre
        else:
            nombreFuncion = proc.__name__   #obtener el nombre de la funcion

        if nombreFuncion in self.metodos:
            raise Exception("El nombre de la funcion ya existe")
        
        self.metodos[nombreFuncion] = proc #agregar la funcion

    def llamarMetodo(self, proc, params = None):
        if not (proc in self.metodos):
            raise MetodoNoExiste("El metodo no existe")
        try:
            if (params != None):
                if isinstance(params, list):
                    res = self.metodos[proc](*params)
                else:
                    res = self.metodos[proc](**params)
            else:
                res = self.metodos[proc]()
        except (TypeError, ValueError) as e:
            raise ArgumentosIncorrectos("Los argumentos son incorrectos")
        except Exception as e:
            raise Exception("Error interno")

        return res

    def obtenerError(self,num): #obtiene el error segun el numero
        errores = {
            -32700: {"code": "-32700", "message": "Parse error"},
            -32600: {"code": "-32600", "message": "Invalid Request"},
            -32601: {"code": "-32601", "message": "Method not found"},
            -32602: {"code": "-32602", "message": "Invalid params"},
            -32603: {"code": "-32603", "message": "Internal error"},
        }
        return errores[num]

    def enviar(self, mensaje,con):
        mensaje = json.dumps(mensaje).encode()
        try:
            con.sendall(mensaje)
        except:
            return

    def tareaCliente(self,con,address):
        con.settimeout(10)
        decoder = json.JSONDecoder()
        buffer = ''
        while True:    
            try:
                mensaje = con.recv(4096)
                if not mensaje:
                    break
                buffer += mensaje.decode()
                while buffer:
                    try:
                        request = False
                        while not request:
                            try:
                                request, index = decoder.raw_decode(buffer)
                                buffer = buffer[index:]
                            except:
                                mensaje = con.recv(4096)
                                if not mensaje:
                                    raise Exception("Conexión cerrada.")
                                buffer += mensaje.decode()

                        version = request["jsonrpc"]
                        metodo = request["method"]
                        params = request.get("params", None)
                        if not "id" in request:
                            try:
                                self.llamarMetodo(metodo, params)
                            except Exception as e:
                                continue
                        else:
                            res = {"jsonrpc": "2.0", "result": self.llamarMetodo(metodo, params), "id": request.get("id", None)}
                            self.enviar(res,con)


                    except KeyError as e:
                        res = {"jsonrpc": "2.0", "error": self.obtenerError(-32600), "id": None}
                        self.enviar(res,con)

                    except MetodoNoExiste as e:
                        res = {"jsonrpc": "2.0", "error": self.obtenerError(-32601), "id": request.get("id", None)}
                        self.enviar(res,con)

                    except ArgumentosIncorrectos as e:
                        res = {"jsonrpc": "2.0", "error": self.obtenerError(-32602), "id": request.get("id", None)}
                        self.enviar(res,con)

                    except Exception as e:
                        res = {"jsonrpc": "2.0", "error": self.obtenerError(-32603), "id": request.get("id", None)}
                        self.enviar(res,con)
                        con.close()
            except Exception as e:
                break
            
    def serve(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.address, self.port))
        self.server.listen(100)

        while True:
            try:
                con, address = self.server.accept()
                print("Cliente conectado :" + str(address))
                hilo = threading.Thread(target=self.tareaCliente, args=(con,address))
                hilo.daemon = True
                hilo.start()
            except:
                return

    def shutdown(self):
        self.server.close()
        print("Servidor cerrado")
        sys.exit()

class MetodoNoExiste(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class ArgumentosIncorrectos(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)