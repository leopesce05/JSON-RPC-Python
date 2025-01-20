from jsonrpc_redesNuestro import connect

print("TEST CLIENTE CON NUESTRA BIBLIOTECA Y SERVIDOR CON BIBLIOTECA ENTREGADA")
conexion = connect('200.0.0.10', 8080)

sumatoria = conexion.sum(3,5,6)
assert sumatoria == 14
print("Funcion Summation correcta")

ec = conexion.echo("Hola Redes")
assert ec == "Hola Redes"
print("Funcion Echo correcta")

ec = conexion.echo_concat(msg1="Hola", msg2=" Redes", msg3="!", msg4="!")
assert ec == "Hola Redes!!"
print("Funcion echo_concat correcta")

ec = conexion.echo_concat(msg1="Hola", msg2=" Redes", msg3="!", msg4="!", notify=True)
assert ec == None
print("Notificacion correcta")

try:
    ec = conexion.FuncionInexistente()
    print("Error, debe generar excepcion")
except Exception as e:
    print(e.code,e.message)

try:
    ec = conexion.echo(3,5)
    print("Error, debe generar excepcion")
except Exception as e:
    print(e.code,e.message)

conexion.close()
