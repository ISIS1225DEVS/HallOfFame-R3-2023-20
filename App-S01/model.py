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
import datetime
from tabulate import tabulate
import matplotlib.pyplot as pl
assert cf
from haversine import haversine, Unit #as hv


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_historial_sismico():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    historial_sismico = {"sismos": None, 
                         "fechas_req1": None,
                         "sig_req4": None,
                         "anios":None, 
                         "magnitudes_req2": None,
                         "profundidades_req5": None}
    historial_sismico["sismos"] = lt.newList("ARRAY_LIST") #Esto es solo lo que se imprimirá en la carga de datos, no hace falta ordenar.
    #historial_sismico["datos_req_1"]=lt.newList("ARRAY_LIST") #Aquí se almacena más información de los sismos que en la lista "sismos"
    historial_sismico["fechas_req1"]= om.newMap(omaptype = 'RBT',  cmpfunction= compare_arbol)
    historial_sismico["sig_req4"] = om.newMap(omaptype="RBT", cmpfunction=compare_sig)
    historial_sismico["anios"]= om.newMap(omaptype="RBT")
    historial_sismico["magnitudes_req2"]= om.newMap(omaptype = 'RBT',  cmpfunction= compare_mag)
    historial_sismico["profundidades"]= om.newMap(omaptype= "RBT")
                                                 # cmpfunction=compare_prof)
    return historial_sismico


# Funciones para agregar informacion al modelo

def add_temblor(historial_sismico, temblor):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    temblor_1 = new_temblor(temblor)
    lt.addLast(historial_sismico["sismos"], temblor_1)
    fechasreq1(historial_sismico, temblor)
    add_temblor_req4(historial_sismico, temblor)
    add_anios_req6(historial_sismico, temblor)
    mag_req2( historial_sismico, temblor)
    add_prof_req_5(historial_sismico, temblor)
    
    return historial_sismico

def add_temblor_req4(historial_sismico, temblor):
    temblor = new_datos(temblor)
    sig_info = om.get(historial_sismico["sig_req4"], float(temblor["sig"]))
    if sig_info:
        sig_info = me.getValue(sig_info)
    else:
        sig_info  = lt.newList()
        om.put(historial_sismico["sig_req4"], float(temblor["sig"]), sig_info)
    lt.addLast(sig_info, temblor)
    
    return historial_sismico  
"""""
def add_datos (historial_sismico, dato):

    dato= new_datos(dato)
    lt.addLast(historial_sismico["datos_req_1"], dato)
    return historial_sismico
"""""
def add_anios_req6(historial_sismico, temblor):
    anio_info = om.get(historial_sismico["anios"], temblor["time"][:4])
    if anio_info:
        anio_info = me.getValue(anio_info)
    else:
        anio_info = new_anio()
        om.put(historial_sismico["anios"], temblor["time"][:4], anio_info)
    add_region(anio_info, temblor)
    add_lat_long(anio_info,temblor)
    
    return historial_sismico

def add_lat_long(anio_info, temblor):
    latitud= round(float(temblor["lat"]), 3)
    longitud= round(float(temblor["long"]), 3)
    tupla= (latitud, longitud)
    temblor = new_dato_con_distancia_req_6(temblor)
    lat_long_info= mp.get(anio_info["lat_long"], tupla)
    if lat_long_info: 
        lat_long_info= me.getValue(lat_long_info)
    else: 
        lat_long_info = lt.newList()
        mp.put(anio_info["lat_long"],tupla, lat_long_info)
    lt.addLast(lat_long_info, temblor)
    return anio_info
    
