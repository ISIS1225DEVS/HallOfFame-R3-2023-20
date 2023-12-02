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
from DISClib.ADT import list as lt

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
csv.field_size_limit(2147483647)

def new_controller():
    """
    Crea una instancia del modelo
    """
    data_structs = {"model" : None }
    data_structs ["model"] = model.new_data_structs()
    return data_structs

# Funciones para la carga de datos

def load_data(control,archivo):
    """
    Carga los datos del reto
    """
    data_structs = control["model"]
    ini=get_time()
    temblores = model.loadData(data_structs,archivo)
    fin=get_time()
    print(delta_time(ini,fin))
    return temblores
 # Funciones auxiliares

def creartabla(lista):
    tipo_lista=lista["type"]
    if tipo_lista == "ARRAY_LIST":
        primer_valor=lista["elements"][0]
    else:
        primer_valor=lista["first"]["info"]
    tabla=model.creartabla(lista,primer_valor)
    return tabla

def resumir_lista(lista,n,orden):
    lista_resumida=model.resumir_lista(lista,n,orden)
    return lista_resumida




# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    data_structs = control["model"]
    resp=model.sort(data_structs)
    return resp


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control,inicialdate,finaldate):
    """
    Retorna el resultado del requerimiento 1
    """
    data_structs = control["model"]
    ini=get_time()
    sismos=model.req_1(data_structs,inicialdate,finaldate)
    fin=get_time()
    print(delta_time(ini,fin))
    lista_final,total_sismos,total_fechas=sismos
    tamaño = lt.size(lista_final)
    if tamaño > 6:
        lista_resumida = model.resumir_lista(lista_final,3,0)
    else:
        lista_resumida = lista_final

    return lista_resumida,total_sismos,total_fechas


def req_2(control, mag_inf, mag_sup):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    data_structs = control["model"]
    ini=get_time()
    sismos=model.req_2(data_structs,mag_inf,mag_sup)
    fin=get_time()
    print(delta_time(ini,fin))
    lista_final,total_sismos,total_llaves,elementos=sismos
    tamaño = lt.size(lista_final)
    if tamaño > 6:
        lista_resumida = model.resumir_lista(lista_final,3,0)
    else:
        lista_resumida = lista_final

    return lista_resumida,total_sismos,total_llaves,elementos,tamaño


def req_3(control, mag_min, depth_max):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    data_structs = control["model"]
    ini=get_time()
    sismos=model.req_3(data_structs,mag_min,depth_max)
    fin=get_time()
    print(delta_time(ini,fin))
    fechas_diferentes,total_eventos,lista_final=sismos
    tamaño = lt.size(lista_final)
    if tamaño > 6:
        lista_resumida = model.resumir_lista(lista_final,3,0)
    else:
        lista_resumida =lista_final 

    return fechas_diferentes,total_eventos,lista_resumida


def req_4(control,sig_min,dis_max):
    """
    Retorna el resultado del requerimiento 4
    """
    data_structs = control["model"]
    ini=get_time()
    sismos=model.req_4(data_structs,sig_min,dis_max)
    fin=get_time()
    print(delta_time(ini,fin))
    sublista,total_eventos,total_fechas=sismos
    tamaño = lt.size(sublista)
    if tamaño > 6:
        lista_resumida = model.resumir_lista(sublista,3,0)
    else:
        lista_resumida =sublista 

    return lista_resumida,total_eventos,total_fechas


def req_5(control,depth_min,nst_min):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    data_structs = control["model"]
    ini=get_time()
    sismos=model.req_5(data_structs, depth_min, nst_min)
    fin=get_time()
    print(delta_time(ini,fin))
    fechas_diferentes,total_eventos,lista_final=sismos
    tamaño = lt.size(lista_final)
    if tamaño > 6:
        lista_resumida = model.resumir_lista(lista_final,3,0)
    else:
        lista_resumida = lista_final

    return fechas_diferentes,total_eventos,lista_resumida

def req_6(control,anio, latitud, longitud, radio, n):
    """
    Retorna el resultado del requerimiento 6
    """
    data_structs = control["model"]
    ini=get_time()
    sismos=model.req_6(data_structs,anio, latitud, longitud, radio, n)
    fin=get_time()
    print(delta_time(ini,fin))
    total_eventos_en_area,evento_mas_sig, pre_events,pos_events,lista_final,codigo,cant_eventos,dif_fechas=sismos
    tamaño = lt.size(lista_final)
    if tamaño > 6:
        lista_resumida = model.resumir_lista(lista_final,3,1)
    else:
        lista_resumida = lista_final

    return total_eventos_en_area,evento_mas_sig, pre_events,pos_events,lista_resumida,codigo,cant_eventos,dif_fechas

def req_7(control,anio,title,propiedad,casillas):
    """
    Retorna el resultado del requerimiento 7
    """
    data_structs = control["model"]
    ini=get_time()
    sismos=model.req_7(data_structs,anio,title,propiedad,casillas)
    fin=get_time()
    print(delta_time(ini,fin))
    total_sis_anio,total_sis_his,prop_min,prop_max,lista_final_fechas,lista_val_hist,intervalos,marcas,nombres,conteos=sismos
    tamaño = lt.size(lista_final_fechas)
    if tamaño > 6:
        lista_resumida = model.resumir_lista(lista_final_fechas,3,1)
    else:
        lista_resumida =lista_final_fechas
    primer_valor=lista_resumida["elements"][0]
    titulos = list(primer_valor.keys())
    valores = [list(fila.values()) for fila in lt.iterator(lista_resumida)]

    

    return total_sis_anio,total_sis_his,prop_min,prop_max,titulos,valores,lista_val_hist,intervalos,marcas,nombres,conteos
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