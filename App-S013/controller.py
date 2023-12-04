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

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

csv.field_size_limit(2147483647)



def new_controller():
    """
    Crea una instancia del modelo
    """
    control={'model': None}

    control["model"] = model.new_data_structs()
    return control
    


# Funciones para la carga de datos

def loadData(control, size, memflag=True):
    """
    Carga los datos del reto
    """
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    earthquake_file  = cf.data_dir + 'temblores-utf8' + size + '.csv'

    input_file = csv.DictReader(open(earthquake_file, encoding="utf-8"))
    catalog = control["model"]
    for data in input_file:
        model.adddatamag(catalog, data)
        model.adddatabydate(catalog["bydate"], data)
        model.adddatadepth(catalog["depth"], data)
        model.adddatabydate1(catalog["bydate1"],data)
    #model.sortdates(control["model"]["earthquakes"])
    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(start_time, stop_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return delta_time, delta_memory

    else:
        # respuesta sin medir memoria
        return delta_time, 0

def fill_empty_values(dic):
    newdic = model.fill_empty_values(dic)
    return newdic


# Funciones de manejo de listas

def newSublist(list, position, size):
    return model.newSublist(list, position, size)

def mergelists(list1, list2):
    return model.mergelists(list1, list2)

# Funciones de requerimientos

def req_1(control, low, high, memflag=True):
    """
    Retorna el resultado del requerimiento 1
    """
    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    catalog=control["model"]
    printlist, size=model.req_1(catalog["bydate"], low, high)
    
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)


    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return printlist,size, delta_time, delta_memory
    else:
        return printlist, size, delta_time, 0


def req_2(control, low, high, memflag=True):
    """
    Retorna el resultado del requerimiento 2
    """
    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    catalog=control["model"]
    printlist, event=model.req_2(catalog["mag"], low, high)
    
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)


    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return printlist,event, delta_time, delta_memory
    else:
        return printlist,event, delta_time, 0


def req_3(control, mag, prof, memflag=True):
    """
    Retorna el resultado del requerimiento 3
    """
    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    catalog=control["model"]

    printlist=model.req_3(catalog, mag, prof)
    
    
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)


    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return printlist, delta_time, delta_memory
    else:
        return printlist, delta_time, 0
    



def req_4(control, gap, sig, memflag = True):
    """
    Retorna el resultado del requerimiento 4
    """
    start_time = getTime()
    
    catalog = control["model"]
    if memflag is True:
        tracemalloc.start
        start_memory = getMemory()
        
    events, tevents = model.req_4_v1(catalog, sig, gap)
    
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return events, tevents, delta_time, delta_memory
    else:
        return events, tevents,  delta_time, 0
    
    
    


def req_5(control, depth, nst, consultnum, memflag = True):
    """
    Retorna el resultado del requerimiento 5
    """
    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    ndates, nevents, printlist = model.req_5(control["model"], depth, nst, consultnum)

    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)


    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return ndates, nevents, printlist, delta_time, delta_memory
    else:
        return ndates, nevents, printlist, delta_time, 0
    
def req_6(control):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(control, year, area, property, memflag=True):
    """
    Retorna el resultado del requerimiento 7
    """
    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    num_filtered_events, num_histogram_events, min_property_value, max_property_value, property_values, histogram_events = model.req_7(control["model"], year, area, property)

    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)


    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return num_filtered_events, num_histogram_events, min_property_value, max_property_value, property_values, histogram_events, delta_time, delta_memory
    else:
        return num_filtered_events, num_histogram_events, min_property_value, max_property_value, property_values, histogram_events, delta_time, 0


def req_8(memflag=True):
    """
    Retorna el resultado del requerimiento 8
    """
    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    model.req_8()

    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)


    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return delta_time, delta_memory
    else:
        return delta_time, 0


# Funciones para medir tiempos de ejecucion

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

# Funciones para medir memoria utilizada en la ejecucion

def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(stop_memory, start_memory):
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
