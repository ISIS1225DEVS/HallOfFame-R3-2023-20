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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf
from datetime import datetime as dt
from tabulate import tabulate
import math as m
#import matplotlib as ml


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    # Inicializar las estructuras de datos
    data_structs = {'temblores': None,
                    'req1y6': None,
                    'req2': None, 
                    'req3': None,   
                    'req4': None,
                    'req5': None,
                    'req7': None}
    
    data_structs['temblores'] = lt.newList('ARRAY_LIST')
    data_structs['req1y6'] = om.newMap(cmpfunction=compare_req1_dates)
    data_structs['req2'] = om.newMap(cmpfunction=compare_req2y3_magnitudes)
    data_structs['req3'] = om.newMap(cmpfunction=compare_req2y3_magnitudes)

    #data_structs['req4'] = lt.newList('ARRAY_LIST')
    data_structs['req5'] = om.newMap(cmpfunction=req5_compare_stations)
    data_structs['req7'] = mp.newMap(80, maptype='PROBING')

    data_structs['req4'] = req4_data
    #data_structs['req5'] = lt.newList('ARRAY_LIST')
    data_structs['req6'] = om.newMap(cmpfunction=compare_req1_dates)
    data_structs['req7'] = mp.newMap(80, maptype='PROBING')

    
    return data_structs


# Funciones para agregar informacion al modelo

def add_data(data_structs, data, choice):
    """
    Función para agregar nuevos elementos a la lista
    """
    columns = ['code','time','lat','long','mag','title','depth','felt','cdi','mmi','tsunami','magType','Type']
    elem = {}

    elem['code'] = data['code']
    
    elem['time'] = get_date_string(data['time'])
    
    elem['lat'] = round(float(data['lat']), 3)
    elem['long'] = round(float(data['long']), 3)
    elem['mag'] = round(float(data['mag']), 3)
    elem['title'] = data['title']
    elem['depth'] = round(float(data['depth']), 3)
    
    if data['felt'] != '':
        elem['felt'] = round(float(data['felt']), 3)
    else:
        elem['felt'] = 'Unknown'
        
    if data['cdi'] != '':
        elem['cdi'] = round(float(data['cdi']), 3)
    else:
        elem['cdi'] = 'Unknown'
        
    if data['mmi'] != '':
        elem['mmi'] = round(float(data['mmi']), 3)
    else:
        elem['mmi'] = 'Unknown'
        
    if str(data['tsunami']) != '0':
        elem['tsunami'] = True
    else:
        elem['tsunami'] = False
        

    elem['magType'] = data['magType']
    elem['type'] = data['type']

        
    lt.addLast(data_structs['temblores'], elem)
    
    req_data_structs(data_structs, data, choice)
                       
    return data_structs

    
    
    
def req_data_structs(data_structs, data, choice):
    """
    Crea una nueva estructura para modelar los datos
    """
    # Cambiar dependiendo de la carga
    if choice == 1 or choice == 6 or choice == 0:
        req1y6_data(data_structs, data)
    if choice == 2 or choice == 0:
        req2_data(data_structs, data)
    if choice == 3 or choice == 0:
        req3_data(data_structs, data)
    if choice == 5 or choice == 0:
        req5_data(data_structs, data)
    if choice == 7 or choice == 0:
        req7_data(data_structs, data)
'''
def req1_data(data_structs, data):
    dates_om = data_structs['req1']
    data['time'] = get_date_string(data['time'])
    data_date = data['time']
    entry = om.get(dates_om, data_date)
    if entry is not None:
        date_list = me.getValue(entry)
    else:
        date_list = lt.newList('ARRAY_LIST')
        om.put(dates_om, data_date, date_list)
        
    lt.addLast(date_list, data)
'''

def req1y6_data(data_structs, data):
    dates_om = data_structs['req1y6']
    data['time'] = get_date_string(data['time'])
    data_date = get_year(data['time'])
    entry = om.get(dates_om, data_date)
    if entry is not None:
        date_list = me.getValue(entry)
    else:
        date_list = lt.newList('ARRAY_LIST')
        om.put(dates_om, data_date, date_list)
        
    lt.addLast(date_list, data)

def req1_data(data_structs, data):

    # TODO Intentar reducir tiempo de carga
    dates_om = data_structs['req1y6']
    data['time'] = get_date_string(data['time'])
    data_date = get_year(data['time'])
    entry = om.get(dates_om, data_date)
    if entry is not None:
        date_list = me.getValue(entry)
    else:
        date_list = lt.newList('ARRAY_LIST')
        om.put(dates_om, data_date, date_list)
        
    lt.addLast(date_list, data)

def req2_data(data_structs, data):
    mags_om = data_structs['req2']
    data_mag = round(float(data['mag']), 0)
    entry = om.get(mags_om, data_mag)
    if entry is not None:
        mag_list = me.getValue(entry)
    else:
        mag_list = lt.newList('ARRAY_LIST')
        om.put(mags_om, data_mag, mag_list)
        
    lt.addLast(mag_list, data)
    
