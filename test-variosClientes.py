from jsonrpc_redesNuestro import connect
import threading

print("PRUEBAS DE VARIOS CLIENTES SIMULTANEOS")

def tareaCliente(con,i):
    print(i,con.sinParamsUnValor())

    print(i, con.concat("asd","la"))
    
    print(i, con.saludar(saludo = "Hola", nombre = "pedro"))

    try:
        (con.concat(8)) 
    except Exception as e:
        
        print(i,e.code, e.message)

    try:
        (con.multiplicar(8,4,8))
    except Exception as e:
        print(i,e.code, e.message)

    
for i in range(10):
    #crea hilo para cada cliente
    conexionCliente = connect('200.0.0.10',8080)
    print(str(i) + "!")
    hilo = threading.Thread(target=tareaCliente,args=(conexionCliente,i))
    hilo.start()

