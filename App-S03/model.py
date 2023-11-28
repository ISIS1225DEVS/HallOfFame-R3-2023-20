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
from datetime import datetime
from haversine import haversine
import folium
from folium.plugins import MarkerCluster
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def newDataStructs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    dataStructs = {}
    dataStructs["seismicEvents"] = lt.newList()
    dataStructs["seismicEventsByDate"] = om.newMap()
    dataStructs["seismicEventsByMag"] = om.newMap()
    dataStructs["seismicEventsBySig"] = om.newMap()
    dataStructs["seismicEventsByDepth"] = om.newMap()
    dataStructs["seismicEventsByYear"] = mp.newMap(100, maptype="PROBING", loadfactor= 0.5)
    return dataStructs

# Funciones para agregar informacion al modelo

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    pass

def addSeismicEvent(dataStructs, seismicEvent):
    seismicEvent["tsunami"] = bool(int(seismicEvent["tsunami"]))
    seismicEvent["year"] = seismicEvent["time"].split("-")[0]
    lt.addLast(dataStructs["seismicEvents"], seismicEvent)
    addSeismicEventByDate(dataStructs, seismicEvent)
    addSeismicEventsByMag(dataStructs, seismicEvent)
    addSeismicEventsBySig(dataStructs, seismicEvent)
    addSeismicEventsByDepth(dataStructs, seismicEvent)
    addSeismicEventByYear(dataStructs, seismicEvent)
   

