from jsonrpc_redesNuestro import connect
import time

print("TEST CERRAR SERVIDOR")

print("ABRIR 4 CONEXIONES")
conexionCliente1 = connect('200.0.0.10',8080)
conexionCliente2 = connect('200.0.0.10',8080)
conexionCliente3 = connect('200.0.0.10',8080)
conexionCliente4 = connect('200.0.0.10',8080)

#CERRAR SERVIDOR
print("CIERRE EL SERVIDOR")
time.sleep(10)

print("CONSULTAS TODOS LOS CLIENTES CON SERVIDOR CERRADO")

try:
    res = conexionCliente1.concat("Conexion ", "cliente 1")
    print(res)
except Exception as e:
    print(e)

try:
    res=conexionCliente2.concat("Conexion ", "cliente 2")
    print(res)
except Exception as e:
    print(e)

try:
    res=conexionCliente3.concat("Conexion ", "cliente 3")
    print(res)
except Exception as e:
    print(e)

try:
    res=conexionCliente4.concat("Conexion ", "cliente 4")
    print(res)
except Exception as e:
    print(e)