def req3_data(data_structs, data):
    mags_om = data_structs['req3']
    data_mag = round(float(data['mag']), 3)
    entry = om.get(mags_om, data_mag)
    if entry is not None:
        depths_om = me.getValue(entry)
    else:
        depths_om = om.newMap(cmpfunction=compare_req3_depth)
        om.put(mags_om, data_mag, depths_om)
        
    data_depth = round(float(data['depth']), 3)
    entry = om.get(depths_om, data_depth)
    if entry is not None:
        date_list = me.getValue(entry)
    else:
        date_list = date_list = lt.newList('ARRAY_LIST')
        om.put(depths_om, data_depth, date_list)
    
    lt.addLast(date_list, data)

def req5_compare_stations(data_1, data_2):
    
    station_1 = float(data_1)
    station_2 = float(data_2)
    
    if station_1 == station_2:
        return 0
    elif station_1 < station_2:
        return -1
    else:
        return 1
    
def req5_compare_mag(data_1, data_2):
    mag_1 = float(data_1)
    mag_2 = float(data_2)
    
    if mag_1 == mag_2:
        return 0
    elif mag_1 < mag_2:
        return -1
    else:
        return 1    
    
    
def req5_data(data_structs, data):
    stations_om = data_structs['req5']# Obtención mapa de estaciones
    if data['nst'] == '':
        data['nst'] = '1'
    data_station = round(float(data['nst']), 3)
    entry = om.get(stations_om, data_station)#definción del entry 
    if entry is not None:
        mags_om = me.getValue(entry)
    else:
        mags_om = om.newMap(cmpfunction=req5_compare_mag)#creación mapa de profundidades
        om.put(stations_om, data_station, mags_om)#se agrega el mapa al mapa de estaciones
        
    data_mag = round(float(data['depth']), 3)
    entry = om.get(mags_om, data_mag)
    if entry is not None:
        date_list = me.getValue(entry)
    else:
        date_list = lt.newList('ARRAY_LIST')#Creación de la lista que contiene toda la información de los eventos
        om.put(mags_om, data_mag, date_list)
    lt.addLast(date_list, data)#Se agregan los datos del evento a la lista
        

'''

#def req_data

def req6_data(data_structs, data):
    dates_om = data_structs['req6']
    data['time'] = get_date_string(data['time'])
    data_date = get_year(data['time'])
    entry = om.get(dates_om, data_date)
    if entry is not None:
        date_list = me.getValue(entry)
    else:
        date_list = lt.newList('ARRAY_LIST')
        om.put(dates_om, data_date, date_list)
        
    lt.addLast(date_list, data)
'''

def req7_data(data_structs, data):
    dates_mp = data_structs['req7']
    data['time'] = get_date_string(data['time'])
    data_date = get_year(data['time'])
    entry = mp.get(dates_mp, data_date)
    if entry is not None:
        places_mp = me.getValue(entry)
    else:
        places_mp = mp.newMap(80, maptype='PROBING')
        mp.put(dates_mp, data_date, places_mp)
        mp.put(places_mp, 'count', lt.newList())
    
    count_entry = mp.get(places_mp, 'count')
    count = me.getValue(count_entry)
    lt.addLast(count, 1)
    
    data_place = data['title']
    if ',' in data_place:
        place_list = data_place.split(',')
        data_place = place_list[len(place_list)-1]
        data_place = data_place[1:len(data_place)]
    entry = mp.get(places_mp, data_place)
    if entry is not None:
        place_list = me.getValue(entry)
    else:
        place_list = lt.newList('ARRAY_LIST')
        mp.put(places_mp, data_place, place_list)
        
    lt.addLast(place_list, data)

# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass

def data_size(data_structs, name=None):
    """
    Retorna el tamaño de la lista de datos
    """
    if name:
        return lt.size(data_structs[name])
    else:
        return lt.size(data_structs)

def new_topbot_sublist(sorted_list, n):
    """creates a list that contains the first n and last n elements of
        a data structure

    Args:
        data_structs (list): original data structure

    Returns:
        list: a list containing the first 3 and last 3 elements of the original list
    """
    topbot = lt.newList('ARRAY_LIST')
    toplist = lt.subList(sorted_list, 1, n)
    botlist = lt.subList(sorted_list, data_size(sorted_list)-n+1, n)
    
    for elem in lt.iterator(toplist):
        list_elem = []
        if type(elem) is dict:
            for value in elem.values():
                list_elem.append(value)
        elif type(elem) is list:
            for value in elem:
                list_elem.append(value)
        lt.addLast(topbot, list_elem)
    
    for elem in lt.iterator(botlist):
        list_elem = []
        if type(elem) is dict:
            for value in elem.values():
                list_elem.append(value)
        elif type(elem) is list:
            for value in elem:
                list_elem.append(value)
        lt.addLast(topbot, list_elem)
        
    return topbot

# Req 1

def req_1(data_structs, start_date, end_date):
    """
    Función que soluciona el requerimiento 1
    """
    # Realizar el requerimiento 1
    dates_om = data_structs['req1y6']
    total_dates = 0
    
    start_year = get_year(start_date)
    exists_min = om.contains(dates_om, start_year)
    if not exists_min:
        start_year = om.ceiling(dates_om, start_year)
        
    end_year = get_year(end_date)
    exists_max = om.contains(dates_om, end_year)
    if not exists_max:
        end_year = om.floor(dates_om, end_year)
    date_range = om.values(dates_om, start_year, end_year)
    
    events_list, count = req_1_list(date_range, total_dates, start_date, end_date)
    
    return events_list, count
    