def addSeismicEventByDate(dataStructs, seismicEvent):
    dateTree = dataStructs["seismicEventsByDate"]
    date = datetime.strptime(seismicEvent["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
    entry = om.get(dateTree, date)
    if entry:
        dateList = me.getValue(entry)
    else:
        dateList = lt.newList()
        om.put(dateTree, date, dateList)
    lt.addLast(dateList, seismicEvent)

def addSeismicEventsByMag(dataStructs, seismicEvent):
    magTree = dataStructs["seismicEventsByMag"]
    mag = float(seismicEvent["mag"])
    entry = om.get(magTree, mag)
    if entry:
        magNode = me.getValue(entry)
    else:
        magNode = newMag()
        om.put(magTree, mag, magNode)
    lt.addLast(magNode["seismicEvents"], seismicEvent)
    addEventToSimpleTree(magNode["seismicEventsByDepth"], seismicEvent, "depth", True)
    
def addSeismicEventsBySig(dataStructs, seismicEvent):
    sigTree = dataStructs["seismicEventsBySig"]
    sig = float(seismicEvent["sig"])
    entry = om.get(sigTree, sig)
    if entry:
        sigNode = me.getValue(entry)
    else:
        sigNode = newSig()
        om.put(sigTree, sig, sigNode)
    lt.addLast(sigNode["seismicEvents"], seismicEvent)
    addEventToSimpleTree(sigNode["seismicEventsByGap"], seismicEvent, "gap", True)
    
def addSeismicEventsByDepth(dataStructs, seismicEvent):
    depthTree = dataStructs["seismicEventsByDepth"]
    depth = float(seismicEvent["depth"])
    entry = om.get(depthTree, depth)
    if entry:
        depthNode = me.getValue(entry)
    else:
        depthNode = newDepth()
        om.put(depthTree, depth, depthNode)
    lt.addLast(depthNode["seismicEvents"], seismicEvent)
    addEventToSimpleTree(depthNode["seismicEventsByNst"], seismicEvent, "nst", True)
    
def addEventToSimpleTree(featureTree, seismicEvent, feature, isFloat=False):
    feature = seismicEvent[feature]
    if isFloat:
        feature = 0 if feature == "" or feature == " " else float(feature)
    entry = om.get(featureTree, feature)
    if entry:
        featureList = me.getValue(entry)
    else:
        featureList = lt.newList()
        om.put(featureTree, feature, featureList)
    lt.addLast(featureList, seismicEvent)
    
def addEventToSimpleMap(featureMap, seismicEvent, feature):
    feature = seismicEvent[feature]
    entry = mp.get(featureMap, feature)
    if entry:
        featureList = me.getValue(entry)
    else:
        featureList = lt.newList()
        mp.put(featureMap, feature, featureList)
    lt.addLast(featureList, seismicEvent)
    
def addSeismicEventByYear(dataStructs, seismicEvent):
    yearMap = dataStructs["seismicEventsByYear"]
    year = seismicEvent["time"].split("-")[0]
    entry = mp.get(yearMap, year)
    if entry:
        yearNode = me.getValue(entry)
    else:
        yearNode = newYear()
        mp.put(yearMap, year, yearNode)
    lt.addLast(yearNode["seismicEvents"], seismicEvent)
    addSeismicEventByPlace(yearNode, seismicEvent)
    
def addSeismicEventByPlace(node, seismicEvent):
    placeMap = node["seismicEventsByPlace"]
    place = seismicEvent["place"].split(",")[-1].strip().title()
    entry = mp.get(placeMap, place)
    if entry:
        placeNode = me.getValue(entry)
    else:
        placeNode = newPlace()
        mp.put(placeMap, place, placeNode)
    lt.addLast(placeNode["seismicEvents"], seismicEvent)
    addEventToSimpleTree(placeNode["sig"], seismicEvent, "sig", True)
    addEventToSimpleTree(placeNode["depth"], seismicEvent, "depth", True)
    addEventToSimpleTree(placeNode["mag"], seismicEvent, "mag", True)

# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass

def newMag():
    mag = {}
    mag["seismicEvents"] = lt.newList("ARRAY_LIST")
    mag["seismicEventsByDepth"] = om.newMap()
    return mag

def newSig():
    sig = {}
    sig["seismicEvents"] = lt.newList("ARRAY_LIST")
    sig["seismicEventsByGap"] = om.newMap()
    return sig

def newDepth():
    depth = {}
    depth["seismicEvents"] = lt.newList("ARRAY_LIST")
    depth["seismicEventsByNst"] = om.newMap()
    return depth

def newYear():
    year = {}
    year["seismicEvents"] = lt.newList("ARRAY_LIST")
    year["seismicEventsByPlace"] = mp.newMap(300, maptype="PROBING", loadfactor= 0.5)
    return year

def newPlace():
    place = {}
    place["seismicEvents"] = lt.newList("ARRAY_LIST")
    place["sig"] = om.newMap()
    place["depth"] = om.newMap()
    place["mag"] = om.newMap()
    return place

# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass

def getNData(data, n):
    filtered = lt.newList("ARRAY_LIST")
    if lt.size(data) <= n:
        filtered = data
    else:
        filtered = lt.subList(data, 1, n)
    return filtered

def getFirstAndLastN(data, n):
    filtered = lt.newList("ARRAY_LIST")
    if lt.size(data) <= 2*n:
        filtered = data
    else:
        filtered = lt.subList(data, 1, n)
        last = lt.subList(data, lt.size(data)-(n-1), n)
        for i in lt.iterator(last):
            lt.addLast(filtered, i)
    return filtered

def getIndex(eventList, searchedEvent):
    index = 0
    for event in lt.iterator(eventList):
        index += 1
        if event == searchedEvent:
            return index
    return 0
        
def getPreAndPosN(eventList, index, N):
    eventSize = lt.size(eventList)
    preEvent = lt.subList(eventList, 1, index)
    posEvent = lt.subList(eventList,index+1, eventSize-index) if index < eventSize else lt.newList()
    preList = lt.subList(preEvent, lt.size(preEvent)-N+1, N) if lt.size(preEvent) > N else preEvent
    posList = lt.subList(posEvent, 1, N) if lt.size(posEvent) > N else posEvent
    for seismicEvent in lt.iterator(posList):
        lt.addLast(preList, seismicEvent)
    return preList

def getIntervals(featureTree, N):
    gap = (om.maxKey(featureTree)-om.minKey(featureTree))/N
    intervals = []
    for i in range(N):
        intervals.append((round((om.minKey(featureTree) + gap*i),2), round((om.minKey(featureTree) + gap*(i+1)),2)))
    return intervals

def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass

def dataSize(dataStructs):
    return lt.size(dataStructs["seismicEvents"])

def req_1(dataStructs, date1, date2):
    events = lt.newList("ARRAY_LIST")
    filtered = lt.newList('ARRAY_LIST')
    dateTree = dataStructs["seismicEventsByDate"]
    initialDate = datetime.strptime(date1,"%Y-%m-%dT%H:%M")
    finalDate = datetime.strptime(date2,"%Y-%m-%dT%H:%M")
    dates = om.keys(dateTree, initialDate, finalDate)
    metaData = {"totalDates": lt.size(dates), "totalSeismicEvents": 0}
    for date in lt.iterator(dates):
        seismicEvents = me.getValue(om.get(dateTree, date))
        for seismicEvent in lt.iterator(seismicEvents):
            lt.addLast(events, seismicEvent)
        date = datetime.strftime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        datum = {'time': date, 'events': lt.size(seismicEvents), 'details': sortData(seismicEvents, compareByDateDescending)}
        lt.addLast(filtered, datum)
        metaData['totalSeismicEvents'] += lt.size(seismicEvents)
    sortData(filtered, compareByDateDescending)
    metaData["map"] = lt.size(events) > 0
    metaData["path"] = "req_1"
    req_8(events, "req_1")
    return filtered, metaData

def req_2(dataStructs, inferiorMagLimit, superiorMagLimit):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    events = lt.newList("ARRAY_LIST")
    filtered = lt.newList("ARRAY_LIST")
    magTree = dataStructs["seismicEventsByMag"]
    magKeys = om.keys(magTree, inferiorMagLimit, superiorMagLimit)
    metaData = {"totalMagnitudes": lt.size(magKeys) ,"totalSeismicEvents": 0}
    for magKey in lt.iterator(magKeys):
        seismicEvents = me.getValue(om.get(magTree, magKey))["seismicEvents"]
        for seismicEvent in lt.iterator(seismicEvents):
            lt.addLast(events, seismicEvent)
        datum = {"mag": magKey, "events": lt.size(seismicEvents), "details": sortData(seismicEvents, compareByDateDescending)}
        lt.addLast(filtered, datum)
        metaData["totalSeismicEvents"] += lt.size(seismicEvents)
    sortData(filtered, compareByMag)
    metaData["map"] = lt.size(events) > 0
    metaData["path"] = "req_2"
    req_8(events, "req_2")
    return filtered, metaData

def req_3(dataStructs, minMag, maxDepth):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    events = lt.newList("ARRAY_LIST")
    filtered = lt.newList("ARRAY_LIST")
    magTree = dataStructs["seismicEventsByMag"]
    magNodes = om.values(magTree, minMag, om.maxKey(magTree))
    dateMap = mp.newMap(200, maptype= "PROBING")
    metaData = {"totalEventsBetweenDates": 0}
    for magNode in lt.iterator(magNodes):
        depthTree = magNode["seismicEventsByDepth"]
        depthLists = om.values(depthTree, om.minKey(depthTree), maxDepth)
        for depthList in lt.iterator(depthLists):
            for seismicEvent in lt.iterator(depthList):
                addEventToSimpleMap(dateMap, seismicEvent, "time")
                lt.addLast(events, seismicEvent)
    for dateKey in lt.iterator(mp.keySet(dateMap)):
        dateList = me.getValue(mp.get(dateMap, dateKey))
        metaData["totalEventsBetweenDates"] += lt.size(dateList)
        datum = {"time": dateKey, "events": lt.size(dateList), "details": sortData(dateList, compareByMag)}
        lt.addLast(filtered, datum)
    metaData["totalDifferentDates"] = mp.size(dateMap)
    sortData(filtered, compareByNumber)
    metaData["map"] = lt.size(events) > 0
    metaData["path"] = "req_3"
    req_8(events, "req_3")
    return getNData(filtered, 10), metaData

def req_4(dataStructs, minSig, maxGap):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    events = lt.newList("ARRAY_LIST")
    filtered = lt.newList("ARRAY_LIST")
    sigTree = dataStructs["seismicEventsBySig"]
    sigNodes = om.values(sigTree, minSig, om.maxKey(sigTree))
    dateMap = mp.newMap(200, maptype="PROBING")
    metaData = {"totalEventsBetweenDates": 0}
    for sigNode in lt.iterator(sigNodes):
        gapTree = sigNode["seismicEventsByGap"]
        gapLists = om.values(gapTree, om.minKey(gapTree), maxGap)
        for gapList in lt.iterator(gapLists):
            for seismicEvent in lt.iterator(gapList):
                addEventToSimpleMap(dateMap, seismicEvent, "time")
                lt.addLast(events, seismicEvent)
    for dateKey in lt.iterator(mp.keySet(dateMap)):
        dateList = me.getValue(mp.get(dateMap, dateKey))
        metaData["totalEventsBetweenDates"] += lt.size(dateList)
        datum = {"time": dateKey, "events": lt.size(dateList), "details": dateList}
        lt.addLast(filtered, datum)
    metaData["totalDifferentDates"] = mp.size(dateMap)
    metaData["map"] = lt.size(events) > 0
    metaData["path"] = "req_4"
    sortData(filtered, compareByNumber)
    req_8(events, "req_4")
    return getNData(filtered, 15), metaData

def req_5(dataStructs, minDepth, minNst):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    events = lt.newList("ARRAY_LIST")
    filtered = lt.newList("ARRAY_LIST")
    depthTree = dataStructs["seismicEventsByDepth"]
    depthNodes = om.values(depthTree, minDepth, om.maxKey(depthTree))
    dateMap = mp.newMap(200, maptype= "PROBING")
    metaData = {"totalDifferentDates": 0, "totalEventsBetweenDates": 0}
    for depthNode in lt.iterator(depthNodes):
        nstTree = depthNode["seismicEventsByNst"]
        nstLists = om.values(nstTree, minNst, om.maxKey(nstTree))
        for nstList in lt.iterator(nstLists):
            for seismicEvent in lt.iterator(nstList):
                addEventToSimpleMap(dateMap, seismicEvent, "time")
                lt.addLast(events, seismicEvent)
    for dateKey in lt.iterator(mp.keySet(dateMap)):
        dateList = me.getValue(mp.get(dateMap, dateKey))
        metaData["totalEventsBetweenDates"] += lt.size(dateList)
        datum = {"time": dateKey, "events": lt.size(dateList), "details": dateList}
        lt.addLast(filtered, datum)
    metaData["totalDifferentDates"] = mp.size(dateMap)
    sortData(filtered, compareByNumber)
    metaData["map"] = lt.size(events) > 0
    metaData["path"] = "req_5"
    req_8(events, "req_5")
    return getNData(filtered, 20), metaData

def req_6(dataStructs, year, lat, lon, r, N):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    filtered = lt.newList("ARRAY_LIST")
    metaData = {"highestEvent": lt.newList(), "maxNPossibleEvents": N*2, "totalEvents": 0}
    eventsInRange = lt.newList("ARRAY_LIST")
    center = (float(lat), float(lon))
    highestSigEvent = {"sig": 0}
    yearMap = dataStructs["seismicEventsByYear"]
    entry = mp.get(yearMap, year)
    if entry:
        seismicEvents = me.getValue(entry)["seismicEvents"]
        for seismicEvent in lt.iterator(seismicEvents):
            distance = haversine(center, (float(seismicEvent["lat"]), float(seismicEvent["long"])))
            if distance <= float(r):
                lt.addLast(eventsInRange, seismicEvent)
                if float(seismicEvent["sig"]) > float(highestSigEvent["sig"]):
                    highestSigEvent = seismicEvent
    sortData(eventsInRange, compareByDateAscending)
    dateMap = mp.newMap(200, maptype= "PROBING")
    for seismicEvent in lt.iterator(getPreAndPosN(eventsInRange, getIndex(eventsInRange, highestSigEvent), N)):
        addEventToSimpleMap(dateMap,seismicEvent, "time")
    for dateKey in lt.iterator(mp.keySet(dateMap)):
        dateList = me.getValue(mp.get(dateMap, dateKey))
        metaData["totalEvents"] += lt.size(dateList)
        datum = {"time": dateKey, "events": lt.size(dateList), "details": dateList}
        lt.addLast(filtered, datum)
    lt.addLast(metaData["highestEvent"], highestSigEvent)
    metaData["differentDates"] = mp.size(dateMap)
    metaData["eventsInRange"] = lt.size(eventsInRange)
    metaData["map"] = lt.size(eventsInRange) > 0
    metaData["path"] = "req_6"
    req_8(eventsInRange, "req_6", r, (lat, lon))
    return sortData(filtered, compareByDateAscending), metaData

def req_7(dataStructs, year, place, feature, N):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    filtered = lt.newList()
    histogram = None
    yearMap = dataStructs["seismicEventsByYear"]
    entry = mp.get(yearMap, year)
    metaData = {}
    if entry:
        placeMap = me.getValue(entry)["seismicEventsByPlace"]
        entry = mp.get(placeMap, place)
        if entry:
            featureTree = me.getValue(entry)[feature]
            filtered = me.getValue(entry)["seismicEvents"]
            intervalList = getIntervals(featureTree, N)
            featureCounters = []
            for interval in intervalList:
                featureLists = om.values(featureTree, interval[0], interval[1])
                eventsCounter = 0
                for featureList in lt.iterator(featureLists):
                    eventsCounter += lt.size(featureList)
                featureCounters.append(eventsCounter)
            histogram = {"x": [str(interval) for interval in intervalList], "y": featureCounters, "title": f'Histogram of {feature} in {place} in {year}', "tableTitle": f'Event details in {place} in {year}', "yLabel": 'Numero de eventos', "xLabel": feature}
    metaData["map"] = lt.size(filtered) > 0
    metaData["path"] = "req_7"
    req_8(filtered, "req_7")
    return sortData(filtered, compareByDateAscending), histogram, metaData


def req_8(events, path, radius=False, center=None):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    eventsMap = folium.Map((0, 0), zoom_start= 2)
    mark = MarkerCluster()
    for event in lt.iterator(events):
        mark.add_child(folium.Marker((event["lat"], event["long"]), popup= createPopUp(event)))
    if radius and center:
        folium.Circle(center, radius*1000, color= "red").add_to(eventsMap)
    eventsMap.add_child(mark)
    eventsMap.save(f'{path}.html')



# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

def compareByDateDescending(registerA, registerB):
    dateA = datetime.strptime(registerA['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    dateB = datetime.strptime(registerB['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    return dateA > dateB

def compareByDateAscending(registerA, registerB):
    dateA = datetime.strptime(registerA['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    dateB = datetime.strptime(registerB['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    return dateA < dateB

def compareByNumber(registerA, registerB):
    return registerA["time"] > registerB["time"]

def compareByNumberAscending(registerA, registerB):
    return registerA["time"] < registerB["time"]

def compareByMag(registerA, registerB):
    return float(registerA["mag"]) > float(registerB["mag"])

def compareBySig(registerA, registerB):
    return registerA["sig"] > registerB["sig"]

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


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass

def sortData(data, cmp_function):
    return sa.sort(data, cmp_function)

def createPopUp(register):
    popUp = '<p class="fs-5" style="color: #03a7bb;">Earthquake Details</p>'
    for key, value in register.items():
        popUp += f'<p><span class="fw-bold" style="color: #03a7bb;">{key.title()}:</span> {str(value).title() if value != "" else "Unavailable"}</p>'
    return f'<div style="width: 200px;">{popUp}</div>'