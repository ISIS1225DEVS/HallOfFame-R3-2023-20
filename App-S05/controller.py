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
 
from DISClib.ADT import orderedmap as om
import config as cf
import model
import time
import csv
import tracemalloc
from DISClib.ADT import list as lt
from tabulate import tabulate

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    control = {
        "model": None
    }
    control["model"] = model.new_data_structs()
    return control


# Funciones para la carga de datos

def load_data(control, size):
    """
    Carga los datos del reto
    """
    loadTemblores(control, size)

def loadTemblores(control, size):
    texto = "earthquakes/temblores-utf8-" +str(size)+".csv"
    tembloresfile = cf.data_dir + texto
    input_file = csv.DictReader(open(tembloresfile, encoding='utf-8'))
    for temblor in input_file:
        model.add_Temblores(control["model"], temblor)
        model.add_TembloresMagnitudes(control["model"], temblor)
        model.add_TembloresSignificancia(control["model"], temblor)
        model.add_temblor(control['model'], temblor)
        date = temblor['time']
        model.add_MapYears(control['model'], temblor, date[:4])
# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    model.sort(control["model"])


# Funciones de consulta sobre el catálogo

def get_firts_and_last_5(control):
    datos = model.get_firts_and_last_5(control)
    return datos
    
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
    start_time = get_time()
    results = model.req_1(control['model'], fecha_inicial, fecha_final)
    end_time = get_time() 
    delta_t = delta_time(start_time, end_time)
    total_temblores = lt.size(results)
    if total_temblores > 7:
        respuesta_lista = lt.newList("ARRAY_LIST")
        for i in range(1,4):
            lt.addLast(respuesta_lista, lt.getElement(results, total_temblores-i+1))
        for i in range(1,4):
            lt.addLast(respuesta_lista, lt.getElement(results, 4-i))
    i = 0
    lista_final = []
    headers=["mag","lat","long","depth","sig","gap","nst","title","cdi","mmi","magType", "type", "code"]
    for dict in lt.iterator(respuesta_lista):
        if len(dict) == 6:
            dict = dict['elements'][0]
        valores = list(dict.values())
        fecha = valores[0]
        valores.pop(0)
        lista_final.append([fecha, '1', tabulate([valores], headers=headers, tablefmt='grid', numalign="center")])
    return lista_final, total_temblores, delta_t
    
def get_datos(datos, pos):
    valores_lista = [valor for valor in lt.getElement(datos,pos).values()]
    for i, valor in enumerate(valores_lista):
        if valor == "":
            valores_lista[i] = 'Unknown'
    return valores_lista

def req_2(control, min_mag, max_mag):
    """
    Retorna el resultado del requerimiento 2
    """
    start_time = get_time()
    results = model.req_2(control['model'], min_mag, max_mag)
    end_time = get_time() 
    delta_t = delta_time(start_time, end_time)
    sub_lista = []
    for lista in lt.iterator(results[1]):
        temporal = []
        if lt.size(lista) > 6:
            primeros = lt.subList(lista, 1, 3)
            ultimos = lt.subList(lista, lt.size(lista)-2, 3)
            for i in range(1,4):
                temporal.append(list(lt.getElement(primeros, i).values()))
            for i in range(1,4):
                temporal.append(list(lt.getElement(ultimos, i).values()))
        else:
            for i in range(1,lt.size(lista)+1):
                temporal.append(list(lt.getElement(lista, i).values()))
        sub_lista.append(temporal)
    lista_grande = []
    headers=["time","mag","lat","long","depth","sig","gap","nst","title","cdi","mmi","magType", "type", "code"]
    i = 0
    for dict in lt.iterator(results[0]):
        dict[2] = tabulate(sub_lista[i], headers=headers, tablefmt='grid', numalign="center")
        lista_grande.append(dict)
        i += 1
    return lista_grande, delta_t, results[2], results[3]


def req_3(control, mag_min, prof_max):
    """
    Retorna el resultado del requerimiento 3
    """
    start_time = get_time()
    results = model.req_3(control['model'], mag_min, prof_max)
    end_time = get_time() 
    delta_t = delta_time(start_time, end_time)
    tamaño = lt.size(results)
    results = lt.subList(results, tamaño-9, 10)
    primeros = lt.subList(results,1, 3)
    ultimos = lt.subList(results, 8, 3)
    respuesta_lista = lt.newList("ARRAY_LIST")
    for i in range(1,4):
        lt.addLast(respuesta_lista, lt.getElement(ultimos, 4-i))
    for i in range(1,4):
        lt.addLast(respuesta_lista, lt.getElement(primeros, 4-i))
    lista_grande = []
    headers=["mag","lat","long","depth","sig","gap","nst","title","cdi","mmi","magType", "type", "code"]
    for dict in lt.iterator(respuesta_lista):
        valores = list(dict.values())
        fecha = valores[0]
        valores.pop(0)
        lista_grande.append([fecha, '1', tabulate([valores], headers=headers, tablefmt='grid', numalign="center")])
    return lista_grande, tamaño, delta_t

def req_4(control,significancia,azimutal_maxima):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    resultados = model.req_4(control["model"],significancia,azimutal_maxima)
    return tabulate(resultados[0]["elements"], "keys", tablefmt="grid") , resultados[1]


def req_5(control, depthMin, nstMin):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    startime = get_time()
    tabla, eventos = model.req_5(control['model'], depthMin, nstMin)
    endtime = get_time()
    time = delta_time(startime, endtime)
    
    return tabla, eventos,time

def req_6(control, year, latRef, longRef, radio, n):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    startime = get_time()
    tablaMaxArea, TablaTop, totalEventsArea, totalSubList, maxArea= model.req_6(control['model'], year, latRef, longRef, radio, n )
    endtime = get_time()
    time = delta_time(startime, endtime)
    
    return tablaMaxArea, TablaTop, totalEventsArea, totalSubList, maxArea, time


def req_7(control, año, title, prop, bins):
    """
    Retorna el resultado del requerimiento 7
    """
    start_time = get_time()
    results = model.req_7(control['model'], año, title, prop, bins)
    end_time = get_time()
    delta_t = delta_time(start_time, end_time)

    return results,delta_t

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