def req_1_list(date_range, total_dates, start_date, end_date):
    event_list = lt.newList('ARRAY_LIST')
    
    details_columns = ['mag','lat','long','depth','sig','gap','nst','title',
                       'cdi', 'mmi', 'magType', 'type', 'code']
    count = {'total_dates':total_dates,
             'events_in_range':0}
        
    for year in lt.iterator(date_range):
        events_map = mp.newMap(maptype='PROBING')
        for event in lt.iterator(year):
            time = get_date_string(event['time'])
            time_value = get_date_value(time)
            start_value = get_date_value(start_date)
            end_value = get_date_value(end_date)
            if (start_value <= time_value) and (time_value <= end_value):
                count['events_in_range'] += 1
                entry = mp.get(events_map, time)
                if entry is None:
                    event_info = {'count':0,
                                  'details':lt.newList('ARRAY_LIST')}
                    mp.put(events_map, time, event_info)
                entry = mp.get(events_map, time)
                event_info = me.getValue(entry)
                
                event_info['count'] += 1
                
                event_elem = []
                req1_details_element(event_elem, event)
                
                details = event_info['details']
                lt.addLast(details, event_elem)
                
        for time in lt.iterator(mp.keySet(events_map)):
            entry = mp.get(events_map, time)
            event = me.getValue(entry)
            
            event_count = event['count']
            details = event['details']
            sort(details, 'req1y3_details')
            if lt.size(details) > 6:
                details = new_topbot_sublist(details, 3)
            elem = [time, event_count,
                    tabulate(lt.iterator(details),
                            tablefmt="grid",
                            headers=details_columns,
                            maxcolwidths = [18,5,5,5,5,5,5,20,11,11,5,20,20])]
            lt.addFirst(event_list, elem)
        
    sort(event_list, 'req1_list')
    return event_list, count

def req1_details_element(event_elem, event):
    event_elem.append(round(float(event['mag']),3))
    event_elem.append(round(float(event['lat']),3))
    event_elem.append(round(float(event['long']),3))
    event_elem.append(round(float(event['depth']),3))
    event_elem.append(event['sig'])
    gap = event['gap']
    if gap != '':
        event_elem.append(round(float(gap),3))
    else:
        event_elem.append(0.000)
    nst = event['nst']
    if nst != '':   
        event_elem.append(float(nst))
    else:
        event_elem.append(1)
    event_elem.append(event['title'])
    cdi = event['cdi']
    if cdi != '':
        event_elem.append(round(float(cdi),3))
    else:
        event_elem.append('Unavailable')
    mmi = event['mmi']
    if mmi != '':
        event_elem.append(round(float(mmi),3))
    else:
        event_elem.append('Unavailable')
    event_elem.append(event['magType'])
    event_elem.append(event['type'])
    event_elem.append(event['code'])


# Req 2

def req_2(data_structs, start_mag, end_mag):
    """
    Función que soluciona el requerimiento 2
    """
    # Realizar el requerimiento 2
    mags_om = data_structs['req2']
    total_magnitudes = 0
    
    minimum = round(float(start_mag), 0)
    exists_min = om.contains(mags_om, minimum)
    if not exists_min:
        start_mag = om.ceiling(mags_om, minimum)
    
    maximum = round((float(end_mag)), 0)
    exists_max = om.contains(mags_om, maximum)
    if not exists_max:
        end_mag = om.floor(mags_om, maximum)

    mag_range = om.values(mags_om, minimum, maximum)
    
    events_list, count = req_2_list(mag_range, total_magnitudes, start_mag, end_mag)
    
    return events_list, count

def req_2_list(mag_range, total_mags, start_mag, end_mag):
    event_list = lt.newList('ARRAY_LIST')
    
    details_columns = ['time','lat','long','depth','sig','gap','nst','title',
                       'cdi','mmi','magType','type','code']
    count = {'total_magnitudes':total_mags,
             'events_in_range':0}
        
    for mag in lt.iterator(mag_range):
        event_count = lt.size(mag)
        details = lt.newList()
        
        events_map = mp.newMap(maptype='PROBING')
        for event in lt.iterator(mag):
            magnitude = round(float(event['mag']), 3)
            
            if round(float(start_mag),3) <= magnitude and magnitude <= round(float(end_mag),3):
                count['events_in_range'] += 1
                entry = mp.get(events_map, magnitude)
                if entry is None:
                    event_info = {'count':0,
                                  'details':lt.newList('ARRAY_LIST')}
                    mp.put(events_map, magnitude, event_info)
                else:
                    event_info = me.getValue(entry)

                event_info['count'] += 1
                event_elem = []
                req2_details_element(event_elem, event)
                details = event_info['details']
                lt.addLast(details, event_elem)
        
        for magnitude in lt.iterator(mp.keySet(events_map)):
            entry = mp.get(events_map, magnitude)
            event = me.getValue(entry)
            
            event_count = event['count']
            details = event['details']
            sort(details, 'req2_details')
            if lt.size(details) > 6:
                details = new_topbot_sublist(details, 3)
            elem = [magnitude, event_count,
                tabulate(lt.iterator(details),
                         tablefmt="grid",
                         headers=details_columns,
                         maxcolwidths = [18,5,5,5,5,5,5,20,11,11,5,20,20])]
            lt.addFirst(event_list, elem)
            
    sort(event_list, 'req2_list')
    return event_list, count

