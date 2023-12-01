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
import datetime
import model
import time
import csv
import tracemalloc
from DISClib.ADT import list as lt
csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    controller = model.new_data_structs()
    return controller


# Funciones para la carga de datos

def load_data(control, filename):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    start_time = get_time() 
    filename = file_name(filename)
    filename = cf.data_dir + filename
    input_file = csv.DictReader(open(filename, encoding="utf-8"),
                                delimiter=",")
    for temblor in input_file:
        temblor = clear_data(temblor)
        lt.addLast(control['temblores'],temblor)
    model.sort(control)
    for temblor in lt.iterator(control['temblores']):
        model.add_data(control, temblor)
    model.updateHeap(control)
    #model.sortbygap(control['sigIndex'])
    stop_time = get_time() 
    d_time = delta_time(start_time, stop_time) 
    return control, d_time

def file_name(filename):
    """
    Esta función se encarga de elegir el nombre correcto del archivo
    a cargar dependiendo de la opción elegida por el usuario
    """
    r = None
    if filename == '1':
        r = 'temblores-utf8-small.csv'
    elif filename == '2':
        r = 'temblores-utf8-5pct.csv'
    elif filename == '3':
        r = 'temblores-utf8-10pct.csv'
    elif filename == '4':
        r = 'temblores-utf8-20pct.csv'
    elif filename == '5':
        r = 'temblores-utf8-30pct.csv'
    elif filename == '6':
        r = 'temblores-utf8-50pct.csv'
    elif filename == '7':
        r = 'temblores-utf8-80pct.csv'
    elif filename == '8':
        r = 'temblores-utf8-large.csv'
    return r

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


def req_1(control, initialDate, finalDate):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    start_time = get_time() 
    initialDate = datetime.datetime.strptime(initialDate, "%Y-%m-%dT%H:%M")
    finalDate = datetime.datetime.strptime(finalDate, "%Y-%m-%dT%H:%M")
    lst, size = model.req_1(control, initialDate, finalDate)
    stop_time = get_time() 
    d_time = delta_time(start_time, stop_time) 
    return lst, size, d_time


def req_2(control, magMin, magMax):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    start_time = get_time() 
    magMin = round(magMin,3)
    magMax = round(magMax,3)
    lst, size = model.req_2(control, magMin, magMax)
    stop_time = get_time() 
    d_time = delta_time(start_time, stop_time) 
    return lst, d_time, size



def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass
def req_3(control, magMin, depthMax):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start_time = get_time()
    float(depthMax)
    float(magMin)
    resultado = model.req_3(control, magMin, depthMax)
    stop_time = get_time() 
    d_time = delta_time(start_time, stop_time) 
    return resultado


def req_4(control, sig, gap):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    start_time = get_time() 
    lst_15, size = model.req_4(control, sig, gap)
    if lt.size(lst_15) <= 6:
        lst_print = lst_15
    else:
        lst_15_size=lt.size(lst_15)
        lst_print = lt.newList()
        # Seleccionar 3 primeros
        for i in range(1,4):
            elemento = lt.getElement(lst_15,i)
            copy = elemento.copy()
            del copy['felt']
            del copy['tsunami']
            lt.addLast(lst_print,copy)
        #Seleccionar 3 últimos
        for i in range(2,-1,-1):
            elemento = lt.getElement(lst_15,lst_15_size-i)
            copy = elemento.copy()
            del copy['felt']
            del copy['tsunami']
            lt.addLast(lst_print,copy)
    stop_time = get_time() 
    d_time = delta_time(start_time, stop_time) 
    return lst_print, size, d_time


def req_5(control, depth, nst):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    start_time = get_time() 
    depth = round(float(depth),3)
    nst = int(float(nst))
    respuesta, size = model.req_5(control, depth, nst)
    stop_time = get_time() 
    d_time = delta_time(start_time, stop_time) 
    return respuesta, size, d_time

def req_6(control, year, lat, long, radio, n):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    year = datetime.datetime.strptime(year,"%Y").year
    lat = float(lat)
    long = float(long)
    radio = int(radio)
    n = int(n)
    start = get_time()
    r = model.req_6(control, year, lat,long,radio,n)
    end=get_time()
    t = end -start
    return r, t


