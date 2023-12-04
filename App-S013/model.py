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

from tabulate import tabulate
import config as cf
from math import radians, cos, sin, asin, sqrt
from datetime import datetime , timedelta , date
import matplotlib.pyplot as plt
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import bst as bs
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf
from tabulate import tabulate
import pro as pr 
import folium
from folium.plugins import MarkerCluster
import webbrowser
import os

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

    data_struct ={"mag": None,"bydate": None, "depth":None, "earthquakes": None}

    data_struct["earthquakes"]=lt.newList("ARRAY_LIST")
    data_struct['mag'] = om.newMap(omaptype='RBT',cmpfunction=compareFunction)
    data_struct['bydate'] = om.newMap(omaptype='RBT',cmpfunction=compare_dates)
    data_struct["depth"]= om.newMap(omaptype='RBT',cmpfunction=compareFunction)
    data_struct["bydate1"]= om.newMap(omaptype='RBT',cmpfunction=comparef)
    return data_struct


# Funciones para agregar informacion al modelo
def adddatabydate1(data_struct, data):
    if om.contains(data_struct, data["time"])==False:
        nueva=lt.newList("ARRAY_LIST")
        lt.addLast(nueva, data)
        om.put(data_struct, data["time"], nueva)
    elif om.contains(data_struct, data["time"]):
        valor=me.getValue(om.get(data_struct, data["time"]))
        lt.addLast(valor,data)
        om.put(data_struct, data["time"], valor)
    return data_struct

def adddatabydate(data_struct, data):
    if om.contains(data_struct, data["time"])==False:
        nueva=lt.newList("ARRAY_LIST")
        lt.addLast(nueva, data)
        om.put(data_struct, data["time"], nueva)
    elif om.contains(data_struct, data["time"]):
        valor=me.getValue(om.get(data_struct, data["time"]))
        lt.addLast(valor,data)
        om.put(data_struct, data["time"], valor)
    return data_struct

def adddatamag(data_struct,data):
    lt.addLast(data_struct["earthquakes"], data)
    datastructure = data_struct["mag"]
    if om.contains(datastructure, data["mag"])==False:
        nueva=lt.newList("ARRAY_LIST")
        lt.addLast(nueva, data)
        om.put(datastructure, data["mag"], nueva)
    elif om.contains(datastructure, data["mag"]):
        valor=me.getValue(om.get(datastructure, data["mag"]))
        lt.addLast(valor,data)
        om.put(datastructure, data["mag"], valor)
    return data_struct

def adddatadepth(data_struct,data):
    if om.contains(data_struct, data["depth"])==False:
        nueva=lt.newList("ARRAY_LIST")
        lt.addLast(nueva, data)
        om.put(data_struct, data["depth"], nueva)
    elif om.contains(data_struct, data["depth"]):
        valor=me.getValue(om.get(data_struct, data["depth"]))
        lt.addLast(valor,data)
        om.put(data_struct, data["depth"], valor)
    return data_struct


   

# Funciones para creacion de datos

