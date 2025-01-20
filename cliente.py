from jsonrpc_redesNuestro import connect
import json

conexionCliente = connect('127.0.0.1',8080)

print("CONEXION CON SERVIDOR 1")
print("ENVIAR PARAMETROS VALIDOS")

#request a un método sin parámetros y que retorna un único valor
res = conexionCliente.sinParamsUnValor()
assert res == True
print("Prueba 1 correcta -> Metodo sin parametros y retorna un valor")

#Un request a un método con parámetros y que retorna mas de un valor
res = conexionCliente.conParamsLista(3,6)
assert res == [3,6]
print("Prueba 2 correcta -> Metodo con parametros y retorna mas de un valor")

#Un request a un método que tiene parámetros no obligatorios y se envían con nombre para identificarlos.
res = conexionCliente.saludar(saludo = "Hola", nombre = "pedro")
assert res == "Hola pedro!"
print("Prueba 3 correcta -> Parametros no obligatorios con identificador")

#Un request a un método que tiene parámetros no obligatorios y se envían con nombre para identificarlos.
res = conexionCliente.saludar(saludo = "Hola", nombre = "pedro" , signo = "?")
assert res == "Hola pedro?"
print("Prueba 4 correcta -> Parametros no obligatorios con identificador")

#Un request a un método con parámetros y que retorna un único valor
res = conexionCliente.concat("Hola"," Redes")
assert res == "Hola Redes"
print("Prueba 5 correcta -> Parametros y retorna un valor")

res = (conexionCliente.maximo(8,4))
assert res == 8
print("Prueba 6 correcta -> Parametros y retorna un valor")

res = (conexionCliente.potencia(2,2))
assert res == 4
print("Prueba 7 correcta -> Parametros y retorna un valor")

#Una notificación a un método sin parámetros
res = conexionCliente.sinParamsUnValor(notify = True)
assert res == None
print("Prueba 8 correcta -> Notificacion sin parametros")

#Una notificación a un método con parámetros
res = (conexionCliente.potencia(2,2,notify = True))
assert res == None
print("Prueba 9 correcta -> Notificacion con parametros")
print()
print()


print("ENVIAR MENSAJES Y PARAMETROS INVALIDOS")

try:
    res =(conexionCliente.maximo(8,8,8)) #mas parametros
    print(res)
except Exception as e:
    print("Prueba 4 Enviar Mas parametros")
    print(e.code, e.message)

try:
    res =(conexionCliente.maximo(8)) #menos parametros
    print(res)
except Exception as e:
    print("Prueba 5 Enviar menos parametros")
    print(e.code, e.message)

try:
    res =(conexionCliente.multiplicar(8,4,8)) #request a un método que no existe
except Exception as e:
    print("Prueba 6 Funcion inexistente")
    print(e.code, e.message)

try:
    mensaje = {  #INVALID REQUEST
    "jsonr": "2.0",
    "id" : "asd"
    }
    mensaje = json.dumps(mensaje)
    res = conexionCliente.testError(mensaje.encode())
except Exception as e:
    print("Prueba 7 Mensaje invalido, jsonrpc incorrecto")
    print(e.code,e.message)



print()
print()




conexionCliente = connect('127.0.0.2',8081)
print("CONEXION CON SERVIDOR 2")
print("ENVIAR PARAMETROS VALIDOS")
res = conexionCliente.multiplicar(3,4)
assert res == 12
print("Prueba 1 correcta")
res = (conexionCliente.dividir(8,4))
assert res == 2
print("Prueba 2 correcta")
res = (conexionCliente.es_triangulo(2,2,2))
assert res == True
print("Prueba 3 correcta")
print()
print()


print("ENVIAR MENSAJES Y PARAMETROS INVALIDOS")
try:
    res =(conexionCliente.multiplicar(8,4,8)) #parametros invalidos
except Exception as e:
    print("Prueba 4.1 -> Parametros invalidos")
    print(e.code,e.message)

try:
    res =(conexionCliente.multiplicar(8)) #parametros invalidos
except Exception as e:
    print("Prueba 4.2 -> Parametros invalidos ->menos parametros")
    print(e.code,e.message)

try:
    res =(conexionCliente.divi(8,4,8)) #FUNCION QUE NO EXISTE
except Exception as e:
    print("Prueba 5 Funcion inexistente")
    print(e.code,e.message)


try:
    mensaje = {  #INVALID REQUEST
    "jsonr": "2.0",
    "id" : "asd"
    }
    mensaje = json.dumps(mensaje)
    res = conexionCliente.testError(mensaje.encode())
except Exception as e:
    print("Prueba 6 Mensaje invalido, jsonrpc incorrecto")
    print(e.code,e.message)

#INTENTO DE ERROR INTERNO
try:
    res = conexionCliente.dividir(8,0)
except Exception as e:
    print("Prueba 7, division entre 0 error interno")
    print(e.code,e.message)

print()
print()
