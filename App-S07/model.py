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
import csv
import math
from tabulate import tabulate
from datetime import datetime,timedelta
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
import matplotlib.pyplot as plt
assert cf

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
    data_structs = {"temblores": None,
                    "fechas" : None,
                    "magnitud" : None,
                    "nst":None,
                    "anio":None
                    }

    data_structs["temblores"] = lt.newList("ARRAY_LIST")
    data_structs["fechas"] = om.newMap(omaptype="RBT")
    data_structs["magnitud"] = om.newMap(omaptype="RBT")
    data_structs["nst"] = om.newMap(omaptype="RBT")
    data_structs["anio"] = om.newMap(omaptype="RBT")
    data_structs["sig"] = om.newMap(omaptype="RBT")

    return data_structs

def add_data_lista(data_structs, sismo):
    """
    Función para agregar nuevos elementos a la lista
    """
    
    lista = data_structs["temblores"]
    lt.addLast(lista,sismo)
    return data_structs


def add_data_arbol_list(mapa,sismo,llave):
    
    llaves = sismo[llave]
    pareja = om.get(mapa,llaves)
    if pareja is None:
        listsismos = lt.newList("ARRAY_LIST")
        lt.addLast(listsismos,sismo)
        om.put(mapa,llaves,listsismos)
    else:
        lista_interior = me.getValue(pareja)
        lt.addLast(lista_interior,sismo)
    return mapa

def add_data_arbol_list_anio(mapa,sismo):
    
    llaves = sismo["time"][:4]
    pareja = om.get(mapa,llaves)
    if pareja is None:
        listsismos = lt.newList("ARRAY_LIST")
        lt.addLast(listsismos,sismo)
        om.put(mapa,llaves,listsismos)
    else:
        lista_interior = me.getValue(pareja)
        lt.addLast(lista_interior,sismo)
    return mapa


def add_data_arbol_arbol(data_structs,archivo, sismo, llave1, llave2):
    llave=sismo[llave1]
    mapa = data_structs[archivo]
    pareja = om.get(mapa,llave)
    if pareja is None:
        depth_map = om.newMap(omaptype="RBT")
        add_data_arbol_list(depth_map,sismo,llave2)
        om.put(mapa,llave,depth_map)
    else:
        depth_map=me.getValue(pareja)
        add_data_arbol_list(depth_map,sismo,llave2)
    return mapa

def loadData(data_structs,archivo):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    archivo = cf.data_dir + "earthquakes/temblores-utf8-"+ archivo
    archivo_leido = csv.DictReader(open(archivo, encoding="utf-8"))
    for cada_linea in archivo_leido:
        if cada_linea["felt"] == "":
            cada_linea["felt"] = "UnKnown"
        else:
            cada_linea["felt"] = round(float(cada_linea["felt"]),3)

        if cada_linea["cdi"] == "":
            cada_linea["cdi"] = "UnKnown"
        else:
            cada_linea["cdi"] = round(float(cada_linea["cdi"]),3)
            
        if cada_linea["mmi"] == "":
            cada_linea["mmi"] = "UnKnown"
        else:
            cada_linea["mmi"] = round(float(cada_linea["mmi"]),3)

        if cada_linea["tsunami"] == "0":
            cada_linea["tsunami"] = "False"
        if cada_linea["nst"] == "":
            cada_linea["nst"]=1
        else:
            cada_linea["nst"]=float(cada_linea["nst"])


        if cada_linea["gap"] == "":
            cada_linea["gap"]=1
        else:
            cada_linea["gap"]=float(cada_linea["gap"])

        cada_linea["depth"]=float(cada_linea["depth"])
        cada_linea["sig"]=float(cada_linea["sig"])
        cada_linea["mag"]=round(float(cada_linea["mag"]),3)
        

        tiempo,update=aproximar_tiempo(cada_linea["time"],cada_linea["updated"])
        cada_linea["time"] = tiempo
        cada_linea["updated"] = update


        dic_imp =  {"code": cada_linea["code"],
                    "time" : cada_linea["time"],
                    "lat" : round(float(cada_linea["lat"]),3),
                    "long": round(float(cada_linea["long"]),3),
                    "mag" : round(float(cada_linea["mag"]),3),
                    "title" : cada_linea["title"],
                    "depth": float(cada_linea["depth"]),
                    "felt" : cada_linea["felt"],
                    "cdi" : cada_linea["cdi"],
                    "mmi": cada_linea["mmi"],
                    "tsunami" : cada_linea["tsunami"]
                    }
        add_data_lista(data_structs,dic_imp)
        add_data_arbol_list(data_structs["fechas"],cada_linea,"time")
        add_data_arbol_list(data_structs["magnitud"],cada_linea,"mag")
        add_data_arbol_list(data_structs["nst"],cada_linea,"nst")
        add_data_arbol_list_anio(data_structs["anio"],cada_linea)
        add_data_arbol_list(data_structs["sig"],cada_linea,"sig")
    return lt.size(data_structs["temblores"])