def req2_details_element(event_elem, event):
    event_elem.append(get_date_string(event['time']))
    event_elem.append(round(float(event['lat']),3))
    event_elem.append(round(float(event['long']),3))
    event_elem.append(round(float(event['depth']),3))
    event_elem.append(event['sig'])
    gap = event['gap']
    if gap != '':
        event_elem.append(round(float(gap),3))
    else:
        event_elem.append(0.000)
    nst = event['nst']
    if nst != '':   
        event_elem.append(float(nst))
    else:
        event_elem.append(1)
    event_elem.append(event['title'])
    cdi = event['cdi']
    if cdi != '':
        event_elem.append(round(float(cdi),3))
    else:
        event_elem.append('Unavailable')
    mmi = event['mmi']
    if mmi != '':
        event_elem.append(round(float(mmi),3))
    else:
        event_elem.append('Unavailable')
    event_elem.append(event['magType'])
    event_elem.append(event['type'])
    event_elem.append(event['code'])


# Req 3

def req_3(data_structs, min_mag, max_depth):
    """
    Función que soluciona el requerimiento 3
    """
    # Realizar el requerimiento 3
    mags_om = data_structs['req3']
    exists_min = om.contains(mags_om, min_mag)
    if not exists_min:
        min_mag = om.ceiling(mags_om, min_mag)
    mag_range = om.values(mags_om, min_mag, om.maxKey(mags_om))
    
    events_list, count = req_3_list(mag_range, max_depth)
    
    return events_list, count

def req_3_list(mag_range, max_depth):
    event_list = lt.newList('ARRAY_LIST')
    
    details_columns = ['mag','lat','long','depth','sig','gap','nst','title',
                       'cdi','mmi','magType','type','code']
    count = {'events_in_range':0}
    permanent_max_depth = max_depth
    
    for mag in lt.iterator(mag_range):
        exists_depth = om.contains(mag, permanent_max_depth)
        if not exists_depth:
            max_depth = om.floor(mag, permanent_max_depth)
        else:
            max_depth = permanent_max_depth
        depth_range = om.values(mag, om.minKey(mag), max_depth)
        details = lt.newList()
        
        for depth in lt.iterator(depth_range):
            events_map = mp.newMap(maptype='PROBING')
            
            for event in lt.iterator(depth):
                count['events_in_range'] += 1
                event_time = get_date_string(event['time'])
                
                entry = mp.get(events_map, event_time)
                if entry is None:
                    event_info = {'count':0,
                                  'details':lt.newList('ARRAY_LIST')}
                    mp.put(events_map, event_time, event_info)
                else:
                    event_info = me.getValue(entry)

                event_info['count'] += 1
                event_elem = []
                req3_details_element(event_elem, event)
                details = event_info['details']
                lt.addLast(details, event_elem)
        
            for time in lt.iterator(mp.keySet(events_map)):
                entry = mp.get(events_map, time)
                event = me.getValue(entry)
                
                event_count = event['count']
                details = event['details']
                sort(details, 'req1y3_details')
                if lt.size(details) > 6:
                    details = new_topbot_sublist(details, 3)
                elem = [time, event_count,
                        tabulate(lt.iterator(details),
                                tablefmt="grid",
                                headers=details_columns,
                                maxcolwidths = [18,5,5,5,5,5,5,20,11,11,5,20,20])]
                lt.addFirst(event_list, elem)
    
    sort(event_list, 'req3_events')
    event_list = lt.subList(event_list, 1, 10)
    
    return event_list, count

def req3_details_element(event_elem, event):
    event_elem.append(round(float(event['mag']),3))
    event_elem.append(round(float(event['lat']),3))
    event_elem.append(round(float(event['long']),3))
    event_elem.append(round(float(event['depth']),3))
    event_elem.append(event['sig'])
    gap = event['gap']
    if gap != '':
        event_elem.append(round(float(gap),3))
    else:
        event_elem.append(0.000)
    nst = event['nst']
    if nst != '':   
        event_elem.append(float(nst))
    else:
        event_elem.append(1)
    event_elem.append(event['title'])
    cdi = event['cdi']
    if cdi != '':
        event_elem.append(round(float(cdi),3))
    else:
        event_elem.append('Unavailable')
    mmi = event['mmi']
    if mmi != '':
        event_elem.append(round(float(mmi),3))
    else:
        event_elem.append('Unavailable')
    event_elem.append(event['magType'])
    event_elem.append(event['type'])
    event_elem.append(event['code'])

# Req 4 funciones empleadas
# ******************************* CREAR UN DICCIONAARIOP CON LA INFORMACION EMCAPSULADA **********************************
def req4_data(data_structs):
    #for y in lt.iterator(data_structs["temblores"]):
    lst_req4 = lt.newList('SINGLE_LINKED')
    for data in lt.iterator(data_structs["temblores"]):
        lt.addLast (lst_req4,{"time":data["time"],
                    "events": 1,
                    "details":{"mag":data["mag"],
                                "lat":data["lat"],
                                "long":data["long"],
                                "depth":data["depth"],
                                "sig":data["sig"],
                                "gap":data["gap"],
                                "nst":data["nst"], 
                                "title":data["title"],
                                "cdi":data["cdi"],
                                "mmi":data["mmi"],
                                "magType":data["magType"],
                                "type":data["type"],
                                "code":data["code"]
                                } 
                        })
        #lt.addLast (lst_req4,capsule_lst)
    #print(capsule_lst)
    return lst_req4
