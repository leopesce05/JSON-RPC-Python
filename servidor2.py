from jsonrpc_redesNuestro import Server
import threading
import time
import sys

def multiplicar(a,b):
    return a*b

def dividir(a,b):
    return a/b

def es_triangulo(lado1, lado2, lado3):
    if lado1 <= 0 or lado2 <= 0 or lado3 <= 0:
        return False
    return ((lado1 + lado2 > lado3) 
            and (lado1 + lado3 > lado2) 
            and (lado2 + lado3 > lado1))

servidor = Server(('127.0.0.2',8081))

servidor.add_method(multiplicar)
servidor.add_method(dividir)
servidor.add_method(es_triangulo)

server_thread = threading.Thread(target=servidor.serve)
server_thread.daemon = True
server_thread.start()

try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    servidor.shutdown()
    sys.exit()