def add_data(datastructure, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    lt.addLast(datastructure, data)
    
    return datastructure   

def newSublist(list, position, size):
    return lt.subList(list, position, size)


def mergelist(list1, list2):

    mergedList = lt.newList('ARRAY_LIST')

    for i in range(lt.size(list1)):
        add_data(mergedList, lt.getElement(list1, i))

    for i in range(lt.size(list2)):
        add_data(mergedList, lt.getElement(list2, i))

    return mergedList

# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    return lt.getElement(data_structs, id)


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    return lt.size(data_structs)


def req_1(data_structs, initialDate, finalDate):
    """
    Función que soluciona el requerimiento 1
    """
    ini=initialDate+":00.000Z"
    fin=finalDate+":59.999Z"
    llaves= bs.keys(data_structs, ini, fin)
    lst = om.values(data_structs, ini, fin)
    map = folium.Map(location=[0, 0], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(map)

    llavesImp=["mag","lat","long","depth","sig","gap","nst","title", "cdi","mmi","magType","type","code"]
    if lt.size(llaves) !=0:
        tabulat=[]
        if lt.size(llaves) > 6:
            firstMatches = newSublist(llaves, 1, 3)
            lastMatches = newSublist(llaves, int(lt.size(llaves)) - 2, 3)
            sampleMatches = mergelists(firstMatches, lastMatches)
            for llave in lt.iterator(sampleMatches):
                value=sacar_informacion(data_structs,llave)
                retorno=dicinformacion(value,llavesImp)
                tabla=tabulate(retorno, headers="keys", tablefmt="fancy_grid",maxcolwidths=[None,None,5, None,9,7,13,6,5,None,6,7,17], showindex=False)
                fi={"Time":llave, "events":len(retorno),"details":tabla}
                tabulat.append(fi)
        else:
            for llave in lt.iterator(llaves):
                value=sacar_informacion(data_structs,llave)
                retorno=dicinformacion(value,llavesImp)
                tabla=tabulate(retorno, headers="keys", tablefmt="fancy_grid",maxcolwidths=[None,None,5, None,9,7,13,6,5,None,6,7,17], showindex=False)
                fi={"Time":llave, "events":len(retorno),"details":retorno}
                tabulat.append(fi)

        for event_list in lt.iterator(lst):
            for event in lt.iterator(event_list):
                coords = [event['lat'], event['long']]
                info = str(event) 

                folium.Marker(location=coords, popup=info).add_to(marker_cluster)
    
        map_file = cf.maps_path + "/req1.html"
        map.save(map_file)
        
    else: 
        return None
    return tabulat, lt.size(llaves)


def req_2(data_structs, initialmag, finalmag):
    """
    Función que soluciona el requerimiento 2
    """
    llavesImp=["time","lat","long","depth","sig","gap","nst","title", "cdi","mmi","magType","type","code"]
    llaves= bs.keys(data_structs, initialmag, finalmag)
    map = folium.Map(location=[0, 0], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(map)
    lst = om.values(data_structs, initialmag, finalmag)
    event=0
    if lt.size(llaves) !=0:
        tabulat=[]
        if lt.size(llaves) > 6:
            firstMatches = newSublist(llaves, 1, 3)
            lastMatches = newSublist(llaves, int(lt.size(llaves)) - 2, 3)
            sampleMatches = mergelists(firstMatches, lastMatches)
            for llave in lt.iterator(sampleMatches):
                value=sacar_informacion(data_structs,llave)
                retorno=dicinformacion(value,llavesImp)
                tabla=tabulate(retorno, headers="keys", tablefmt="fancy_grid",maxcolwidths=[None,None,5, None,9,7,13,6,5,None,6,7,17], showindex=False)
                fi={"mag":llave, "events":len(retorno),"details":tabla}
                tabulat.append(fi)
                event+=len(retorno)
        else:
            for llave in lt.iterator(llaves):
                value=sacar_informacion(data_structs,llave)
                retorno=dicinformacion(value,llavesImp)
                tabla=tabulate(retorno, headers="keys", tablefmt="fancy_grid",maxcolwidths=[None,None,5, None,9,7,13,6,5,None,6,7,17], showindex=False)
                fi={"mag":llave, "events":len(retorno),"details":retorno}
                tabulat.append(fi)
                event+=len(retorno)

        for event_list in lt.iterator(lst):
            for event in lt.iterator(event_list):
                coords = [event['lat'], event['long']]
                info = str(event) 
    
                folium.Marker(location=coords, popup=info).add_to(marker_cluster)
    
        map_file = cf.maps_path + "/req2.html"
        map.save(map_file)
        
    else: 
        return None
    return tabulat,event


def req_3(data_structs, mag, prof):
    
    """
    Función que soluciona el requerimiento 3
    magnitud minima osea revisar los mayores
    profundidad maxima no superable
    """
    llavesImp=["mag","lat","long","depth","sig","gap","nst","title", "cdi","mmi","magType","type","code"]
    profundidad=data_structs["depth"]
    magnitud=data_structs["mag"]
    maxMag=bs.maxKey(magnitud)
    minpro=bs.minKey(profundidad)
    listmag=bs.keys(magnitud,mag, maxMag)
    listapro=bs.keys(profundidad, minpro, prof)
    lst = om.values(data_structs["depth"], float(mag)+0.1, maxMag)
    map = folium.Map(location=[0, 0], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(map)
    mapdata = lt.newList('ARRAY_LIST')
    for lstdepth in lt.iterator(lst):
        for item in lt.iterator(lstdepth):
            if item["depth"] == "" or item["depth"] == None:
                continue
            elif float(item["depth"]) <= float(prof)-0.1:
                lt.addLast(mapdata, item)

    if lt.size(listmag) != 0 and lt.size(listapro) !=0:
        tabulat=[]
        iguales, magi, profe=encontrar_semejantes(listmag,listapro, magnitud)
        if lt.size(iguales)>10:
            lastMatches = newSublist(iguales, int(lt.size(iguales)) - 10, 10)
            for fecha in lt.iterator(lastMatches):
                val=sacar_informacionre3(data_structs["bydate"], fecha)
                retorno=dicinformacion_req3(val,llavesImp,magi, profe)
                tabla=tabulate(retorno, headers="keys", tablefmt="fancy_grid",maxcolwidths=[None,None,5, None,9,7,13,6,5,None,6,7,17], showindex=False)
                fi={"Time":fecha, "events":len(retorno),"details":tabla}
                tabulat.append(fi)
        else:
            for fecha in lt.iterator(iguales):
                val=sacar_informacionre3(data_structs["bydate1"], fecha)
                retorno=dicinformacion_req3(val,llavesImp,magi, profe)
                tabla=tabulate(retorno, headers="keys", tablefmt="fancy_grid",maxcolwidths=[None,None,5, None,9,7,13,6,5,None,6,7,17], showindex=False)
                fi={"Time":fecha, "events":len(retorno),"details":retorno}
                tabulat.append(fi)

        for event in lt.iterator(mapdata):
            coords = [event['lat'], event['long']]
            info = str(event) 

            folium.Marker(location=coords, popup=info).add_to(marker_cluster)
    
        map_file = cf.maps_path + "/req3.html"
        map.save(map_file)
    else:
        return None
    return tabulat

def req_4_v1(data_structs, sig, gap):
    """
    Función que soluciona el requerimiento 4
    """
    seismic_events = data_structs['earthquakes']
    filtered_events = om.newMap(omaptype='RBT',
                                comparefunction= comparedates)

    for event in lt.iterator(seismic_events):
        if event['sig'] > sig and event['gap'] < gap:
            date = event['time'].split("T")[0]
            if om.contains(filtered_events, date):
                date_events = om.get(filtered_events, date)['value']
            else:
                date_events = lt.newList('ARRAY_LIST')
                om.put(filtered_events, date, date_events)
            lt.addLast(date_events, event)

    sorted_dates = merg.sort(om.keySet(filtered_events), comparedates)
    recent_dates = lt.subList(sorted_dates, lt.size(sorted_dates) - 14, 15)

    recent_events = lt.newList('ARRAY_LIST')
    for date in lt.iterator(recent_dates):
        date_events = om.get(filtered_events, date)['value']
        for event in lt.iterator(date_events):
            lt.addLast(recent_events, event)

    return recent_events

    
    

def req_5(data_structs, depth, nst, consultnum):
    """
    Función que soluciona el requerimiento 5
    """
    data = lt.newList("ARRAY_LIST")
    maxdepth = om.maxKey(data_structs["depth"])
    lst = om.values(data_structs["depth"], depth, maxdepth)
    totalevents = 0
    map = folium.Map(location=[0, 0], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(map)
    full = lt.newList("ARRAY_LIST")

    if lst == None:
        return None

    for lstdepth in lt.iterator(lst):
        for item in lt.iterator(lstdepth):
            dic = {"time": None, "events": None, "details": []}
            innerdic = {}
            if item["nst"] == "" or item["nst"] == None:
                item["nst"] = 1
            if float(item["nst"]) >= nst:
                lt.addLast(full, item)
                if dic["time"] == None:
                    dic["time"] = item["time"][:16]
                    dic["events"] = 1
                    totalevents += 1
                    innerdic = {"mag": item["mag"], "lat": item["lat"], "long": item["long"], "depth": item["depth"], "sig": item["sig"], 
                                "gap": item["gap"], "nst": item["nst"], "title": item["title"], "cdi": item["cdi"], "mmi": item["mmi"], 
                                "magType": item["magType"], "type": item["type"], "code": item["code"]}
                    dic["details"].append(innerdic)
                    lt.addLast(data, dic)
                else:
                    dic["events"] += 1
                    totalevents += 1
                    innerdic = {"mag": item["mag"], "lat": item["lat"], "long": item["long"], "depth": item["depth"], "sig": item["sig"], 
                                "gap": item["gap"], "nst": item["nst"], "title": item["title"], "cdi": item["cdi"], "mmi": item["mmi"], 
                                "magType": item["magType"], "type": item["type"], "code": item["code"]}
                    dic["details"].append(innerdic)
                    lt.addLast(data, dic)

    sort_time(data)

    # Se mira si el tamaño de el array es mayor al solicitado, si lo es se toman los ultimos x datos pedidos
    if int(lt.size(data)) > consultnum:
        selectedData = newSublist(data, int(lt.size(data)) - consultnum + 1, consultnum)
        mapdata = newSublist(full, int(lt.size(data)) - consultnum + 1, consultnum)
    else:
        selectedData = data
        mapdata = full

    for event in lt.iterator(mapdata):
        coords = [event['lat'], event['long']]
        info = str(event) 

        folium.Marker(location=coords, popup=info).add_to(marker_cluster)
    
    map_file = cf.maps_path + "/req5.html"
    map.save(map_file)

    # Conversión a lista de python para tabulate
    finaldata = []
    if lt.size(selectedData) > 6:
        first3 = newSublist(selectedData, 1, 3)
        last3 = newSublist(selectedData, int(lt.size(selectedData)) - 2, 3)
        sampleData = mergelists(first3, last3)
        for item in lt.iterator(sampleData):
            newdetails = tabulate(item["details"], headers="keys", tablefmt="fancy_grid")
            item["details"] = newdetails
            finaldata.append(item)   
    else:    
        for item in lt.iterator(data):
            newdetails = tabulate(item["details"], headers="keys", tablefmt="fancy_grid")
            item["details"] = newdetails
            finaldata.append(item)

    return lt.size(data), totalevents, finaldata


def req_6(data_structs, year, ref_lat, ref_long, radius, N):
    """
    Función que soluciona el requerimiento 6
    """
    
    year_events = lt.newList('ARRAY_LIST')
    area_events = om.newMap('RBT')
    
    # Filter events by year and distance
    
    for y_event in lt.iterator(data_structs["earthquakes"]):
        if datetime.strptime(y_event['time'], '%Y-%m-%dT%H:%M:%S.%fZ').year == year:
            lt.addLast(year_events, year)
    
    for a_event in lt.iterator(data_structs["earthquakes"]):
        if harvesine_equation((ref_long, ref_lat, a_event['long'], a_event['lat']) <= radius):
            om.put(area_events, radius, a_event["lat"] )
        
        
    most_sig_event = om.maxKey(area_events)
    sort_events = merg.sort(year_events, compare_dates)
    
    
    
    closest_events = sort_events[om.maxKey( most_sig_event - N)]
    

    return most_sig_event, om.size(area_events), closest_events
    
    
    


def req_7(data_structs, year, area, property):
    """
    Función que soluciona el requerimiento 7
    """
    minkey = year + "-01-01T00:00:00.000Z"
    maxkey = year + "-12-31T23:59:59.999Z"
    lst = om.values(data_structs["bydate"], minkey, maxkey)
    map = folium.Map(location=[0, 0], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(map)
    full = lt.newList("ARRAY_LIST")
    
    if lst is None:
        return None

    filtered_events = []
    property_values = []
    for event_list in lt.iterator(lst):
        for event in lt.iterator(event_list):
            if area in event['place'] and event[property] != "":
                lt.addLast(full, event)
                filtered_events.append(event)
                property_values.append(event[property])

    for event in lt.iterator(full):
        coords = [event['lat'], event['long']]
        info = str(event) 

        folium.Marker(location=coords, popup=info).add_to(marker_cluster)

    map_file = cf.maps_path + "/req7.html"
    map.save(map_file)

    sorted_values = sorted(property_values)
    sorted_values = [float(value) for value in sorted_values]

    min_property_value = min(property_values)
    max_property_value = max(property_values)

    sorted_events = sorted(filtered_events, key=lambda event: event["time"])
    first_3 = sorted_events[:3]
    last_3 = sorted_events[-3:]
    finalevents = first_3 + last_3

    histogram_events = []
    for event in finalevents:
        histogram_event = {
            'time': event['time'],
            'lat': event['lat'],
            'long': event['long'],
            'title': event['title'],
            'code': event['code'],
            property: event[property]
        }
        histogram_events.append(histogram_event)

    return len(lst), len(histogram_events), min_property_value, max_property_value, sorted_values, histogram_events


def req_8():
    """
    Función que soluciona el requerimiento 8
    """
    map_files = ['req1.html', 'req2.html', 'req3.html', 'req4.html', 'req5.html', 'req6.html', 'req7.html']

    for map_file in map_files:
        
        full_path = os.path.join(cf.maps_path, map_file)

        if os.path.exists(full_path):
            webbrowser.open_new_tab(full_path)
        else:
            print(f"El archivo {full_path} no existe, se ha saltado.")


# Funciones utilizadas para comparar elementos dentro de una lista

def mergelists(list1, list2):

    mergedList = lt.newList('ARRAY_LIST')

    for i in lt.iterator(list1):
        lt.addFirst(mergedList, i)

    for i in lt.iterator(list2):
        lt.addFirst(mergedList, i)

    return mergedList

def sacar_informacion(data, llave):
    value=me.getValue(om.get(data, llave))
    final=value["elements"]
    sampleMatches = 0
    nueva=volverlista(final)
    if lt.size(nueva) >6:
        firstMatches = newSublist(nueva, 1, 3)
        lastMatches = newSublist(nueva, int(lt.size(nueva)) - 2, 3)
        sampleMatches = mergelists(firstMatches, lastMatches)
    else:
        sampleMatches=nueva

    return sampleMatches 

def sacar_informacionre3(data, llave):
    value=me.getValue(om.get(data, llave))
    final=value["elements"]

    return final
def volverlista(lista):
    nueva=lt.newList("ARRAY_LIST")
    for i in lista:
        lt.addLast(nueva, i)
    return nueva


def encontrar_semejantes(lista1, lista2, data1,):
    final=lt.newList("ARRAY_LIST")
    mag=[]
    prof=[]
    sort1=merg.sort(lista1,sort)
    sort2=merg.sort(lista2,sort)
    print(sort1)
    for cada in lt.iterator(sort1):
        val=me.getValue(om.get(data1, cada))
        valeu=val["elements"]
        for i in valeu:
            dat=i["depth"]
            if dat in lt.iterator(sort2):
                di=i["time"]
                print(di)
                if di not in final:
                    lt.addLast(final,di)
                    mag.append(cada)
                    prof.append(dat)
    var=merg.sort(final,compare_dates)
    return var, mag, prof

def newSublist(list, position, size):
    return lt.subList(list, position, size)

def dicinformacion(lista, llaves):
    list=[]
    for cada in lt.iterator(lista):
        dicf={}
        for llave in llaves:
            if llave in cada.keys():
                if cada[llave]!= "":
                    dicf[llave]=cada[llave]
                else:
                    dicf[llave]="Unknow"
        list.append(dicf)
    return list

def dicinformacion_req3(lista, llaves,mag, prof):
    list=[]
    for cada in lista:
        dicf={}
        if cada["mag"] in mag and cada["depth"] in prof:
            for llave in llaves:
                if llave in cada.keys():
                    if cada[llave]!= "":
                        dicf[llave]=cada[llave]
                else:
                    dicf[llave]="Unknow"
        list.append(dicf)
    return list

def comparef(key_1, key_2):
    """
    Función encargada de comparar dos llaves para una mapa ordenado.
    args: key_1: Llave 1
            key_2: Llave 2
    return: 1 si key_1 es mayor que key_2
    """
    if (key_1 == key_2):
        return 0
    elif (key_1 > key_2):
        return 1
    else:
        return -1

def compareFunction(key_1, key_2):
    """
    Función encargada de comparar dos llaves para una mapa ordenado.
    args: key_1: Llave 1
            key_2: Llave 2
    return: 1 si key_1 es mayor que key_2
    """
    key_1 = float(key_1)
    key_2 = float(key_2)
    
    
    if (key_1 == key_2):
        return 0
    elif (key_1 > key_2):
        return 1
    else:
        return -1
        
        
def compareNorm(key_1, key_2):
    
    if (key_1 == key_2):
        return 0
    elif key_1 > key_2:
        
        return 1
    else:
        return -1
            
    
    
    
def comparetime(value_1, value_2):
    """
    Función encargada de comparar dos llaves para una mapa ordenado.
    args: key_1: Llave 1
            key_2: Llave 2
    return: 1 si key_1 es mayor que key_2
    """
    dateformat = "%Y-%m-%dT%H:%M"
    date1 = datetime.strptime(value_1["time"], dateformat)
    date2 = datetime.strptime(value_2["time"], dateformat)

    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
    
def compare_dates(value_1, value_2): #Este es para comparar fechas al construir arboles
    dateformat = "%Y-%m-%dT%H:%M:%S.%fZ"
    date1 = datetime.strptime(value_1, dateformat)
    date2 = datetime.strptime(value_2, dateformat)

    if date1 == date2:
        return 0
    elif date1 > date2:
        return 1
    else:
        return -1
    
def comparedates(value_1, value_2): #comparar normal
    dateformat = "%Y-%m-%dT%H:%M:%S.%fZ"
    date1 = datetime.strptime(value_1["time"], dateformat)
    date2 = datetime.strptime(value_2["time"], dateformat)

    if date1 == date2:
        return 0
    elif date1 > date2:
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
    dateformat = "%Y-%m-%dT%H:%M:%S.%fZ"
    value1 = datetime.strptime(data_1, dateformat)
    value2 = datetime.strptime(data_2, dateformat)

    return value1<value2


def sort(value1,value2):
    """
    Función encargada de ordenar la lista con los datos
    """
    return value1>value2

def sort_time(list):
    """
    Función encargada de ordenar la lista con los datos
    """
    sortedlist = quk.sort(list, comparetime)
    return sortedlist

def sortdates(list):
    """
    Función encargada de ordenar la lista con los datos
    """
    sortedlist = quk.sort(list, comparedates)
    return sortedlist

#Funciones de calculo

def harvesine_equation(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = radians(float(lon1)),radians(float(lat1)),radians(float(lon2)),radians(float(lat2))
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    in_parenthesis = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    in_arcsin = 2 * asin(sqrt(in_parenthesis)) 
    radio_earth = 6371

    return in_arcsin * radio_earth

# Funciones de datos

def fill_empty_values(dic):
    for key in dic.keys():
        if not dic[key] and key != "nst":
            dic[key] = "Unknown"
        elif not dic[key]:
            dic[key] = 1
    return dic