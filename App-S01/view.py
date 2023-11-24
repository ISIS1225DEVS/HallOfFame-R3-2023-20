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
default_limit = 1000
sys.setrecursionlimit(default_limit*10)
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
import matplotlib.pyplot as pl



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
    print("2- Conocer los eventos sísmicos entre dos fechas")
    print("3-  Conocer los eventos sísmicos entre dos magnitudes")
    print("4- Consultar los 10 eventos más recientes según una magnitud y profundidad indicadas ")
    print("5- Consultar los 15 eventos sísmicos más recientes según su significancia y una distancia azimutal ")
    print("6- Consultar los 20 eventos más recientes para una  profundidad dada y registrados por un cierto número de estaciones ")
    print("7-  Reportar el evento más significativo y los N eventos más próximos cronológicamente ocurridos dentro del área alrededor de un punto")
    print("8-  Graficar un histograma anual de los eventos ocurridos según la región y propiedades de los eventos")
    print("0- Salir")


def load_data(control, tamanio, memory):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    temblores, time, memoria = controller.load_data(control, tamanio, memory)
    return temblores, time, memoria
def tamanio_archivo():
    working = True
    while working:
        print ('----------Tamaños disponibles de archivo---------------')
        print("1- 5pct")
        print("2- 10pct")
        print('3- 20pct')
        print('4- 30pct')
        print('5- 50pct')
        print('6- 80pct')
        print('7- large')
        print('8- small')
        opcion = int(input("Seleccione el tamaño de los archivos que desea cargar: \n"))
        tamanio_archivo = "large"
        if opcion == 1:
            tamanio_archivo = "5pct"
            working = False
        elif opcion == 2:
            tamanio_archivo = "10pct"
            working = False
        elif opcion == 3:
            tamanio_archivo = "20pct"
            working = False
        elif opcion == 4:
            tamanio_archivo = '30pct'
            working = False
        elif opcion == 5:
            tamanio_archivo = '50pct'
            working = False
        elif opcion == 6:
            tamanio_archivo = '80pct'
            working = False
        elif opcion == 7:
            tamanio_archivo = 'large'
            working = False
        elif opcion == 8:
            tamanio_archivo = 'small'
            working = False
        else:
            print("ingrese una opción valida")
    return tamanio_archivo



def print_tabla(list, sample=5, maxcol=None):
    size = lt.size(list)
    if size <= sample*2:
        print("Hay menos de", sample*2,  "registros...")
        print(tabulate(lt.iterator(list),headers="keys", tablefmt = "grid", showindex=False, maxcolwidths=maxcol))
    else:
        print("Hay más de", sample*2, "registros...")
        list_sample = lt.subList(list,1,sample)
        list_ultimos = lt.subList(list,size-(sample-1),sample)
        for dato in lt.iterator(list_ultimos):
            lt.addLast(list_sample, dato)
        print(tabulate(lt.iterator(list_sample),headers="keys", tablefmt = "grid", showindex=False, maxcolwidths=maxcol))

def print_carga(list, dt, memoria=False):
    print("--------------------------------------------------------")
    print("Tamaño del archivo de eventos sismicos: ", str(mp.size(list)))
    print("--------------------------------------------------------")
    print()
    print("=========================================================")
    print("============== REPORTE DE EVENTOS SISMICOS ==============")
    print("=========================================================")
    print()
    print("Imprimirendo los primeros 5 y ultimos 5 registros...")
    print()
    print("--- RESULTADOS DE LOS SISMOS ---")
    print("     Total de sismos: "+ str(mp.size(list)))
    print_tabla(list, maxcol=16)
    
    if memoria:
        print("Tiempo total de carga [ms]: " + str(round(dt,3)) + " || Memoria utilizada [kB]: " + str(round(memoria, 3)))
    else:
        print("Tiempo total de carga [ms]: " + str(round(dt,3)))
    print()
    
def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1( total_sismos,total_fechas, Eventos_ocurridos, initialDate , finalDate, d_time ):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    print("=============== REQUERIMIENTO No. 1 Resultados ===============")
    print("Total de fechas diferentes: " + str(total_fechas))
    print("No. total de sismos registrados : "+ str(total_sismos))
    print()
    print_tabla(Eventos_ocurridos,3)
    print()
    print("Tiempo de ejecución: " , round(d_time, 3))
    print()
   


def print_req_2(total_sismos,total_magnitudes, Eventos_ocurridos, d_time):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    print("=============== REQUERIMIENTO No. 2 Resultados ===============")
    print("Total de magnitudes diferentes: " + str(total_magnitudes))
    print("No. total de sismos registrados en el rango de magnitudes ingresado : "+ str(total_sismos))
    print()
    print_tabla(Eventos_ocurridos, 3)
    print()
    print("Tiempo de ejecución: " , round(d_time, 3))
    print()


def print_req_3(total_sismos , total_fechas, eventos_ocurridos,d_time):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    print("=============== REQUERIMIENTO No. 3 Resultados ===============")
    print("Total de fechas diferentes: " + str(total_fechas))
    print("No. total de sismos registrados : "+ str(total_sismos))
    print()
    print_tabla(eventos_ocurridos, 3)
    print()
    print("Tiempo de ejecución: " , round(d_time, 3))
    print()


def print_req_4(total_fechas, total_eventos, eventos, d_time):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    print("=============== REQUERIMIENTO No. 4 Resultados ===============")
    print("Total de fechas diferentes: " + str(total_fechas))
    print("Total de eventos entre fechas: " + str(total_eventos))
    print()
    print_tabla(eventos,3)
    print()
    print("Tiempo de ejecución: " , round(d_time, 3))
    print()


