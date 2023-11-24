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
csv.field_size_limit(2147483647)
import tracemalloc
import datetime




"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    control = {"model": None}
    control["model"] = model.new_historial_sismico()
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    return control


# Funciones para la carga de datos

def load_data(control, tamanio, memory):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    time_i = get_time()
    if memory:
        tracemalloc.start()
        memory_i = get_memory()
    sismos_file = cf.data_dir + "earthquakes/temblores-utf8-" + str(tamanio) + ".csv"
    input_file = csv.DictReader(open(sismos_file, encoding="utf8"))
    for temblor in input_file:
        model.add_temblor(control["model"], temblor)
  
    time_f = get_time()
    time = delta_time(time_i,time_f)
    if memory:
        memory_f = get_memory()
        tracemalloc.stop()
        memory = delta_memory(memory_f, memory_i)


    return control["model"]["sismos"], time, memory




        



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


def req_1(control, initialDate ,finalDate):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    initialDate = datetime.datetime.strptime(initialDate, "%Y-%m-%dT%H:%M")
    finalDate = datetime.datetime.strptime(finalDate, "%Y-%m-%dT%H:%M")
    tiempo_i = get_time()
    total_sismos ,total_fechas, Eventos_ocurridos = model.req_1(control["model"], initialDate, finalDate)
    tiempo_f = get_time()
    d_tiempo = delta_time(tiempo_i,tiempo_f)

    return total_sismos ,total_fechas, Eventos_ocurridos, d_tiempo
    


def req_2(control, limit_inferior , limit_superior):
    """
    Retorna el resultado del requerimiento 2

    """
    tiempo_i = get_time()
    total_sismos,total_magnitudes, Eventos_ocurridos = model.req_2(control["model"],limit_inferior , limit_superior)
    tiempo_f = get_time()
    d_tiempo = delta_time(tiempo_i,tiempo_f)
    return total_sismos,total_magnitudes, Eventos_ocurridos, d_tiempo

def req_3(control, mag_min , depth_max):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    tiempo_i = get_time()
    total_sismos ,total_fechas, eventos_ocurridos = model.req_3(control["model"], mag_min  , depth_max)
    tiempo_f = get_time()
    d_tiempo = delta_time(tiempo_i,tiempo_f)
    return total_sismos,total_fechas,  eventos_ocurridos, d_tiempo

def req_4(control, sig, gap):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    tiempo_i = get_time()
    total_fechas, eventos_totales, eventos = model.req_4(control["model"], sig, gap)
    tiempo_f = get_time()
    d_tiempo = delta_time(tiempo_i,tiempo_f)
    return total_fechas, eventos_totales, eventos, d_tiempo


def req_5(control, profundidad, estaciones):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    tiempo_i = get_time()
    total_eventos,total_fechas,v_eventos = model.req_5(control["model"], profundidad, estaciones)
    tiempo_f = get_time()
    d_tiempo = delta_time(tiempo_i,tiempo_f)
    return total_eventos, total_fechas,v_eventos, d_tiempo



def req_6(control, anio,lat,long,radio,n):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    tiempo_i = get_time()
    t_fecha, e_significativo, t_eventos_radio, n_eventos, te_año, codigo_sig, eventos_despues, eventos_antes = model.req_6(control["model"],anio,lat,long,radio,n)
    tiempo_f = get_time()
    d_tiempo = delta_time(tiempo_i,tiempo_f)
    return t_fecha, e_significativo, t_eventos_radio, n_eventos, te_año, codigo_sig, eventos_despues, eventos_antes, d_tiempo


def req_7(control, anio, region, propiedad, bins ):
    """
    Retorna el resultado del requerimiento 7
    """
    tiempo_i = get_time()
    total, fig = model.req_7(control["model"], anio, region, propiedad, bins)
    tiempo_f = get_time()
    d_time = delta_time(tiempo_i, tiempo_f)
    # TODO: Modificar el requerimiento 7
    return total, fig, d_time
    


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
