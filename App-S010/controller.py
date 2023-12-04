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
from collections import defaultdict

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos

    control = {
        model:None
    }
    control = model.new_data_structs()
    

    return control


# Funciones para la carga de datos

def load_data(control, tamanho):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    memflag=True
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory =get_memory()

#logica

    file =  cf.data_dir+"/earthquakes/temblores-utf8-" + tamanho + ".csv"
    input_file = csv.DictReader(open(file, encoding="utf8"))
    for goalscorer in input_file:
        info = model.add_data(control,goalscorer)
        

#fin logica
    stop_time = get_time()
    delta_time_2 = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory_2=delta_memory(stop_memory, start_memory)
    return info, delta_time_2, delta__memory_2




# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    return model.sort(control)


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, fecha_inicial, fecha_final):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    fecha_i = fecha_inicial + ':00.000000Z'
    fecha_f = fecha_final + ':00.000000Z'
    start_time=get_time()
    lista = model.req_1(control, fecha_i, fecha_f)
    stop_time=get_time()
    delta_time_r=delta_time(start_time,stop_time)
    time_events = {}

    
    for event in lista:
        
        full_time = event['time']
        simplified_time = full_time[:16]  

        if simplified_time not in time_events:
            time_events[simplified_time] = {
                'time': simplified_time,
                'eventos': 0,
                'detalles': []
            }

        time_events[simplified_time]['eventos'] += 1

        event_details = event.copy()
        del event_details['time']
        time_events[simplified_time]['detalles'].append(event_details)

    
    r = list(time_events.values())

    return r,delta_time_r

def req_2(control,mag1,mag2):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    start_time=get_time()
    lista= model.req_2(control,mag1,mag2)
    stop_time=get_time()
    delta_time_r=delta_time(start_time,stop_time)
    time_events = {}

    
    for event in lista:
        
        simplified_time = event['mag']
         

        if simplified_time not in time_events:
            time_events[simplified_time] = {
                'mag': simplified_time,
                'eventos': 0,
                'detalles': []
            }

        time_events[simplified_time]['eventos'] += 1

        event_details = event.copy()
        del event_details['mag']
        time_events[simplified_time]['detalles'].append(event_details)

    
    r = list(time_events.values()),delta_time_r

    return r




def req_3(control, magnitud, profundidad):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start_time=get_time()

    lista = model.req_3(control, magnitud, profundidad)
    stop_time=get_time()
    delta_time_r=delta_time(start_time,stop_time)

    time_events = {}

    
    for event in lista:
        
        full_time = event['time']
        simplified_time = full_time[:16]  

        if simplified_time not in time_events:
            time_events[simplified_time] = {
                'time': simplified_time,
                'eventos': 0,
                'detalles': []
            }

        time_events[simplified_time]['eventos'] += 1

        event_details = event.copy()
        del event_details['time']
        time_events[simplified_time]['detalles'].append(event_details)

    
    r = list(time_events.values())

    return r[:10],delta_time_r




def req_4(control,sig,gap):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    start_time=get_time()

    lista = model.req_4(control, sig, gap)
    stop_time=get_time()
    delta_time_r=delta_time(start_time,stop_time)

    time_events = {}

    
    for event in lista:
        
        full_time = event['time']
        simplified_time = full_time[:16]  

        if simplified_time not in time_events:
            time_events[simplified_time] = {
                'time': simplified_time,
                'eventos': 0,
                'detalles': []
            }

        time_events[simplified_time]['eventos'] += 1

        event_details = event.copy()
        del event_details['time']
        time_events[simplified_time]['detalles'].append(event_details)

    
    r = list(time_events.values())

    return r[:15],delta_time_r


def req_5(control, depth, nst):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    memflag=True
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory =get_memory()
    
    lista = model.req_5(control, depth, nst)
    
    stop_time = get_time()
    delta_time = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory = delta_memory(stop_memory, start_memory)

    time_events = {}

    for event in lista:
        
        full_time = event['time']
        simplified_time = full_time[:16]  

        if simplified_time not in time_events:
            time_events[simplified_time] = {
                'time': simplified_time,
                'eventos': 0,
                'detalles': []
            }

        time_events[simplified_time]['eventos'] += 1

        del event['time']
        time_events[simplified_time]['detalles'].append(event)

    
    r = list(time_events.values())
    return r[:20], delta_time, delta__memory

def req_6(control, anio, latitud, longitud, radio, num_eventos):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    memflag=True
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory =get_memory()
    
    evento_prominente, numero_de_eventos, lista = model.req_6(control, anio, latitud, longitud, radio, num_eventos)
    
    stop_time = get_time()
    delta_time = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory = delta_memory(stop_memory, start_memory)

    time_events = {}

    for event in lista['elements']:
        
        full_time = event['time']
        simplified_time = full_time[:16]  

        if simplified_time not in time_events:
            time_events[simplified_time] = {
                'time': simplified_time,
                'eventos': 0,
                'detalles': []
            }

        time_events[simplified_time]['eventos'] += 1

        del event['time']
        time_events[simplified_time]['detalles'].append(event)

    
    r = list(time_events.values())
    return evento_prominente, numero_de_eventos, r, delta_time, delta__memory

def req_7(control, anio, region, p):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    
    start_time=get_time()
    lista = model.req_7(control, anio, region)
    stop_time=get_time()
    delta_time_r=delta_time(start_time,stop_time)
    if p == 1:
        for event_details in lista['elements']:
            del event_details['place']
            del event_details['updated']
            del event_details['tz']
            del event_details['felt']
            del event_details['alert']
            del event_details['status']
            del event_details['tsunami']
            del event_details['net']
            del event_details['ids']
            del event_details['sources']
            del event_details['types']
            del event_details['dmin']
            del event_details['rms']
            del event_details['mmi']
            del event_details['magType']
            del event_details['type']
            del event_details['code']
    elif p == 2:
        for event_details in lista['elements']:
            del event_details['place']
            del event_details['updated']
            del event_details['tz']
            del event_details['felt']
            del event_details['alert']
            del event_details['status']
            del event_details['tsunami']
            del event_details['net']
            del event_details['ids']
            del event_details['sources']
            del event_details['types']
            del event_details['dmin']
            del event_details['rms']
            del event_details['cdi']
            del event_details['magType']
            del event_details['type']
            del event_details['code']
    else:
        for event_details in lista['elements']:
            del event_details['place']
            del event_details['updated']
            del event_details['tz']
            del event_details['felt']
            del event_details['alert']
            del event_details['status']
            del event_details['tsunami']
            del event_details['net']
            del event_details['ids']
            del event_details['sources']
            del event_details['types']
            del event_details['dmin']
            del event_details['rms']
            del event_details['cdi']
            del event_details['magType']
            del event_details['type']
            del event_details['code']
            del event_details['mmi']

    return lista['elements'], delta_time_r


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