def aproximar_tiempo(time,update):
        #Aproximar Time
        fecha_en_formato = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
        if fecha_en_formato.second > 30:
            fecha_redondeada = fecha_en_formato + timedelta(minutes=1)  # Aproximar hacia arriba, sumando un minuto
        else:
            fecha_redondeada = fecha_en_formato.replace(second=0, microsecond=0)
        time_redondeado= fecha_redondeada.strftime("%Y-%m-%dT%H:%M")

        #Aproximar Update
        update_en_formato = datetime.strptime(update, "%Y-%m-%dT%H:%M:%S.%fZ")
        if update_en_formato.second > 30:
            update_redondeada = update_en_formato + timedelta(minutes=1)  # Aproximar hacia arriba, sumando un minuto
        else:
            update_redondeada = update_en_formato.replace(second=0, microsecond=0)
        update_redondeado = update_redondeada.strftime("%Y-%m-%dT%H:%M")

        return time_redondeado, update_redondeado

# Funciones auxiliares


def creartabla (lista,primer_valor): 
    titulos = primer_valor.keys()
    filas =[]
    for partido in lt.iterator(lista):
        fila=[]
        valores=partido.values()
        fila.extend(valores)
        filas.append(fila)
    tabla = tabulate(filas, headers = titulos, tablefmt = "grid" )
    return tabla


def resumir_lista(lista_final,n, orden):
    """
    Crea una tabala en donde se encuentran los primeros 3 valores y los ultimos 3 valores de la lista que ingresa
    """
    nueva_lista=lt.newList("ARRAY_LIST")
    m = lt.size(lista_final)
    if n == 3 and orden == 0:
        posiciones =[m,m-1,m-2,3,2,1]
    elif n==3 and orden==1:
        posiciones =[1,2,3,m-2,m-1,m]
    elif n == 5 and orden == 0:
        posiciones = [1,2,3,4,5,m-4,m-3,m-2,m-1,m]
    for i in posiciones:
        elemento = lt.getElement(lista_final,i)
        lt.addLast(nueva_lista,elemento)
    return nueva_lista


def big_dict(llave,primer,events,details):
    """
    Crear diccionarios para imprimir dentro de la tabla
    """
    big_dict = {primer : llave,
                "events" : events,
                "details" : details}
    return big_dict

    
def min_dict(sismo,primer):
    """
    Crear diccionarios para imprimir dentro de la tabla
    """

    min_dict = {primer: sismo[primer],
                "lat" : round(float(sismo["lat"]),3),
                "long": round(float(sismo["long"]),3),
                "depth": sismo["depth"],
                "sig" : sismo["sig"],
                "gap" : sismo["gap"],
                "nst": sismo["nst"],
                "title" : sismo["title"],
                "cdi" : sismo["cdi"],
                "mmi": sismo["mmi"],
                "magType" : sismo["magType"],
                "type" : sismo["type"],
                "code": sismo["code"]}
    return min_dict



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

## Funciones requerimientos
def req_1(data_structs,inicialdate,finaldate):
    """
    Función que soluciona el requerimiento 1
    """
    date_map = data_structs["fechas"]
    rango_llaves = om.keys(date_map,inicialdate,finaldate)
    total_fechas = lt.size(rango_llaves)
    total_sismos = 0
    lista_final = lt.newList("ARRAY_LIST")

    for llave in lt.iterator(rango_llaves):
        pareja = om.get(date_map,llave)
        sismos = me.getValue(pareja)
        sismo_x_fecha= lt.size(sismos)
        total_sismos += sismo_x_fecha
        lista_dic = lt.newList("ARRAY_LIST")
        for sismo in lt.iterator(sismos):
            pequeno =  min_dict(sismo,"mag")
            lt.addLast(lista_dic,pequeno)
        details=creartabla(lista_dic,lista_dic["elements"][0])

        dict_grande = big_dict(llave,"time",sismo_x_fecha,details)
        lt.addLast(lista_final,dict_grande)
    return lista_final,total_sismos,total_fechas

