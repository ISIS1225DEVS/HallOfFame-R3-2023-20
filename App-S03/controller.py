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


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = model.newDataStructs()
    return control


# Funciones para la carga de datos

def load_data(control, filename):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    pass

def loadData(control,numero):
    return loadSeismicEvents(control,numero)

def loadSeismicEvents(control,numero):
    if numero == 1: 
         seismicEventsFile = cf.data_dir + 'temblores-utf8-small.csv'
    elif numero == 2: 
        seismicEventsFile = cf.data_dir + 'temblores-utf8-5pct.csv'
    elif numero == 3: 
        seismicEventsFile = cf.data_dir + 'temblores-utf8-10pct.csv'
    elif numero == 4:
        seismicEventsFile = cf.data_dir + 'temblores-utf8-20pct.csv'
    elif numero == 5: 
        seismicEventsFile = cf.data_dir + 'temblores-utf8-30pct.csv'
    elif numero == 6: 
        seismicEventsFile = cf.data_dir + 'temblores-utf8-50pct.csv'
    elif numero == 7: 
        seismicEventsFile = cf.data_dir + 'temblores-utf8-80pct.csv'
    elif numero == 8: 
        seismicEventsFile = cf.data_dir + 'temblores-utf8-large.csv'
    inputFile = csv.DictReader(open(seismicEventsFile , encoding='utf-8'))
    for seismicEvent in inputFile:
        model.addSeismicEvent(control, seismicEvent)
    return model.dataSize(control)

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

def getFirstAndLastN(data, n):
    filtered = model.getFirstAndLastN(data, int(n))
    return filtered

def req_1(control, date1, date2):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    tracemalloc.start()
    start_memory = get_memory()
    filtered, metaData = model.req_1(control, date1, date2)
    stop_memory = get_memory()
    tracemalloc.stop()
    deltaMemory = delta_memory(stop_memory, start_memory)
    return filtered, metaData, deltaMemory


def req_2(control, inferiorMagLimit, superiorMagLimit):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    tracemalloc.start()
    start_memory = get_memory()
    filtered, metaData = model.req_2(control, float(inferiorMagLimit), float(superiorMagLimit))
    stop_memory = get_memory()
    tracemalloc.stop()
    deltaMemory = delta_memory(stop_memory, start_memory)
    return filtered, metaData, deltaMemory


def req_3(control, minMag, maxDepth):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    tracemalloc.start()
    start_memory = get_memory()
    filtered, metaData = model.req_3(control, float(minMag), float(maxDepth))
    stop_memory = get_memory()
    tracemalloc.stop()
    deltaMemory = delta_memory(stop_memory, start_memory)
    return filtered, metaData, deltaMemory


def req_4(control, minSig, maxGap):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    tracemalloc.start()
    start_memory = get_memory()
    filtered, metaData = model.req_4(control, float(minSig), float(maxGap))
    stop_memory = get_memory()
    tracemalloc.stop()
    deltaMemory = delta_memory(stop_memory, start_memory)
    return filtered, metaData, deltaMemory


def req_5(control, minDepth, minNst):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    tracemalloc.start()
    start_memory = get_memory()
    filtered, metaData = model.req_5(control, float(minDepth), float(minNst))
    stop_memory = get_memory()
    tracemalloc.stop()
    deltaMemory = delta_memory(stop_memory, start_memory)
    return filtered, metaData, deltaMemory

def req_6(control, date, lat, lon, r, n):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    tracemalloc.start()
    start_memory = get_memory()
    filtered, metaData = model.req_6(control, str(date), float(lat), float(lon), float(r), int(n))
    stop_memory = get_memory()
    tracemalloc.stop()
    deltaMemory = delta_memory(stop_memory, start_memory)
    return filtered, metaData, deltaMemory


def req_7(control, year, place, feature, N):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    tracemalloc.start()
    start_memory = get_memory()
    filtered, histogram, metaData = model.req_7(control, year, place.title(), feature.lower(), int(N))
    stop_memory = get_memory()
    tracemalloc.stop()
    deltaMemory = delta_memory(stop_memory, start_memory)
    return filtered, histogram, metaData, deltaMemory


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
