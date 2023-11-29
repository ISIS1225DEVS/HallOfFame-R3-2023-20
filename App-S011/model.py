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
import folium
from folium import Popup
from folium.plugins import MarkerCluster
from folium import Tooltip
import datetime
import math
import os
import html
from datetime import date
assert cf

MAP_TILE = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}'
MAP_ATTRIBUTES = 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012'
MAX_MAP_PROPS = 100000

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
    #TODO: Inicializar las estructuras de datos
    control = {}

    control['lista_temblores'] = lt.newList('ARRAY_LIST', compare)
    
    control['temblores_mag'] = om.newMap(omaptype='BST',
                                      cmpfunction=compareDates)
    control['temblores']= om.newMap(omaptype='BST',
                                      cmpfunction=compareDates)
    control["By_year"]=om.newMap(omaptype='BST',
                                      cmpfunction=compareDates)    
    control['temblores_sig']= om.newMap(omaptype='RBT',
                                        cmpfunction=compareFloats)
    
    control['temblores_gap']= om.newMap(omaptype='RBT',
                                        cmpfunction=compareFloats)
    
    control['quakes_req6']= lt.newList('ARRAY_LIST', compare)
    
    
    control['temblores_depth'] = om.newMap(omaptype= 'BST', 
                                           cmpfunction=compareFloats)
    return control  


# Funciones para agregar informacion al modelo