def req_2(data_structs,mag_inf,mag_sup):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    #Se extraen las llaves en el rango de magnitud
    mag_map = data_structs["magnitud"]
    rango_llaves = om.keys(mag_map,mag_inf,mag_sup)
    total_llaves = lt.size(rango_llaves)

    #Se crea un contador vacío
    total_sismos = 0

    #Se halla la cantidad total de eventos 
    elementos = lt.size(data_structs["temblores"])

    #Se crea una lista vacía
    lista_final = lt.newList("ARRAY_LIST")

    #Se itera sobre las llaves del rango de magnitudes y se obtiene su valor
    for llave in lt.iterator(rango_llaves):
        pareja = om.get(mag_map,llave)
        sismos = me.getValue(pareja)

    #Se halla la cantidad de sismos dobre este rango y se va sumando al contador de total de sismos
        sismo_entre_magnitudes= lt.size(sismos)
        total_sismos += sismo_entre_magnitudes

    #Se crea una lista vacía
        lista_dic = lt.newList("ARRAY_LIST")

    #Se iteran sobre los eventos dentro del rango de magnitudes y se agrega el valor "time" a la lista vacía anterior
        for sismo in lt.iterator(sismos):
            pequeno =  min_dict(sismo,"time")
            lt.addLast(lista_dic,pequeno)

    #Se ordenan los valores del más reciente al más antiguo
        quk.sort(lista_dic, cmpFechaReciente)

    #Se halla la cantidad de valores dentro de la lista
        size_lista_dic = lt.size(lista_dic)

    #Se crea una sublista en caso de que hayan más de 6 valores dentro de la lista
        if size_lista_dic > 6:
            sublista = resumir_lista(lista_dic,3,1)
        else:
            sublista = lista_dic

    #Se crea la tabla de datails
        details=creartabla(sublista,sublista["elements"][0])

    #Se crean los diccionarios para la tabla grande
        dict_grande  = big_dict(llave, "mag", sismo_entre_magnitudes, details)

    #Se agragan a la lista vacía inicial
        lt.addLast(lista_final, dict_grande)

    return lista_final, total_sismos, total_llaves, elementos


def req_3(data_structs, mag_min, depth_max):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    #Sacar llaves en rango de magnitud
    mapa_mag=data_structs["magnitud"]
    mag_max=om.maxKey(mapa_mag)
    llaves_estaciones=om.keys(mapa_mag,mag_min,mag_max)

    #Creacion de contadores y mapas
    total_eventos=0
    filtrado_eventos=om.newMap(omaptype="RBT")

    #Comprobacion de profundidad máxima
    for estacion in lt.iterator(llaves_estaciones):
        sismos=me.getValue(om.get(mapa_mag,estacion))
        for sis in lt.iterator(sismos):
            prof=int(sis["depth"])
            if prof<=depth_max:
                total_eventos+=1
                add_data_arbol_list(filtrado_eventos,sis,"time")

    #Sacar los 10 sismos mas recientes
    fechas_diferentes=om.size(filtrado_eventos)
    keys=om.keySet(filtrado_eventos)
    llaves_finales=lt.subList(keys,lt.size(keys)-9,10)
    lista_final=lt.newList("ARRAY_LIST")
    
    #Hacer diccionarios para la impresión de sismos finales
    for ll in lt.iterator(llaves_finales):
        sismo_x_fecha=me.getValue(om.get(filtrado_eventos,ll))
        lista_final_sis=lt.newList("ARRAY_LIST")
        for sismo in lt.iterator(sismo_x_fecha):
            pequeno =  min_dict(sismo,"mag")
            lt.addLast(lista_final_sis,pequeno)
        details=creartabla(lista_final_sis,lista_final_sis["elements"][0])

        dict_grande = big_dict(ll,"time",lt.size(sismo_x_fecha),details)
        lt.addLast(lista_final,dict_grande)

    return fechas_diferentes,total_eventos,lista_final