def add_region(anio_info, temblor):
    if "," in temblor["title"]:
        region = temblor["title"].split(",")[1].strip()
    else:
        region = temblor["title"].split("-")[1].strip()
    region_info = mp.get(anio_info["regiones"], region)
    if region_info:
        region_info = me.getValue(region_info)
    else:
        region_info = new_region()
        mp.put(anio_info["regiones"], region, region_info)
    if temblor["mag"] != "":
        temblor_mag = new_temblor_mag(temblor)
        mag_info = om.get(region_info["mag"], round(float(temblor["mag"]),3))
        if mag_info:
            mag_info = me.getValue(mag_info)
        else:
            mag_info = lt.newList()
            om.put(region_info["mag"], round(float(temblor["mag"]),3), mag_info)
        lt.addLast(mag_info, temblor_mag)
        
    if temblor["depth"] != "":
        temblor_depth = new_temblor_depth(temblor)
        depth_info = om.get(region_info["depth"], round(float(temblor["depth"]),3))
        if depth_info:
            depth_info = me.getValue(depth_info)
        else:
            depth_info = lt.newList()
            om.put(region_info["depth"], round(float(temblor["depth"]),3), depth_info)
        lt.addLast(depth_info, temblor_depth)
        
    if temblor["sig"] != "":
        temblor_sig = new_temblor_sig(temblor)
        sig_info = om.get(region_info["sig"], round(float(temblor["sig"]) ,3))
        if sig_info:
            sig_info = me.getValue(sig_info)
        else:
            sig_info = lt.newList()
            om.put(region_info["sig"], round(float(temblor["sig"]),3), sig_info)
        lt.addLast(sig_info, temblor_sig)
        
    return anio_info

def add_prof_req_5(historial_sismico, temblor):
    tupla=(temblor["depth"], temblor["nst"])
    prof_info= om.get(historial_sismico["profundidades"], tupla)
    if prof_info:
        prof_info= me.getValue(prof_info)
    else: 
        prof_info= new_datos(temblor)
        om.put(historial_sismico["profundidades"], tupla ,prof_info)

    return historial_sismico

# Funciones para creacion de datos
def new_temblor_mag(temblor):
    
    time = round_date(temblor["time"])
    #time = datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%S.%fZ")
    temblor = {"time": time,
               "lat": round(float(temblor["lat"]),3),
               "long": round(float(temblor["long"]),3),
               "title": temblor["title"],
               "code": temblor["code"],
               "mag": round(float(temblor["mag"]), 3)}
    return temblor
    
def new_temblor_depth(temblor):
    time = round_date(temblor["time"])
    #time = datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%S.%fZ")
    temblor = {"time": time,
               "lat": round(float(temblor["lat"]),3),
               "long": round(float(temblor["long"]),3),
               "title": temblor["title"],
               "code": temblor["code"],
               "depth": round(float(temblor["depth"]), 3)}
    return temblor
    
def new_temblor_sig(temblor):
    time = round_date(temblor["time"])
    #time = datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%S.%fZ")
    temblor = {"time": time,
               "lat": round(float(temblor["lat"]),3),
               "long": round(float(temblor["long"]),3),
               "title": temblor["title"],
               "code": temblor["code"],
               "depth": round(float(temblor["sig"]), 3)}
    return temblor


def new_region():
    region = {"mag": None,
              "depth": None,
              "sig": None}
    region["mag"] = om.newMap("BST", compare_mag)
    region["depth"] = om.newMap("BST", compare_deph)
    region["sig"] = om.newMap("BST", compare_sig)
    
    return region
    
def new_anio():
    anio = {"regiones": None, 
            "lat_long":None}
    
    anio["regiones"] = mp.newMap(maptype="PROBING")
    anio["lat_long"] = mp.newMap(maptype="PROBING" )
    return anio

def new_temblor(temblor):
    if temblor["felt"] == "":
        felt = "Unknown"
    else:
        felt = round(float(temblor["felt"]), 3)
    if temblor["cdi"] == "":
        cdi = "Unknown"
    else:
        cdi = round(float(temblor["cdi"]), 3)
    if temblor["mmi"] == "":
        mmi = "Unknown"
    else:
        mmi = round(float(temblor["mmi"]), 3)
    if temblor["tsunami"] == "0":
        tsunami = "False "
    else:
        tsunami = "True "
    time = round_date(temblor["time"])
    #time = datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%S.%fZ")
    
    temblor = {"code": temblor["code"],
               "time": time,
               "lat": round(float(temblor["lat"]), 3),
               "long":round(float(temblor["long"]), 3),
               "mag": round(float(temblor["mag"]), 3),
               "title": temblor["title"],
               "depth": round(float(temblor["depth"]), 3),
               "felt": felt,
               "cdi": cdi,
               "mmi": mmi,
               "tsunami": tsunami}
    return temblor
 
