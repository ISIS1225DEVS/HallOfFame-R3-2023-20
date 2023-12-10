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
assert cf
from tabulate import tabulate
import traceback
import sys
import datetime

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
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    return controller.new_controller() 


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
    #TODO: Realizar la carga de datos
    tamaño = input('selecciona el tamaño de la muestra de datos que desea cargar: \n')
    size_data = tamaño
    size_temblores = controller.load_data(control, size_data)
    print('-----------------------------------------------------------------------------------------------')
    print('Tamaño total de la lista de temblores: ' + str(size_temblores))
    print('----------------------------------------------------------------------------------------------- \n')
    temblores = getn(control['model']['temblores'],5)
    lista_copia = [{'code': d['code'], 'time': d['time'], 'lat': d['lat'], 'long': d['long'], 'mag': d['mag'], 'title': d['title'],
            'depth': d['depth'], 'felt': d['felt'], 'cdi': d['cdi'], 'mmi': d['mmi'], 'tsunami' :d['tsunami']} for d in lt.iterator(temblores)]
    print('===================================================================================================' + '\n')
    print('-------EARTHQUAKE DATA--------' + '\n')    
    print('===================================================================================================' + '\n')
    print('printing the first 5 and the 5 last elements of the list \n')
    print(tabulate(lista_copia, headers='keys', tablefmt='fancy_grid'))


    
def getn(lista,n):
    if lt.size(lista) > n:
        first= lt.subList(lista, 1,n)
        last = lt.subList(lista, lt.size(lista)-(n-1),n)
        
        for elementos in lt.iterator(last):
            lt.addLast(first, elementos)
        return first
    else:
        return lista


def print_req_1(control, date1, date2):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    size, lista , delta = controller.req_1(control, date1, date2)
    print('===================================================================================================' + '\n')
    print ('Numero de eventos entre ' + date1 + ' y ' + date2 + ': ' + str(size))
    lista = getn(lista,3)
    print('Tiempo estimado [ms]: ' + str(delta) )
    print(tabulate(lt.iterator(lista), headers='keys', tablefmt='fancy_grid'))

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    limite_inf = float(input('Favor ingrese la magnitud que desea trabajar como limite inferior en la busqueda\n'))
    limite_sup = float(input('Favor ingrese la magnitud que desea trabajar como limite superior en la busqueda\n'))
    size, keys, lista, delta, llave = controller.req_2(control, limite_inf, limite_sup)
    print('Total different magnitudes: {}'.format(keys))
    print('Total events between {} and {}: {}'.format(limite_inf, limite_sup, size))
    print('Total events only in firs and last 3: {}'.format(llave))
    print('El tiempo total de consulta es de {}ms'.format(delta))
    print(tabulate(lt.iterator(lista), headers= 'keys', tablefmt='fancy_grid'))


def print_req_3(control, mag, profundidad):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    
    lista,numero,delta = controller.req_3(control, mag, profundidad)
    print('===================================================================================================' + '\n')
    print ('Numero de eventos: ' + str(numero))
    lista = getn(lista,3)
    print('Tiempo estimado [ms]: ' + str(delta) )
    print(tabulate(lt.iterator(lista), headers='keys', tablefmt='fancy_grid'))

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    sigMin = float(input('Favor ingrese el numero de significancia minima que desea consultar\n'))
    gapMax = float(input('Favor ingrese el numero de distancia azimutal maxima\n'))

    total_dates, total_events, lista = controller.req_4(control, sigMin, gapMax)
    print('Numero de fechas con mas de ' + str(sigMin) + ' eventos: ' + str(total_dates))
    print('Numero de fechas con mas de ' + str(sigMin) + ' eventos: ' + str(total_dates))
    print("\n")
    if lt.size(lista) > 15:
        lista = lt.subList(lista, 1,15)
    titulos = ['mag', 'lat', 'long', 'title', 'depth', 'felt', 'cdi', 'mmi', 'magType', 'type', 'code']
    for dato in lt.iterator(lista):
        dato["details"] = tabulate(lt.iterator(filtrar(dato["details"],titulos)), headers='keys', tablefmt='fancy_grid')
    print(tabulate(lt.iterator(getn(lista,3)), headers='keys', tablefmt='fancy_grid'))



def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    prof_min = float(input('Favor ingrese la profundidad minima que desea consultar\n'))
    num_estaciones = float(input('Favor ingrese el numero minimo de estaciones que detectan el evento\n'))
    size, eventos, lista, delta = controller.req_5(control, prof_min, num_estaciones)
    print('Total different dates : {}'.format(size))
    print('Total events between {} depth and {}nst : {}'.format(prof_min, num_estaciones, eventos))
    print('Total time: {}'.format(delta))
    print(tabulate(lt.iterator(lista), headers= 'keys', tablefmt= 'fancy_grid'))

def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    anio = input('Ingresa el año: ')
    lat = input('Ingresa la latitud (lat): ')
    long = input('Ingresa la longitud (long): ')
    radio = input('ingresa el radio :')
    n = input('Ingresa el numero: ')
    numero_eventos, maximo_eventos, numero_fechas, eventos_entre_fechas, lista_max, lista_eventos, delta = controller.req_6(control, anio, lat, long, radio, n)
    print('Tiempo estimado [ms] :' + str(delta))
    print('Numero de eventos con radio de ' + radio + ' [km]: ' + str(numero_eventos))
    print('Numero de eventos maximos con radio de ' + radio + ' [km]: ' + str(maximo_eventos))
    print('Numero de eventos en el año ' + anio + ': ' + str(numero_fechas))
    print('Numero de eventos entre fechas: ' + str(eventos_entre_fechas),"\n")
    titulos = ['time', 'mag', 'lat', 'long', 'title', 'depth', 'felt', 'cdi', 'mmi', 'magType', 'type', 'code']
    print(tabulate(lt.iterator(filtrar(lista_max,titulos)), headers='keys', tablefmt='fancy_grid'))
    print(tabulate(lt.iterator(getn(lista_eventos,3)), headers='keys', tablefmt='fancy_grid'))
    


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    anio = int(input('Favor ingrese el año que desea analizar\n'))
    title = input('Favor ingrese el lugar de la region asociada que desea analizar\n').lower()
    propiedad = input('Favor ingrese la propiedad que desea: mag, depth o sig\n').lower()
    div = int(input('Favor ingrese el numero de casillas que desea\n'))
    delta = controller.req_7(control, anio, title, propiedad, div)
    print('El tiempo de impresion de su grafica ha sido de {}ms'.format(delta))

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass

def filtrar(lista,titulos):
    lista_r = lt.newList()
    for dato in lt.iterator(lista):
        diccionario = {}
        for titulo in titulos:
             diccionario[titulo] = dato[titulo]
        lt.addLast(lista_r,diccionario)
    return lista_r
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
            fecha1 = input('Fecha inicial del intervalo (en formato "%Y-%m-%dT%H:%M").')
            fecha2 = input('Fecha final del intervalo (en formato "%Y-%m-%dT%H:%M").')
            print_req_1(control, fecha1, fecha2)
        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            mag = input('Ingresa la magnitud que deseas: ')
            profundidad = input('Ingresa la profundidad: ')
            print_req_3(control, mag, profundidad)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

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



