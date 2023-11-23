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
from datetime import datetime, timedelta
from tabulate import tabulate
import re
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
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
    control = {'temblores': None,
                'ArbolFechas': None,
                'ArbolMagnitudes': None,
                }
    control['temblores'] = lt.newList(datastructure='ARRAY_LIST')
    control['ArbolFechas'] = om.newMap(omaptype='RBT',
                                      cmpfunction=compareDates)
    control['ArbolMagnitudes'] = om.newMap(omaptype='RBT',
                                      cmpfunction=compareMargnitudes)
    
    control['ArbolSignificancia'] = om.newMap(omaptype='RBT',
                                      cmpfunction=compareSignificancia)
    
    control['depthTree'] = om.newMap(omaptype='RBT',
                                      cmpfunction=compareDepth)

    control['mapYears'] = mp.newMap(50,
                             maptype="CHAINING",
                             loadfactor=4)
    
    
    
    
    return control


# Funciones para agregar informacion al modelo

def add_Temblores(control, temblor):
    date_registro = temblor["time"]
    date_registro = datetime.strptime(date_registro, '%Y-%m-%dT%H:%M:%S.%fZ')
    if date_registro.second >= 30:
        date_registro += timedelta(seconds=60 - date_registro.second)
    if date_registro.minute == 59:
        date_registro += timedelta(hours=1)
    else:
        date_registro = date_registro.replace(second=0)
    date_registro = date_registro.strftime('%Y-%m-%d %H:%M')
    date_registro = datetime.strptime(date_registro, '%Y-%m-%d %H:%M')
    datos_temblor_lista = new_data_lista(temblor, date_registro)
    datos_temblor = new_data_mapa(temblor, date_registro)
    lt.addLast(control["temblores"], datos_temblor_lista)
    try:    
        ExistDate = om.contains(control["ArbolFechas"], date_registro)
        if ExistDate == True:
            entry = om.get(control["ArbolFechas"], date_registro)
            temblor_i = me.getValue(entry)
        else:
            temblor_i = lt.newList(datastructure="ARRAY_LIST")
            mp.put(control["ArbolFechas"], date_registro, temblor_i)
        lt.addLast(temblor_i, datos_temblor)
    except Exception:
        return None

def add_TembloresMagnitudes(control, temblor):
    magnitud = temblor["mag"]
    date_registro = temblor["time"]
    date_registro = datetime.strptime(date_registro, '%Y-%m-%dT%H:%M:%S.%fZ')
    if date_registro.second >= 30:
        date_registro += timedelta(seconds=60 - date_registro.second)
    if date_registro.minute == 59:
        date_registro += timedelta(hours=1)
    else:
        date_registro = date_registro.replace(second=0)
    date_registro = date_registro.strftime('%Y-%m-%d %H:%M')
    date_registro = datetime.strptime(date_registro, '%Y-%m-%d %H:%M')
    datos_temblor = new_data_mapa(temblor, date_registro)
    try:    
        ExistDate = om.contains(control["ArbolMagnitudes"], magnitud)
        if ExistDate == True:
            entry = om.get(control["ArbolMagnitudes"], magnitud)
            temblor_i = me.getValue(entry)
        else:
            temblor_i = lt.newList(datastructure="ARRAY_LIST")
            mp.put(control["ArbolMagnitudes"], magnitud, temblor_i)
        lt.addLast(temblor_i, datos_temblor)
    except Exception:
        return None

