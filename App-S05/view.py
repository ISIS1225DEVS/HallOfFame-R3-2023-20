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
import time
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
from DISClib.ADT import orderedmap as om
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

default_limit = 1000
sys.setrecursionlimit(default_limit*10)
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
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    print('\nCuántos datos desea cargar?')
    print('1: Pocos datos')
    print('2: 5% de los datos')
    print('3: 10% de los datos')
    print('4: 20% de los datos')
    print('5: 30% de los datos')
    print('6: 50% de los datos')
    print('7: 80% de los datos')
    print('8: 100% de los datos')
    llave = True
    while llave == True:
        size = input("Ingrese la opcion que desea:\n")
        size = int(size)
        if size in range(0,9):
            llave = False
            if size == 1:
                size = "small"
            elif size == 2:
                size = "5pct"
            elif size == 3:
                size = "10pct"
            elif size == 4:
                size = "20pct"
            elif size == 5:
                size = "30pct"
            elif size == 6:
                size = "50pct"
            elif size == 7:
                size = "80pct"
            elif size == 8:
                size = "large"
            results = controller.load_data(control, size)
        else:
            print("ingrese una opción valida")
    controller.sort(control)
    print("\nLoaded Earthquakes: "+str(lt.size(control["model"]['temblores']))+"\n")
    print_data(control)

def print_data(control):
    """
        Función que imprime un dato dado su ID
    """
    headers=["code","time","lat","long","mag","title","depth","felt","cdi","mmi","tsunami"]
    datos = controller.get_firts_and_last_5(control["model"])
    print(tabulate(datos, headers= headers, tablefmt="grid"))

def print_req_1(control, fecha_inicial, fecha_final):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    respuesta = controller.req_1(control, fecha_inicial, fecha_final)
    headers=["time","events","details"]
    print("El tiempo que duro en realizar este requerimiento en ms fueron " +  str(round(respuesta[2],2)))
    print('Total events between dates '+ str(respuesta[1]))
    print(tabulate(respuesta[0], headers= headers, tablefmt="grid"))
    
def print_req_2(control, min_mag, max_mag) :
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    respuesta = controller.req_2(control, min_mag, max_mag)
    print("El tiempo que duro en realizar este requerimiento en ms fueron " +  str(round(respuesta[1],2)))
    headers=["mag","events","details"]
    print('Total Different magnitudes: '+ str(respuesta[2]))
    print('Total events between dates: '+ str(respuesta[3]))
    print(tabulate(respuesta[0], headers= headers, tablefmt="grid"))

def print_req_3(control, mag_min, prof_max):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    respuesta = controller.req_3(control, mag_min, prof_max)
    print("El tiempo que duro en realizar este requerimiento en ms fueron " +  str(round(respuesta[2],2)))
    headers=["time","events","details"]
    print('Total events between dates: '+ str(respuesta[1]))
    print(tabulate(respuesta[0], headers= headers, tablefmt="grid"))


def print_req_4(control,significancia,azimutal_maxima):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    results = controller.req_4(control,float(significancia),float(azimutal_maxima))
    print("\nEl numero de eventos sismicos registrados es de: "+str(results[1])+"\n")
    print(results[0])


def print_req_5(control, depthMin, nstMin):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    tabla, eventos,time = controller.req_5(control, depthMin, nstMin)
    print('\n ========== Req No. 5 Results ==========')
    print('Total events between dates: ' + str(eventos))
    print('Selecting the first 20 results... \n')
    print('Consult size: ' + str(eventos) + ' The first and last 3 of the 20 results are: ')
    print(tabla)
    print('\nTiempo de ejecución: ' + str(time))


def print_req_6(control, year, latRef, longRef, radio, n ):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    tablaMaxArea, tablaTop, totalEventsArea, totalSubList, maxArea, time = controller.req_6(control, year, latRef, longRef, radio, n)
    
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
    print('\nTiempo de ejecución: ' + str(time))

def print_req_7(control, año, title, prop, bins):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    respuesta = controller.req_7(control, año, title, prop, bins)
    print("El tiempo que duro en realizar este requerimiento en ms fueron " +  str(round(respuesta[1],2)))
    if respuesta[0][0]<6:
        mensaje = ", se mostraran todos los datos."
    else:
        mensaje = ", se mostraran los primeros y ultimos 3 datos."
    print("\nEl tamaño de la consulta fue de "+str(respuesta[0][0])+mensaje+"\n")
    columnas = respuesta[0][1]
    for columna in columnas[2]:
        altura = columna.get_height()
        plt.text(columna.get_x() + columna.get_width()/2., altura + 0.1, f'{int(altura)}', ha='center', va='bottom')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('mag')
    plt.ylabel('No. Events')
    plt.title('Histograma de '+str(prop)+' en '+str(title)+' en '+str(año))
    plt.show()
    
    tabla_texto = respuesta[0][2]
    fig,ax = plt.subplots()
    plt.text(0.1, 0.1, tabla_texto, va='center', ha='left', family='monospace', fontsize=10)
    ax.axis('off')
    plt.title('Detalles del evento en '+title+" en "+str(año))
    plt.show()
    
    return  
    


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


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
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 2:
            fecha_inicial = input("Ingrese la fecha inicial en formato %Y-%m-%dT%H:%M: ")
            fecha_final = input("Ingrese la fecha final en formato %Y-%m-%dT%H:%M: ")
            print_req_1(control, fecha_inicial, fecha_final)

        elif int(inputs) == 3:
            min_mag = input("Ingrese el límite inferior de la magnitud (float): ")
            max_mag = input("Ingrese el límite superior de la magnitud (float): ")
            print_req_2(control, min_mag, max_mag)

        elif int(inputs) == 4:
            mag_min = input("Ingrese la magnitud minima del evento: ")
            prof_max = input("Ingrese la profundidad maxima del evento: ")
            print_req_3(control, mag_min, prof_max)

        elif int(inputs) == 5:
            significancia = input("Ingrese la significancia minima del evento: ")
            azimutal_maxima = input("Ingrese la distancia azimutal maxima del evento: ")
            print_req_4(control,significancia,azimutal_maxima)

        elif int(inputs) == 6:
            depthMin = input('Ingrese la profundidad Minima: ')
            nstMin = input('Ingrese la nst Minima: ')
            print_req_5(control, depthMin, nstMin)

        elif int(inputs) == 7:
            year = input('ingrese el año a consultar: ')
            latRef = float(input('Ingrese la latitud de referencia: '))
            longRef = float(input('Ingrese la longitud de referencia: '))
            radio = float(input('Ingrese el radio del area: '))
            n = int(input('Ingrese la cantidad de elementos a consultar: '))
                
            print_req_6(control, year, latRef, longRef, radio, n )

        elif int(inputs) == 8:
            año = input("Ingrese el año que desea consultar (en formato %Y): ")
            title = input("Ingrese el titulo de la region asociada: ")
            prop = input("Ingrese la propiedad de conteo (magnitud, profundida o significancia): ")
            bins = input("Ingrese el numero de bins que desea: ")
            print_req_7(control, año, title, prop, bins)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")

