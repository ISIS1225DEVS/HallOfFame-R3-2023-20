"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om

assert cf
from tabulate import tabulate
import traceback

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    control = controller.new_controller()
    return control

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1 - Conocer los eventos sísmicos entre dos fechas")
    print("3- Ejecutar Requerimiento 2 - Conocer los eventos sísmicos entre dos magnitudes")
    print("4- Ejecutar Requerimiento 3- Consultar los 10 eventos más recientes según una magnitud y profundidad indicadas ")
    print("5- Ejecutar Requerimiento 4 - Consultar los 15 eventos sísmicos más recientes según su significancia y una distancia azimutal")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6- Reportar el evento más significativo y los N eventos más próximos cronólogicamente ocurridos dentro del área alrededor de un punto ")
    print("8- Ejecutar Requerimiento 7 - Graficar un histograma anual de los eventos ocurridos según la región y propiedades de los eventos")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")

def print_tamano():
    print("1. small")
    print("2. 5%")
    print("3. 10%")
    print("4. 20%")
    print("5. 30%")
    print("6. 50%")
    print("7. 80%")
    print("8. Large")

def load_data(control,escogido,memoria):
    """
    Carga los datos
    """
    data = controller.load_data(control, escogido,memoria)
    return data

#Funciones de print

def print_data(control,data):
    """
        Función que imprime un dato dado su 
    """
    print(f"earthquake event size: {data[0]}")

    d_time = data[1][0]
    d_memory = data[1][1]

    print(f"El parametro 'DELTA TIME' corresponde a: {d_time}")
    if d_memory != False:
        print(f"El parametro 'DELTA MEMORY' corresponde a: {d_memory}")

    printeoTitulo("EARQUAKE RECORDS REPORT")
    #cada columna de los datos
    headers = ["code","time","lat","long",
               "mag","title","depth","felt",
               "cdi", "mmi", "tsunami"]
    
    interes = "sismos"
    tablita = controller.makeTablita(control, headers, interes, data[0],10)

    print("\n")
    print(tablita)

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    inicialDate = input("Fecha inicial: ")+":00.000Z"
    finalDate = input("Fecha final: ")+":00.000Z"
    data,deltas = controller.req_1(control,inicialDate, finalDate,"F")

    printeoTBase("Req No. 1 Inputs")
    print(f"Star date: {inicialDate}")
    print(f"End date: {finalDate}")

    printeoTBase("Req No. 1 Results")

    print(f"Total different dates: {data[0]}")
    print(f"Total events between dates: {data[1]}")
    d_time = deltas[0]

    print(f"El parametro 'DELTA TIME' corresponde a: {d_time}")
    print("\n")

    print(f"Consult size: {data[0]} Only first and last 3 results are:" )

    #cada columna de los datos
    headers = ["time","events", "details"]
    tablita = controller.makeTablitaMap_1(data[2], headers, data[0])

    print("\n")
    print(tablita)

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    inicialMag = (input("El límite inferior de la magnitud:"))
    finalMag = (input("El límite superior de la magnitud: "))
    data,deltas = controller.req_2(control,inicialMag, finalMag,"F")

    printeoTBase("Req No. 2 Inputs")
    print(f"Star mag: {inicialMag}")
    print(f"End mag: {finalMag}")

    printeoTBase("Req No. 2 Results")

    print(f"Total different magnitudes: {data[0]}")
    print(f"Total events between magnitudes: {data[1]}")
    d_time = deltas[0]

    print(f"El parametro 'DELTA TIME' corresponde a: {d_time}")
    print("\n")

    print(f"Only first and last 3 results are:" )

    #cada columna de los datos
    headers = ["mag","events", "details"]
    tablita = controller.makeTablitaMap_2(data[2], headers, data[0])

    print("\n")
    print(tablita)



def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    magni = input("La magnitud mínima a tener en cuenta: ")
    depth = input("La profundidad máxima a tener en cuenta: ")
    data,deltas = controller.req_3(control,magni, depth,"F")

    printeoTBase("Req No. 3 Inputs")
    print(f"Min significance: {magni}")
    print(f"Max gap: {depth}")

    printeoTBase("Req No. 3 Results")

    print(f"Total different dates: {data[0]}")
    print(f"Total events between dates: {data[1]}")
    d_time = deltas[0]

    print(f"El parametro 'DELTA TIME' corresponde a: {d_time}")
    print("\n")

    print(f"Consult size: {data[0]} Only first and last 3 results are:" )

    #cada columna de los datos
    headers = ["time","events", "details"]
    tablita = controller.makeTablitaMap_3(data[2], headers, om.size(data[2]))

    print("\n")
    print(tablita)


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    signif = input("La significancia mínima que quiere tener en cuenta: ")
    gap = input("La distancia azimutal máxima que quiere tener en cuenta: ")
    data,deltas = controller.req_4(control,signif, gap,"F")
    printeoTBase("Req No. 4 Inputs")
    print(f"Min significance: {signif}")
    print(f"Max gap: {gap}")

    printeoTBase("Req No. 4 Results")

    print(f"Total different dates: {data[0]}")
    print(f"Total events between dates: {data[1]}")
    d_time = deltas[0]

    print(f"El parametro 'DELTA TIME' corresponde a: {d_time}")
    print("\n")

    print(f"Consult size: {data[0]} Only first and last 3 results are:" )
    
    #cada columna de los datos
    headers = ["time","events", "details"]
    tablita = controller.makeTablitaMap_1(data[2], headers, data[0])

    print("\n")
    print(tablita)


