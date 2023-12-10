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
from DISClib.Algorithms.Sorting import mergesort as merg
csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    controller = {
        'model': None
    }
    controller['model'] = model.new_data_structs()
    return controller


# Funciones para la carga de datos
def load_data(control, size_data):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    size_total_temblores = load_temblores(control, size_data)
    return size_total_temblores

def load_temblores(control, size_data):
    result_file = cf.data_dir + "earthquakes/temblores-utf8-" + size_data +".csv"
    input_file = csv.DictReader(open(result_file, encoding= "utf-8"))
    for temblores in input_file:
        date_str = ":".join(temblores['time'].split(":")[0:2])
        temblores['time'] = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
        if temblores['felt'] == '' or temblores['felt'] == ' ' or temblores['felt'] == None:    
            temblores['felt'] = 'Unknow'
        else:
            temblores['felt'] =  temblores['felt']
        if temblores['cdi'] == '' or  temblores['cdi'] == ' ' or temblores['cdi'] == None:
            temblores['cdi'] = 'Unknow'
        else:
            temblores['cdi'] =  temblores['cdi']
        if temblores['mmi'] == '' or temblores['mmi'] == ' ' or temblores['mmi'] == None:
            temblores['mmi'] = "Unknown"
        else:
            temblores['mmi'] = float(temblores['mmi'])
        if temblores['alert'] == '' or ' ' or None:
            temblores['alert'] = "Unknown"
        if temblores['status'] == '' or ' ' or None:
            temblores['status'] = "Unknown"
        if temblores['tsunami'] == '' or temblores['tsunami'] == ' ' or temblores['tsunami'] == None or temblores['tsunami'] == '0':
            temblores['tsunami'] = False
        else:
            temblores['tsunami'] = True
        if temblores['gap'] == '' or temblores['gap'] == ' ' or temblores['gap'] == None:    
            temblores['gap'] = 0
        else:
            temblores['gap'] =  temblores['gap']
        if temblores['dmin'] == '' or temblores['dmin'] == ' ' or temblores['dmin'] == None:
            temblores['dmin'] = 'Unknow'
        else:
            temblores['dmin'] =  temblores['dmin']
        if temblores['rms'] == '' or temblores['rms'] == ' ' or temblores['rms'] == None:
            temblores['rms'] = 'Unknow'
        else:
            temblores['rms'] =  temblores['rms']
        if temblores['magType'] == '' or temblores['magType'] == ' ' or temblores['magType'] == None:
            temblores['magType'] = 'Unknow'
        else:
            temblores['magType'] =  temblores['magType']
        if temblores['type'] == '' or temblores['type'] == ' ' or temblores['type'] == None:
            temblores['type'] = 'Unknow'
        else:
            temblores['type'] =  temblores['type']
        if temblores['title'] == '' or temblores['title'] == ' ' or temblores['title'] == None:
            temblores['title'] = 'Unknow'
        else:
            temblores['title'] =  temblores['title']
        if temblores['place'] == '' or temblores['place'] == ' ' or temblores['place'] == None:
            temblores['place'] = 'Unknow'
        else:
            temblores['place'] =  temblores['place']
        if temblores['ids'] == '' or temblores['ids'] == ' ' or temblores['ids'] == None:
            temblores['ids'] = 'Unknow'
        else:
            temblores['ids'] =  temblores['ids']
        if temblores['mag'] == '' or temblores['mag'] == ' ' or temblores['mag'] == None:
            temblores['mag'] = 'Unknow'
        else:
            temblores['mag'] =  float(temblores['mag'])
        if temblores['place'] == '' or temblores['place'] == ' ' or temblores['place'] == None:
            temblores['place'] = 'Unknow'
        else:
            temblores['place'] =  temblores['place']
        if temblores['type'] == '' or temblores['type'] == ' ' or temblores['type'] == None:
            temblores['type'] = 'Unknow'
        else:
            temblores['type'] =  temblores['type']
        if temblores['nst'] == '' or temblores['nst'] == ' ' or temblores['nst'] == None:
            temblores['nst'] = 1
        else:
            temblores['nst'] =  temblores['nst']
        model.add_temblor(control['model'], temblores)
        model.updateDate(control["model"]["anio"], temblores)
        model.updateMag(control["model"]["magnitud"], temblores)
        model.updateDate_fecha(control["model"]["fecha"], temblores)
        model.updatedepth(control["model"]["depth"], temblores)
        model.updateSig(control["model"]["sig"], temblores)
    return model.size_data(control['model'])
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


def req_1(control, date1, date2):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    start_time = get_time()
    date1 = datetime.datetime.strptime(date1, "%Y-%m-%dT%H:%M")
    date2 = datetime.datetime.strptime(date2, "%Y-%m-%dT%H:%M")
    tamaño, lista = model.req_1(control['model'], date1, date2)
    stop_time = get_time()
    delta =delta_time(start_time, stop_time)
    return tamaño, lista, delta

def req_2(control, limite_inf, limite_sup):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    start_time = get_time()
    size, keys, lista_r, llave = model.req_2(control['model'], limite_inf, limite_sup)
    stop_time = get_time()
    delta = delta_time(start_time, stop_time)
    return size, keys, lista_r, delta, llave

def req_3(control, mag, profundidad):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start_time = get_time()
    mag = float(mag)
    profundidad =float(profundidad)
    lista, numero_total = model.req_3(control['model'],mag,profundidad)
    stop_time = get_time()
    delta =delta_time(start_time, stop_time)

    return lista, numero_total, delta

def req_4(control, sigMin, gapMax):
    """
    Retorna el resultado del requerimiento 4
    """
    return model.req_4(control['model'], float(sigMin), float(gapMax))

def req_5(control, prof_min, est_min):
    """
    Retorna el resultado del requerimiento 5
    """
    start_time = get_time()
    size, eventos, lista = model.req_5(control['model'], prof_min, est_min)
    stop = get_time()
    delta = delta_time(start_time, stop)
    return size, eventos, lista, delta
    

def req_6(control, anio, lat, long, radio, n):
    """
    Retorna el resultado del requerimiento 6
    """
    start_time = get_time()
    numero_eventos, maximo_eventos, numero_fechas, eventos_entre_fechas, lista_max, lista_eventos =  model.req_6(control['model'], int(anio), float(lat), float(long), float(radio), int(n))
    stop = get_time()
    delta = delta_time(start_time, stop)
    return numero_eventos, maximo_eventos, numero_fechas, eventos_entre_fechas, lista_max, lista_eventos, delta 

def req_7(control, anio, title, propiedad, div):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    delta = model.req_7(control['model'], anio, title, propiedad, div)
    return delta

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