def req_7(control, year, area, prop, bins):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    start_time = get_time() 
    num_eq_year, num_eq_year_title, h_bins, h_values, min_val, max_val, lt_hist_data, t = model.req_7(control, year, area, prop, bins)
    stop_time = get_time() 
    d_time = delta_time(start_time, stop_time) 
    return num_eq_year, num_eq_year_title, h_bins, h_values, min_val, max_val, lt_hist_data , d_time


def req_8(control, req,parametros):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    p = lt.newList('ARRAY_LIST')
    if req == 1:
        p1 = datetime.datetime.strptime(lt.getElement(parametros,1), "%Y-%m-%dT%H:%M")
        p2 = datetime.datetime.strptime(lt.getElement(parametros,2), "%Y-%m-%dT%H:%M")
        lt.addLast(p,p1)
        lt.addLast(p,p2)
    
    elif req == 2:
        p1 = float(lt.getElement(parametros,1))
        p2 = float(lt.getElement(parametros,2))
        lt.addLast(p,p1)
        lt.addLast(p,p2)
        
    elif req == 4:
        p1 = float(lt.getElement(parametros,1))
        p2 = float(lt.getElement(parametros,2))
        lt.addLast(p,p1)
        lt.addLast(p,p2)
        
    elif req == 5:
        p1 = round(float(lt.getElement(parametros,1)),3)
        p2 = int(lt.getElement(parametros,2))
        lt.addLast(p,p1)
        lt.addLast(p,p2)
    
    elif req == 6:
        p1 = datetime.datetime.strptime(lt.getElement(parametros,1),"%Y").year
        p2 = float(lt.getElement(parametros,2))
        p3 = float(lt.getElement(parametros,3))
        p4 = int(lt.getElement(parametros,4))
        p5 = int(lt.getElement(parametros,5))
        lt.addLast(p,p1)
        lt.addLast(p,p2)
        lt.addLast(p,p3)
        lt.addLast(p,p4)
        lt.addLast(p,p5)
        
    elif req == 7:
        p1 = int(lt.getElement(parametros,1))
        lt.addLast(p, p1)
        lt.addLast(p, lt.getElement(parametros,2))
    start = get_time()
    r=model.req_8(control, req, p)
    end = get_time()
    d_time = delta_time(start, end)
    return r, d_time
        


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


#Función para limpiar datos

def clear_data(data):
    """
    Recibe como parámetro el registro del sismo y retorna el mismo registro 
    con la información relevante en el formato deseado.
    """
    # Propiedades relevantes para el análisis
    imp_prop = ('depth', 'mag', 'cdi', 'mmi', 'lat', 'long', 'gap', 
                'nst', 'felt', 'sig', 
                'title', 'magType', 'type', 'code',
                'time', 'tsunami')
    # Diccionario vacío para guardar el registro limpio
    new_data={}
    for prop in imp_prop:
        # Si no hay información
        if (not prop in data) or data[prop] in (None, "", " "):
            # Float
            if prop in ('depth', 'mag', 'cdi', 'mmi'):
                new_data[prop] = 1.0
            elif prop in ('lat', 'long'):
                new_data[prop] = 0.0
            elif prop == 'gap':
                new_data[prop] = 0.0
            # Int
            elif prop in ('nst', 'felt'):
                new_data[prop] = 1
            elif prop == 'sig':
                new_data[prop] = 0
            # Str
            elif prop in ('title', 'magType', 'type', 'code'):
                new_data[prop] = 'unknown'
            # Datetime
            elif prop == 'time':
                new_data[prop] = datetime.datetime(year=1997, month=1, day=1, hour=0, minute=0)
            # Bool
            elif prop == 'tsunami':
                new_data[prop] = False
        # Si hay información
        else:
            # Float
            if prop in ('depth', 'mag', 'cdi', 'mmi', 'lat', 'long', 'gap'):
                new_data[prop] = round(float(data[prop]),3)
            # Int
            elif prop in ('nst', 'felt', 'sig'):
                new_data[prop] = int(float(data[prop]))
            # Str    
            elif prop in ('title', 'magType', 'type', 'code'):
                new_data[prop] = data[prop].lower()
            # Datetime
            elif prop == 'time':
                date_f = data[prop]
                new_data[prop] = datetime.datetime.strptime(date_f[0:16], "%Y-%m-%dT%H:%M")
            # Bool
            elif prop == 'tsunami':
                new_data[prop] = False
                if data[prop] in ('True', 'true', True, 'TRUE', 1):
                    new_data[prop] = True
    return new_data