def add_data_ms(control, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    lt.addLast(control['lista_temblores'], data)
    updateDate(control["temblores_mag"],data)
    uptime(control["temblores"],data)
    up_depth(control['temblores_depth'],data)
    agregar_req_7(control["By_year"],data)
    up_significance(control, data)
    up_gap(control, data)
    up_req6(control, data)
    return control
    #TODO: Crear la función para agregar elementos a una lista
    

def up_req6(data_structs, data):
    info = nuevo(data)
    fecha = datetime.datetime.strptime(info["time"], '%Y-%m-%d %H:%M:%S')
    info['time']=fecha
    lt.addLast(data_structs['quakes_req6'], info)

def updateDate(mapa, data):
    mag = round(float(data['mag']),3)
    entry = om.get(mapa, mag)
    if entry is None:
        datentry = new_data()
        om.put(mapa,mag, datentry)
    else:
        datentry = me.getValue(entry)
    add_data(datentry, data)
    lt.addLast(datentry["By_mag"],data)
    return mapa

def uptime(mapa,data):
    occurreddate = data['time']
    fecha = datetime.datetime.strptime(occurreddate, "%Y-%m-%dT%H:%M:%S.%fZ")
   
    entry = om.get(mapa, fecha)
    if entry is None:
        datentry = new_data()
        om.put(mapa, fecha, datentry)
    else:
        datentry = me.getValue(entry)
    add_data_by_date(datentry,data)
    lt.addLast(datentry["By_time"],data)
    return mapa

def up_significance(data_structs, data):
    mapa = data_structs['temblores_sig']
    info = nuevo(data)
    if not info['sig']:
        info['sig']=0
    sig = info['sig']
    entry = om.get(mapa, sig)
    if entry is None:
        dataentry = lt.newList("ARRAY_LIST",cmpfunction=cmp_quakes)
    else:
        dataentry = me.getValue(entry)
    lt.addLast(dataentry, info)
    om.put(mapa, sig, dataentry)

def up_gap(data_structs, data):
    mapa = data_structs['temblores_gap']
    info = nuevo(data)
    if not info['gap']:
        info['gap']=0
    gap= round(float(info['gap']),3)
    entry = om.get(mapa, gap)
    if entry is None:
        dataentry = lt.newList("ARRAY_LIST",cmpfunction=cmp_quakes)
    else:
        dataentry = me.getValue(entry)
    lt.addLast(dataentry, info)
    om.put(mapa, gap, dataentry)

def up_depth(mapa, data):
    depth = data['depth']
    entry = om.get(mapa, depth)
    
    if entry is None:
        depth_entry = new_data()
        om.put(mapa,depth,depth_entry)
    else:
        depth_entry = me.getValue(entry)
    add_data(depth_entry,data)
    lt.addLast(depth_entry['By_depth_lst'],data)
    return mapa
    

# Funciones para creacion de datos

def new_data():
    """ 
    Crea una nueva estructura para modelar los datos
    """
    data= {}
    data["By_depth"]=om.newMap(omaptype='BST',
                                      cmpfunction=compareDates)
    data["By_mag"]= lt.newList("ARRAY_LIST")
    
    data["By_time"] = lt.newList("ARRAY_LIST")
   
    data["By_date"] = om.newMap(omaptype="BST",
                                cmpfunction=compareDates)
    data["By_depth_lst"] = lt.newList('ARRAY_LIST')
    
    return data

def add_data(structs,data):
    mapa= structs["By_depth"]
    entry= om.get(mapa,float(data["depth"]))
    if entry:
        lista= me.getValue(entry)
    else:
        lista= lt.newList("ARRAY_LIST")
        om.put(mapa,float(data["depth"]),lista)
    lt.addLast(lista,data)
    return structs

def add_data_by_date(structs,data):
    mapa= structs["By_date"]
    entry = om.get(mapa, data["time"])
    #occurreddate = data['time']
    #fecha = datetime.datetime.strptime(occurreddate, "%Y-%m-%dT%H:%M:%S.%fZ")
    #dates = fecha.strftime('%Y-%m-%dT%H:%M')
    #entry = om.get(mapa, data["time"])
    if entry is None:
        datentry = lt.newList("ARRAY_LIST")
        om.put(mapa,data["time"], datentry)
    
    else:
        datentry = me.getValue(entry)
        #om.put(mapa,data["time"],datentry)
    lt.addLast(datentry,data)
    return structs


    #TODO: Crear la función para estructurar los datos
    pass
def compare_elements(keyname, element):
    shootout_entry = me.getKey(element)
    if keyname== shootout_entry:
        return 0
    elif keyname>shootout_entry:
        return 1
    else:
        return -1

# Funciones de consulta
def get_data_5(data_structs,tamano):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista   
    resultados = lt.newList("ARRAY_LIST")
    lt.addFirst(resultados,lt.firstElement(data_structs))
    for b in range(2,6):
        p = lt.getElement(data_structs, b)
        lt.addLast(resultados, p)
    for b in range (0,5):
        p = lt.getElement(data_structs, (tamano-4+b))
        lt.addLast(resultados, p)
    return resultados

def get_data_3(data_structs,tamano):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista   
    resultados = lt.newList("ARRAY_LIST")
    lt.addFirst(resultados,lt.firstElement(data_structs))
    for b in range(2,4):
        p = lt.getElement(data_structs, b)
        lt.addLast(resultados, p)
    for b in range (0,3):
        p = lt.getElement(data_structs, (tamano-2+b))
        lt.addLast(resultados, p)
    return resultados


def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    return lt.size(data_structs)
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(control, fecha_inicio, fecha_final):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    fecha_in = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M')
    fecha_fin = datetime.datetime.strptime(fecha_final, '%Y-%m-%dT%H:%M')
    lst_rango_fechas = om.keys(control["temblores"],fecha_in, fecha_fin)
    
    total = 0
    lista_final = lt.newList("SINGLE_LINKED")
    all_quakes = lt.newList("ARRAY_LIST")
    for lst_fecha in lt.iterator(lst_rango_fechas):
        respuesta = me.getValue(om.get(control["temblores"],lst_fecha))
        tamanio = lt.size(respuesta["By_time"])
        total += tamanio
        dic = {"time" : lst_fecha, "mag": lst_fecha, "Adicional": lt.newList("ARRAY_LIST")}
        info_adicional = dic["Adicional"]
        
        orden = merg.sort(respuesta["By_time"], compare_results_list)
        
        if tamanio < 6:
            for ele in lt.iterator(orden):
                d = nuevo(ele)
                lt.addLast(all_quakes, d)
                lt.addLast(info_adicional,d)
        else:
            for x in lt.iterator(orden):
                lt.addLast(all_quakes, x)
            for date in range(1,4):
                info = lt.getElement(orden,date)
                info = nuevo(info)
                lt.addLast(info_adicional,info)
            for date in range(0,3): 
                info = lt.getElement(orden,date,(tamanio-2+date))
                info = lt.addLast(info_adicional,info)
                lt.addLast(info_adicional,info)
        lt.addFirst(lista_final,info_adicional)
    return lista_final, total, all_quakes
         
def req_2(analyzer,initialmag, finalmag ):
    """
    Función que soluciona el requerimiento 2
    """
    total=0
    lista= lt.newList("SINGLE_LINKED")
    lst = om.keys(analyzer['temblores_mag'], initialmag, finalmag)
    all_quakes = lt.newList("ARRAY_LIST")
    for lstmag in lt.iterator(lst):
        result= me.getValue(om.get(analyzer['temblores_mag'],lstmag))
        tamano=lt.size(result["By_mag"])
        total+=tamano
        diccionario={"mag":lstmag,"Events":tamano,"Details":lt.newList("ARRAY_LIST")}
        detalles=diccionario["Details"]
        ordenada= merg.sort(result["By_mag"],compare_results_list)
        if tamano<6:
            for cada in lt.iterator(ordenada):
                dato=nuevo(cada)
                lt.addLast(detalles,dato)
                lt.addLast(all_quakes, dato)

        else:
            for x in lt.iterator(ordenada):
                lt.addLast(all_quakes, x)
            for b in range(1,4):
                dato = lt.getElement(ordenada, b)
                dato=nuevo(dato)
                lt.addLast(detalles,dato)
            for b in range (0,3):
                dato = lt.getElement(ordenada, (tamano-2+b))
                dato=nuevo(dato)
                lt.addLast(detalles,dato)
        lt.addFirst(lista,diccionario)
    return lista,total, all_quakes
    # TODO: Realizar el requerimiento 2
    
def nuevo(cada):
    fecha = datetime.datetime.strptime(cada["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
    dates = fecha.strftime('%Y-%m-%d %H:%M:%S')
    dato= {"time":dates,"mag":cada["mag"],"lat":cada["lat"],"long":cada["long"],"depth":cada["depth"],"sig":cada["sig"],"gap":cada["gap"],
           "nst":cada["nst"],"title":cada["title"],"cdi":cada["cdi"],"mmi":cada["mmi"],"magType":cada["magType"],"type": cada["type"],"code":cada["code"]}
    return dato
def req_3(data_structs,magnitud,profundidad):
    """
    Función que soluciona el requerimiento 3
    """
    #cambie a float la profundidad carga de datos
    mapa = data_structs["temblores_mag"]
    lista_final= lt.newList("ARRAY_LIST")
    diccionario=om.newMap("RBT")
    maxima_mg = om.maxKey(mapa)
    llaves = om.values(mapa,magnitud,maxima_mg)
    for cada in lt.iterator(llaves):
        mapita=cada["By_depth"]
        minimo_prof= om.minKey(mapita)
        resultado= om.values(mapita,minimo_prof,profundidad)
        for ca in lt.iterator(resultado):
            for temblor in lt.iterator(ca):
                lt.addLast(lista_final,temblor)
                fecha = datetime.datetime.strptime(temblor["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
                dates = fecha.strftime('%Y-%m-%dT%H:%M')
                entry= om.get(diccionario,dates)
                if entry:
                    valor= me.getValue(entry)
                else:
                    valor={"time":dates,"events":0,"details":lt.newList("ARRAY_LIST")}
                    om.put(diccionario,dates,valor)
                lista= valor["details"]
                h= nuevo(temblor)
                lt.addLast(lista,h)
                valor["events"]+=1
    pri= primeros(diccionario)

    return pri, lt.size(lista_final)
    #return pri,lista_final,lt.size(lista_final)


def primeros(mapa):
    lista= lt.newList("SINGLE_LINKED")
    lista_final= om.keySet(mapa)
    de= lt.size(lista_final)
    sublista= lt.subList(lista_final,de-9,10)
    for cada in lt.iterator(sublista):
         result= me.getValue(om.get(mapa,cada))
         lt.addFirst(lista,result)
    return lista
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs, min_sig, max_gap):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    sig_om = data_structs['temblores_sig']
    gap_om = data_structs['temblores_gap']

    results = lt.newList("ARRAY_LIST", cmpfunction=cmp_quakes)

    max_sig = om.maxKey(sig_om)
    sig_keys = om.keys(sig_om, min_sig, max_sig)
    min_gap = om.minKey(gap_om)
    gap_keys = om.keys(gap_om, min_gap, max_gap)

    entries_map = mp.newMap(lt.size(sig_keys)*2.1, 
                            maptype="PROBING", 
                            loadfactor=0.5,
                            cmpfunction=compare_elements)

    dates_map = mp.newMap(lt.size(sig_keys), 
                            maptype="PROBING", 
                            loadfactor=0.5,
                            cmpfunction=compare_elements)
    for key in lt.iterator(sig_keys):
        quakes_list = me.getValue(om.get(sig_om,key))
        for quake in lt.iterator(quakes_list):
            mp.put(entries_map, quake['code'], quake)
    
    for key in lt.iterator(gap_keys):
        quakes_list = me.getValue(om.get(gap_om, key))
        for quake in lt.iterator(quakes_list):
            if mp.contains(entries_map, quake['code']):
                lt.addLast(results, quake)
                if not mp.contains(dates_map, quake['time']):
                    mp.put(dates_map, quake['time'],1)

    merg.sort(results, req4_sort_criteria)
    size = lt.size(results)
    dates = mp.size(dates_map)

    if size>15:
        return_list = lt.subList(results,1,15)
    
    else:
        return_list = results
    
    return return_list, size, dates



def req_5(control, depth_min, min_estaciones_mon ):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    key_max = om.maxKey(control["temblores_depth"])
    lst_rango_depth = om.keys(control['temblores_depth'], depth_min, key_max)
    total = 0
    lst_final = lt.newList("SINGLE_LINKED")
    
    for lst_depth in lt.iterator(lst_rango_depth):
        valores_rango_depth = me.getValue(om.get(control['temblores_depth'],lst_depth))
       
        for cada in lt.iterator(valores_rango_depth['By_depth_lst']): 
           
            estaciones_mon = cada['nst']
            if estaciones_mon == "":
                estaciones_mon = 0
            else:
                estaciones_mon  = float(cada['nst'])
                        
            if estaciones_mon >= min_estaciones_mon:
                total += 1
                lt.addLast(lst_final,cada)
   
    merg.sort(lst_final, compare_results_list)
               
    lista_final_1 =lt.newList("ARRAY_LIST")          
    if lt.size(lst_final) <= 20:
        top_20 = lst_final
    else:
        top_20 = lt.subList(lst_final,1,20)
        
    if lt.size(top_20) < 6: 
        for ele in lt.iterator(top_20):
            d = nuevo(ele)
            lt.addLast(lista_final_1,d)
    else:
        for dato in range(1,4):
            info = lt.getElement(top_20,dato)
            lt.addLast(lista_final_1,info)
    
        for i in range(lt.size(top_20) - 2, lt.size(top_20) + 1): 
            info = lt.getElement(top_20,i)
            lt.addLast(lista_final_1,info)
        
    return lista_final_1, total, top_20
             
def harvesine_formula(lat1, long1, data):
    #Defines the distance between a given point and a seismic event as defined by the Harvesine formula.
    
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    long1 = math.radians(long1)
    lat2 = math.radians(float(data['lat']))
    long2 = math.radians(float(data['long']))

    # Haversine formula
    dlat = lat2 - lat1
    dlong = long2 - long1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlong / 2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Calculate the distance
    distance = R * c

    return distance

def req_6(data_structs,lat, long, radius, n_events, f_year):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    all_q = data_structs['quakes_req6']
    area_q = lt.newList("ARRAY_LIST")

    most_sig= 0
    sig_event = None
    post_events = 0
    pre_events = 0

    delta_ti = mp.newMap(lt.size(area_q)*2.1,
                        maptype="PROBING", 
                        loadfactor=0.5,
                        cmpfunction=compare_elements)

    return_list = lt.newList("ARRAY_LIST")

    for quake in lt.iterator(all_q):
        if quake['time'].year == f_year:
            dist = harvesine_formula(lat,long,quake)
            if dist<=radius:
                if not quake['sig']:
                    quake['sig']=0
                lt.addLast(area_q, quake)
                if float(quake['sig'])>float(most_sig):
                    most_sig = quake['sig']
                    sig_event = quake
    sig_code = sig_event['code']

    for quake in lt.iterator(area_q):
        diff_t = (sig_event['time']-quake['time']).total_seconds()
        mp.put(delta_ti, diff_t,quake)
    
    times_list = lt.newList('ARRAY_LIST')
    for t in lt.iterator(mp.keySet(delta_ti)):
        lt.addLast(times_list,t)
    
    merg.sort(times_list, req6_sort_criteria)

    dates_map = mp.newMap(n_events*4.1, 
                            maptype="PROBING", 
                            loadfactor=0.5,
                            cmpfunction=compare_elements)

    
    for key in lt.iterator(times_list):
        event = me.getValue(mp.get(delta_ti, key))
        if key<0 and pre_events<n_events:
            lt.addLast(return_list, event)
            pre_events+=1
            if not mp.contains(dates_map, event['time']):
                    mp.put(dates_map, event['time'],1)
        elif key>0 and post_events<n_events:
            lt.addLast(return_list, event)
            post_events+=1
            if not mp.contains(dates_map, event['time']):
                    mp.put(dates_map, event['time'],1)
    lt.addLast(return_list, sig_event)
    if not mp.contains(dates_map, sig_event['time']):
                    mp.put(dates_map, sig_event['time'],1)
                    
    merg.sort(return_list, req6_sort_criteria2)
    total_events = lt.size(return_list)
    total_dates = mp.size(dates_map)
    radius_events = lt.size(area_q)

    return return_list, post_events, pre_events, total_events, total_dates, sig_code, sig_event, radius_events


def req_7(data_structs,año, titulo, condicion, bins):
    """
    Función que soluciona el requerimiento 7
    """
    #crear nuevo mapa
    #funcion de agregar
    #añadir data
    #llamar la funcion en carga de datos

    mapa= data_structs["By_year"]
    result= me.getValue(om.get(mapa,año))
    mapa_de_lacondicon= om.newMap(omaptype='RBT',
                                      cmpfunction=compareDates)
    mapa_data= om.newMap(omaptype='RBT',
                                      cmpfunction=compareDates)
    diccionario ={}
    titulos = om.keySet(result["arbol"])
    cantidad_año= lt.size(result["lista"])
    totales=0
    total_list = lt.newList("ARRAY_LIST")
    for cada in lt.iterator(titulos):
        if titulo in cada:
            lisat_condicion= me.getValue(om.get(result["arbol"],cada))
            for data in lt.iterator(lisat_condicion):
                totales+=1
                lt.addLast(total_list,data)
                if not data[condicion]=="" and not data[condicion]==0:
                    mapa_data=uptime(mapa_data,data)
                    mapa_de_lacondicon= add_data_req_condicion(mapa_de_lacondicon, float(data[condicion]))
                    if float(data[condicion]) in diccionario:
                        diccionario[float(data[condicion])]+=1
                    else:
                        diccionario[float(data[condicion])]=1
    minimo = om.minKey(mapa_de_lacondicon)
    maximo= om.maxKey(mapa_de_lacondicon)
    usados = 0
    for cada in lt.iterator(om.valueSet(mapa_de_lacondicon)):
        usados+= int(cada)
    lista=sacas(mapa_data, condicion)
    return diccionario, totales,cantidad_año, usados,minimo, maximo,lista, total_list

def sacas(mapa, condicion):
    llaves= om.valueSet(mapa)
    lista= lt.newList("ARRAY_LIST")
    for cada in lt.iterator(llaves): 
        for evento in lt.iterator(cada['By_time']):
            fecha = datetime.datetime.strptime(evento["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
            dates = fecha.strftime('%Y-%m-%dT%H:%M')
            entrada= {"time":dates,"lat":round(float(evento["lat"]),3),"long":round(float(evento["long"]),3),"title":evento["title"],"code":evento["code"], condicion:evento[condicion]}
            lt.addLast(lista, entrada)
    return lista
                

            


    # TODO: Realizar el requerimiento 7
    pass
def agregar_req_7(mapa,data):
    occurreddate = data['time']
    fecha = datetime.datetime.strptime(occurreddate, "%Y-%m-%dT%H:%M:%S.%fZ")
    dates = fecha.strftime('%Y')
    entry = om.get(mapa, dates)
    if entry is None:
        datentry = {"lista":lt.newList("ARRAY_LIST"),"arbol":om.newMap(omaptype='RBT',
                                      cmpfunction=compareDates)}
        om.put(mapa, dates, datentry)
    else:
        datentry = me.getValue(entry)
    add_data_req_7(datentry,data)
    lt.addLast(datentry["lista"],data)
    return mapa

def add_data_req_7(structs,data):
    mapa= structs["arbol"]
    entry= om.get(mapa,(data["title"]))
    if entry:
        lista= me.getValue(entry)
    else:
        lista= lt.newList("ARRAY_LIST")
        om.put(mapa,(data["title"]),lista)
    lt.addLast(lista,data)
    return structs

def add_data_req_condicion(structs,llave):
    mapa= structs
    llave= round(llave,3)
    entry= om.get(mapa,llave)
    if entry:
        lista= int(me.getValue(entry))
    else:
        lista= 0
    lista+=1
    om.put(mapa,llave,lista)
    return structs

def add_data_req_condicion_data(structs,data, llave):
    mapa= structs
    llave= round(llave,3)
    entry= om.get(mapa,llave)
    if entry:
        lista= (me.getValue(entry))
    else:
        lista= lt.newList("ARRAY_LIST")
        om.put(mapa,llave,lista)
    lt.addLast(lista,data)
    return structs


def req_8(data_structs, req, list_result=None, lat=0, long=0, radius=0):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    props = 0
    if req=='0':
        try:
            m= folium.Map(tiles=MAP_TILE, 
                        attr=MAP_ATTRIBUTES)
            mCluster = MarkerCluster(name="Cluster").add_to(m)
            path = '.\\Data\\maps\\req0.html'
            for result in lt.iterator(data_structs['lista_temblores']):
                mssg=''
                for key in result:
                    mssg += f'{key}: {result[key]}\n'
                folium.Marker(location=[float(result['lat']),float(result['long'])],
                            tooltip= html.escape(result['title']).replace('`','&#96;'),
                            popup=Popup(mssg,parse_html=True)).add_to(mCluster)
                props+=1
                if props>MAX_MAP_PROPS:
                    break
            folium.LayerControl().add_to(m)
            m.save(path)
            os.system(f'start {path}')
        except Exception as e:
            print('Ocurrió un error con el mapa. Mostrando textura por defecto.')
            m= folium.Map()
            mCluster = MarkerCluster(name="Cluster").add_to(m)
            path = '.\\Data\\maps\\req0.html'
            for result in lt.iterator(data_structs['lista_temblores']):
                mssg=''
                for key in result:
                    mssg += f'{key}: {result[key]}\n'
                folium.Marker(location=[float(result['lat']),float(result['long'])],
                            tooltip= html.escape(result['title']).replace('`','&#96;'),
                            popup=Popup(mssg,parse_html=True)).add_to(mCluster)
                props+=1
                if props>MAX_MAP_PROPS:
                    break
            folium.LayerControl().add_to(m)
            m.save(path)
            os.system(f'start {path}')

    elif req=='1':
        try:
            m= folium.Map(tiles=MAP_TILE, 
                        attr=MAP_ATTRIBUTES)
            mCluster = MarkerCluster(name="Cluster").add_to(m)
            path = '.\\Data\\maps\\req1.html'
            for result in lt.iterator(list_result):
                mssg=''
                for key in result:
                    mssg += f'{key}: {result[key]}\n'
                folium.Marker(location=[float(result['lat']),float(result['long'])],
                            tooltip= html.escape(result['title']).replace('`','&#96;'),
                            popup=Popup(mssg,parse_html=True)).add_to(mCluster)
                props+=1
                if props>MAX_MAP_PROPS:
                    break
            folium.LayerControl().add_to(m)
            m.save(path)
            os.system(f'start {path}')
        except Exception as e:
            print('Ocurrió un error con el mapa. Mostrando textura por defecto.')
            m= folium.Map()
            mCluster = MarkerCluster(name="Cluster").add_to(m)
            path = '.\\Data\\maps\\req4.html'
            for result in lt.iterator(list_result):
                mssg=''
                for key in result:
                    mssg += f'{key}: {result[key]}\n'
                folium.Marker(location=[float(result['lat']),float(result['long'])],
                            tooltip= html.escape(result['title']).replace('`','&#96;'),
                            popup=Popup(mssg,parse_html=True)).add_to(mCluster)
                props+=1
                if props>MAX_MAP_PROPS:
                    break
            folium.LayerControl().add_to(m)
            m.save(path)
            os.system(f'start {path}') 
    
    elif req=='2':
        try:
            m= folium.Map(tiles=MAP_TILE, 
                        attr=MAP_ATTRIBUTES)
            mCluster = MarkerCluster(name="Cluster").add_to(m)
            path = '.\\Data\\maps\\req2.html'
            for result in lt.iterator(list_result):
                mssg=''
                for key in result:
                    mssg += f'{key}: {result[key]}\n'
                folium.Marker(location=[float(result['lat']),float(result['long'])],
                            tooltip= html.escape(result['title']).replace('`','&#96;'),
                            popup=Popup(mssg,parse_html=True)).add_to(mCluster)
                props+=1
                if props>MAX_MAP_PROPS:
                    break
            folium.LayerControl().add_to(m)
            m.save(path)
            os.system(f'start {path}')
        except Exception as e:
            print('Ocurrió un error con el mapa. Mostrando textura por defecto.')
            m= folium.Map()
            mCluster = MarkerCluster(name="Cluster").add_to(m)
            path = '.\\Data\\maps\\req4.html'
            for result in lt.iterator(list_result):
                mssg=''
                for key in result:
                    mssg += f'{key}: {result[key]}\n'
                folium.Marker(location=[float(result['lat']),float(result['long'])],
                            tooltip= html.escape(result['title']).replace('`','&#96;'),
                            popup=Popup(mssg,parse_html=True)).add_to(mCluster)
                props+=1
                if props>MAX_MAP_PROPS:
                    break
            folium.LayerControl().add_to(m)
            m.save(path)
            os.system(f'start {path}') 

    elif req=='3':
        try:
            m= folium.Map(tiles=MAP_TILE, 
                        attr=MAP_ATTRIBUTES)
            mCluster = MarkerCluster(name="Cluster").add_to(m)
            path = '.\\Data\\maps\\req3.html'
            for result in lt.iterator(list_result):
                mssg=''
                for key in result:
                    mssg += f'{key}: {result[key]}\n'
                folium.Marker(location=[float(result['lat']),float(result['long'])],
                            tooltip= html.escape(result['title']).replace('`','&#96;'),
                            popup=Popup(mssg,parse_html=True)).add_to(mCluster)
                props+=1
                if props>MAX_MAP_PROPS:
                    break
            folium.LayerControl().add_to(m)
            m.save(path)
            os.system(f'start {path}')
        except Exception as e:
            print('Ocurrió un error con el mapa. Mostrando textura por defecto.')
            m= folium.Map()
            mCluster = MarkerCluster(name="Cluster").add_to(m)
            path = '.\\Data\\maps\\req4.html'
            for result in lt.iterator(list_result):
                mssg=''
                for key in result:
                    mssg += f'{key}: {result[key]}\n'
                folium.Marker(location=[float(result['lat']),float(result['long'])],
                            tooltip= html.escape(result['title']).replace('`','&#96;'),
                            popup=Popup(mssg,parse_html=True)).add_to(mCluster)
                props+=1
                if props>MAX_MAP_PROPS:
                    break
            folium.LayerControl().add_to(m)
            m.save(path)
            os.system(f'start {path}') 

    elif req=='4':
        try:
            m= folium.Map(tiles=MAP_TILE, 
                        attr=MAP_ATTRIBUTES)
            mCluster = MarkerCluster(name="Cluster").add_to(m)
            path = '.\\Data\\maps\\req4.html'
            for result in lt.iterator(list_result):
                mssg=''
                for key in result:
                    mssg += f'{key}: {result[key]}\n'
                folium.Marker(location=[float(result['lat']),float(result['long'])],
                            tooltip= html.escape(result['title']).replace('`','&#96;'),
                            popup=Popup(mssg,parse_html=True)).add_to(mCluster)
                props+=1
                if props>MAX_MAP_PROPS:
                    break
            folium.LayerControl().add_to(m)
            m.save(path)
            os.system(f'start {path}')
        except Exception as e:
            print('Ocurrió un error con el mapa. Mostrando textura por defecto.')
            m= folium.Map()
            mCluster = MarkerCluster(name="Cluster").add_to(m)
            path = '.\\Data\\maps\\req4.html'
            for result in lt.iterator(list_result):
                mssg=''
                for key in result:
                    mssg += f'{key}: {result[key]}\n'
                folium.Marker(location=[float(result['lat']),float(result['long'])],
                            tooltip= html.escape(result['title']).replace('`','&#96;'),
                            popup=Popup(mssg,parse_html=True)).add_to(mCluster)
                props+=1
                if props>MAX_MAP_PROPS:
                    break
            folium.LayerControl().add_to(m)
            m.save(path)
            os.system(f'start {path}')

    elif req=='5':
        try:
            m= folium.Map(tiles=MAP_TILE, 
                        attr=MAP_ATTRIBUTES)
            mCluster = MarkerCluster(name="Cluster").add_to(m)
            path = '.\\Data\\maps\\req5.html'
            for result in lt.iterator(list_result):
                mssg=''
                for key in result:
                    mssg += f'{key}: {result[key]}\n'
                folium.Marker(location=[float(result['lat']),float(result['long'])],
                            tooltip= html.escape(result['title']).replace('`','&#96;'),
                            popup=Popup(mssg,parse_html=True)).add_to(mCluster)
                props+=1
                if props>MAX_MAP_PROPS:
                    break
            folium.LayerControl().add_to(m)
            m.save(path)
            os.system(f'start {path}')
        except Exception as e:
            print('Ocurrió un error con el mapa. Mostrando textura por defecto.')
            m= folium.Map()
            mCluster = MarkerCluster(name="Cluster").add_to(m)
            path = '.\\Data\\maps\\req5.html'
            for result in lt.iterator(list_result):
                mssg=''
                for key in result:
                    mssg += f'{key}: {result[key]}\n'
                folium.Marker(location=[float(result['lat']),float(result['long'])],
                            tooltip= html.escape(result['title']).replace('`','&#96;'),
                            popup=Popup(mssg,parse_html=True)).add_to(mCluster)
                props+=1
                if props>MAX_MAP_PROPS:
                    break
            folium.LayerControl().add_to(m)
            m.save(path)
            os.system(f'start {path}')

    elif req=='6':
        try:
            m= folium.Map(tiles=MAP_TILE, 
                        attr= MAP_ATTRIBUTES)
            mCluster = MarkerCluster(name="Cluster").add_to(m)
            path = '.\\Data\\maps\\req6.html'
            for result in lt.iterator(list_result):
                mssg=''
                for key in result:
                    mssg += f'{key}: {result[key]}\n'
                folium.Marker(location=[float(result['lat']),float(result['long'])],
                            tooltip= html.escape(result['title']).replace('`','&#96;'),
                            popup=Popup(mssg,parse_html=True)).add_to(mCluster)
                props+=1
                if props>MAX_MAP_PROPS:
                    break
            folium.LayerControl().add_to(m)
            circle = folium.Circle(location=[lat, long],
                                radius=radius*1000,
                                color='orange',
                                fill=True,
                                fill_color='orange',
                                fill_opacity=0.2)
            circle.add_to(m)
            m.save(path)
            os.system(f'start {path}')
        except Exception as e:
            print(f'An error occured. Check your internet connection \n')
            m= folium.Map()
            mCluster = MarkerCluster(name="Cluster").add_to(m)
            path = '.\\Data\\maps\\req6.html'
            for result in lt.iterator(list_result):
                mssg=''
                for key in result:
                    mssg += f'{key}: {result[key]}\n'
                folium.Marker(location=[float(result['lat']),float(result['long'])],
                            tooltip= html.escape(result['title']).replace('`','&#96;'),
                            popup=Popup(mssg,parse_html=True)).add_to(mCluster)
                props+=1
                if props>MAX_MAP_PROPS:
                    break
            folium.LayerControl().add_to(m)
            circle = folium.Circle(location=[lat, long],
                                radius=radius*1000,
                                color='orange',
                                fill=True,
                                fill_color='orange',
                                fill_opacity=0.2)
            circle.add_to(m)
            m.save(path)
            os.system(f'start {path}')

    elif req=='7':
        try:
            m= folium.Map(tiles=MAP_TILE, 
                        attr=MAP_ATTRIBUTES)
            mCluster = MarkerCluster(name="Cluster").add_to(m)
            path = '.\\Data\\maps\\req7.html'
            for result in lt.iterator(list_result):
                mssg=''
                for key in result:
                    mssg += f'{key}: {result[key]}\n'
                folium.Marker(location=[float(result['lat']),float(result['long'])],
                            tooltip= html.escape(result['title']).replace('`','&#96;'),
                            popup=Popup(mssg,parse_html=True)).add_to(mCluster)
                props+=1
                if props>MAX_MAP_PROPS:
                    break
            folium.LayerControl().add_to(m)
            m.save(path)
            os.system(f'start {path}')
        except Exception as e:
            print('Ocurrió un error con el mapa. Mostrando textura por defecto.')
            m= folium.Map()
            mCluster = MarkerCluster(name="Cluster").add_to(m)
            path = '.\\Data\\maps\\req7.html'
            for result in lt.iterator(list_result):
                mssg=''
                for key in result:
                    mssg += f'{key}: {result[key]}\n'
                folium.Marker(location=[float(result['lat']),float(result['long'])],
                            tooltip= html.escape(result['title']).replace('`','&#96;'),
                            popup=Popup(mssg,parse_html=True)).add_to(mCluster)
                props+=1
                if props>MAX_MAP_PROPS:
                    break
            folium.LayerControl().add_to(m)
            m.save(path)
            os.system(f'start {path}')
# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    if data_1 == data_2:
        return 0
    elif data_1>data_2:
        return 1
    return -1

def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareFloats(data1, data2):

    if (float(data1) == float(data2)):
        return 0
    elif (float(data1) > float(data2)):
        return 1
    else:
        return -1
# Funciones de ordenamiento
    

def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass
def compare_results_list(data1, data2):
    fecha1= datetime.datetime.strptime(data1['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
    date_1 = fecha1.strftime('%Y-%m-%d %H:%M:%S')
    fecha2= datetime.datetime.strptime(data2['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
    date_2 = fecha2.strftime('%Y-%m-%d %H:%M:%S')
    if fecha1>fecha2:
        return True
    else :
        return False

def cmp_quakes(data1, data2):
    if data1['code']==data2['code']:
        return 0
    elif data1['code']>data2['code']:
        return 1
    else:
        return -1
    
def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass

def req4_sort_criteria(data1, data2):
    date1=data1['time']
    date2=data2['time']
    if date1>date2:
        return True
    return False

def req6_sort_criteria(data1, data2):
    if abs(data1)<abs(data2):
        return True
    return False

def req6_sort_criteria2(data1, data2):
    if data1['time']<data2['time']:
        return True
    else:
        return False