def print_req_5(total_eventos, total_fechas, v_eventos, d_time):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    print("=============== REQUERIMIENTO No. 5 Resultados=================")
    print("Total de fechas en donde ocurrieron eventos con tales caracteristicas: " + str(total_fechas))
    print("Total de eventos ocurridos en estas fechas con tales caracteristicas: " + str(total_eventos))
    print()
    print_tabla(v_eventos,3)
    print()
    print("Tiempo de ejecución: ", round(d_time,3))
    print()
    



def print_req_6(n, t_fecha, e_significativo, t_eventos_radio, n_eventos, te_año, codigo_sig, eventos_depues, eventos_antes, d_time):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    print("===============REQUERMIENTO No. 6 Resultados================")
    print()
    print("Codigo del evento de maxima magnitud: ", codigo_sig)
    print("N eventos posteriores: ", eventos_despues)
    print("N eventos previos: ", eventos_antes)
    print()
    print("Cantidad de eventos en el radio: "+ str(t_eventos_radio))
    print("Cantidad de eventos en el año elegido: " + str(te_año))
    print("Numero maximo de posibles eventos: ", int(n)*2)
    print("Total de fechas diferentes: ", t_fecha)
    print("Total de eventso entre fechas: ", (eventos_antes+eventos_despues+1))
    print()
    print("-------- Evento Maximo --------")
    print(tabulate(lt.iterator(e_significativo), headers="keys", tablefmt = "grid", showindex=False, maxcolwidths=16 ))
    print()
    print("------- Eventos mas cercanos en orden cronologico--------")
    print("Los eventos mas significativos relacionados con el evento maximo: ", codigo_sig)
    print()
    print_tabla(n_eventos, 3)
    print()
    print("Tiempo de ejecución: ", round(d_time,3))
    print()
          
    # TODO: Imprimir el resultado del requerimiento 6
    

def print_req_7(total, fig, time):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    print("=============== Req No. 7 Results ===============")
    print("Tamaño de consulta: " + str(total) + " Los primeros y ultimos 3 registros son:")
    fig
    pl.show()
    print("Tiepo de ejecución: " , round(time, 3))


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
    memory = False
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            tamanio = tamanio_archivo()
            print("Cargando información de los archivos ....\n")
            temblores, time, memoria = load_data(control, tamanio, memory)
            print_carga(temblores, time, memoria)
        elif int(inputs) == 2:

            initialDate= input("Ingrese la fecha incial de su interés: \n")
            finalDate= input("Ingrese la fecha final de su interés: \n")
            total_sismos , total_fechas, Eventos_ocurridos, d_time =controller.req_1 (control , initialDate, finalDate)
            print_req_1(total_sismos,total_fechas,  Eventos_ocurridos, initialDate , finalDate, d_time)
  

        elif int(inputs) == 3:
            limit_inferior= round(float(input("Ingrese el límite inferior del rango de magnitud: ")), 3)
            limit_superior= round(float(input("Ingrese el superior inferior del rango de magnitud: ")), 3)
            total_sismos, total_magnitudes, Eventos_ocurridos , d_time = controller.req_2(control, limit_inferior, limit_superior)
            print_req_2(total_sismos,total_magnitudes, Eventos_ocurridos, d_time)

        elif int(inputs) == 4:
            mag_min = round(float(input("Ingrese el límite inferior del rango de magnitud: ")), 3)
            depth_max = input("Ingrese el limite máximo del rango de profundidades:  ")
            print("Buscando la información solicitada ...")
            total_sismos ,total_fechas,  eventos_ocurridos, d_time = controller.req_3(control, mag_min, depth_max)
            print_req_3(total_sismos,total_fechas, eventos_ocurridos, d_time)

        elif int(inputs) == 5:
            sig = input("Ingrese la significancia: \n")
            gap = input("Ingrese la distancia azimutal: \n")
            total_fechas, total_eventos, eventos, d_time = controller.req_4(control, sig, gap)
            print_req_4(total_fechas, total_fechas, eventos, d_time)

        elif int(inputs) == 6:
            profundidad= input("Ingrese el minimo de profundidad: \n ")
            estaciones= input("Ingrese la cantidad minima de estacionea: \n")
            total_eventos, total_fechas, v_eventos, d_time = controller.req_5(control, profundidad, estaciones)
            print_req_5(total_eventos,total_fechas,v_eventos,d_time)

        elif int(inputs) == 7:
            anio= input("Ingrese el año que desee consultar: \n")
            lat=input("ingrese la latitud de referncia: \n")
            long=input("Ingrese la longitud de referencia: \n")
            radio=input("Ingrese el radio del area circudante: \n")
            n=input( "Ingrese la cantidad de eventos que desee revisar: \n")
            t_fecha, e_significativo, t_eventos_radio, n_eventos, te_año, codigo_sig, eventos_despues, eventos_antes, d_time= controller.req_6(control, anio, lat, long, radio, n)
            print_req_6(n, t_fecha, e_significativo, t_eventos_radio, n_eventos, te_año, codigo_sig, eventos_despues, eventos_antes,  d_time)

        elif int(inputs) == 8:
            anio = input("Ingrese el año de interes: \n")
            prop = input("Ingrese la propiedad de interes (mag, sig, depth): \n")
            region = input("Ingrese la region de interes: \n")
            bins = input("Ingrese el numero de segmentos para el histograma: \n")
            print("Buscando la información solicitada ...")
            total, fig, time = controller.req_7(control, anio, region, prop, bins)
            print_req_7(total, fig, time)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