def add_TembloresSignificancia(control, temblor):
    significancia = float(temblor["sig"])
    date_registro = temblor["time"]
    date_registro = datetime.strptime(date_registro, '%Y-%m-%dT%H:%M:%S.%fZ')
    if date_registro.second >= 30:
        date_registro += timedelta(seconds=60 - date_registro.second)
    if date_registro.minute == 59:
        date_registro += timedelta(hours=1)
    else:
        date_registro = date_registro.replace(second=0)
    date_registro = date_registro.strftime('%Y-%m-%d %H:%M')
    date_registro = datetime.strptime(date_registro, '%Y-%m-%d %H:%M')
    datos_temblor = new_data_mapa(temblor, date_registro)
    try:    
        ExistDate = om.contains(control["ArbolSignificancia"], significancia)
        if ExistDate == True:
            entry = om.get(control["ArbolSignificancia"], significancia)
            temblor_i = me.getValue(entry)
        else:
            temblor_i = lt.newList(datastructure="ARRAY_LIST")
            mp.put(control["ArbolSignificancia"], significancia, temblor_i)
        lt.addLast(temblor_i, datos_temblor)
    except Exception:
        return None
    
def add_temblor(control, earthquake):
    
    earthquakecopy = earthquake.copy()
    
    if earthquakecopy['nst'] == '' or earthquakecopy['nst'] == ' ' or earthquakecopy['nst'] == None:
        earthquakecopy['nst'] = '-2000'
        
    if earthquakecopy['gap'] == '' or earthquakecopy['gap'] == ' ' or earthquakecopy['gap'] == None:
        earthquakecopy['gap'] = 'unknown'    
    if earthquakecopy['cdi'] == '' or earthquakecopy['cdi'] == ' ' or earthquakecopy['cdi'] == None:
        earthquakecopy['cdi'] = 'unknown'
    if earthquakecopy['mmi'] == '' or earthquakecopy['nst'] == ' ' or earthquakecopy['nst'] == None:
        earthquakecopy['mmi'] = 'unknown'
    
    newtime = earthquakecopy['time'][:16]
    
    earthquakecopy['time'] = newtime    
    updateDateIndex(control['depthTree'], earthquakecopy)

def updateDateIndex(map, earthquake):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
        
    depth = earthquake["depth"]
    entry = om.get(map, depth)
    if entry is None:
        datentry = newDataEntry(earthquake)
        om.put(map, depth, datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, earthquake)
    
    return map

def addDateIndex(datentry, earthquake):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry["lstearthquakes"]
    lt.addLast(lst, earthquake)
    nstIndex = datentry["nstIndex"]
    offentry = om.get(nstIndex, earthquake["nst"])
    if (offentry is None):
        entry = newNstEntry(earthquake["nst"], earthquake)
        lt.addLast(entry["lstearthquakes"], earthquake)
        om.put(nstIndex, earthquake["nst"], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry["lstearthquakes"], earthquake)
    return datentry

