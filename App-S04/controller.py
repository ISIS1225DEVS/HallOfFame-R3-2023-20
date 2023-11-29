﻿"""
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
csv.field_size_limit(2147483647)
import tracemalloc
import sys

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {'model': None}
    control['model'] = model.new_data_structs()
    return control


### Funciones para la carga de datos

def load_data(control, size, memflag, choice):
    """
    Carga los datos del reto
    """
    data_structs = control['model']
    
    start_time = get_time()
    
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
    
    ti_t = get_time()
    t_size= load_earthquakes_data(data_structs, size, choice)
    tf_t = get_time()
    delta_t_t = delta_time(ti_t,tf_t)
        
    # Ordenamiento de las estructuras de los requerimientos
    size = t_size
    time = delta_t_t
    
    sort(data_structs['req1y6'], 'req6')
    # toma el tiempo al final del proceso
    stop_time = get_time()
    # calculando la diferencia en tiempo
    d_time = delta_time(start_time, stop_time)
    
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        d_memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return size, time, d_time, d_memory
    else:
        return size, time, d_time, None

def load_earthquakes_data(data_structs, size, choice):
    resultsfile = cf.data_dir + 'earthquakes/temblores-utf8-'+size+'.csv'
    input_file = csv.DictReader(open(resultsfile, encoding='utf-8'))
    for result in input_file:
        model.add_data(data_structs, result, choice)
    return model.data_size(data_structs, 'temblores')

def create_data_list(sorted_list, n):
    new_list = model.new_topbot_sublist(sorted_list, n)
    return new_list


# Funciones de ordenamiento

def sort(data_structs, file_name):
    """
    Ordena los datos del modelo
    """
    # Llamar la función del modelo para ordenar los datos
    return model.sort(data_structs, file_name)


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, start_date, end_date, memflag, n):
    """
    Retorna el resultado del requerimiento 1
    """
    data_structs = control['model']
    
    ti = get_time()
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
        
    events_list, count = model.req_1(data_structs, start_date, end_date)
    
    tf = get_time()
    time = delta_time(ti, tf)
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
    else:
        memory = None
        
    if model.data_size(events_list) <= 2*n:
        return events_list, None, count, time, memory
    else:
        return events_list, model.new_topbot_sublist(events_list, n), count, time, memory


def req_2(control, start_mag, end_mag, memflag, n):
    """
    Retorna el resultado del requerimiento 2
    """
    # Modificar el requerimiento 2
    data_structs = control['model']
    
    ti = get_time()
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
        
    events_list, count = model.req_2(data_structs, start_mag, end_mag)
    
    tf = get_time()
    time = delta_time(ti, tf)
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
    else:
        memory = None
        
    if model.data_size(events_list) <= 2*n:
        return events_list, None, count, time, memory
    else:
        return events_list, model.new_topbot_sublist(events_list, n), count, time, memory


def req_3(control, min_mag, max_depth, memflag, n):
    """
    Retorna el resultado del requerimiento 3
    """
    # Modificar el requerimiento 3
    data_structs = control['model']
    
    ti = get_time()
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
        
    events_list, count = model.req_3(data_structs, min_mag, max_depth)
    
    tf = get_time()
    time = delta_time(ti, tf)
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
    else:
        memory = None
        
    if model.data_size(events_list) <= 2*n:
        return events_list, None, count, time, memory
    else:
        return events_list, model.new_topbot_sublist(events_list, n), count, time, memory


def req_4(control,memflag,min_sig,max_gap):
    """
    Retorna el resultado del requerimiento 4
    """
    # Modificar el requerimiento 4
    data_structs = control['model']
    
    ti = get_time()
    
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
        
    file = model.req_4(data_structs, min_sig, max_gap)
    
    tf = get_time()
    time = delta_time(ti, tf)
    
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
    else:
        memory = None   
    #print("TIME: ",tf)
    #print("MEMORY: ",memory)              
    return file

def req_5(control, stations, depth, memflag):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    data_structs = control['model']
    
    ti = get_time()
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
        
    events_list, count = model.req_5(data_structs, depth, stations)
    
    tf = get_time()
    time = delta_time(ti, tf)
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
    else:
        memory = None
        
    return events_list, model.new_topbot_sublist(events_list, 3), count, time, memory

def req_6(control, year, r, n, latref, longref, memflag, nn):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    data_structs = control['model']
    
    ti = get_time()
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
        
    events_list, count, sig_event = model.req_6(data_structs, year, r, n, latref, longref)
    
    tf = get_time()
    time = delta_time(ti, tf)
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
    else:
        memory = None
        
    if model.data_size(events_list) <= 2*nn:
        return events_list, None, count, time, memory, sig_event
    else:
        return events_list, model.new_topbot_sublist(events_list, nn), count, time, memory, sig_event


def req_7(control, year, title, prop, bins, memflag, n):
    """
    Retorna el resultado del requerimiento 7
    """
    # Modificar el requerimiento 7
    data_structs = control['model']
    
    ti = get_time()
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
        
    events_list, count, histogram_list = model.req_7(data_structs, year, title, prop, bins)
    
    tf = get_time()
    time = delta_time(ti, tf)
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
    else:
        memory = None
        
    if model.data_size(events_list) <= 2*n:
        return events_list, None, count, time, memory, histogram_list
    else:
        return events_list, model.new_topbot_sublist(events_list, n), count, time, memory, histogram_list


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