def req_4(data_structs,sig_min,dis_max):
    """
    Función que soluciona el requerimiento 4
    """
    #sacar llaves en mayores a sig_min
    sig_map = data_structs["sig"]
    sig_max=om.maxKey(sig_map)
    llaves_sig=om.keys(sig_map,sig_min,sig_max)
    new_time_map = om.newMap(omaptype="RBT")
    total_eventos = 0

    #filtrar por dis_max
    for valor in lt.iterator(llaves_sig):
        pareja = om.get(sig_map,valor)
        sismos=me.getValue(pareja)
        for sismo in lt.iterator(sismos):
            dis = int(sismo["gap"])
            if dis_max>=dis:
                total_eventos+=1
                add_data_arbol_list(new_time_map,sismo,"time")

    #Sacar los 15 sismos mas recientes
    total_fechas=om.size(new_time_map)
    total=om.keySet(new_time_map)
    fechas=lt.subList(total,lt.size(total)-14,15)
    lista_final=lt.newList("ARRAY_LIST")
    
    #Hacer diccionarios para imprimir de sismos finales
    for fecha in lt.iterator(fechas):
        pareja = om.get(new_time_map,fecha)
        sismo_x_fecha=me.getValue(pareja)
        lista_pequeno=lt.newList("ARRAY_LIST")
        for sismo in lt.iterator(sismo_x_fecha):
            pequeno =  min_dict(sismo,"mag")
            lt.addLast(lista_pequeno,pequeno)
        details=creartabla(lista_pequeno,lista_pequeno["elements"][0])

        dict_grande = big_dict(fecha,"time",lt.size(sismo_x_fecha),details)
        lt.addLast(lista_final,dict_grande)

    return lista_final,total_eventos,total_fechas
                

    


def req_5(data_structs, depth_min, nst_min):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    #Sacar llaves en rango de NST
    mapa_estaciones=data_structs["nst"]
    est_max=om.maxKey(mapa_estaciones)
    llaves_estaciones=om.keys(mapa_estaciones,nst_min,est_max)

    #Creacion de contadores y mapas
    total_eventos=0
    filtrado_eventos=om.newMap(omaptype="RBT")

    #Comprobacion de profundidad minima
    for estacion in lt.iterator(llaves_estaciones):
        sismos=me.getValue(om.get(mapa_estaciones,estacion))
        for sis in lt.iterator(sismos):
            prof=int(sis["depth"])
            if prof>=depth_min:
                total_eventos+=1
                add_data_arbol_list(filtrado_eventos,sis,"time")

    #Sacar los 20 sismos mas recientes
    fechas_diferentes=om.size(filtrado_eventos)
    keys=om.keySet(filtrado_eventos)
    llaves_finales=lt.subList(keys,lt.size(keys)-19,20)
    lista_final=lt.newList("ARRAY_LIST")
    
    #Hacer diccionarios para imprimir de sismos finales
    for ll in lt.iterator(llaves_finales):
        sismo_x_fecha=me.getValue(om.get(filtrado_eventos,ll))
        lista_final_sis=lt.newList("ARRAY_LIST")
        for sismo in lt.iterator(sismo_x_fecha):
            pequeno =  min_dict(sismo,"mag")
            lt.addLast(lista_final_sis,pequeno)
        details=creartabla(lista_final_sis,lista_final_sis["elements"][0])

        dict_grande = big_dict(ll,"time",lt.size(sismo_x_fecha),details)
        lt.addLast(lista_final,dict_grande)

    return fechas_diferentes,total_eventos,lista_final


