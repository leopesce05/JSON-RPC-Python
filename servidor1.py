from jsonrpc_redesNuestro import Server
import time
import sys
import threading

def concat(a,b):
    return a+b

def maximo(a,b):
    if a>b:
        return a
    else:
        return b

def potencia(a,b):
    return a**b

def sinParamsUnValor():
    return True

def conParamsLista(v1,v2):
    return [v1,v2]

def saludar(nombre, saludo="Hola", signo="!"):
    return saludo + " " + nombre + signo

servidor = Server(('127.0.0.1',8080))

servidor.add_method(concat)
servidor.add_method(maximo)
servidor.add_method(potencia)
servidor.add_method(sinParamsUnValor)
servidor.add_method(conParamsLista)
servidor.add_method(saludar)

server_thread = threading.Thread(target=servidor.serve)
server_thread.daemon = True
server_thread.start()

try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    servidor.shutdown()
    sys.exit()