def new_datos(dato):
    if dato["nst"] == "":
        nst = "1"
    else:
        nst = dato["nst"]
    if dato["cdi"] == "":
        cdi = "Unknown"
    else:
        cdi = round(float(dato["cdi"]), 3)
    if dato["gap"] == "":
        gap= "Unknown"

    elif dato["gap"] is int:
         gap= round(float(dato["gap"]), 3)
    
    if dato["mmi"] == "":
        mmi = "Unknown"
    elif dato["mmi"] is int:
        mmi = round(float(dato["mmi"]), 3)
    
    
    #time = datetime.datetime.strptime(dato["time"],"%Y-%m-%dT%H:%M:%S.%fZ")
    time = round_date(dato["time"])
    dato = {"date": time,
               "mag": round(float(dato["mag"]), 3),
               "lat": round(float(dato["lat"]), 3),
               "long":round(float(dato["long"]), 3),
               "depth": round(float(dato["depth"]), 3),
               "sig":dato["sig"] ,
               "gap":dato["gap"],
               "nst": nst,
               "title": dato["title"],
               "cdi": cdi,
               "mmi": dato["mmi"],
               "magType": dato["magType"],
               "type": dato["type"],
               "code": dato["code"]}
    return dato 

def fechasreq1(historial_sismico, temblor):

    arbol_fechas= historial_sismico["fechas_req1"]
    fecha= temblor["time"]
    
    fecha = datetime.datetime.strptime(fecha,"%Y-%m-%dT%H:%M:%S.%fZ")
    fecha = fecha.strftime("%Y-%m-%dT%H:%M")
    
    if om.contains(arbol_fechas, fecha):
        list_datos= om.get(arbol_fechas, fecha)
        list_datos=me.getValue(list_datos)
        dato_sin_time= new_dato_sin_time(temblor)
        lt.addLast(list_datos, dato_sin_time)
    else:
        lista= lt.newList(datastructure="ARRAY_LIST")
        dato_sin_time= new_dato_sin_time(temblor)
        lt.addLast(lista, dato_sin_time)
        om.put(arbol_fechas, fecha, lista)
        
    return historial_sismico

def mag_req2 ( historial_sismico , temblor):
    arbol_magnitudes = historial_sismico["magnitudes_req2"]
    mag= round(float(temblor["mag"]),3)
    if om.contains(arbol_magnitudes, mag):
        list_datos= om.get(arbol_magnitudes, mag)
        list_datos=me.getValue(list_datos)
        dato_completo= new_datos(temblor)
        lt.addLast(list_datos, dato_completo)
       
    else:
        lista= lt.newList(datastructure="ARRAY_LIST")
        dato_completo= new_datos(temblor)
        lt.addLast(lista, dato_completo)
        om.put(arbol_magnitudes, mag, lista)
        
    
    return historial_sismico


def new_dato_sin_time(dato):
    if dato["nst"] == "":
        nst = "1"
    else:
        nst = dato["nst"]
    if dato["cdi"] == "":
        cdi = "Unknown"
    else:
        cdi = dato["cdi"]
    if dato["gap"] == "":
        dato["gap"] = "Unknown"
    elif dato["gap"] is int:
        dato["gap"]= round(float(dato["gap"]), 3)

    if dato["mmi"] == "":
        dato["mmi"] = "Unknown"
    elif dato["mmi"] is int:
        dato["mmi"] = round(float(dato["mmi"]), 3)

    dato_sin_time={"mag": round(float(dato["mag"]), 3),
               "lat": round(float(dato["lat"]), 3),
               "long":round(float(dato["long"]), 3),
               "depth": round(float(dato["depth"]), 3),
               "sig":dato["sig"] ,
               "gap":dato["gap"],
               "nst": nst,
               "title": dato["title"],
               "cdi": cdi,
               "mmi": dato["mmi"],
               "magType": dato["magType"],
               "type": dato["type"],
               "code": dato["code"]}
    
    return dato_sin_time

def new_dato_con_distancia_req_6(dato):
    if dato["nst"] == "":
        nst = "1"
    else:
        nst = dato["nst"]
    if dato["cdi"] == "":
        cdi = "Unknown"
    else:
        cdi = dato["cdi"]
    if dato["gap"] == "":
        dato["gap"] = "Unknown"
    elif dato["gap"] is int:
        dato["gap"]= round(float(dato["gap"]), 3)

    if dato["mmi"] == "":
        dato["mmi"] = "Unknown"
    elif dato["mmi"] is int:
        dato["mmi"] = round(float(dato["mmi"]), 3)

    time = round_date(dato["time"])
    dato_con_distancia={"date": time ,
                        "mag": round(float(dato["mag"]), 3),
               "lat": round(float(dato["lat"]), 3),
               "long":round(float(dato["long"]), 3),
               "depth": round(float(dato["depth"]), 3),
               "sig":dato["sig"] ,
               "gap":dato["gap"],
               "distance": 0,
               "nst": nst,
               "title": dato["title"],
               "cdi": cdi,
               "mmi": dato["mmi"],
               "magType": dato["magType"],
               "type": dato["type"],
               "code": dato["code"]}
    
    return dato_con_distancia