# ******************************* TRANSFORMAR TEXTO A FORMATO DE FECHA **********************************
def time_operabile(date):
    time =date['time']
    format = '%Y-%m-%dT%H:%M'
    trans_date = dt.strptime(time,format)
    return trans_date
# ******************************* COMPARAR DOS TIEMPOS *************************************   
def sort_comparation_time (data_1, data_2):

    if time_operabile(data_1) != time_operabile(data_2):
        return time_operabile(data_1)>time_operabile(data_2)
    #else:
     #   return data_1['country']<data_2['country']
# ******************************* RETORNA LOS PRIMEROS Y ULTIMOS 3 *************************************  
def first_last(informacion):
    
    if lt.size(informacion) < 6:
        return informacion
    primeros = lt.subList(informacion,1,3)
    ultimos = lt.subList(informacion,lt.size(informacion)-2,3)
    respuesta = lt.newList('ARRAY_LIST')
    for i in lt.iterator(primeros):
        lt.addLast(respuesta,i)
    for i1 in lt.iterator(ultimos):
        lt.addLast(respuesta,i1) 
    return respuesta
# Req 4

def req_4(data_structs,min_sig,max_gap):
    """
    Función que soluciona el requerimiento 4
    """
    # Realizar el requerimiento 4

    
    data_lst = lt.newList('SINGLE_LINKED')   
    data_data = req4_data(data_structs)
    for mg in lt.iterator(data_data):
        #print(mg["details"]["sig"])
        if min_sig < mg["details"]["sig"] and mg["details"]["gap"] < max_gap:
            mg["details"] = tabulate([mg["details"]],headers="keys",tablefmt="grid")
            lt.addLast(data_lst,mg) 
            
    quk.sort(data_lst,sort_comparation_time)
    count = 0
    lst_fnd = lt.newList('SINGLE_LINKED')


def req5_event_criteria(data_1, data_2):
    time_1 = get_date_string(data_1['time'])
    time_2 = get_date_string(data_2['time'])
    if time_1 != time_2:
        return time_1 < time_2

        

def req_5(data_structs, depth, stations):

    for std in lt.iterator(data_lst):      
        if count <= 15:
            lt.addLast(lst_fnd,std)
            count +=1 
    respuesta = first_last(lst_fnd)
        
    return respuesta  
def req_5(data_structs):

    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    
    stations_om = data_structs['req5']#Obtención mapa de estaciones
    entry = om.get(stations_om, float(stations))
    if entry is not None:#busqueda de la estación mínima en el mapa
        min_stations = stations
    else:
        min_stations = om.ceiling(stations_om, stations)#en caso de que no se encuentre la cantidad mínima se busca el mínimo más cercano que
                                                        #se encuentre en el mapa   
    stations_range = om.values(stations_om, min_stations, om.maxKey(stations_om)) #Obtención del rango de estaciones permitidas
    event_list = lt.newList('ARRAY_LIST')  
    for station in lt.iterator(stations_range):#Recorrido estaciones en rango permitido
        min_depth = depth
        exist_depth = om.contains(station, min_depth)#Búsqueda de la profundidad mínima en el mapa de profundidades
        if not exist_depth:
            min_depth = om.ceiling(station, depth)#En caso de que no se encuentra la profundidad mínima se busca el mínimo más cercano que se
                                                  #se encuentre en el mapa  
            if min_depth == None:
                continue
        depth_range = om.values(station, min_depth, om.maxKey(station))#Obtención del rango de profundidades permitidas
        for depth_1 in lt.iterator(depth_range):#Recorrido del rango de profundidades permitidas
            for event in lt.iterator(depth_1):
                lt.addLast(event_list, event)#Se agrega la información del evento a la lista de eventos
                
    event_list_sorted = sa.sort(event_list, req5_event_criteria)#Ordenamiento de la lista por fecha son método shellsort
    contador = lt.size(event_list_sorted)#Contador para cantidad de eventos encontrados en los rangos permitidos
    
    if contador > 20:
        top_twenty_list = lt.subList(event_list_sorted, contador-19, 20)#Obtención de los 20 eventos más recientes
    else:
        top_twenty_list = event_list_sorted
        
    lista_final_tabulate = lt.newList('ARRAY_LIST')#tratamiento de datos para usar tabulate correctamente
    for final_event in lt.iterator(top_twenty_list):
        
        evento_final = {'time':None,
                   'events': None,
                'details': lt.newList('ARRAY_LIST')}
        
        elemento = {'mag': None,
                                   'lat': None,
                                   'long': None,
                                   'depth': None,
                                   'sig': None,
                                   'gap': None,
                                   'nst': None,
                                   'title': None,
                                   'cdi': None,
                                   'mmi': None,
                                   'magType': None,
                                   'type': None,
                                   'code': None}
                                   
        
        evento_final['time'] = get_date_string(final_event['time'])
        elemento['mag'] = final_event['mag']
        elemento['lat'] = final_event['lat']
        elemento['long'] = final_event['long']
        elemento['depth'] = final_event['depth']
        elemento['sig'] = final_event['sig']
        elemento['gap'] = final_event['gap']
        elemento['nst'] = final_event['nst']
        elemento['title'] = final_event['title']
        elemento['cdi'] = final_event['cdi']
        elemento['mmi'] = final_event['mmi']
        elemento['magType'] = final_event['magType']
        elemento['type'] = final_event['type']
        elemento['code'] = final_event['code']
        evento_final['events'] = 1
        lt.addLast(evento_final['details'],elemento)
        evento_final['details'] = tabulate(lt.iterator(evento_final['details']),tablefmt='grid',headers='keys')
        #evento_final['details'] = tabulate(evento_final['details'],headers='keys',tablefmt='grid')
        
        
        
        
        lt.addLast(lista_final_tabulate, evento_final)
    return lista_final_tabulate, contador
        
    

        
        
        
    
    
      
    
             

        
        
    
    
    
    
    