def newNstEntry(nst, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {"nst": None, "lstearthquakes": None}
    ofentry["nst"] = nst
    ofentry["lstearthquakes"] = lt.newList("ARRAY_LIST")
    
    return ofentry


def newDataEntry(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {"nstIndex": None, "lstearthquakes": None}
    entry["nstIndex"] = om.newMap(omaptype='RBT',
                                      cmpfunction= compareDepth)

    entry["lstearthquakes"] = lt.newList("SINGLE_LINKED", compareDepth)
    lt.addLast(entry["lstearthquakes"], crime)
    return entry

def add_MapYears(football_data, datos, year):
    dates = football_data['mapYears']
    ExistDate = mp.contains(dates, year)
    if ExistDate == True:
        entry = mp.get(dates, year)
        torneo_i = me.getValue(entry)
    else:
        torneo_i = newDateEntry(year)
        mp.put(dates, year , torneo_i)
    lt.addLast(torneo_i['datos'], datos )

def newDateEntry(date):
    entry = {}
    entry['date'] = date
    entry['datos'] = lt.newList('ARRAY_LIST')
    return entry




    
# Funciones para creacion de datos
def new_data_lista(info, date_registro):
    """
    Crea una nueva estructura para modelar los datos
    """
    data={}
    headers=["code","time","lat","long","mag","title","depth","felt","cdi","mmi","tsunami"]
    for header in headers:
        data[header]=info[header]
    data["time"] = date_registro
    if data["tsunami"] == "0":
        data["tsunami"] = "False"
    return data

def new_data_mapa(info, date_registro):
    """
    Crea una nueva estructura para modelar los datos
    """
    data={}
    headers=["time","mag","lat","long","depth","sig","gap","nst","title","cdi","mmi","magType", "type", "code"]
    for header in headers:
        data[header]=info[header]
    data["time"] = date_registro
    if data["cdi"] == "":
        data["cdi"] = "Unavailable"
    if data["mmi"] == "":
        data["mmi"] = "Unavailable"
    if data["gap"] == "":
        data["gap"] = "0"
    if data["nst"] == "":
        data["nst"] = "1"
    return data

def get_firts_and_last_5(model):
    primeros = lt.subList(model['temblores'],1, 5)
    ultimos = lt.subList(model['temblores'],lt.size(model['temblores'])-4,5)
    datos = (ultimos,primeros)
    results = [None,None,None,None,None,None,None,None,None,None]
    for i in range(1,6):
            results[5-i] = get_datos(datos[0],i)
            results[10-i] = get_datos(datos[1],i)
    return results  

def get_datos(datos, pos):
    valores_lista = [valor for valor in lt.getElement(datos,pos).values()]
    for i, valor in enumerate(valores_lista):
        if valor == "":
            valores_lista[i] = 'Unknown'
    return valores_lista
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


def req_1(control, fecha_inicial, fecha_final):
    """
    Función que soluciona el requerimiento 1
    """
    fecha_inicial = datetime.strptime(fecha_inicial, '%Y-%m-%dT%H:%M')
    fecha_final = datetime.strptime(fecha_final, '%Y-%m-%dT%H:%M') 
    results = om.values(control['ArbolFechas'], fecha_inicial, fecha_final)
    lista = lt.newList(datastructure='ARRAY_LIST')
    for temblor_i in lt.iterator(results):
        size = lt.size(temblor_i)
        if size > 1:
            for temblor_e in lt.iterator(temblor_i):
                lt.addLast(lista, temblor_e)
        else:
            lt.addLast(lista, temblor_i)
    return lista

def req_2(data_structs, min_mag, max_mag):
    """
    Función que soluciona el requerimiento 2
    """
    min_mag = str(float(min_mag))
    max_mag = str(float(max_mag))
    lista = om.values(data_structs['ArbolMagnitudes'], min_mag, max_mag)
    diferent_mag = lt.size(lista)
    total_events = 0
    for lista_i in lt.iterator(lista):
        total_events += lt.size(lista_i)
    primeros = lt.subList(lista, 1, 3)
    ultimos = lt.subList(lista, lt.size(lista)-2, 3)
    lista_grande = lt.newList(datastructure='ARRAY_LIST')
    for i in range(1,4):
        lt.addLast(lista_grande, [lt.getElement(lt.getElement(primeros,i), 1)['mag'], lt.size(lt.getElement(primeros,i)), ''])
    for i in range(1,4):
        lt.addLast(lista_grande, [lt.getElement(lt.getElement(ultimos,i), 1)['mag'], lt.size(lt.getElement(ultimos,i)), ''])
    sub_lista = lt.newList(datastructure='ARRAY_LIST')
    for i in range(1,4):
        primeros_i = quk.sort(lt.getElement(primeros,i),sort_criteria)
        lt.addLast(sub_lista, primeros_i)
    for i in range(1,4):
        ultimos_i = quk.sort(lt.getElement(ultimos,i),sort_criteria)
        lt.addLast(sub_lista, ultimos_i)
    return lista_grande, sub_lista, diferent_mag, total_events


def req_3(data_structs, mag_min, prof_max):
    """
    Función que soluciona el requerimiento 3
    """
    mag_max = om.maxKey(data_structs['ArbolMagnitudes'])
    lista = om.values(data_structs['ArbolMagnitudes'], mag_min, mag_max)
    prof_max = int(float(prof_max))
    temblores = lt.newList(datastructure='ARRAY_LIST')
    for magnitud in lt.iterator(lista):
        for temblor in lt.iterator(magnitud):
            prof_i = int(float(temblor['depth']))
            if prof_i <= prof_max:
                lt.addLast(temblores, temblor)
    temblores_ordenado = quk.sort(temblores, sort_criteria)
    return temblores_ordenado

def req_4(data_structs,sig,gap):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    
    lista_acorde_sig = om.values(data_structs["ArbolSignificancia"],sig,float(om.maxKey(data_structs["ArbolSignificancia"])))
    arbolAsimutal = om.newMap(omaptype='RBT',
                                      cmpfunction=compareAzimutal)
    for i in lt.iterator(lista_acorde_sig):
        for o in lt.iterator(i):
            ArbolDistanciaAzimutal(arbolAsimutal,o)
    lista_acorde_sig_gap = om.values(arbolAsimutal,gap,float(om.maxKey(arbolAsimutal)))
    arbolFechas =  om.newMap(omaptype='RBT',
                                      cmpfunction=compareDates)
    for i in lt.iterator(lista_acorde_sig_gap):
        for o in lt.iterator(i):
            ArbolFechas(arbolFechas,o)
    numero_eventos = om.size(arbolFechas)
    ultimos_15 = lt.newList("ARRAY_LIST")
    while lt.size(ultimos_15)<15 and not om.isEmpty(arbolFechas):
        max = om.get(arbolFechas,om.maxKey(arbolFechas))
        lt.addLast(ultimos_15,me.getValue(max))
        om.remove(arbolFechas,om.maxKey(arbolFechas))
        
    para_printear = lt.newList("ARRAY_LIST")
    if lt.size(ultimos_15)<=6:
        for i in lt.iterator(ultimos_15):
            dato = {"time":lt.getElement(i,1)["time"],
                    "events":lt.size(i),
                    "details":ArmarDetailReq4(i)
            }
            lt.addLast(para_printear,dato)
    else:
        for i in range(1,4):
            temblor = lt.getElement(ultimos_15,i)
            dato = {"time":lt.getElement(temblor,1)["time"],
                    "events":lt.size(temblor),
                    "details":ArmarDetailReq4(temblor)
            }
            lt.addLast(para_printear,dato)
        for i in range(lt.size(ultimos_15)-2,lt.size(ultimos_15)+1):
            temblor = lt.getElement(ultimos_15,i)
            dato = {"time":lt.getElement(temblor,1)["time"],
                    "events":lt.size(temblor),
                    "details":ArmarDetailReq4(temblor)
            }
            lt.addLast(para_printear,dato)
    return para_printear , numero_eventos


def ArmarDetailReq4(temblores):
    data_tabla = lt.newList("ARRAY_LIST")
    for i in lt.iterator(temblores):
        dato = {
            "mag":i["mag"],
            "lat":i["lat"],
            "long":i["long"],
            "depth":i["depth"],
            "sig":i["sig"],
            "gap":i["gap"],
            "nst":i["nst"],
            "title":i["title"],
            "cdi":i["cdi"],
            "mmi":i["mmi"],
            "magType":i["magType"],
            "type":i["type"],
            "code":i["code"],
        }
        lt.addLast(data_tabla,dato)
    quk.sort(data_tabla,CriterioArmarDetailReq4)
    tabla = tabulate(data_tabla["elements"], "keys", tablefmt="grid")
        
    return tabla
def CriterioArmarDetailReq4(dato1,dato2):
    if dato1["nst"] == None:
        dato1["nst"] = 0
    if dato2["nst"] == None:
        dato2["nst"] = 0
        
    if dato1["nst"]<dato2["nst"]:
        return True
    else:
        return False


def ArbolFechas(arbol, temblor):
    fecha = temblor["time"]
    
    try:    
        ExistDate = om.contains(arbol, fecha)
        if ExistDate == True:
            entry = om.get(arbol, fecha)
            temblor_i = me.getValue(entry)
            lt.addLast(temblor_i, temblor)

        else:
            temblor_i = lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(temblor_i, temblor)
            mp.put(arbol, fecha, temblor_i)
    except Exception:
        return None 
  
def ArbolDistanciaAzimutal(arbol, temblor):
    if temblor["gap"] ==None:
        temblor["gap"] = 0
    DistanciaAzimutal = float(temblor["gap"])

    try:    
        ExistAz = om.contains(arbol, DistanciaAzimutal)
        if ExistAz == True:
            entry = om.get(arbol, DistanciaAzimutal)
            temblor_i = me.getValue(entry)
        else:
            temblor_i = lt.newList(datastructure="ARRAY_LIST")
            mp.put(arbol, DistanciaAzimutal, temblor_i)
        lt.addLast(temblor_i, temblor)
    except Exception:
        return None  


def req_5(data_structs, depthMin, nstMin):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    
    map = data_structs['depthTree']
    solucion = lt.newList('ARRAY_LIST')

    
    lstDepths = om.values(map, depthMin, om.maxKey(map) )
    
    for entry in lt.iterator(lstDepths):
        nstIndex = entry['nstIndex']
        Lstnst = om.values(nstIndex, nstMin, om.maxKey(nstIndex))
        for entrynst in lt.iterator(Lstnst):
            listanst = entrynst['lstearthquakes']
            for terremoto in lt.iterator(listanst):
                lt.addLast(solucion, terremoto)
        
    sortedsolution =   quk.sort(solucion, sort_criteria_REQ5)
    
    if lt.size(sortedsolution) > 20:
        FinalSolution = lt.subList(sortedsolution, 1,20)
    else:
        FinalSolution = sortedsolution

    #Creación de la tabla de respuetsas
    if lt.size(FinalSolution)> 6:
        FinalSolution= FirstandALst(FinalSolution)
        
    
    SolutionTable = lt.newList('ARRAY_LIST')

    for earthquake in lt.iterator(FinalSolution):
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
            'gap': round(float(earthquake['gap']), 3) if earthquake['gap'] != 'unknown' else earthquake['gap'],
            'nst': round(float(earthquake['nst']), 3),
            'title': earthquake['title'],
            'cdi': round(float(earthquake['cdi']), 3) if earthquake['cdi'] != 'unknown' else earthquake['cdi'],
            'mmi': round(float(earthquake['mmi']), 3) if earthquake['mmi'] != 'unknown' else earthquake['mmi'],
            'magType': earthquake['magType'],
            'type': earthquake['type'],
            'code': earthquake['code']
        }

        infoearthquake['details'] = tabulate([detailsearthquake], headers='keys', tablefmt="grid")
        lt.addLast(SolutionTable, infoearthquake)

    solutionElements = SolutionTable['elements']
    SolutionTableF = tabulate(solutionElements, headers='keys', tablefmt="grid")

    return SolutionTableF, lt.size(solucion)


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

def req_6(data_structs, year, latRef, longRef, radio, n):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    mapYears = data_structs['mapYears']
    
    entry = mp.get(mapYears, year )
    earthquakesYear = me.getValue(entry)['datos']
    tembloresArea = lt.newList('ARRAY_LIST')
    
    for temblor in lt.iterator(earthquakesYear):
        if AreaPresent(latRef, longRef, float(temblor['lat']),   float(temblor['long']), radio ):
            temblor['distance'] = haversine(latRef, longRef, float(temblor['lat']),   float(temblor['long']))
            lt.addLast(tembloresArea, temblor)
    
    sortedAreas = quk.sort(tembloresArea, sort_criteria_REQ6)
    maxArea, posicion= encontrar_mayor_magnitud(sortedAreas)
    
    Sublista = obtener_sublista(sortedAreas, posicion, n)
    
    
    if lt.size(Sublista) <= 6:
        TablaMaxArea, TablaTopN = CreateTables(maxArea, Sublista)
    else:
        List6 = FirstandALst(Sublista)
        TablaMaxArea, TablaTopN = CreateTables(maxArea, List6)
    
    
    return TablaMaxArea, TablaTopN, lt.size(tembloresArea), lt.size(Sublista), maxArea



def CreateTables(maxArea, Sublista):
    
    if maxArea['gap'] == '' or maxArea['gap'] == ' ' or maxArea['gap'] == None:
        maxArea['gap'] = 'unknown'

    if maxArea['nst'] == '' or maxArea['nst'] == ' ' or maxArea['nst'] == None:
        maxArea['nst'] = 'unknown'

    if maxArea['cdi'] == '' or maxArea['cdi'] == ' ' or maxArea['cdi'] == None:
        maxArea['cdi'] = 'unknown'
    
    if maxArea['mmi'] == '' or maxArea['mmi'] == ' ' or maxArea['mmi'] == None:
        maxArea['mmi'] = 'unknown'
    
       
    maxAreaFormat = {
        'time': maxArea['time'][:16],
        'mag': round(float(maxArea['mag']), 3),
        'lat': round(float(maxArea['lat']), 3),
        'long': round(float(maxArea['long']), 3),
        'depth': round(float(maxArea['depth']), 3),
        'sig': round(float(maxArea['sig']), 3),
        'gap': round(float(maxArea['gap']), 3) if maxArea['gap'] != 'unknown' else maxArea['gap'],
        'distance': round(float(maxArea['distance']), 3 ),
        'nst': round(float(maxArea['nst']), 3) if maxArea['nst'] != 'unknown' else maxArea['nst'],
        'title': maxArea['title'],
        'cdi': round(float(maxArea['cdi']), 3) if maxArea['cdi'] != 'unknown' else maxArea['cdi'],
        'mmi': round(float(maxArea['mmi']), 3) if maxArea['mmi'] != 'unknown' else maxArea['mmi'],
        'magType': maxArea['magType'],
        'type': maxArea['type'],
        'code': maxArea['code']
        }

    maxAreaFormatT = [maxAreaFormat]
    TableMaxArea = tabulate(maxAreaFormatT, headers = 'keys', tablefmt='grid' )
    
    SolutionTable = lt.newList('ARRAY_LIST')

    for earthquake in lt.iterator(Sublista):
        
        if earthquake['gap'] == '' or earthquake['gap'] == ' ' or earthquake['gap'] == None:
            earthquake['gap'] = 'unknown'

        if earthquake['nst'] == '' or earthquake['nst'] == ' ' or earthquake['nst'] == None:
            earthquake['nst'] = 'unknown'

        if earthquake['cdi'] == '' or earthquake['cdi'] == ' ' or earthquake['cdi'] == None:
            earthquake['cdi'] = 'unknown'
    
        if earthquake['mmi'] == '' or earthquake['mmi'] == ' ' or earthquake['mmi'] == None:
            earthquake['mmi'] = 'unknown'
        
        
        infoearthquake = {
            'time': earthquake['time'][:16],
            'events': 1
        }
            
        detailsearthquake = {
            'mag': round(float(earthquake['mag']), 3),
            'lat': round(float(earthquake['lat']), 3),
            'long': round(float(earthquake['long']), 3),
            'depth': round(float(earthquake['depth']), 3),
            'sig': round(float(earthquake['sig']), 3),
            'gap': round(float(earthquake['gap']), 3) if earthquake['gap'] != 'unknown' else earthquake['gap'],
            'distance': round(float(earthquake['distance']), 3 ),
            'nst': round(float(earthquake['nst']), 3) if earthquake['nst'] != 'unknown' else earthquake['nst'],
            'title': earthquake['title'],
            'cdi': round(float(earthquake['cdi']), 3) if earthquake['cdi'] != 'unknown' else earthquake['cdi'],
            'mmi': round(float(earthquake['mmi']), 3) if earthquake['mmi'] != 'unknown' else earthquake['mmi'],
            'magType': earthquake['magType'],
            'type': earthquake['type'],
            'code': earthquake['code']
            }
        
        infoearthquake['details'] = tabulate([detailsearthquake], headers='keys', tablefmt="grid")
        lt.addLast(SolutionTable, infoearthquake)
        
    solutionElements = SolutionTable['elements']
    SolutionTableF = tabulate(solutionElements, headers='keys', tablefmt="grid")
    
    return TableMaxArea, SolutionTableF

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
        lt.addLast(sublista, lista[i] )

    # Agrega el elemento en la posición
    lt.addLast(sublista, lista[posicion])

    # Agrega los elementos hacia abajo de la posición
    for i in range(posicion + 1, min(posicion + n + 1, len(lista))):
        lt.addLast(sublista, lista[i])

    return sublista        

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

def AreaPresent(lat1, lon1, lat2, lon2, radio):
    return haversine(lat1, lon1, lat2, lon2) < radio
   
    


def req_7(data_structs, año, title, prop, bins):
    """
    Función que soluciona el requerimiento 7
    """
    bins_considerar = bins
    fecha_inicial = datetime.strptime(año, '%Y')
    fecha_final= datetime.strptime(str(int(año)+1), '%Y')
    fecha_inicial = fecha_inicial.replace(month=1, day=1, hour=0, minute=0)
    fecha_inicial = om.ceiling(data_structs['ArbolFechas'], fecha_inicial)
    fecha_final = fecha_final.replace(month=1, day=1, hour=0, minute=0)
    fecha_final = om.floor(data_structs['ArbolFechas'], fecha_final)
    lista_temblores = om.values(data_structs['ArbolFechas'], fecha_inicial, fecha_final)
    lista_filtrada = lt.newList(datastructure='ARRAY_LIST')
    max_prop = -1000
    min_prop = 1000
    for temblor_i in lt.iterator(lista_temblores):
        size = lt.size(temblor_i)
        if size > 1:
            for temblor_e in lt.iterator(temblor_i):
                title_e = temblor_e['title']
                match = re.search(r', (.+)$', title_e)
                if match:
                     region = match.group(1)
                prop_e = temblor_e[prop] 
                if region == title and prop_e != "":
                    lt.addLast(lista_filtrada, temblor_e)
                    prop_e = float(prop_e)
                    if prop_e > max_prop:
                        max_prop = prop_e
                    if prop_e < min_prop:
                        min_prop = prop_e
        else:
            title_i = temblor_i['elements'][0]['title']
            match = re.search(r', (.+)$', title_i)
            region = ''
            if match:
                region = match.group(1)
            prop_i = temblor_i['elements'][0][prop]
            if region == title and prop_i != "":
                lt.addLast(lista_filtrada, temblor_i['elements'][0])
                prop_i = float(prop_i)
                if prop_i > max_prop:
                    max_prop = prop_i
                if prop_i < min_prop:
                    min_prop = prop_i                
    tamaño = lt.size(lista_filtrada)
    dif = max_prop - min_prop
    rango_bins = round(dif/int(bins),2)
    if prop == 'mag':
        quk.sort(lista_filtrada, sort_criteria_mag)
    elif prop == 'sig':
        quk.sort(lista_filtrada, sort_criteria_sig)
    elif prop =='depth':
        quk.sort(lista_filtrada, sort_criteria_depht)
        
    contador_rango = min_prop
    datos = lt.newList("ARRAY_LIST")
    for i in lt.iterator(lista_filtrada):
        rango = str(round(contador_rango,2))+"-"+str(round(contador_rango+rango_bins,2))
        if float(i[prop]) >=round(contador_rango,2) and float(i[prop]) <=round(contador_rango+rango_bins,2):
            lt.addLast(datos,rango)
        else:
            contador_rango+=rango_bins
            rango = str(round(contador_rango,2))+"-"+str(round(contador_rango+rango_bins,2))
            lt.addLast(datos,rango)

    datos_tabla = datos["elements"]
    
    quk.sort(lista_filtrada,sort_criteria)
    tabla_detalles = lt.newList("ARRAY_LIST")
    if lt.size(lista_filtrada)>6:
        for i in range(1,4):
            detalles = lt.getElement(lista_filtrada,i)
            dato = {
                "time":detalles["time"],
                "lat":detalles["lat"],
                "long":detalles["long"],
                "title":detalles["title"],
                "code":detalles["code"],
                prop:detalles[prop],
            }
            lt.addLast(tabla_detalles,dato)
        for i in range(lt.size(lista_filtrada)-2,lt.size(lista_filtrada)+1):
            detalles = lt.getElement(lista_filtrada,i)
            dato = {
                "time":detalles["time"],
                "lat":detalles["lat"],
                "long":detalles["long"],
                "title":detalles["title"],
                "code":detalles["code"],
                prop:detalles[prop],
            }
            lt.addLast(tabla_detalles,dato)
    else:
        for detalles in lt.iterator(lista_filtrada):
            dato = {
                "time":detalles["time"],
                "lat":detalles["lat"],
                "long":detalles["long"],
                "title":detalles["title"],
                "code":detalles["code"],
                prop:detalles[prop],
            }
            lt.addLast(tabla_detalles,dato)
    histograma = plt.hist(datos_tabla, bins = int(bins_considerar), color = "darkseagreen",edgecolor = "black",linewidth = 2, rwidth=0.8)
    
    
    
    tabla_texto = tabulate(tabla_detalles["elements"], headers='keys', tablefmt='fancy_grid')
    


    return tamaño , histograma , tabla_texto


    
def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compareDates(date1, date2):
    """
    Función encargada de comparar dos datos
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareMargnitudes(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
    
def compareSignificancia(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareAzimutal(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 < date2):
        return 1
    else:
        return -1
    

def compareDepth(date1, date2):
    date1 = float(date1)
    date2 = float(date2)
    
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
    
 # Funciones de ordenamiento
 
def sort_criteria_REQ6(date_1, date_2):
    formato = "%Y-%m-%dT%H:%M:%S.%fZ"
    
    if datetime.strptime(date_1["time"], formato) < datetime.strptime(date_2['time'], formato):
        return True
    elif datetime.strptime(date_1["time"], formato) == datetime.strptime(date_2['time'], formato):
        if date_1['mag'] > date_2['mag']:
            return True
        else:
            return False
    
    return False

def sort_criteria_REQ5(date_1, date_2):
    formato = "%Y-%m-%dT%H:%M"
    
    if datetime.strptime(date_1["time"], formato) > datetime.strptime(date_2['time'], formato):
        return True
    elif datetime.strptime(date_1["time"], formato) == datetime.strptime(date_2['time'], formato):
        if date_1['mag'] > date_2['mag']:
            return True
        else:
            return False
    
    return False
    

        
    
def sort_criteria_depht(date_1, date_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    date_1 = date_1["depth"]
    date_2 = date_2["depth"]
    if date_1 < date_2:
        return True
    else: 
        return False
    
def sort_criteria_sig(date_1, date_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    date_1 = date_1["sig"]
    date_2 = date_2["sig"]
    if date_1 < date_2:
        return True
    else: 
        return False
        
def sort_criteria_mag(date_1, date_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    date_1 = date_1["mag"]
    date_2 = date_2["mag"]
    if date_1 <= date_2:
        return True
    else: 
        return False
    
def sort_criteria(date_1, date_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    date_1 = date_1["time"]
    date_2 = date_2["time"]
    if date_1 < date_2:
        return True
    else: 
        return False


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    sub_list = lt.subList(data_structs["temblores"],1,lt.size(data_structs["temblores"]))
    quk.sort(sub_list, sort_criteria)
    data_structs["temblores"] = sub_list