"""def new_prof(temblor):
    #fecha = datetime.datetime.strptime(temblor["time"],"%Y-%m-%dT%H:%M:%S.%fZ")
    #fecha = fecha.strftime("%Y-%m-%dT%H:%M")
    fecha = round_date(temblor["time"])
    data= {"time": fecha,
           "mag":temblor["mag"],
           "lat":temblor["lat"],
           "long":temblor["long"],
           "depth":temblor["depth"],
           "sig":temblor["sig"], 
           "gap":temblor["gap"],
           "nst": temblor["nst"],
           "title": temblor["nst"],
           "cdi": temblor["cdi"],
           "mmi": temblor["mmi"],
           "magType": temblor["magType"],
           "type":temblor["type"],
           "code":temblor["code"]}
    return data"""

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(historial_sismico, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(historial_sismico):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(historial_sismico, initialDate , finalDate):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1

    Eventos_ocurridos= lt.newList('ARRAY_LIST')
    arbol = historial_sismico["fechas_req1"]

    lista_keys = om.keys(arbol, finalDate, initialDate)
    total_fechas= lt.size(lista_keys) 
    
    total_sismos= 0
    for fecha in lt.iterator(lista_keys):
        
        lista_valor = om.get(arbol, fecha)
        lista_valor = me.getValue(lista_valor)
        events= lt.size(lista_valor)
        total_sismos += events
        lista_organizada= new_eventos_ocurridos(fecha, events, lista_valor)
        lt.addLast(Eventos_ocurridos, lista_organizada)
   

    return total_sismos,total_fechas, Eventos_ocurridos

def new_eventos_ocurridos (fecha ,events , lista_valor ):

    info_completa={"time": fecha,
                       "events": events,
                       "details": None
                       }
    info_completa["details"]= tabulate(lt.iterator(lista_valor), headers="keys", tablefmt="grid", showindex=False, maxcolwidths=16)
    return info_completa

def new_eventos_ocurridos_sin_tabla (fecha ,events , lista_valor ):

    info_completa={"time": fecha,
                       "events": events,
                       "details": lista_valor}
    #info_completa["details"]= tabulate(lt.iterator(lista_valor), headers="keys", tablefmt="grid", showindex=False, maxcolwidths=16)
    return info_completa

def round_date(a):
    sec = a[17:19]
    min= a[14:16]
    hr = a[11:13]
    day = a[8:10]
    month = a[5:7]
    anio = a[:4]
    if float(sec)>30:
        min = int(min)+1
        if min > 59:
            min = 0
            hr = int(hr) + 1
            if hr > 23:
                hr = 0
                day = int(day) + 1
                if int(month) == 2:
                    if int(anio)%4 == 0 and day >29:
                        day = 1
                        month = 3
                    elif int(anio)%4 != 0 and day > 28:
                        day = 1
                        month = 3
                elif int(month) in [4,6,9,11] and int(day) > 30:
                    month = int(month) + 1
                    day = 1
                elif int(month) in [1,3,5,7,8,10,12] and int(day) > 31:
                    month = int(month) + 1
                    day = 1
                if int(month) > 12:
                    month = 1
                    day = 1
                    anio = int(anio) + 1
    
    partes_fecha = month, day, hr, min
    partes_format = []
    for el in partes_fecha:
        if int(el) < 10:
            el = "0" + str(int(el))
        partes_format.append(str(el))
    fecha = str(anio) + "-" + partes_format[0] + "-" + partes_format[1] + "T" + partes_format[2] + ":" + partes_format[3]
    return fecha




def req_2(historial_sismico, limit_inferior , limit_superior):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    
    eventos_ocurridos = lt.newList('ARRAY_LIST')
    arbol= historial_sismico["magnitudes_req2"]
    lista_keys= om.keys(arbol, limit_inferior, limit_superior)
    total_sismos = 0
    for mag in lt.iterator(lista_keys):
        lista_valor = om.get(arbol, mag)
        lista_valor = me.getValue(lista_valor)
        events= lt.size(lista_valor)
        total_sismos += events
        lista_organizada= new_eventos_mag(mag, events, lista_valor)
        
        lt.addFirst(eventos_ocurridos, lista_organizada)

    
    total_magnitudes= om.size(eventos_ocurridos)

    return total_sismos,total_magnitudes,  eventos_ocurridos

def new_eventos_mag (mag , events , lista_valor):

    info_completa={"mag": mag,
                       "events": events,
                       "details": None
                       }
    
    if lt.size(lista_valor)>6:
            lista_organizada2=lt.newList(datastructure="ARRAY_LIST")
            primer = lt.firstElement(lista_valor)
            segundo= lt.getElement(lista_valor, 2)
            tercero= lt.getElement(lista_valor, 3)
            ultimo= lt.lastElement(lista_valor)
            penultimo=lt.getElement(lista_valor, -2)
            antepenultimo=lt.getElement(lista_valor, -3)
            lt.addLast(lista_organizada2, primer)
            lt.addLast(lista_organizada2, segundo)
            lt.addLast(lista_organizada2, tercero)
            lt.addLast(lista_organizada2, antepenultimo)
            lt.addLast(lista_organizada2, penultimo)
            lt.addLast(lista_organizada2, ultimo)

            lista_valor= lista_organizada2

    info_completa["details"]= tabulate(lt.iterator(lista_valor), headers="keys", tablefmt="grid", showindex=False, maxcolwidths=16)



    return info_completa


def req_3(historial_sismico, mag_min , depth_max):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    
    mag_list= om.values(historial_sismico["magnitudes_req2"], mag_min, om.maxKey(historial_sismico["magnitudes_req2"]))
    total_sismos= 0 
    eventos_fecha= om.newMap(omaptype="RBT", cmpfunction=compare_arbol)

    for sismos in lt.iterator(mag_list):
        for sismo in lt.iterator(sismos):
            if sismo["depth"] == "Unknown" or float(sismo["depth"]) <= float(depth_max):
                sismo_2= new_dato_sin_time(sismo)
                total_sismos +=1 
                fecha_eventos= om.get(eventos_fecha, sismo["date"])
                if fecha_eventos:
                    fecha_eventos= me.getValue(fecha_eventos)
                    details= fecha_eventos["details"]
                    lt.addLast(details, sismo_2)
                    fecha_eventos["events"]+=1
                else:
                    details= lt.newList()
                    lt.addLast(details, sismo_2)
                    fecha_eventos= new_eventos_ocurridos_sin_tabla(sismo["date"], 1, details)
                    om.put(eventos_fecha,sismo["date"], fecha_eventos)

    total_fechas= om.size(eventos_fecha)
    eventos_fecha= om.values(eventos_fecha, om.minKey(eventos_fecha), om.maxKey(eventos_fecha))
    eventos_ocurridos= lt.newList()
    num = 0
    i = 1
    while num < 10:
        elem = lt.getElement(eventos_fecha, i)
        num += elem["events"]
        elem["details"] = tabulate(lt.iterator(elem["details"]), headers="keys", tablefmt="grid", showindex=False, maxcolwidths=16)
        lt.addLast(eventos_ocurridos, elem)
        i += 1   
        
    return total_sismos ,total_fechas,  eventos_ocurridos




def req_4(historial_sismico, sig, gap):
    
    sig_list = om.values(historial_sismico["sig_req4"], sig, om.maxKey(historial_sismico["sig_req4"]))
    eventos_totales = 0
    eventos = om.newMap(omaptype="RBT", cmpfunction=compare_arbol)
    for sismos in lt.iterator(sig_list):
        for sismo in lt.iterator(sismos):
            if sismo["gap"] == "Unknown" or float(sismo["gap"]) <= float(gap):
                sismo_2 = new_dato_sin_time(sismo) 
                eventos_totales +=1
                fecha_info = om.get(eventos, sismo["date"])
                if fecha_info:
                    fecha_info = me.getValue(fecha_info)
                    details= fecha_info["details"]
                    lt.addLast(details, sismo_2)
                    fecha_info["events"] += 1
                else:
                    details = lt.newList()
                    lt.addLast(details, sismo_2)
                    fecha_info = new_eventos_ocurridos_sin_tabla(sismo["date"],1, details)
                    om.put(eventos, sismo["date"], fecha_info)

    total_fechas = om.size(eventos)
    eventos = om.values(eventos, om.minKey(eventos), om.maxKey(eventos))
    eventos_final = lt.newList()
    
    # Para seleccionar los 15 ultimos eventos != 15 ultimas fechas.
    num = 0
    i = 1
    while num < 15:
        elem = lt.getElement(eventos, i)
        num += elem["events"]
        elem["details"] = tabulate(lt.iterator(elem["details"]), headers="keys", tablefmt="grid", showindex=False, maxcolwidths=16)
        lt.addLast(eventos_final, elem)
        i += 1   
        
    return total_fechas, eventos_totales, eventos_final
            
    
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(historial_sismico, profundidad, estaciones):   
    """
    Función que soluciona el requerimiento 5
    """
    arbol_prof= historial_sismico["profundidades"]
    que_cumplen= lt.newList("ARRAY_LIST", cmpfunction= compare_prof)
    v_eventos= lt.newList("ARRAY_LIST")
    llaves= om.keySet(arbol_prof)
    for nodo in lt.iterator(llaves):
        if nodo[0] >= profundidad and nodo[1]>= estaciones: 
            tupla= om.get(arbol_prof, nodo)
            valor= me.getValue(tupla)
            lt.addLast(que_cumplen,valor)
    total_eventos= lt.size(que_cumplen)  
    fechas= []
    for evento in lt.iterator(que_cumplen):
        if evento["date"] not in fechas: 
            fechas.append(evento["date"])
    total_fechas= len(fechas)
    mapa_fechas= om.newMap(omaptype= "RBT", cmpfunction= compare_arbol)
    for sismo in lt.iterator(que_cumplen):
        info= om.get(mapa_fechas, sismo["date"])
        if info: 
            info= me.getValue(info)
        else: 
            info= lt.newList()
            fecha= sismo["date"]
            mp.put(mapa_fechas, fecha, info)
        valor= new_dato_sin_time(sismo)
        lt.addLast(info,valor)
    
    keys= om.keys(mapa_fechas, om.minKey(mapa_fechas), om.maxKey(mapa_fechas)) 
    for key in lt.iterator(keys):
        details= mp.get(mapa_fechas,key)
        details= me.getValue(details)
        events= lt.size(details)
        tabla= new_eventos_ocurridos(key, events, details) #
        lt.addLast(v_eventos, tabla)
    while lt.size(v_eventos) > 20:
        lt.removeLast(v_eventos)
    
    return total_eventos,total_fechas, v_eventos

def req_6(historial_sismico, anio,lat,long,radio,n):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    que_cumplen= lt.newList("ARRAY_LIST") 
    anios= historial_sismico["anios"]
    anio= om.get(anios, anio)
    anio_1= me.getValue(anio)
    mapa= anio_1["lat_long"] 
    valores= mp.keySet(mapa)
    coordenada= ((round(float(lat),3)),(round(float(long),3)))
    te_anio= 0
    for evento in lt.iterator(valores):
        tupla= mp.get(mapa,evento)
        valor= me.getValue(tupla)
        for sismo in lt.iterator(valor):
            te_anio += 1
            distancia= haversine(evento, coordenada)
            if distancia <= float(radio):
                sismo["distance"] += distancia
                lt.addLast(que_cumplen, sismo)
                
    sa.sort(que_cumplen, compare_sig_req6)
    pre_e_significativo= lt.firstElement(que_cumplen)
    codigo_sig = pre_e_significativo["code"]
    fecha_e_significativo= pre_e_significativo["date"]
    e_significativo= lt.newList("ARRAY_LIST")
    lt.addLast(e_significativo, pre_e_significativo) 
    sa.sort(que_cumplen, compare_fechas_req6)
    menores= st.newStack("DOUBLE_LINKED")
    mayores= qu.newQueue("SINGLE_LINKED")
    for event in lt.iterator(que_cumplen):
        if event["date"] < fecha_e_significativo:
            st.push(menores,event)
        else: 
            qu.enqueue(mayores,event)
    pre_n_eventos= lt.newList("ARRAY_LIST")
    i= 0
    while i < int(n) and not st.isEmpty(menores):
        elemento = st.pop(menores)
        lt.addLast(pre_n_eventos, elemento)
        i+=1
        
    eventos_antes = lt.size(pre_n_eventos)
        
    while i <= (int(n) + 1) and not  qu.isEmpty(mayores): 
        elem= qu.dequeue(mayores)
        lt.addLast(pre_n_eventos, elem)
        i+=1
    eventos_despues = lt.size(pre_n_eventos)-(eventos_antes + 1)
    
    fechas=om.newMap(omaptype= "RBT", cmpfunction= compare_arbol_req_6)
    for sism in lt.iterator(pre_n_eventos): 
        sism_info= om.get(fechas, sism["date"])
        if sism_info:
            sism_info=me.getValue(sism_info)
        else:
            sism_info= lt.newList()
            fecha= sism["date"]
            mp.put(fechas, fecha, sism_info)
        valor= new_details(sism)
        lt.addLast(sism_info,valor)
    
    n_eventos= lt.newList("ARRAY_LIST")
    fechas_keys= om.keys(fechas, om.minKey(fechas), om.maxKey(fechas))
    for fecha in lt.iterator(fechas_keys):
        details= om.get(fechas, fecha)
        details= me.getValue(details)
        events = lt.size(details)
        tabla= new_eventos_ocurridos(fecha, events, details)
        lt.addLast(n_eventos, tabla)
        
    t_fechas = lt.size(n_eventos)
    
    t_eventos_radio= lt.size(que_cumplen) 
      
    return t_fechas, e_significativo, t_eventos_radio, n_eventos, te_anio, codigo_sig, eventos_despues, eventos_antes
    """fechas=mp.newMap(maptype= "CHAINING")
    for sism in lt.iterator(pre_n_eventos): 
        sism_info= mp.get(fechas, sism["date"])
        if sism_info:
            sism_info=me.getValue(sism_info)
        else:
            sism_info= lt.newList()
            fecha= sism["date"]
            mp.put(fechas, fecha, sism_info)
        valor= new_details(sism)
        lt.addLast(sism_info,valor)
    
    n_eventos= lt.newList("ARRAY_LIST")
    fechas_keys= mp.keySet(fechas)
    for fecha in lt.iterator(fechas_keys):
        details= mp.get(fechas, fecha)
        details= me.getValue(details)
        events = mp.size(details)
        tabla= new_eventos_ocurridos(fecha, events, details)
        lt.addLast(n_eventos, tabla)
    
    t_eventos_radio= lt.size(que_cumplen) 
    
    return t_fechas, e_significativo, t_eventos_radio, n_eventos, te_anio, codigo_sig, eventos_despues, eventos_antes"""

def new_details(sism):
    details= {"mag": sism["mag"],
              "lat": sism["lat"],
              "long": sism["long"],
              "depth": sism["depth"],
              "sig": sism["sig"],
              "gap": sism["gap"],
              "distance": sism["distance"], 
              "nst": sism["nst"],
              "magType": sism["magType"], 
              "type": sism["type"],
              "code": sism["code"]}
    return details

def req_7(historial_sismico, anio,region, propiedad, bins):
    """
    Función que soluciona el requerimiento 7
    """    
    # TODO: Realizar el requerimiento 7
    anio_info = om.get(historial_sismico["anios"], anio)
    anio_info = me.getValue(anio_info)
    region_info = mp.get(anio_info["regiones"], region)
    region_info = me.getValue(region_info)
    prop = region_info[propiedad]
    max_prop =om.maxKey(prop)
    min_prop = om.minKey(prop)
    incremento = (float(max_prop) - float(min_prop))/int(bins)
    x =[] 
    y = []
    sismos = lt.newList()
    lim_inferior = min_prop
    while len(y) < int(bins):
        frecuencia = 0
        lim_inferior = round(lim_inferior,3)
        lim_superior = round(lim_inferior + incremento,3)
        rango_prop = om.values(prop, lim_inferior, lim_superior)
        for eventos in lt.iterator(rango_prop):
            frecuencia += lt.size(eventos)
            for evento in lt.iterator(eventos):
                lt.addLast(sismos, evento)
        if lim_inferior != min_prop:
            lim_no_incluido = om.get(prop, lim_inferior)
            if lim_no_incluido:
                lim_no_incluido = me.getValue(lim_no_incluido)
                frecuencia -= lt.size(lim_no_incluido)
            etiqueta = "(" + str(lim_inferior)+ "-"+ str(lim_superior)+"]"
        else:
            etiqueta = "["+str(lim_inferior)+ "-"+ str(lim_superior) +"]"
        x.append(etiqueta)
        y.append(frecuencia)
        
        lim_inferior += incremento

    quk.sort(sismos, cmp_fechas)
    
    sismos_list = []
    total = lt.size(sismos)
    if lt.size(sismos) > 6:
        mini_list = lt.subList(sismos, 1 ,3)
        ultimos = lt.subList(sismos, lt.size(sismos)-(2), 3)
        for el in lt.iterator(ultimos):
            lt.addLast(mini_list, el)
        sismos = mini_list
    for sismo in lt.iterator(mini_list):
            sismo = list(sismo.values())
            sismos_list.append(sismo)
            
    # Codigo para generar la figura --- AQUI NO SE IMPRIMIRA, se ará en consola.        
    fig = pl.figure()
    gs = fig.add_gridspec(2, hspace=1.5)
    (ax, ax1) = gs.subplots(sharex=False, sharey=False)
    #fig, ax = pl.subplots()
    ax.bar(x, y, width=0.75,color="#A2D9CE",edgecolor="black" )
    for i in range(0, (len(x))):
        ax.text(i, y[i], y[i], ha="center")
        
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.tick_params(axis='x', rotation=45)
    ax.set_title("Histograma de " + str(propiedad) +" en " + str(region) + " en " + str(anio))
    ax.set_xlabel(str(propiedad))
    ax.set_ylabel("No. Eventos")

    tabla = ax1.table(cellText=sismos_list, colLabels=["time", "lat", "long", "title", "code", propiedad], loc="center", cellLoc="center",colWidths=[0.14,0.055,0.08,0.3,0.08,0.05])
    tabla.scale(1.7,0.8)
    tabla.set_fontsize (14)
    ax1.axis("off")
    ax1.set_title("Detalles de los eventos " + " en " + str(region) + " en " + str(anio))
    
    return  total, fig
    
    

            


def req_8(historial_sismico):
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


def sort(historial_sismico):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass

def CompareDates (date1 , date2):
    """
    Compara dos fechas
    """

    if (date1 == date2):
        return 0
    elif (date1 < date2):
        return 1
    else:
        return -1
    
    
def compare_arbol(fecha1, fecha2):
    fecha2 = datetime.datetime.strptime( fecha2, "%Y-%m-%dT%H:%M")
    if type(fecha1) == str:
        fecha1 = datetime.datetime.strptime( fecha1, "%Y-%m-%dT%H:%M")
    if fecha1 == fecha2:
        return 0
    elif fecha1 < fecha2:
        return 1
    else:
        return -1
    
def compare_arbol_req_6(fecha1, fecha2):
    fecha2 = datetime.datetime.strptime( fecha2, "%Y-%m-%dT%H:%M")
    if type(fecha1) == str:
        fecha1 = datetime.datetime.strptime( fecha1, "%Y-%m-%dT%H:%M")
    if fecha1 == fecha2:
        return 0
    elif fecha1 < fecha2:
        return -1
    else:
        return 1
    
def compare_mag(mag1, mag2):

    if float(mag1) == float(mag2):
        return 0
    elif float(mag1) > float(mag2):
        return 1
    else:
        return -1
   
def compare_prof(prof_1, prof_2):
    if float(prof_1[0])== float(prof_2[0]):
        return 0
    elif float(prof_1[0]) > float(prof_2[0]):
        return 1
    else: 
        return -1
    
    
    

def compare_sig(sg1, sg2):
    if float(sg1) == float(sg2):
        return 0
    elif float(sg1) > float(sg2):
        return 1
    else:
        return -1
    
def compare_deph(dp1, dp2):
    if float(dp1) == float(dp2):
        return 0
    elif float(dp1) < float(dp2):
        return 1
    else:
        return -1
   

def compare_fechas_req6(date_1 , date_2):
    #if date_1["date"] > date_2["date"]:
        #return 1
    if date_1["date"] < date_2["date"]:
        return True
    else:
        return False
    
def cmp_fechas(dt1, dt2):
    if dt1["time"] < dt2["time"]:
        return True
    else:
        return False
    
def compare_sig_req6(dic_1, dic_2):
    if dic_1["sig"] > dic_2["sig"]:
        return True
    else:
        return False



    