# Req 6

def req_6(data_structs, year, r, n, latref, longref):
    """
    Función que soluciona el requerimiento 6
    """
    # Realizar el requerimiento 6
    dates_om = data_structs['req1y6']
    entry_year_list = om.get(dates_om, year)
    year_list = me.getValue(entry_year_list)
    r = int(r)
    n = int(n)
    latref = round(float(latref), 3)
    longref = round(float(longref), 3)
    
    sig_event, index, sig_time  = req6_most_significat_event(year_list, r, latref, longref)
    year_list = lt.subList(year_list, index+1, (lt.size(year_list) - index)) 
    
    event_list, count = req6_list(year_list, sig_time, r, n, latref, longref)
    
    return event_list, count, sig_event
    
def req6_most_significat_event(year_list, r, latref, longref):
    index = 0
    for event in lt.iterator(year_list):
        lat = round(float(event['lat']),3)
        long = round(float(event['long']),3)
        distance = haversine_distance(latref, lat, longref, long)
        index += 1
        if abs(distance) <= r:
            sig_event, time = req6_sig_element(event, distance)
            return sig_event, index, time

def haversine_distance(lat1, lat2, long1, long2):
    lat1 = m.radians(lat1)
    lat2 = m.radians(lat2)
    long1 = m.radians(long1)
    long2 = m.radians(long2)
    
    halflatdiff = (lat2 - lat1)/2
    first_term = m.sin(halflatdiff)**2
    
    coslat1 = m.cos(lat1)
    coslat2 = m.cos(lat2)
    halflongdiff = (long2 - long1)/2
    second_term = coslat1 * coslat2 * (m.sin(halflongdiff)**2)
    
    in_root_expression = first_term + second_term
    
    final_term = m.asin(m.sqrt(in_root_expression))
    
    distance = 2*final_term*6341
    
    return abs(distance)

def req6_sig_element(event, distance):
    event_elem = []
    sig_event = lt.newList('ARRAY_LIST')
    time = get_date_string(event['time'])
    event_elem.append(time)
    event_elem.append(round(float(event['mag']),3))
    event_elem.append(round(float(event['lat']),3))
    event_elem.append(round(float(event['long']),3))
    event_elem.append(round(float(event['depth']),3))
    event_elem.append(event['sig'])
    gap = event['gap']
    if gap != '':
        event_elem.append(round(float(gap),3))
    else:
        event_elem.append(0.000)
    event_elem.append(distance)
    nst = event['nst']
    if nst != '':   
        event_elem.append(float(nst))
    else:
        event_elem.append(1)
    event_elem.append(event['title'])
    cdi = event['cdi']
    if cdi != '':
        event_elem.append(round(float(cdi),3))
    else:
        event_elem.append('Unavailable')
    mmi = event['mmi']
    if mmi != '':
        event_elem.append(round(float(mmi),3))
    else:
        event_elem.append('Unavailable')
    event_elem.append(event['magType'])
    event_elem.append(event['type'])
    event_elem.append(event['code'])
    
    lt.addFirst(sig_event, event_elem)
    
    return sig_event, time

def req6_list(year_list, sig_time, r, n, latref, longref):
    greater_event_list = lt.newList('ARRAY_LIST')
    lesser_event_list = lt.newList('ARRAY_LIST')
    details_columns = ['mag','lat','long','depth','sig','gap','distance','nst','title',
                       'cdi','mmi','magType','type','code']
    count = {'events_in_range':0}
    events_map = mp.newMap(maptype='PROBING')
    for event in lt.iterator(year_list):
        lat = round(float(event['lat']),3)
        long = round(float(event['long']),3)
        distance = haversine_distance(latref, lat, longref, long)
        if round(distance,0) <= r:
            count['events_in_range'] += 1
            event_time = get_date_string(event['time'])
            entry = mp.get(events_map, event_time)
            if entry is None:
                event_info = {'count':0,
                                'details':lt.newList('ARRAY_LIST')}
                mp.put(events_map, event_time, event_info)
            else:
                event_info = me.getValue(entry)

            event_info['count'] += 1
            event_elem = []
            req6_details_element(event_elem, event, distance)
            details = event_info['details']
            lt.addLast(details, event_elem)
    
    for time in lt.iterator(mp.keySet(events_map)):
            entry = mp.get(events_map, time)
            event = me.getValue(entry)
            event_count = event['count']
            details = event['details']
            sort(details, 'req1y3_details')
            if lt.size(details) > 6:
                details = new_topbot_sublist(details, 3)
            value = date_difference(time, sig_time)
            elem = [time, event_count,
                    tabulate(lt.iterator(details),
                            tablefmt="grid",
                            headers=details_columns,
                            maxcolwidths = [18,5,5,5,5,5,20,11,11,11,11,20,20]),
                    value]
            if value > 0:
                lt.addFirst(lesser_event_list, elem)
            else:
                lt.addFirst(greater_event_list, elem)
            
    event_list = lt.newList('ARRAY_LIST')
    sort(lesser_event_list, 'req6_events')
    sort(greater_event_list, 'req6_events')
    
    lesser_size = lt.size(lesser_event_list)    
    if lesser_size < n:
        for event in lt.iterator(lesser_event_list):
            lt.addLast(event_list, event)
    else:
        for i in range(n):
            event = lt.getElement(lesser_event_list, i+1)
            lt.addLast(event_list, event)
            
    greater_size = lt.size(greater_event_list)    
    if greater_size < n:
        for event in lt.iterator(greater_event_list):
            lt.addLast(event_list, event)
    else:
        for i in range(n):
            event = lt.getElement(greater_event_list, i+1)
            lt.addLast(event_list, event)
    
    sort(event_list, 'req6_events')
    
    new_list = lt.newList('ARRAY_LIST')
    for event in lt.iterator(event_list):
        event = event[0:3]
        lt.addLast(new_list, event)
    size = lt.size(new_list)
    count['size'] = size

    return new_list, count

