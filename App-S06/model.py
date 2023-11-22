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
assert cf
from datetime import datetime
from datetime import timedelta
from haversine import haversine, Unit

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
    analyzer = {"earthquakes": None,
                "magnitudes": None
                }
    
    analyzer["earthquakes"] = lt.newList("ARRAY_LIST")
    analyzer["magnitudes"] = om.newMap(omaptype="RBT")
    analyzer["dateIndex"] = om.newMap(omaptype='RBT',
                                      cmpfunction=compareDates)
    return analyzer


# Funciones para agregar informacion al modelo

def addEarthquake(analyzer, earthquake):
    """
    adicionar un terremoto a la lista de terremotos y en el arbol
    """
    lt.addLast(analyzer["earthquakes"], earthquake)
    updateMagnitud(analyzer["magnitudes"], earthquake)
    updateDateIndex(analyzer['dateIndex'], earthquake)
    return analyzer

def updateMagnitud(map, earthquake):
    """
    Se toma la magnitud del temblor y se busca si ya existe en el arbol
    dicha magnitud.  
    """
    if earthquake["mag"] == "":
        magnitud == -1
    else:
        magnitud = float(earthquake["mag"])
    entry = om.get(map, magnitud)
    if entry is None:
        datentry = newMagEntry(earthquake)
        om.put(map, magnitud, datentry)
    else:
        datentry = me.getValue(entry)
        addMagIndex(datentry, earthquake)
    return map

def updateDateIndex(map, earthquake):
    if earthquake["time"] == "":
        time == "0000-050-050T00:00:00.000000Z"
        date = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
        date = date.strftime('%Y-%m-%dT%H:%M')
        date = datetime.strptime(date, '%Y-%m-%dT%H:%M')
    else:
        time = earthquake['time']
        date = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
        date = date.strftime('%Y-%m-%dT%H:%M')
        date = datetime.strptime(date, '%Y-%m-%dT%H:%M')
    entry = om.get(map, date)
    if entry is None:
        datentry = newDataEntry(earthquake)
        om.put(map, date, datentry)
    else:
        datentry = me.getValue(entry)
        addDateIndex(datentry, earthquake)
    return map

def updateProf(map, earthquake):
    """
    Se toma la magnitud del temblor y se busca si ya existe en el arbol
    dicha magnitud.  
    """
    if earthquake["depth"] == "":
        prof == -1
    else:
        prof = float(earthquake["depth"])
    entry = om.get(map, prof)
    if entry is None:
        datentry = newProfEntry(earthquake)
        om.put(map, prof, datentry)
    else:
        datentry = me.getValue(entry)
        addProfIndex(datentry, earthquake)
    return map

def updateSig(map, earthquake):
    """
    Se toma la magnitud del temblor y se busca si ya existe en el arbol
    dicha magnitud.  
    """
    if earthquake["sig"] == "":
        sig == -1
    else:
        sig = float(earthquake["sig"])
    entry = om.get(map, sig)
    if entry is None:
        datentry = newSigEntry(earthquake)
        om.put(map, sig, datentry)
    else:
        datentry = me.getValue(entry)
        addSigIndex(datentry, earthquake)
    return map

def addMagIndex(datentry, earthquake):
    """
    Actualiza un indice de magnitudes.
    """
    lst = datentry["lstmags"]
    lt.addLast(lst, earthquake)
    return datentry