def print_req_5(control):
    """
    Imprime el resultado del requerimiento 5
    """
    mindepth = input("La profundidad mínima a tener en cuenta: ")
    minnst = input("El número mínimo de estaciones a tener en cuenta: ")
    resultado, total = controller.req_5(control, mindepth, minnst)

    if total == 0:
        print("No se encontraron eventos que cumplan con los criterios especificados.")
    else:
        print(f"Total de eventos encontrados: {total}")

        for event in resultado:
            print("===================================")
            print(f"Fecha y Hora del evento: {event['time']}")
            print(f"Magnitud del evento: {event['mag']}")
            print(f"Latitud: {event['lat']}")
            print(f"Longitud: {event['long']}")
            print(f"Profundidad: {event['depth']}")
            print(f"Significancia: {event['sig']}")
            print(f"Distancia azimutal: {event['gap']}")
            print(f"Número de estaciones utilizadas: {event['nst']}")
            print(f"Título del evento sísmico: {event['title']}")
            print(f"Intensidad máxima (DYFI): {event['cdi']}")
            print(f"Intensidad máxima instrumental estimada: {event['mmi']}")
            print(f"Algoritmo de cálculo de magnitud: {event['magType']}")
            print(f"Tipo de evento sísmico: {event['type']}")
            print(f"Código del evento: {event['code']}")
            print("===================================")

        if total > 20:
            print("... y más eventos.")


def print_req_6(control, year, latRef, longRef, radio, n ):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    tablaMaxArea, tablaTop, totalEventsArea, totalSubList, maxArea = controller.req_6(control, year, latRef, longRef, radio, n)
    
    print('\n ========== Req No. 6 Results ==========')
    print('Number of events within radius: '  + str(totalEventsArea))
    print('Max number of possible events: ' +str(2*n ))
    print('Total events: ' + str(totalSubList) + '\n')
    print('----- Max Event -----')
    print(tablaMaxArea)
    print('----- Nearest Events in chronological order -----')
    print('Most important events relate to the max event: ' + str(maxArea['code']) )
    print('\n')
    print('Consult size: ' + str(totalSubList)  + ' Only first and last 3 results are:  ')
    print(tablaTop)


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    year = input("Favor indique el año del cual desea conocer los eventos: ")
    title = input("Favor indique el titulo de la region: ")
    propiedad = input("Favor indique la propiedad que desea tener en cuenta: ")
    bins = input("Favor indicar el número de intervalos que deasea ver en el histograma: ")
    data,deltas = controller.req_7(control,year, title, propiedad, bins,"F")

    printeoTBase("Req No. 7 Inputs")
    print(f"Year: {year}")
    print(f"Area of interest: {title}")
    print(f"Property of interest: {propiedad}")
    print(f"Number of bins: {bins}")

    printeoTBase("Req No. 7 Results")

    d_time = deltas[0]

    print(f"El parametro 'DELTA TIME' corresponde a: {d_time}")
    print("\n")

    print(f"Consult size: {data[0]} Only first and last 3 results are:" )
    
    # Cada columna de los datos
    headers = ["time","lat", "long", "title", "code", propiedad]
    
    controller.crear_imagen(data[2],data[3],propiedad, title, year, headers, data[1],bins)
    

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass

def printeoTitulo(texto):
    numLineas = (50 - len(texto) - 2) //2
    print("\n"+"="*50)
    print("="*numLineas + " " + texto + " "+ "="*numLineas)
    print("="*50)

def printeoTBase(texto):
    numLineas = (50 - len(texto) - 2) //2
    print("\n")
    print("="*numLineas + " " + texto + " "+ "="*numLineas)

# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')

        if int(inputs) == 1:
            control = new_controller()
            print("Favor indicar el tamaño de los archivos con los cuales desea trabajar")
            print_tamano()
            numerito = int(input("Escoja tamaño: "))
            escogido = controller.escogerTamano(numerito)
            print("Entre los parametros del programa que se desean conocer siempre se tendrá 'DELTA TIME'.")
            print("Puede conocer, además, el parametro 'DELTA MEMORIA' para analisis de la eficiencia del programa.")
            print("Por lo anterior:")
            memoria = input("Especifique si desea conocer el parametro 'DELTA MEMORIA' (True/False): ")
            print(f"Cargando información de los archivos con tamaño {escogido}....\n")
            data = load_data(control,escogido,memoria)
            print_data(control,data)

        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            year = input('ingrese el año a consultar: ')
            latRef = float(input('Ingrese la latitud de referencia: '))
            longRef = float(input('Ingrese la longitud de referencia: '))
            radio = float(input('Ingrese el radio del area: '))
            n = int(input('Ingrese la cantidad de elementos a consultar: '))
                
            print_req_6(control, year, latRef, longRef, radio, n )

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