def req_6(data_structs,anio, latitud, longitud, radio, n):
    """
    Función que soluciona el requerimiento 6
    """
    
    #Extraer mapa anios
    mapa_anios=data_structs["anio"]
    an = om.get(mapa_anios,anio)
    if an is None:
        return(0,0,0,0,0,0)
    else:
        lista_sismos = me.getValue(an)


    total_eventos_en_area=0
    sis_en_espacio=om.newMap(omaptype="RBT")
    sis_x_fechas=om.newMap(omaptype="RBT")

    #Comprobar si estan en el radio necesario, con la ecuacion de Harvesine
    for sismo in lt.iterator(lista_sismos):
        lat1,lon1,lat2,lon2 = map(math.radians, [latitud, longitud, float(sismo["lat"]), float(sismo["long"])])
        dif_long=lon2-lon1
        dif_lat=lat2-lat1
        raiz=((math.sin(dif_lat/2))**2)+((math.cos(lat1))*(math.cos(lat2)*((math.sin(dif_long/2))**2)))
        ars=math.asin(math.sqrt(raiz))
        d=2*(ars)*6371
        if d <=radio:
            total_eventos_en_area+=1
            sismo["distance"]=d
            add_data_arbol_list(sis_en_espacio,sismo,"sig")
            add_data_arbol_list(sis_x_fechas,sismo,"time")
    

    #Encontrar el evento mas significativo
    sismo_m=om.maxKey(sis_en_espacio)
    s_m=me.getValue(om.get(sis_en_espacio,sismo_m))
    if lt.size(s_m)!=1:
        mas_dyfi=0
        for sismo in lt.iterator(s_m):
            dfyi=sismo["felt"]
            if dfyi!="UnKnown" and dfyi>mas_dyfi:
                mas_dyfi=dfyi
                sismo_mas=sismo
        if mas_dyfi ==0:
            sismo_mas=s_m["elements"][0]
    else:
        sismo_mas=s_m["elements"][0]

    codigo=sismo_mas["code"]
    #Armar diccionario evento mas significativo para imprimir
    evento_mas_s={"time":sismo_mas["time"],
                    "mag":sismo_mas["mag"],
                    "lat":sismo_mas["lat"],
                    "long":sismo_mas["long"],
                    "depth":sismo_mas["depth"],
                    "sig":sismo_mas["sig"],
                    "gap":sismo_mas["gap"],
                    "distance":sismo_mas["distance"],
                    "nst":sismo_mas["nst"],
                    "title":sismo_mas["title"],
                    "cdi":sismo_mas["cdi"],
                    "mmi":sismo_mas["mmi"],
                    "magType":sismo_mas["magType"],
                    "type":sismo_mas["type"],
                    "code":sismo_mas["code"]}
    evento_mas_sig=lt.newList("ARRAY_LIST")
    lt.addLast(evento_mas_sig,evento_mas_s)
    om.deleteMax(sis_en_espacio)


    #Encontrar mas cercanos por fecha al mas significativo

    #Antes
    min_fecha=om.minKey(sis_x_fechas)
    llaves_sis_menores=om.keys(sis_x_fechas,min_fecha,sismo_mas["time"])
    if lt.size(llaves_sis_menores)>n:
        llaves_men=lt.subList(llaves_sis_menores,lt.size(llaves_sis_menores)-n-1,n+1)
    else: 
        llaves_men=llaves_sis_menores
    pre_events=lt.size(llaves_men)

    #Despues
    max_fecha=om.maxKey(sis_x_fechas)
    llaves_sis_mayores=om.keys(sis_x_fechas,sismo_mas["time"],max_fecha)
    lt.removeFirst(llaves_sis_mayores)
    if lt.size(llaves_sis_mayores)>n:
        llaves_mayo=lt.subList(llaves_sis_mayores,1,n)
    else: 
        llaves_mayo=llaves_sis_mayores
    pos_events=lt.size(llaves_mayo)

    #Crear listas y contadores finales
    fechas2= lt.newList("ARRAY_LIST")
    cant_eventos=0
    lista_final=lt.newList("ARRAY_LIST")

    #Formar diccionario para sismos antes
    for llave in lt.iterator(llaves_men):
        sis=me.getValue(om.get(sis_x_fechas,llave))
        lista_final_sis=lt.newList("ARRAY_LIST")
        for sismo in lt.iterator(sis):
            if lt.isPresent(fechas2,sismo["time"])==0:
                lt.addLast(fechas2,sismo["time"])
            cant_eventos+=1
            pequeno =  min_dict(sismo,"mag")
            lt.addLast(lista_final_sis,pequeno)
            details=creartabla(lista_final_sis,lista_final_sis["elements"][0])
            fecha=sismo["time"]

        dict_grande = big_dict(fecha,"time",1,details)
        lt.addLast(lista_final,dict_grande)

    #Formar diccionario para sismos después
    for llave in lt.iterator(llaves_mayo):
        sis=me.getValue(om.get(sis_x_fechas,llave))
        lista_final_sis=lt.newList("ARRAY_LIST")
        for sismo in lt.iterator(sis):
            if lt.isPresent(fechas2,sismo["time"])==0:
                lt.addLast(fechas2,sismo["time"])
            cant_eventos+=1
            pequeno =  min_dict(sismo,"mag")
            lt.addLast(lista_final_sis,pequeno)
            details=creartabla(lista_final_sis,lista_final_sis["elements"][0])
            fecha=sismo["time"]

        dict_grande = big_dict(fecha,"time",1,details)
        lt.addLast(lista_final,dict_grande)

    dif_fechas=lt.size(fechas2)

    return total_eventos_en_area,evento_mas_sig, pre_events,pos_events,lista_final,codigo,cant_eventos,dif_fechas


