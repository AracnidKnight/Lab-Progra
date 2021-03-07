#   IMPORTACIONES
import datetime

#   CARGA DE DATOS INICIALES
nombre_archivo = "denuncias.dato"

# Listas de opciones
tipos_denuncia = [
    "Robo",  "Acoso Sexual",
    "Objeto perdido", "Abuso"
]
lineas = [
    "Linea 1",  "Linea 2", 
    "Linea 3",  "Linea 4", 
    "Linea 4A", "Linea 5",
    "Linea 6"
]

# Interfaz de cada usuario
texto_admin = """
Hola, administrador. Por favor elija una opción

1) Ver denuncias
2) Filtrar por fecha
3) Filtrar por linea
4) Filtrar por estación
5) Salir
"""
texto_usuario = """
Por favor elija una opción

1) Registrar denuncia
2) Ver denuncias
3) Salir
"""

#   FUNCIONES
# Calcula el tiempo que paso desde X fecha
def tiempoDesde(fecha):
    ahora = datetime.datetime.now()

    # Calcula el tiempo en segundos desde la fecha
    duracion = (ahora - fecha).total_seconds()

    # Da los minutos desde la fecha
    minutos = duracion//60

    return minutos

# Pide seleccionar una opción de una lista
def pedirOpcion(opciones):
    op = -1
    while op < 1 or op > len(opciones):
        # Imprimir cada opción
        for i in range(len(opciones)):
            print(str(i + 1) + ") " + opciones[i])
        
        # Pedir opción
        op = int(input("=>"))
    
    # Devolver opcion seleccionada
    return opciones[op - 1]

# Imprimir las denuncias del registro
def imprimirDenuncias(filtros = {}):
    # Formato de titulo y denuncias
    formato_titulo = "\n{:^10} | {:^20} | {:^20} | {:^30} | {:^40}"
    formato_linea = "{:^10} | {:^20} | {:20} | {:^30} | {:40}"

    # Imprimir titulo
    titulo = formato_titulo.format("Linea", "Estación", "Tipo denuncia", "Fecha", "Descripción")
    print(titulo)

    # Imprimir denuncias
    for denuncia in denuncias:
        tipo = denuncia["tipo"]
        fecha = denuncia["fecha"]
        descripcion = denuncia["descripcion"]
        linea = denuncia["linea"]
        estacion = denuncia["estacion"]

        # Filtros
        valido = True
        # Filtros de fechas
        if "fecha" in filtros:
            if filtros["fecha"] == "Últimos 30min" and tiempoDesde(fecha) > 30:
                valido = False
            if filtros["fecha"] == "Ultima hora" and tiempoDesde(fecha) > 60:
                valido = False
        # Filtros de lineas
        if "linea" in filtros:
            if filtros["linea"] != linea and filtros["linea"] != "Todas":
                valido = False
        # Filtros de estaciones
        if "estacion" in filtros:
            if filtros["estacion"] != estacion and filtros["estacion"] != "":
                valido = False
        
        # Imprimir lista
        if valido:
            entrada = formato_linea.format(linea, estacion, tipo, str(fecha), descripcion)
            print(entrada)

# Registrar una nueva denuncia en el registro
def registrarDenuncia(linea = ""):
    # Se abre el archivo para añadir nuevas denuncias
    escritor_registro = open(nombre_archivo, "a")

    # Pedir datos para almacenar denuncia
    print("Ingrese el tipo de denuncia")
    tipo = pedirOpcion(tipos_denuncia)

    descripcion = input("Describa la situación =>")
    fecha = datetime.datetime.now()

    if linea == "":
        print("Ingrese la linea en la que se encuentra")
        linea = pedirOpcion(lineas)
    
    estacion = input("Ingrese la estación donde se encuentra =>")
    

    # Objeto de nueva denuncia
    nueva_denuncia = {
        "tipo": tipo,
        "descripcion": descripcion,
        "linea": linea,
        "estacion": estacion,
        "fecha": fecha
    }
    denuncias.append(nueva_denuncia)

    # Se agrega una coma para añadirla a la lista si ya habia una antes
    if(len(denuncias) > 1):
        escritor_registro.write(",")
    
    # Se formatea la denuncia para tener formato JSON
    texto_denuncia = str(nueva_denuncia)
    escritor_registro.write(texto_denuncia.replace("'", '"'))

    # Cierra el archivo para actualizar cambios
    escritor_registro.close()


#   FLUJO PROGRAMA
if __name__ == "__main__":
    # Carga de denuncias a partir del archivo
    lector_registro = open(nombre_archivo, "r")

    registro = "[" + lector_registro.read() + "]"
    denuncias = eval(registro)

    lector_registro.close()
    
    # Comienzo del programa
    nombre = input("Ingrese su nombre =>")

    if nombre.upper() == "ADMIN":
        # Interfaz admin
        filtros = {}
        lineas_fil = ["Todas"]
        lineas_fil.extend(lineas)
        fecha_fil = ["Todas", "Últimos 30min", "Ultima hora"]

        opcion = 0
        while(opcion != 5):
            print(texto_admin, end="")
            opcion = int(input("=>"))

            if opcion < 1 or opcion > 5:
                print("Ingrese una opcion valida")

            if opcion == 1:
                imprimirDenuncias()
            if opcion == 2:
                print("Filtrar fecha por:")
                fecha = pedirOpcion(fecha_fil)
                imprimirDenuncias({"fecha": fecha})
            if opcion == 3:
                print("Filtrar linea por:")
                linea = pedirOpcion(lineas_fil)
                imprimirDenuncias({"linea": linea})
            if opcion == 4:
                print("Filtrar estacion por:")
                estacion = input()
                imprimirDenuncias({"estacion": estacion})
            
    else:
        # Interfaz usuario
        print("Ingrese la linea en la que se encuentra")
        linea = pedirOpcion(lineas)
        filtro = {
            "fecha": "Últimos 30min",
            "linea": linea
        }

        opcion = 0
        while(opcion != 3):
            print(texto_usuario, end="")
            opcion = int(input("=>"))

            if opcion < 1 or opcion > 3:
                print("Ingrese una opcion valida")

            
            if opcion == 1:
                registrarDenuncia(linea)
            if opcion == 2:
                imprimirDenuncias(filtro)