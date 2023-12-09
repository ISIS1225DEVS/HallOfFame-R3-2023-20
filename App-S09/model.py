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
import datetime
from tabulate import tabulate
from operator import itemgetter
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
import numpy as np
import re
from math import radians, sin, cos, sqrt, atan2
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos

def newCatalog():
    """ Inicializa el catalogo de sismos

    Crea una lista vacia para guardar todos los sismos con los datos indicados 
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    catalog = {"sismos": None,
                "dateIndex": None,
                "sigIndex": None,
                }

    catalog["sismos"] = lt.newList("ARRAY_LIST", compareCode)

    catalog["dateIndex"] = om.newMap(omaptype="RBT",
                                    cmpfunction=compareDates)
    catalog["sigIndex"] = om.newMap(omaptype="RBT",
                                    cmpfunction=compareDates)
    catalog["yearIndex"]= om.newMap(omaptype="RBT",
                                    cmpfunction=compareDates)
    catalog["magIndex"]= om.newMap(omaptype="RBT",
                                    cmpfunction=compareDates)
    catalog["depthIndex"]= om.newMap(omaptype="RBT",
                                    cmpfunction=compareDates)
    catalog["nstIndex"]= om.newMap(omaptype="RBT",
                                    cmpfunction=compareDates)
    catalog['mapYears'] = mp.newMap(5000,
                             maptype="CHAINING",
                             loadfactor=4)
    
    catalog["dateSigGapIndex"] = om.newMap(omaptype="RBT",
                                    cmpfunction=compareDates)
    return catalog


# Funciones para agregar informacion al modelo

def add_data(catalog, sismo):
    """
    adicionar un sismo a la lista de sismos y en los arboles
    """
    
    lt.addLast(catalog["sismos"], sismo)
    updateDateIndex(catalog["dateIndex"], sismo)
    updateSigIndex(catalog["sigIndex"], sismo)
    updateYearIndex(catalog["yearIndex"], sismo)
    updateMagIndex(catalog["magIndex"], sismo)
    updateMapYears(catalog["mapYears"],sismo)
    updateDepthIndex(catalog["depthIndex"],sismo)
    return catalog

def updateMapYears(mapYears, datos):
    year = datos["time"].year
    ExistDate = mp.contains(mapYears, year)
    if ExistDate == True:
        entry = mp.get(mapYears, year)
        torneo_i = me.getValue(entry)
    else:
        torneo_i = newDateEntryReq6(year)
        mp.put(mapYears, year, torneo_i)
    lt.addLast(torneo_i['datos'], datos)

def newDateEntryReq6(date):
    entry = {}
    entry['date'] = date
    entry['datos'] = lt.newList('ARRAY_LIST')
    return entry# Corregir tipología de datos

def sismo_correcto(sismo):
    names = ["mag","place","time","updated",
             "tz","felt","cdi","mmi","alert",
             "status","tsunami","sig","net",
             "code","ids","sources","types",
             "nst","dmin","rms","gap","magType",
             "type","title","long","lat","depth"]
    n = len(names)

    for i in range(n):
        if sismo[names[i]] == "" or sismo[names[i]] == " " or sismo[names[i]] == None:
            if i == 10:
                sismo[names[i]] = False
            elif i == 2 or i == 3:
                sismo[names[i]] = datetime.datetime.strptime("1970-01-01T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
            elif i ==17:
                sismo[names[i]] = 1
            elif i in [20,11]:
                sismo[names[i]] = 0
            else:
                sismo[names[i]] = "Unknown"
        else: 
            if i == 2 or i ==3:
                sismo[names[i]] = datetime.datetime.strptime(sismo[names[i]],"%Y-%m-%dT%H:%M:%S.%fZ") 
            elif i == 10:
                if sismo[names[i]] == "0":
                    sismo[names[i]] = False
                else: 
                    sismo[names[i]] = True
            elif i in [0,4,5,6,7,17,18,19,20,24,25,26]:
                sismo[names[i]] = float(sismo[names[i]])
                sismo[names[i]] = round(sismo[names[i]],3)
                if i in [17,11]:
                    sismo[names[i]] = int(sismo[names[i]])
            
    return sismo

def updateDateIndex(map, sismo):
    sismodate = sismo["time"]
    entry = om.get(map, sismodate)
    if entry is None:
        datentry = newDateEntry(sismo)
        om.put(map, sismodate, datentry)
    else:
        datentry = me.getValue(entry)
        lt.addLast(datentry["lstSismos"], sismo)
        datentry["events"] +=1
        om.put(map, sismodate, datentry)

    return map

def updateDepthIndex(map, sismo):
    sismodate = sismo["depth"]
    entry = om.get(map, sismodate)
    if entry is None:
        datentry = newDepthEntry(sismo)
        om.put(map, sismodate, datentry)
    else:
        datentry = me.getValue(entry)
        lt.addLast(datentry["lstSismos"], sismo)
        datentry["events"] +=1
        om.put(map, sismodate, datentry)

    return map

def newDepthEntry(sismo):
    """
    Crea una entrada en el indice por depth, es decir en el arbol
    binario.
    """
    entry = {"depth": None, "events": 0, "lstSismos": None}
    entry["lstSismos"] = lt.newList("ARRAY_LIST", compareDates)
    lt.addLast(entry["lstSismos"], sismo)
    entry["events"] +=1
    entry["depth"] =sismo["depth"]
    return entry

def updateSigIndex(map, sismo):
    sismosig = sismo["sig"]
    entry = om.get(map, sismosig)
    if entry is None:
        datentry = newSigEntry(sismo)
        om.put(map, sismosig, datentry)
    else:
        datentry = me.getValue(entry)
        lt.addLast(datentry["lstSismos"], sismo)
        datentry["events"] +=1
        om.put(map, sismosig, datentry)

    return map

def newDateEntry(sismo):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {"time": None, "events": 0, "lstSismos": None}
    entry["lstSismos"] = lt.newList("ARRAY_LIST", compareDates)
    lt.addLast(entry["lstSismos"], sismo)
    entry["events"] +=1
    entry["time"] = sismo["time"]
    return entry

def newSigEntry(sismo):
    """
    Crea una entrada en el indice por sig, es decir en el arbol
    binario.
    """
    entry = {"sig": None, "events": 0, "lstSismos": None}
    entry["lstSismos"] = lt.newList("ARRAY_LIST", compareDates)
    lt.addLast(entry["lstSismos"], sismo)
    entry["events"] +=1
    entry["sig"] =sismo["sig"]
    return entry

def updateYearIndex(map, sismo):
    sismodate = sismo["time"]
    anio = str(sismodate.year)
    anio = datetime.datetime.strptime(anio, "%Y")
    entry = om.get(map, anio)
    if entry is None:
        datentry = newDateEntry(sismo)
        om.put(map, anio, datentry)
    else:
        datentry = me.getValue(entry)
        lt.addLast(datentry["lstSismos"], sismo)
        datentry["events"] +=1
        om.put(map, anio, datentry)

    return map

def newYearEntry(sismo):
    """
    Crea una entrada en el indice por year, es decir en el arbol
    binario.
    """
    entry = {"year": None, "events": 0, "lstSismos": None}
    entry["lstSismos"] = lt.newList("ARRAY_LIST", compareDates)
    lt.addLast(entry["lstSismos"], sismo)
    entry["events"] +=1
    anio = str(sismo["date"].year)
    anio = datetime.datetime.strptime(anio, "%Y")
    entry["year"] = anio
    return entry


def newMagEntry(sismo):
    """
    Crea una entrada en el indice por sig, es decir en el arbol
    binario.
    """
    entry = {"mag": None, "events": 0, "lstSismos": None}
    entry["lstSismos"] = lt.newList("ARRAY_LIST", compareDates)
    lt.addLast(entry["lstSismos"], sismo)
    entry["events"] +=1
    entry["mag"] =sismo["mag"]
    return entry

def updateMagIndex(map, sismo):
    sismomag = sismo["mag"]
    entry = om.get(map, sismomag)
    if entry is None:
        datentry = newMagEntry(sismo)
        om.put(map, sismomag, datentry)
    else:
        datentry = me.getValue(entry)
        lt.addLast(datentry["lstSismos"], sismo)
        datentry["events"] +=1
        om.put(map, sismomag, datentry)
    return map
# Funciones de consulta


def req_1(catalog,inicialDate, finalDate):
    """
    Función que soluciona el requerimiento 1
    """
    lst = om.values(catalog["dateIndex"], inicialDate, finalDate)
    filtrada = om.newMap(omaptype="RBT",
                        cmpfunction=compareDates)
    totaldates = 0
    totalevents = 0
    for lstsismos in lt.iterator(lst):
        fecha = lstsismos["time"]
        om.put(filtrada,fecha,lstsismos)
        totaldates +=1
        totalevents += lstsismos["events"]

    return totaldates, totalevents, filtrada
    


def req_2(catalog,inicialMag, finalMag):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    lst = om.values(catalog["magIndex"], inicialMag, finalMag)
    filtrada = om.newMap(omaptype="RBT",
                        cmpfunction=compareDates)
    totaldates = 0
    totalevents = 0
    for lstsismos in lt.iterator(lst):
        magni = lstsismos["mag"]
        om.put(filtrada,magni,lstsismos)
        totaldates +=1
        totalevents += lstsismos["events"]
    return totaldates, totalevents, filtrada
    



def req_3(catalog, nmag, ndepth):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    maxmag = om.maxKey(catalog["magIndex"])
    lst = om.values(catalog["magIndex"],nmag, maxmag)

    filtrada = om.newMap(omaptype="RBT",
                        cmpfunction=compareDates)
    totaldates = 0
    totalevents = 0
    for datos in lt.iterator(lst):
        sismos = datos["lstSismos"]
        eventos = datos["events"]
        if eventos != 0:
            for sismo in lt.iterator(sismos):
                depth = sismo["depth"]
                if depth <= ndepth:
                    updateDateIndex(filtrada, sismo)
                    totaldates +=1
                    totalevents +=1

    if om.size(filtrada)<=10:
        return totaldates, totalevents, filtrada
    else:
        filtrada2 = om.newMap(omaptype="RBT",
                            cmpfunction=compareDates)
        for _ in range(10):
            key = om.maxKey(filtrada)
            value = om.get(filtrada,key)
            value = me.getValue(value)
            om.deleteMax(filtrada)
            om.put(filtrada2,key=key,value=value)
        return totaldates, totalevents, filtrada2



def req_4(catalog, nsig, ngap):
    """
    Función que soluciona el requerimiento 4
    """
    maxsig = om.maxKey(catalog["sigIndex"])
    lst = om.values(catalog["sigIndex"],nsig, maxsig)

    filtrada = om.newMap(omaptype="RBT",
                        cmpfunction=compareDates)
    totaldates = 0
    totalevents = 0
    for datos in lt.iterator(lst):
        sismos = datos["lstSismos"]
        eventos = datos["events"]
        if eventos != 0:
            for sismo in lt.iterator(sismos):
                gap = sismo["gap"]
                if gap <= ngap:
                    updateDateIndex(filtrada, sismo)
                    totaldates +=1
                    totalevents +=1

    if om.size(filtrada)<=15:
        return totaldates, totalevents, filtrada
    else:
        filtrada2 = om.newMap(omaptype="RBT",
                            cmpfunction=compareDates)
        for _ in range(15):
            key = om.maxKey(filtrada)
            value = om.get(filtrada,key)
            value = me.getValue(value)
            om.deleteMax(filtrada)
            om.put(filtrada2,key=key,value=value)
        return totaldates, totalevents, filtrada2



def req_5(catalog, mindepth, minnst):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5

    prof = om.maxKey(catalog["depthIndex"])
    estaciones = om.maxKey(catalog["nstIndex"])

    filtro = om.values(catalog["depthIndex"], mindepth, prof)

    listaFin = lt.newList(datastructure="ARRAY_LIST")
    for valor in lt.iterator(filtro):
        condicion = om.values(catalog["nstIndex"], minnst, estaciones)
        for temblor in lt.iterator(condicion):
            for est in lt.iterator(temblor["nst"]):
                lt.addLast(listaFin, est)

    Final = lt.size(listaFin)

    sorteados = sorted(lt.toArray(listaFin), key=lambda x: x["time"], reverse=True)

    elegidos = lt.subList(sorteados, 0, 20) if Final > 20 else sorteados

    return elegidos, Final

#!---------------------------------------------------------
#!------------------ DANGER ZONE -------------------
def req_6(data_structs, year, latRef, longRef, radio, n):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    mapYears = data_structs['mapYears']
    year = int(year)
    entry = mp.get(mapYears, year)
    earthquakesYear = me.getValue(entry)
    earthquakesYear = earthquakesYear['datos']
    tembloresArea = lt.newList('ARRAY_LIST')

    for temblor in lt.iterator(earthquakesYear):
        if AreaPresent(latRef, longRef, float(temblor['lat']),   float(temblor['long']), radio):
            temblor['distance'] = haversine(latRef, longRef, float(
                temblor['lat']),   float(temblor['long']))
            lt.addLast(tembloresArea, temblor)

    sortedAreas = quk.sort(tembloresArea, sort_criteria_REQ6)
    maxArea, posicion = encontrar_mayor_magnitud(sortedAreas)

    Sublista = obtener_sublista(sortedAreas, posicion, n)

    if lt.size(Sublista) <= 6:
        TablaMaxArea, TablaTopN = CreateTables(maxArea, Sublista)
    else:
        List6 = FirstandALst(Sublista)
        TablaMaxArea, TablaTopN = CreateTables(maxArea, List6)

    return TablaMaxArea, TablaTopN, lt.size(tembloresArea), lt.size(Sublista), maxArea


def AreaPresent(lat1, lon1, lat2, lon2, radio):
    return haversine(lat1, lon1, lat2, lon2) < radio


def sort_criteria_REQ6(dato_1, dato_2):

    if dato_1["time"] < dato_2['time']:
        return True
    elif dato_1["time"] == dato_2['time']:
        if dato_1['mag'] > dato_2['mag']:
            return True
        else:
            return False

    return False


def FirstandALst(top):
    n = lt.size(top)
    topF = lt.newList('ARRAY_LIST')
    lt.addLast(topF, lt.getElement(top, 1))
    lt.addLast(topF, lt.getElement(top, 2))
    lt.addLast(topF, lt.getElement(top, 3))
    lt.addLast(topF, lt.getElement(top, n-2))
    lt.addLast(topF, lt.getElement(top, n-1))
    lt.addLast(topF, lt.getElement(top, n))

    return topF


def encontrar_mayor_magnitud(lista_earthquakes):
    if not lista_earthquakes:
        return None, None

    max_magnitud = 0
    max_magnitud_dict = None
    posicion = None

    for i, earthquake in enumerate(lt.iterator(lista_earthquakes)):
        magnitud_actual = float(earthquake['mag'])
        if magnitud_actual > max_magnitud:
            max_magnitud = magnitud_actual
            max_magnitud_dict = earthquake
            posicion = i

    return max_magnitud_dict, posicion


def obtener_sublista(lista, posicion, n):
    """
    Retorna una nueva sublista con n elementos arriba de la posición,
    el elemento en la posición y n elementos abajo de la posición.
    Si no hay suficientes elementos, se agregan los que haya.
    """

    lista = lista['elements']

    sublista = lt.newList('ARRAY_LIST')

    # Agrega los elementos hacia arriba de la posición
    for i in range(max(0, posicion - n), posicion):
        lt.addLast(sublista, lista[i])

    # Agrega el elemento en la posición
    lt.addLast(sublista, lista[posicion])

    # Agrega los elementos hacia abajo de la posición
    for i in range(posicion + 1, min(posicion + n + 1, len(lista))):
        lt.addLast(sublista, lista[i])

    return sublista


def CreateTables(maxArea, Sublista):

    if maxArea['gap'] == '' or maxArea['gap'] == ' ' or maxArea['gap'] == None:
        maxArea['gap'] = 'Unknown'

    if maxArea['nst'] == '' or maxArea['nst'] == ' ' or maxArea['nst'] == None:
        maxArea['nst'] = 'Unknown'

    if maxArea['cdi'] == '' or maxArea['cdi'] == ' ' or maxArea['cdi'] == None:
        maxArea['cdi'] = 'Unknown'

    if maxArea['mmi'] == '' or maxArea['mmi'] == ' ' or maxArea['mmi'] == None:
        maxArea['mmi'] = 'Unknown'

    maxAreaFormat = {
        'time': maxArea['time'],
        'mag': round(float(maxArea['mag']), 3),
        'lat': round(float(maxArea['lat']), 3),
        'long': round(float(maxArea['long']), 3),
        'depth': round(float(maxArea['depth']), 3),
        'sig': round(float(maxArea['sig']), 3),
        'gap': round(float(maxArea['gap']), 3) if maxArea['gap'] != 'Unknown' else maxArea['gap'],
        'distance': round(float(maxArea['distance']), 3),
        'nst': round(float(maxArea['nst']), 3) if maxArea['nst'] != 'Unknown' else maxArea['nst'],
        'title': maxArea['title'],
        'cdi': round(float(maxArea['cdi']), 3) if maxArea['cdi'] != 'Unknown' else maxArea['cdi'],
        'mmi': round(float(maxArea['mmi']), 3) if maxArea['mmi'] != 'Unknown' else maxArea['mmi'],
        'magType': maxArea['magType'],
        'type': maxArea['type'],
        'code': maxArea['code']
    }

    maxAreaFormatT = [maxAreaFormat]
    TableMaxArea = tabulate(maxAreaFormatT, headers='keys', tablefmt='grid')

    SolutionTable = lt.newList('ARRAY_LIST')

    for earthquake in lt.iterator(Sublista):

        if earthquake['gap'] == '' or earthquake['gap'] == ' ' or earthquake['gap'] == None:
            earthquake['gap'] = 'Unknown'

        if earthquake['nst'] == '' or earthquake['nst'] == ' ' or earthquake['nst'] == None:
            earthquake['nst'] = 'Unknown'

        if earthquake['cdi'] == '' or earthquake['cdi'] == ' ' or earthquake['cdi'] == None:
            earthquake['cdi'] = 'Unknown'

        if earthquake['mmi'] == '' or earthquake['mmi'] == ' ' or earthquake['mmi'] == None:
            earthquake['mmi'] = 'Unknown'

        infoearthquake = {
            'time': earthquake['time'],
            'events': 1
        }

        detailsearthquake = {
            'mag': round(float(earthquake['mag']), 3),
            'lat': round(float(earthquake['lat']), 3),
            'long': round(float(earthquake['long']), 3),
            'depth': round(float(earthquake['depth']), 3),
            'sig': round(float(earthquake['sig']), 3),
            'gap': round(float(earthquake['gap']), 3) if earthquake['gap'] != 'Unknown' else earthquake['gap'],
            'distance': round(float(earthquake['distance']), 3),
            'nst': round(float(earthquake['nst']), 3) if earthquake['nst'] != 'Unknown' else earthquake['nst'],
            'title': earthquake['title'],
            'cdi': round(float(earthquake['cdi']), 3) if earthquake['cdi'] != 'Unknown' else earthquake['cdi'],
            'mmi': round(float(earthquake['mmi']), 3) if earthquake['mmi'] != 'Unknown' else earthquake['mmi'],
            'magType': earthquake['magType'],
            'type': earthquake['type'],
            'code': earthquake['code']
        }

        infoearthquake['details'] = tabulate(
            [detailsearthquake], headers='keys', tablefmt="grid")
        lt.addLast(SolutionTable, infoearthquake)

    solutionElements = SolutionTable['elements']
    SolutionTableF = tabulate(
        solutionElements, headers='keys', tablefmt="grid")

    return TableMaxArea, SolutionTableF


def haversine(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en kilómetros
    R = 6371.0

    # Convierte las coordenadas de grados a radianes
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Diferencias de coordenadas
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula de Haversine
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distancia en kilómetros
    distance = R * c

    return distance

#! -----------------------------------------
#!---------------------------------------------------------
def req_7(catalog, year, title, propiedad, bins):
    """
    Función que soluciona el requerimiento 7
    """
    mapYears = catalog["yearIndex"]
    datorYear = om.get(mapYears,year)
    sismosYear = me.getValue(datorYear)

    sismos = sismosYear["lstSismos"]

    mapProp = om.newMap(omaptype="RBT",
                        cmpfunction=compareDates)
    
    filtrada = om.newMap(omaptype="RBT",
                        cmpfunction=compareDates)
    
    for sismo in lt.iterator(sismos):
        if title in sismo["title"]:
            updateDateIndex_7(filtrada,sismo, propiedad)
            updatePropIndex_7(mapProp,sismo, propiedad)
    
    prop_min = float(om.minKey(mapProp))
    prop_max = float(om.maxKey(mapProp))
    inter_total = prop_max-prop_min
    lin_int = round(prop_min,2)
    paso = round((inter_total/bins), 2)
    n_pasos = bins

    intervalos = om.newMap(omaptype="RBT",
                          cmpfunction=compareDates)
    
    for i in range(1,n_pasos+1):
        if i < n_pasos:

            lsu_int = round((lin_int+ paso),2)
            llave = f"({lin_int}, {lsu_int}]"
            valor = 0
            eventos  = om.values(mapProp, lin_int, lsu_int)
            for evento in lt.iterator(eventos):
                valor += evento["events"]
            om.put(intervalos,llave, valor)

        else:
            llave = f"({lin_int}, {prop_max}]"
            valor = 0
            eventos  = om.values(mapProp, lin_int, prop_max)
            for evento in lt.iterator(eventos):
                valor += evento["events"]
            om.put(intervalos,llave, valor)

        lin_int = lsu_int
    
    #Sacar valores:

    llaves_int = om.keySet(intervalos)

    numpy_intervalos = []
    valores = []

    for llave in lt.iterator(llaves_int):
        numpy_intervalos.append(llave)
        dato = om.get(intervalos,llave)
        valores.append(me.getValue(dato))
    
    numpy_intervalos = np.array(numpy_intervalos)
    valores = np.array(valores)
    tamano = om.size(filtrada)

    return tamano, filtrada,numpy_intervalos,valores

def updateDateIndex_7(map, sismo,prop):
    sismodate = sismo["time"]
    entry = om.get(map, sismodate)
    if entry is None:
        datentry = newDateEntry_7(sismo,prop)
        om.put(map, sismodate, datentry)

    return map

def newDateEntry_7(sismo,prop):
    """
    Crea una entrada en el indice por fecha para el req7,
    es decir en el arbol binario.
    """
    entry = {"time": None,
            "lat": None, 
            "long": None,
            "title": None,
            "code": None,
            prop: None}
    
    entry["time"]= sismo["time"]
    entry["lat"]= sismo["lat"]
    entry["long"]= sismo["long"]
    entry["title"]= sismo["title"]
    entry["code"]= sismo["code"]
    entry[prop] = sismo[prop]

    return entry

def updatePropIndex_7(map,sismo, prop):
    sismoprop = sismo[prop]
    entry = om.get(map, sismoprop)
    if entry is None:
        datentry = newPropEntry_7(sismo,prop)
        om.put(map, sismoprop, datentry)
    else:
        datentry = me.getValue(entry)
        datentry["events"] +=1
        om.put(map,sismoprop, datentry)
    return map

def newPropEntry_7(sismo,prop):
    entry = {prop: None,
            "events": 0}
    
    entry[prop] = sismo[prop]
    entry["events"] +=1

    return entry

def crear_imagen(intervalos, values, prop, place, year, headers, datos,bins):
    # Configurar un estilo global para todos los gráficos y tablas
    data = datos_tabla_matplot(datos,headers, prop)
    # Crear una figura con dos subparcelas
    fig, axs = plt.subplots(2, 1, sharey=True, tight_layout=True, figsize=(10, 8))

    # Crear el histograma en la primera subparcela
    crear_grafico_histograma(axs[0], intervalos, values, prop, place, year)

    # Crear la tabla en la segunda subparcela
    crear_tabla_eventos(axs[1], data, place, year)

    # Guardar la figura
    plt.savefig(f'grafico-{year}-{prop}-{place}-{bins}.png')

    # Mostrar la figura
    plt.show()

def crear_grafico_histograma(ax, intervalos, values, prop, place, year):

    bars = ax.bar(intervalos, values, color="#BA6BDF", edgecolor="#800AE0")
    ax.set_xticks(intervalos)
    ax.set_xticklabels(intervalos, rotation=45, fontsize=8)
    ax.set_facecolor('none')
    ax.set_ylabel("No. Events", fontsize=10)
    ax.set_xlabel(f"{prop}", fontsize=10)
    ax.set_title(f'Histogram of {prop} in {place} in {year}')
    ax.spines['top'].set_visible(False)    # Mostrar la espina superior
    ax.spines['right'].set_visible(False) 
    ax.bar_label(bars, fontsize=8)
    ax.grid(True, linestyle= '--',linewidth = 0.5, axis = "y", color = "#404040")


def crear_tabla_eventos(ax, datos, place, year):
    ax.axis("off")
    ax.axis('tight')
    ax.set_title(f"Events details in {place} in {year}")
    tabla = ax.table(cellText=datos, cellLoc="center", loc= "center")
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(6)
    tabla.auto_set_column_width([4, 2, 2, 5, 1, 1])
    tabla.scale(2, 2.5)

def datos_tabla_matplot(map, headers, prop):
    matriz = []
    matriz.append(headers)
    tamano = om.size(map)
    if tamano<=6:
        for i in range(1,tamano+1):
            sismo_list = []
            inicial = om.maxKey(map)
            fecha = om.get(map,inicial)
            sismo = me.getValue(fecha)
            sismo_list.append(sismo["time"])
            sismo_list.append(sismo["lat"])
            sismo_list.append(sismo["long"])
            sismo_list.append(sismo["title"])
            sismo_list.append(sismo["code"])
            sismo_list.append(sismo[prop])
            map = om.deleteMax(map)
            matriz.append(sismo_list)
    else:
        for i in range(1,4):
            sismo_list = []
            inicial = om.minKey(map)
            fecha = om.get(map,inicial)
            sismo = me.getValue(fecha)
            sismo_list.append(sismo["time"])
            sismo_list.append(sismo["lat"])
            sismo_list.append(sismo["long"])
            sismo_list.append(sismo["title"])
            sismo_list.append(sismo["code"])
            sismo_list.append(sismo[prop])
            map = om.deleteMin(map)
            matriz.append(sismo_list)
    
        for i in range(1,4): 
            sismo_list = []
            inicial = om.maxKey(map)
            fecha = om.get(map,inicial)
            sismo = me.getValue(fecha)
            sismo_list.append(sismo["time"])
            sismo_list.append(sismo["lat"])
            sismo_list.append(sismo["long"])
            sismo_list.append(sismo["title"])
            sismo_list.append(sismo["code"])
            sismo_list.append(sismo[prop])
            map = om.deleteMax(map)
            matriz.insert(4,sismo_list)
    
    return matriz


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compareCode(code1, code2):
    """
    Función encargada de comparar dos sismos
    """
    if (code1 == code2):
        return 0
    elif code1 > code2:
        return 1
    else:
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
def compareDatesSort(coso1, coso2):
    date1 = coso1["time"]
    date2 = coso2["time"]
    """
    Compara dos fechas
    """
    if (date1 > date2):
        return True
    else:
        return False


# Funciones de ordenamiento
def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    sa.sort(data_structs, compareDatesSort)


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

# Funcion para mejorar la interfaz con el usuario

def makeTablita (listaT, nombres, tamano,n):
    if n%2 != 0:
        n +=1

    n_1 = (n//2)+1
    n_2 = (n//2)-1
    
    rows = []
    if tamano<=n:
        for i in range(1,tamano+1):
            sismo = lt.getElement(listaT,i)
            row = []
            for parametro in nombres:
                 row.append(sismo[parametro])
            rows.append(row)
    else:
        for i in range(1,n_1):
            sismo = lt.getElement(listaT,i)
            row = []
            for parametro in nombres:
                row.append(sismo[parametro])
            rows.append(row)
    
        for i in range(tamano-n_2,tamano+1): 
            sismo = lt.getElement(listaT,i)
            row = []
            for parametro in nombres:
                 row.append(sismo[parametro])
            rows.append(row)
    
    return tabulate(rows,nombres,tablefmt='simple_grid')

def makeTablitaMap_1 (map, nombres, tamano):
    orden  = ["mag","lat","long","depth",
               "sig","gap","nst","title","cdi",
                "mmi","magType", "type", "code"]
    rows = []
    if tamano<=6:
        for i in range(1,tamano+1):
            row = []
            inicial = om.maxKey(map)
            fecha = om.get(map,inicial)
            sismo = me.getValue(fecha)
            row.append(inicial)
            row.append(sismo[nombres[1]])
            dat = makeTablita(sismo["lstSismos"], orden, sismo[nombres[1]],1)
            row.append(dat)
            map = om.deleteMax(map)
            rows.append(row)
    else:
        for i in range(1,4):
            row = []
            inicial = om.maxKey(map)
            fecha = om.get(map,inicial)
            sismo = me.getValue(fecha)
            row.append(inicial)
            row.append(sismo[nombres[1]])
            dat = makeTablita(sismo["lstSismos"], orden, sismo[nombres[1]],1)
            row.append(dat)
            map = om.deleteMax(map)
            rows.append(row)
    
        for i in range(1,4): 
            row = []
            inicial = om.minKey(map)
            fecha = om.get(map,inicial)
            sismo = me.getValue(fecha)
            row.append(inicial)
            row.append(sismo[nombres[1]])
            dat = makeTablita(sismo["lstSismos"], orden, sismo[nombres[1]],1)
            row.append(dat)
            map = om.deleteMin(map)
            rows.insert(3,row)
    
    return tabulate(rows,nombres,tablefmt='simple_grid')

def makeTablitaMap_2 (map, nombres, tamano):
    orden  = ["time","lat","long","depth",
               "sig","gap","nst","title","cdi",
                "mmi","magType", "type", "code"]
    rows = []
    if tamano<=6:
        for i in range(1,tamano+1):
            row = []
            inicial = om.maxKey(map)
            fecha = om.get(map,inicial)
            sismo = me.getValue(fecha)
            row.append(inicial)
            row.append(sismo[nombres[1]])
            sort(sismo["lstSismos"])
            dat = makeTablita(sismo["lstSismos"], orden, sismo[nombres[1]],6)
            row.append(dat)
            map = om.deleteMax(map)
            rows.append(row)
    else:
        for i in range(1,4):
            row = []
            inicial = om.maxKey(map)
            fecha = om.get(map,inicial)
            sismo = me.getValue(fecha)
            row.append(inicial)
            row.append(sismo[nombres[1]])
            sort(sismo["lstSismos"])
            dat = makeTablita(sismo["lstSismos"], orden, sismo[nombres[1]],6)
            row.append(dat)
            map = om.deleteMax(map)
            rows.append(row)
    
        for i in range(1,4): 
            row = []
            inicial = om.minKey(map)
            fecha = om.get(map,inicial)
            sismo = me.getValue(fecha)
            row.append(inicial)
            row.append(sismo[nombres[1]])
            sort(sismo["lstSismos"])
            dat = makeTablita(sismo["lstSismos"], orden, sismo[nombres[1]],6)
            row.append(dat)
            map = om.deleteMin(map)
            rows.insert(3,row)
    
    return tabulate(rows,nombres,tablefmt='simple_grid')

def makeTablitaMap_3 (map, nombres, tamano):
    orden  = ["mag","lat","long","depth",
               "sig","gap","nst","title","cdi",
                "mmi","magType", "type", "code"]
    rows = []

    if tamano<=6:
        for i in range(1,tamano+1):
            row = []
            inicial = om.maxKey(map)
            fecha = om.get(map,inicial)
            sismo = me.getValue(fecha)
            row.append(inicial)
            row.append(sismo[nombres[1]])
            sort(sismo["lstSismos"])
            dat = makeTablita(sismo["lstSismos"], orden, sismo[nombres[1]],6)
            row.append(dat)
            map = om.deleteMax(map)
            rows.append(row)
    else:
        for i in range(1,4):
            row = []
            inicial = om.maxKey(map)
            fecha = om.get(map,inicial)
            sismo = me.getValue(fecha)
            row.append(inicial)
            row.append(sismo[nombres[1]])
            sort(sismo["lstSismos"])
            dat = makeTablita(sismo["lstSismos"], orden, sismo[nombres[1]],6)
            row.append(dat)
            map = om.deleteMax(map)
            rows.append(row)
    
        for i in range(1,4): 
            row = []
            inicial = om.minKey(map)
            fecha = om.get(map,inicial)
            sismo = me.getValue(fecha)
            row.append(inicial)
            row.append(sismo[nombres[1]])
            sort(sismo["lstSismos"])
            dat = makeTablita(sismo["lstSismos"], orden, sismo[nombres[1]],6)
            row.append(dat)
            map = om.deleteMin(map)
            rows.insert(3,row)
    
    return tabulate(rows,nombres,tablefmt='simple_grid')


# Funciones de calculo de tamaño

def sismosSize(catalog):
    return lt.size(catalog["sismos"])