def req6_details_element(event_elem, event, distance):
    event_elem.append(round(float(event['mag']),3))
    event_elem.append(round(float(event['lat']),3))
    event_elem.append(round(float(event['long']),3))
    event_elem.append(round(float(event['depth']),3))
    event_elem.append(event['sig'])
    gap = event['gap']
    if gap != '':
        event_elem.append(round(float(gap),3))
    else:
        event_elem.append(0.000)
    event_elem.append(distance)
    nst = event['nst']
    if nst != '':   
        event_elem.append(float(nst))
    else:
        event_elem.append(1)
    event_elem.append(event['title'])
    cdi = event['cdi']
    if cdi != '':
        event_elem.append(round(float(cdi),3))
    else:
        event_elem.append('Unavailable')
    mmi = event['mmi']
    if mmi != '':
        event_elem.append(round(float(mmi),3))
    else:
        event_elem.append('Unavailable')
    event_elem.append(event['magType'])
    event_elem.append(event['type'])
    event_elem.append(event['code'])

def mix_list(old_list,new_list,n):
    pass

# Req 7

def req_7(data_structs, year, title, prop, bins):
    """
    Función que soluciona el requerimiento 7
    """
    #Realizar el requerimiento 7
    dates_mp = data_structs['req7']
    entry = mp.get(dates_mp, year)
    places_mp = me.getValue(entry)
    entry = mp.get(places_mp, title)
    place_list = me.getValue(entry)
    
    count_entry = mp.get(places_mp, 'count')
    count = me.getValue(count_entry)
    year_count = lt.size(count)
    
    event_list, count, histogram_list = req7_list(place_list, prop, year_count)
    
    return event_list, count, histogram_list

def req7_list(place_list, prop, year_count):
    event_list = lt.newList()
    histogram_list = []

    count = {'total_events':year_count,
             'events_in_range':0}

    for event in lt.iterator(place_list):
        
        if event[prop] != '':
            event_prop = round(float(event[prop]),3)
        else:
            event_prop = 'Unkown'
        
        if event_prop != 'Unkown':
            count['events_in_range'] += 1
            elem = []
            req7_elem(elem, event, prop)
            lt.addLast(event_list, elem)
            histogram_list.append(event_prop)
    
    sort(event_list, 'req7_events')
    count['max'] = lt.firstElement(event_list)[-1]
    count['min'] = lt.lastElement(event_list)[-1]
    sort(event_list, 'req1_list')
     
    return event_list, count, histogram_list
   
def req7_elem(elem, event, prop):
    time = get_date_string(event['time'])
    elem.append(time)
    elem.append(round(float(event['lat']),3))
    elem.append(round(float(event['long']),3))
    elem.append(round(float(event['depth']),3))
    elem.append(event['sig'])
    gap = event['gap']
    if gap != '':
        elem.append(round(float(gap),3))
    else:
        elem.append(0)
    nst = event['nst']
    if nst != '':
        elem.append(float(nst))
    else:
        elem.append(1)
    elem.append(event['title'])
    elem.append(event[prop])

# Req 8

def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def get_date_value(date, loading=False):
    '''
    # Version 1
    if len(date) > 16:
        date_value = dt.strptime(date,'%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        date_value = dt.strptime(date,'%Y-%m-%dT%H:%M')
    date_value = int(date_value.strftime('%Y%m%d%H%M'))
    '''
    # Version 2
    if len(date) > 16 and loading:
        date_value = dt.strptime(date,'%Y-%m-%dT%H:%M:%S.%fZ')
        date_value = date_value.strftime('%Y')
    elif loading:
        date_value = dt.strptime(date,'%Y')
        date_value = date_value.strftime('%Y')
    else:
        date_value = dt.strptime(date, '%Y-%m-%dT%H:%M')
        date_value = date_value.strftime('%Y%m%d%H%M')
    
    return int(date_value)
    

