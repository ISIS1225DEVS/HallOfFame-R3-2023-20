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

csv.field_size_limit(2147483647)
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    analyzer = model.new_data_structs()
    return analyzer


# Funciones para la carga de datos

def load_data(control, filename):
    """
    Carga los datos del reto
    """
    filename = cf.data_dir + filename
    input_file = csv.DictReader(open(filename, encoding="utf-8"),
                                delimiter=",")
    for earthquake in input_file:
        model.addEarthquake(control, earthquake)
    return control


# Funciones de ordenamiento

def sort_req5(control):
    """
    Ordena los datos del modelo
    """
    size=model.lt.size(control)
    srt=model.sort_req5(control,size)
    return srt


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(analyzer,fecha_ini,fecha_fin):
    """
    Retorna el resultado del requerimiento 1
    """
    start_time = get_time()
    resultado, sismos = model.req_1(analyzer, fecha_ini,fecha_fin)
    end_time = get_time()
    delta = delta_time(start_time,end_time)
    return resultado, sismos ,delta


def req_2(map,magI,magF):
    """
    Retorna el resultado del requerimiento 2
    """
    TI=get_time()
    restult=model.req_2(map,magI,magF)
    TF=get_time()
    delta= delta_time(TI,TF)
    return restult,delta



def req_3(analyzer,mag,depth):
    """
    Retorna el resultado del requerimiento 3
    """
    start_time = get_time()
    resultado, sismos = model.req_3(analyzer, mag, depth)
    end_time = get_time()
    delta = delta_time(start_time,end_time)
    return resultado, sismos ,delta


def req_4(control, minsig, maxgap):
    """
    Retorna el resultado del requerimiento 4
    """
    TI=get_time()
    resultado, cantidad_de_sismos = model.req_4(control,minsig,maxgap)
    TF=get_time()
    delta=delta_time(TI,TF)
    return resultado, cantidad_de_sismos, delta
    # TODO: Modificar el requerimiento 4
    pass


def req_5(control,mindepth,minnst):
    """
    Retorna el resultado del requerimiento 5
    """
    TI=get_time()
    result,t,v= model.req_5(control,mindepth,minnst)
    TF=get_time()
    result=model.lt.subList(result,1,20)
    delta=delta_time(TI,TF)
    return result,t,v,delta

def req_6(lista,anio,latitud,longitud,radio,N):
    """
    Retorna el resultado del requerimiento 6
    """
    TI=get_time()
    result= model.req_6(lista,anio,latitud,longitud,radio,N)
    TF=get_time()
    delta=delta_time(TI,TF)
    return result,delta


def req_7(analyzer, anio, title, prop):
    """
    Retorna el resultado del requerimiento 7
    """
    start_time = get_time()
    tabla, histo = model.req_7(analyzer, anio, title, prop)
    end_time = get_time()
    delta = delta_time(start_time,end_time)
    return tabla, histo, delta


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
