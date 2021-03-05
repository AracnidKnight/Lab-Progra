from datetime import datetime
import json

#   CARGA DE DATOS INICIALES
nombre_archivo = "denuncias.json"
texto_admin = """
Hola, administrador. Por favor eliga una opción

1) Ver denuncias
2) Registrar denuncia
3) Salir
"""

# Carga de denuncias apartir del archivo
denuncias = []
try:
    lector_registro = open(nombre_archivo, "r")

    # Se lee el archivo y se des-serealiza
    registro = "[" + lector_registro.read() + "]"
    denuncias = json.loads(registro)
    
    lector_registro.close()
except:
    # En caso de que no haya archivo este se reinicia
    escritor_registro = open(nombre_archivo, "w")
    escritor_registro.close()

# Se abre el archivo para añadir nuevas denuncias
escritor_registro = open(nombre_archivo, "a")


#   FUNCIONES
# Imprimir las denuncias del registro
def imprimirDenuncias():
    print()
    linea = "{:^20} | {:^40}".format("Tipo denuncia", "Descripcion")
    print(linea)
    for denuncia in denuncias:
        linea = "{:20} | {:40}".format(denuncia["tipo"], denuncia["descripcion"])
        print(linea)

# Registrar una nueva denuncia en el registro
def registrarDenuncia():
    tipo = input("Ingrese el tipo de denuncia =>")
    descripcion = input("Describa la situación =>")
    fecha = '"' + str(datetime.now()) + '"'

    nueva_denuncia = {
        "tipo": tipo,
        "descripcion": descripcion,
        "fecha": fecha
    }

    denuncias.append(nueva_denuncia)

    # Se agrega una coma para añadirla a la lista si ya habia una antes
    if(len(denuncias) > 1):
        escritor_registro.write(",")
    
    # Se formatea la denuncia para tener formato JSON
    texto_denuncia = str(nueva_denuncia)
    escritor_registro.write(texto_denuncia.replace("'", '"'))


#   FLUJO PROGRAMA
nombre = input("Ingrese su nombre =>")
if nombre.upper() == "ADMIN":
    opcion = 0
    while(opcion != 3):
        print(texto_admin, end="")
        opcion = int(input("=>"))

        if opcion < 1 or opcion > 3:
            print("Ingrese una opcion valida")

        if opcion == 1:
            imprimirDenuncias()
        if opcion == 2:
            registrarDenuncia()
else:
    input("Ingrese la estación donde se encuentra")

    opcion = 0
    while(opcion != 3):
        print(texto_admin, end="")
        opcion = int(input("=>"))

        if opcion < 1 or opcion > 3:
            print("Ingrese una opcion valida")

        if opcion == 1:
            imprimirDenuncias()
        if opcion == 2:
            registrarDenuncia()

escritor_registro.close()