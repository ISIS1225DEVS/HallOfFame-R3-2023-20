"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import time
import csv
import tracemalloc
import datetime

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    catalog = model.newCatalog()
    return catalog


# Funciones para la carga de datos

def load_data(catalog, escogido,memoria):
    """
    Carga los datos del reto
    """
    deltas = inicializardelta(memoria)
    sismosfile = cf.data_dir + 'temblores-utf8-'+escogido +'.csv'
    input_file = csv.DictReader(open(sismosfile, encoding="utf-8"),
                                delimiter=",")
    for sismo in input_file:
        sismo = model.sismo_correcto(sismo)
        model.add_data(catalog, sismo)
    tamano = model.sismosSize(catalog)
    deltas = calcular_deltas(memoria,deltas)
    return tamano,deltas

def inicializardelta(memoria):
    datoMemoria = 0
    if memoria == "True":
        tracemalloc.start()
        datoMemoria = get_memory()
    
    datoTime = get_time()

    return datoTime,datoMemoria

def calcular_deltas(memoria, inicial):
    itime, imemoria = inicial
    ftime = get_time()

    if memoria == "True":
        fmemoria = get_memory()
        tracemalloc.stop()

    time_d = delta_time(itime,ftime)
    memoria_d = False
    if memoria == "True":
        memoria_d = delta_memory(fmemoria,imemoria)
    
    return time_d, memoria_d

    
def escogerTamano(numerito):
    if numerito == 1:
        escogido = "small"
    elif numerito == 2:
        escogido = "5pct"
    elif numerito == 3:
        escogido = "10pct"
    elif numerito == 4:
        escogido = "20pct"
    elif numerito == 5:
        escogido = "30pct"
    elif numerito == 6:
        escogido = "50pct"
    elif numerito == 7:
        escogido = "80pct"
    elif numerito == 8:
        escogido = "large"
    else:
        print("opción invalida, predeterminado small")
        escogido = "small"
    return escogido

def makeTablita(catalog, headers, interes, tamano,n):
    tablita = model.makeTablita(catalog[interes], headers, tamano,n)
    return tablita

def makeTablitaMap_1 (list_map, nombres, tamano):
    tablita = model.makeTablitaMap_1 (list_map, nombres, tamano)
    return tablita
def makeTablitaMap_2 (list_map, nombres, tamano):
    tablita = model.makeTablitaMap_2 (list_map, nombres, tamano)
    return tablita
def makeTablitaMap_3(list_map, nombres, tamano):
    tablita = model.makeTablitaMap_3 (list_map, nombres, tamano)
    return tablita
# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control,inicialDate, finalDate, memoria):
    """
    Retorna el resultado del requerimiento 1
    """
    deltas = inicializardelta(memoria)
    inicialDate = datetime.datetime.strptime(inicialDate, "%Y-%m-%dT%H:%M:%S.%fZ")
    finalDate = datetime.datetime.strptime(finalDate, "%Y-%m-%dT%H:%M:%S.%fZ")
    data = model.req_1(control,inicialDate, finalDate)
    deltas = calcular_deltas(memoria,deltas)
    return data, deltas

def req_2(control,inicialMag, finalMag, memoria):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    deltas = inicializardelta(memoria)
    inicialMag= float(inicialMag)
    finalMag = float(finalMag)
    data = model.req_2(control,inicialMag, finalMag)
    deltas = calcular_deltas(memoria,deltas)
    return data, deltas



def req_3(control, magni, depth, memoria):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    deltas = inicializardelta(memoria)
    magni=float(magni)
    depth = float(depth)
    data= model.req_3(control, magni, depth)
    deltas = calcular_deltas(memoria,deltas)
    return data, deltas


def req_4(control, signif, gap, memoria):
    """
    Retorna el resultado del requerimiento 4
    """
    deltas = inicializardelta(memoria)
    gap = float(gap)
    data= model.req_4(control, signif, gap)
    deltas = calcular_deltas(memoria,deltas)
    return data, deltas


def req_5(control, mindepth, minnst):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    return model.req_5(control, mindepth, minnst)

def req_6(control, year, latRef, longRef, radio, n):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    timeInicial = get_time()
    tablaMaxArea, TablaTop, totalEventsArea, totalSubList, maxArea= model.req_6(control, year, latRef, longRef, radio, n )
    timeFinal = get_time()
    print("El tiempo de la función 2 es de: "+str(delta_Time(timeInicial,timeFinal))+"m/s")
    
    return tablaMaxArea, TablaTop, totalEventsArea, totalSubList, maxArea


def req_7(control,year, title, propiedad, bins,memoria):
    """
    Retorna el resultado del requerimiento 7
    """
    deltas = inicializardelta(memoria)
    year = datetime.datetime.strptime(year, "%Y")
    bins = int(bins)
    data= model.req_7(control, year, title, propiedad, bins)
    deltas = calcular_deltas(memoria,deltas)
    return data, deltas

def crear_imagen(intervalos, values, propiedad, title, year, headers, datos,bins):
    return model.crear_imagen(intervalos,values, propiedad, title, year, headers, datos,bins)

def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory

def delta_Time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return round(elapsed,2)