def get_date_string(date):
    if len(date) > 16:
        date_string = dt.strptime(date,'%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        date_string = dt.strptime(date,'%Y-%m-%dT%H:%M')
    date_string = date_string.strftime('%Y-%m-%dT%H:%M')
    return date_string

def get_year(date):
    date_string = dt.strptime(date,'%Y-%m-%dT%H:%M')
    date_string = date_string.strftime('%Y')
    return date_string

def date_difference(date1, date2):
    multiplicatives = [1,12,365,8760,525600]
    date1_value = dt.strptime(date1, '%Y-%m-%dT%H:%M')
    date1_list = date1_value.strftime('%Y,%m,%d,%H,%M').split(',')
    value1 = 0
    i = 0
    while i < len(date1_list):
        value1 += (int(date1_list[i]))/multiplicatives[i]
        i+=1
    
    date2_value = dt.strptime(date2, '%Y-%m-%dT%H:%M')
    date2_list = date2_value.strftime('%Y,%m,%d,%H,%M').split(',')
    value2 = 0
    i = 0
    while i < len(date2_list):
        value2 += (int(date2_list[i]))/multiplicatives[i]
        i+=1
        
    return value2 - value1


def compare_req1_dates(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    # Crear función comparadora de la lista
    time1 = data_1
    time2 = data_2
    
    value1 = get_date_value(time1, True)
    value2 = get_date_value(time2, True)
    
    if (value1 == value2):
        return 0
    elif (value1 > value2):
        return 1
    else:
        return -1
    
def compare_req2y3_magnitudes(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    # Crear función comparadora de la lista
    mag1 = round(float(data_1), 3)
    mag2 = round(float(data_2), 3)

    if (mag1 == mag2):
        return 0
    elif (mag1 > mag2):
        return 1
    else:
        return -1
    
def compare_req3_depth(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    # Crear función comparadora de la lista
    if data_1 != None:
        dep1 = round(float(data_1), 3)
    else:
        dep1 = 0.000
    if data_2 != None:
        dep2 = round(float(data_2), 3)
    else:
        dep2 = 0

    if (dep1 == dep2):
        return 0
    elif (dep1 > dep2):
        return 1
    else:
        return -1

# Funciones de ordenamiento


def sort_req1_details_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    mag1 = data_1[0]
    mag2 = data_2[0]
    
    return mag1 > mag2

def sort_req2_details_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    time1 = data_1[0]
    time2 = data_2[0]
    
    value1 = get_date_value(time1)
    value2 = get_date_value(time2)
    
    return value1 > value2

def sort_req3_events(data_1, data_2):
    time1 = data_1[0]
    time2 = data_2[0]
    
    value1 = get_date_value(time1)
    value2 = get_date_value(time2)
    
    return value1 > value2

def sort_req5_events(data_1, data_2):
    time1 = data_1[0]
    time2 = data_2[0]
    
    value1 = get_date_value(time1)
    value2 = get_date_value(time2)
    
    return value1 > value2



def sort_req1_list(data_1, data_2):
    time1 = data_1[0]
    time2 = data_2[0]
    
    value1 = get_date_value(time1)
    value2 = get_date_value(time2)
    
    return value1 > value2

def sort_req2_list(data_1, data_2):
    mag1 = data_1[0]
    mag2 = data_2[0]
    
    return mag1 > mag2

def sort_req5_details_criteria(data_1, data_2):
    
    
    mag1 = data_1[0]
    mag2 = data_2[0]
    
    return mag1 > mag2
    

def sort_req6(data_1, data_2):
    sig1 = int(data_1['sig'])
    sig2 = int(data_2['sig'])
    
    time1 = data_1['time']
    time2 = data_2['time']
    
    value1 = get_date_value(time1)
    value2 = get_date_value(time2)
    
    if sig1 != sig2:
        return sig1 > sig2
    else:
        return value1 > value2
    
def sort_req6_events(data_1, data_2):
    
    value1 = abs(data_1[3])
    value2 = abs(data_2[3])
    
    return value1 < value2

def sort_req7_events(data_1, data_2):
    prop1 = float(data_1[-1])
    prop2 = float(data_2[-1])
    time1 = data_1[0]
    time2 = data_2[0]
    
    value1 = get_date_value(time1)
    value2 = get_date_value(time2)
    
    if prop1 != prop2:
        return prop1 > prop2
    else:
        return value1 < value2
        

def sort(data_structs, file_name):
    """
    Función encargada de ordenar la lista con los datos
    """
    if file_name == 'req1y3_details':
        criteria = sort_req1_details_criteria
        merg.sort(data_structs, criteria)
    elif file_name == 'req2_details':
        criteria = sort_req2_details_criteria
        merg.sort(data_structs, criteria)
    elif file_name == 'req3_events':
        criteria = sort_req3_events
        merg.sort(data_structs, criteria)
    elif file_name == 'req5_events':
        criteria = sort_req5_events
    elif file_name == 'req5_details':
        criteria = sort_req5_details_criteria
    elif file_name == 'req1_list':
        criteria = sort_req1_list
        merg.sort(data_structs, criteria)
    elif file_name == 'req2_list':
        criteria = sort_req2_list
        merg.sort(data_structs, criteria)
    elif file_name == 'req6':
        criteria = sort_req6
        dates_list = mp.valueSet(data_structs)
        for date in lt.iterator(dates_list):
            merg.sort(date, criteria)
    elif file_name == 'req6_events':
        criteria = sort_req6_events
        merg.sort(data_structs, criteria)
    elif file_name == 'req7_events':
        criteria = sort_req7_events
        merg.sort(data_structs, criteria)
    