def updateDate5(map, earthquake):
    """
    Se toma la magnitud del temblor y se busca si ya existe en el arbol
    dicha magnitud.  
    """
    date= datetime.strptime(earthquake["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
    entry = om.get(map, date)
    if entry is None:
        datentry = newDate5(earthquake)
        om.put(map, date, datentry)
    else:
        datentry = me.getValue(entry)
        addDate5(datentry, earthquake)
    return map

def addDate5(datentry, earthquake):
    """
    Actualiza un indice de magnitudes.
    """
    lst = datentry["lstdate"]
    lt.addLast(lst, earthquake)
    return datentry

def updateSig(map, earthquake):
    """
    Se toma la magnitud del temblor y se busca si ya existe en el arbol
    dicha magnitud.  
    """
    if earthquake["sig"]=="":
        sig=0
    else:
        sig= float(earthquake["sig"])
    entry = om.get(map, sig)
    if entry is None:
        datentry = newSig(earthquake)
        om.put(map, sig, datentry)
    else:
        datentry = me.getValue(entry)
        addSig(datentry, earthquake)
    return map

def addSig(datentry, earthquake):
    """
    Actualiza un indice de magnitudes.
    """
    lst = datentry["lstsig"]
    lt.addLast(lst, earthquake)
    return datentry

def addDateIndex(datentry, earthquake):
    """
    Actualiza un indice de fechas
    """
    lst = datentry['lsttime']
    lt.addLast(lst, earthquake)
    return datentry

def addProfIndex(datentry, earthquake):
    """
    Actualiza un indice de magnitudes.
    """
    lst = datentry["lstprof"]
    lt.addLast(lst, earthquake)
    return datentry

def addSigIndex(datentry, earthquake):
    """
    Actualiza un indice de magnitudes.
    """
    lst = datentry["lstsig"]
    lt.addLast(lst, earthquake)
    return datentry

# Funciones para creacion de datos

def newMagEntry(earthquake):
    """
    Crea una entrada en el indice por magnitudes, es decir en el arbol
    binario.
    """
    entry = {"lstmags": None}
    entry["lstmags"] = lt.newList("SINGLE_LINKED")
    lt.addLast(entry["lstmags"], earthquake)
    return entry

def newDate5(earthquake):
    """
    Crea una entrada en el indice por magnitudes, es decir en el arbol
    binario.
    """
    entry = {"lstdate": None}
    entry["lstdate"] = lt.newList("SINGLE_LINKED")
    lt.addLast(entry["lstdate"], earthquake)
    return entry

def newSig(earthquake):
    """
    Crea una entrada en el indice por magnitudes, es decir en el arbol
    binario.
    """
    entry = {"lstsig": None}
    entry["lstsig"] = lt.newList("SINGLE_LINKED")
    lt.addLast(entry["lstsig"], earthquake)
    return entry

def newDataEntry(earthquake):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'lsttime': None}
    entry['lsttime'] = lt.newList('SINGLE_LINKED', compareDates)
    lt.addLast(entry["lsttime"], earthquake)
    return entry

def newProfEntry(earthquake):
    """
    Crea una entrada en el indice por magnitudes, es decir en el arbol
    binario.
    """
    entry = {"lstprof": None}
    entry["lstprof"] = lt.newList("SINGLE_LINKED")
    lt.addLast(entry["lstprof"], earthquake)
    return entry

def newSigEntry(earthquake):
    """
    Crea una entrada en el indice por magnitudes, es decir en el arbol
    binario.
    """
    entry = {"lstsig": None}
    entry["lstsig"] = lt.newList("SINGLE_LINKED")
    lt.addLast(entry["lstsig"], earthquake)
    return entry


# Funciones de consulta

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
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(analyzer, fecha_ini, fecha_fin):
    """
    Función que soluciona el requerimiento 1
    """
    fecha_ini = datetime.strptime(fecha_ini, '%Y-%m-%dT%H:%M')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M')
    lista = lt.newList("SINGLE_LINKED")
    datos = om.values(analyzer['dateIndex'], fecha_ini, fecha_fin)
    sismos = 0
    for fechas in lt.iterator(datos):
        tabla = {"time": None, "events": None, "details": None}
        eventos = fechas["lsttime"]
        ev = lt.firstElement(eventos)
        fecha = ev["time"]
        tabla["time"] = fecha 
        tabla["events"] = lt.size(eventos)
        tabla["details"] = eventos
        lt.addFirst(lista,tabla)
        sismos += lt.size(fechas['lsttime'])
    return lista, sismos


def req_2(map,magI,magF):
    """
    Función que soluciona el requerimiento 2
    """
    earthquakes = om.values(map,magI,magF)
    resultados=lt.newList("SINGLE_LINKED")
    tmag = lt.size(earthquakes)
    teve=0
    for earth in lt.iterator(earthquakes):
        datos={"mag":None,"events":None,"details":None}
        eventos= earth["lstmags"]
        d1 = lt.firstElement(eventos)
        magnitud= d1["mag"]
        datos["mag"]= magnitud 
        datos["events"] = lt.size(eventos)
        datos["details"] = eventos
        lt.addFirst(resultados,datos)
        e=lt.size(eventos)
        teve+= e
    return resultados,tmag,teve



def req_3(analyzer, mag, depth):
    """
    Función que soluciona el requerimiento 3
    """
    req3 = om.newMap(omaptype='RBT',cmpfunction=compareDates)
    lista = lt.newList("ARRAY_LIST")
    final = lt.newList("SINGLE_LINKED")
    for sismos in lt.iterator(analyzer["earthquakes"]):
        if float(sismos["mag"]) >= mag and float(sismos["depth"]) <= depth:
            lt.addLast(lista, sismos)
    numero = lt.size(lista)
    for sismos in lt.iterator(lista):
        updateDateIndex(req3, sismos)
    datos = om.valueSet(req3)
    for sismos in lt.iterator(datos):
        tabla = {"time": None, "events": None, "details": None}
        eventos = sismos["lsttime"]
        ev = lt.firstElement(eventos)    
        fecha = ev["time"]
        tabla["time"] = fecha 
        tabla["events"] = lt.size(eventos)
        tabla["details"] = eventos
        lt.addFirst(final,tabla)
            
    return final, numero



def req_4(analyzer, minsig, maxgap):
    """
    Función que soluciona el requerimiento 4
    """
    lista_sismos = analyzer["earthquakes"]
    sismos_ordenados = merg.sort(lista_sismos, sort_criteria)
    resultado = lt.newList("ARRAY_LIST")

    for sismo in lt.iterator(sismos_ordenados):
        if sismo["cdi"] == "":
            sismo["cdi"] = "Unavailable"
        if sismo["mmi"] == "":
            sismo["mmi"] = "Unavailable"
        gap = sismo["gap"]
        sig = sismo["sig"]
        if gap != "" and sig != "":
            gap = sismo["gap"]
            sig = sismo["sig"]
            if float(sig) >= minsig and float(gap) <= maxgap:
                sismo["mag"]= sismo["mag"]
                sismo["lat"] = sismo["lat"]
                sismo["long"] = sismo["long"]
                sismo["depth"] = sismo["depth"]
                sismo["sig"] = sismo["sig"]
                sismo["gap"] = sismo["gap"]
                sismo["nst"] = sismo["nst"]
                sismo["title"] = sismo["title"]
                sismo["cdi"] = sismo["cdi"]
                sismo["mmi"]= sismo["mmi"]
                sismo["magType"] = sismo["magType"]
                sismo["type"] = sismo["type"]
                sismo["code"] = sismo["code"]
                lt.addLast(resultado, sismo)

    cantidad_de_sismos = lt.size(resultado)
    return lt.subList(resultado,1,15), cantidad_de_sismos
    # TODO: Realizar el requerimiento 4
    pass


def req_5(lista,mindepth,minnst):
    """
    Función que soluciona el requerimiento 5
    """
    dates = om.newMap(omaptype="RBT")
    resultados = lt.newList("SINGLE_LINKED")
    teve=0
    for earth in lt.iterator(lista):
        if earth["depth"]=="":
            depth = 0
        else: 
            depth= float(earth["depth"])
        if earth["nst"]=="":
            nst = 1
        else: 
            nst= float(earth["nst"])
        if depth >= mindepth and nst>= minnst:
            updateDate5(dates, earth)
    valores= om.valueSet(dates)
    tdate = lt.size(dates)
    for ear in lt.iterator(valores):
        datos={"time":None,"events":None,"details":None}
        eventos= ear["lstdate"]
        d1 = lt.firstElement(eventos)
        tiempo= d1["time"]
        datos["time"]= tiempo 
        datos["events"] = lt.size(eventos)
        datos["details"] = eventos
        lt.addFirst(resultados,datos)
        e=lt.size(eventos)
        teve+= e
    
    return resultados,tdate,teve

def req_6(lista,anio,latitud,longitud,radio,N):
    """
    Función que soluciona el requerimiento 6
    """
    signi= om.newMap(omaptype="RBT")
    dates= om.newMap(omaptype="RBT")
    resultados= lt.newList("SINGLE_LINKED")
    teve=0
    for earthquake in lt.iterator(lista):
        date= datetime.strptime(earthquake["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        num= datetime.strftime(date, "%Y")
        if earthquake["lat"] =="":
            lat=0
        else:
            lat= float(earthquake["lat"])
        if earthquake["long"] =="":
            lon=0
        else:
            lon= float(earthquake["long"])
        punto1= (lat,lon)
        punto2= (latitud,longitud)
        hav=haversine(punto1,punto2)
        earthquake["hav"]=hav
        if hav <= radio and num == anio:
            updateSig(signi,earthquake)
            updateDate5(dates, earthquake)
    teve=om.size(dates)
    masSig= om.maxKey(signi)
    sigval= om.get(signi,masSig)
    listasig=me.getValue(sigval)
    for i in lt.iterator(listasig["lstsig"]):
        fecha= datetime.strptime(i["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        datos_significativo=i
    tamañoDates= om.size(dates)
    valores= om.valueSet(dates)
    muestra=lt.newList("SINGLE_LINKED")
    if tamañoDates <= N:
        muestra=valores
    else:
        datval= om.get(dates,fecha)
        datval=me.getValue(datval)
        lt.addLast(muestra,datval["lstdate"])
        antes= om.floor(dates,fecha-timedelta(seconds=1))
        despues=om.ceiling(dates,fecha+timedelta(seconds=1))
        while N > lt.size(muestra):
    
            if antes == None and despues != None:
                datdesp = om.get(dates,despues)
                datdesp=me.getValue(datdesp)
                lt.addFirst(muestra,datdesp["lstdate"])
                despues = om.ceiling(dates,despues+timedelta(seconds=1))
            elif antes != None and despues == None:
                datant = om.get(dates,antes)
                datant=me.getValue(datant)
                lt.addLast(muestra,datant["lstdate"])
                antes = om.floor(dates,antes-timedelta(seconds=1))

            elif antes!= None and despues != None:
                delta_antes= fecha-antes
                delta_despues= despues-fecha
                if delta_antes > delta_despues:
                    datdesp = om.get(dates,despues)
                    datdesp=me.getValue(datdesp)
                    lt.addFirst(muestra,datdesp["lstdate"])
                    despues = om.ceiling(dates,despues+timedelta(seconds=1))
                elif delta_antes < delta_despues:
                    datant = om.get(dates,antes)
                    datant=me.getValue(datant)
                    lt.addLast(muestra,datant["lstdate"])
                    antes = om.floor(dates,antes-timedelta(seconds=1))
                elif delta_despues==delta_antes:
                    datdesp = om.get(dates,despues)
                    datdesp=me.getValue(datdesp)
                    lt.addFirst(muestra,datdesp["lstdate"])
                    despues = om.ceiling(dates,despues+timedelta(seconds=1))
                    datant = om.get(dates,antes)
                    datant=me.getValue(datant)
                    lt.addLast(muestra,datant["lstdate"])
                    antes = om.floor(dates,antes-timedelta(seconds=1))
    for m in lt.iterator(muestra):
        datos= {"time":None,"events":None,"details":None}
        d1= lt.firstElement(m)
        tiempo= d1["time"]
        datos["time"]= tiempo 
        datos["events"] = lt.size(m)
        datos["details"] = m
        lt.addLast(resultados,datos)
    return datos_significativo, resultados,teve

def req_7(analyzer,anio,title,prop):
    """
    Función que soluciona el requerimiento 7
    """
    req7T = om.newMap(omaptype='RBT',cmpfunction=compareDates)
    req7M = om.newMap(omaptype='RBT',cmpfunction=compareDates)
    req7P = om.newMap(omaptype='RBT',cmpfunction=compareDates)
    req7S = om.newMap(omaptype='RBT',cmpfunction=compareDates)
    lista = lt.newList("ARRAY_LIST")
    for sismos in lt.iterator(analyzer["earthquakes"]):
        if title in sismos["title"] and anio in sismos["time"]:
            lt.addLast(lista, sismos)
    for sismos in lt.iterator(lista):
        updateDateIndex(req7T, sismos)
    datos = om.valueSet(req7T)

    tabla = lt.newList("ARRAY_LIST")
    for sismos in lt.iterator(datos):
        eventos = sismos["lsttime"]
        for sismos2 in lt.iterator(eventos):
            lt.addLast(tabla,sismos2)

    propiedad = lt.newList("SINGLE_LINKED")
    if prop == "mag":
        for sismos in lt.iterator(lista):
            updateMagnitud(req7M, sismos)
        datos = om.valueSet(req7M)
        for sismos in lt.iterator(datos):
            eventos = sismos["lstmags"]
            for sismos2 in lt.iterator(eventos):
                lt.addFirst(propiedad, sismos2)
        
    elif prop == "depth":
        for sismos in lt.iterator(lista):
            updateProf(req7P, sismos)
        datos = om.valueSet(req7P)
        for sismos in lt.iterator(datos):
            eventos = sismos["lstprof"]
            for sismos2 in lt.iterator(eventos):
                lt.addFirst(propiedad, sismos2)
    elif prop == "sig":
        for sismos in lt.iterator(lista):
            updateSig(req7S, sismos)
        datos = om.valueSet(req7S)
        for sismos in lt.iterator(datos):
            eventos = sismos["lstsig"]
            for sismos2 in lt.iterator(eventos):
                lt.addFirst(propiedad, sismos2)

    return tabla, propiedad


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento


def sort_criteria_req5(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    fecha1= data_1["time"]
    fecha2= data_2["time"]
    if fecha1 > fecha2:
        cambiar=True
    else:
        cambiar=False
    return cambiar


def sort_req5(data,size):
    """
    Función encargada de ordenar la lista con los datos
    """
    sub_list = lt.subList(data, 1, size)
    sorted_list = merg.sort(sub_list, sort_criteria_req5)
    return sorted_list
def sort_criteria(data_1, data_2):
    """
    Función de comparación para ordenar los datos
    """
    return (str(data_1["time"]) > str(data_2["time"]))

def compareearth(e1,e2):
    """
    compara dos sismos
    """
    if (e1 == e2):
        return 0
    elif (e1 > e2):
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
    
def compareMags(mag1, mag2):
    """
    Compara dos tipos de crimenes
    """
    mag = me.getKey(mag2)
    if (mag1 == mag):
        return 0
    elif (mag1 > mag):
        return 1
    else:
        return -1