def sis_por_distancia(sismo_mas,llaves_sismos,sis_en_espacio,n):
    """"
    Encontrar las llaves de los sismos con menor distancia al mas significativo
    """
    long_mas=float(sismo_mas["long"])
    lat_mas=float(sismo_mas["lat"])
    sis_por_distancia=om.newMap(omaptype="RBT")

    for llave_sis in lt.iterator(llaves_sismos):
        sismo_n=me.getValue(om.get(sis_en_espacio,llave_sis))
        for sismo in lt.iterator(sismo_n):
            lat1,lon1,lat2,lon2 = map(math.radians, [lat_mas, long_mas, float(sismo["lat"]), float(sismo["long"])])
            dif_long=lon2-lon1
            dif_lat=lat2-lat1
            raiz=((math.sin(dif_lat/2))**2)+((math.cos(lat1))*(math.cos(lat2)*((math.sin(dif_long/2))**2)))
            ars=math.asin(math.sqrt(raiz))
            d=2*(ars)*6371
            sismo["distancia"]=d
            add_data_arbol_list(sis_por_distancia,sismo,"distancia")
    
    dist=om.keySet(sis_por_distancia)
    if lt.size(dist)>n:
        llaves_menor_distancia=lt.subList(dist,1,n)
    else:
        llaves_menor_distancia=dist
    return llaves_menor_distancia,sis_por_distancia


def req_7(data_structs,anio,title,propiedad,casillas):
    """
    Función que soluciona el requerimiento 7
    """
    anios = data_structs["anio"]
    pareja = om.get(anios,anio)
    fechas = me.getValue(pareja)
    total_sis_anio = lt.size(fechas)
    mapa_title = om.newMap(omaptype="RBT")
    mapa_propiedad = om.newMap(omaptype="RBT")
    lista_val_hist = lt.newList("ARRAY_LIST")
 
    for fecha in lt.iterator(fechas):
        if title in fecha["title"] and fecha[propiedad]!= "" and fecha[propiedad]!= 1:
            add_data_arbol_list(mapa_title,fecha,"time")
            add_data_arbol_list(mapa_propiedad,fecha,propiedad)
            lt.addLast(lista_val_hist,fecha[propiedad])


    total_sis_his = om.size(mapa_title)
    prop_min = om.minKey(mapa_propiedad)
    prop_max =om.maxKey(mapa_propiedad)
    sismos_anio = om.keySet(mapa_title)
    lista_final_fechas = lt.newList("ARRAY_LIST")


    for cada_llave in lt.iterator(sismos_anio):
        pareja_2 = om.get(mapa_title,cada_llave)
        fechas = me.getValue(pareja_2)
        for fecha in lt.iterator(fechas):
            dic_imp = {"time": fecha["time"],
                       "lat" : fecha["lat"],
                       "long": fecha["long"],
                       "title": fecha["title"],
                       "code" : fecha["code"],
                       propiedad : fecha[propiedad]}
            lt.addLast(lista_final_fechas, dic_imp)
    
    ancho_intervalo = round((prop_max-prop_min)/casillas,2)
    intervalos = lt.newList("ARRAY_LIST")
    lt.addLast(intervalos,prop_min)
    for i in range(1,casillas):
        primer_elemento = round(prop_min + i*ancho_intervalo,2)
        x = lt.isPresent(intervalos,primer_elemento)
        if x == 0:
            lt.addLast(intervalos,primer_elemento)
        siguiente = round(primer_elemento + ancho_intervalo,2)
        lt.addLast(intervalos,siguiente)

        
    marcas = lt.newList("ARRAY_LIST")
    nombres = lt.newList("ARRAY_LIST")
    mapa_count= om.newMap(omaptype="RBT")
    for i in range(1,lt.size(intervalos)):
        primero = lt.getElement(intervalos,i)
        segundo = lt.getElement(intervalos,i+1)
        A = round(primero+segundo,2)
        B = round(A/2,2)
        lt.addLast(marcas,B)
        cada_nombre = f"({primero} - {segundo}]"
        lt.addLast(nombres,cada_nombre)
        count=0
        for val in lt.iterator(lista_val_hist):
            if i == 1:
                if val >= primero and val <= segundo:
                    count+=1
            else:
                if val > primero and val <= segundo:
                    count+=1
        om.put(mapa_count,cada_nombre,count)
    conteos = om.valueSet(mapa_count)
    return total_sis_anio,total_sis_his,prop_min,prop_max,lista_final_fechas,lista_val_hist,intervalos,marcas,nombres,conteos








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

def cmpFechaReciente(dato1,dato2):
    if dato1["time"] > dato2["time"]:
        return True
    return False


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
