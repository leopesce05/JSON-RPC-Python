from jsonrpc_redesNuestro import connect

print("TEST CERRAR CLIENTES")

print("ABRIR CONEXIONES")
conexionCliente1 = connect('200.0.0.10',8080)
conexionCliente2 = connect('200.0.0.10',8080)
conexionCliente3 = connect('200.0.0.10',8080)
conexionCliente4 = connect('200.0.0.10',8080)

print("CONSULTAS TODOS LOS CLIENTES")
print(conexionCliente1.concat("Conexion ", "cliente 1"))
print(conexionCliente2.concat("Conexion ", "cliente 2"))
print(conexionCliente3.concat("Conexion ", "cliente 3"))
print(conexionCliente4.concat("Conexion ", "cliente 4"))

print("CERRAR CLIENTE 1 Y 2")
conexionCliente1.close()
conexionCliente2.close()

print("CONSULTAS CLIENTES 3 Y 4")
print(conexionCliente3.concat("Consulta ", "cliente 3"))
print(conexionCliente4.concat("Conexion ", "cliente 4"))

