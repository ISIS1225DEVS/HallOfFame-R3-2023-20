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
import math
import folium
from folium.plugins import MarkerCluster
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
    analyzer = {'temblores':None, 
                'dateIndex':None, 
                'dateIndex_1':None,
                'sigIndex':None,
                "depthIndex": None,
                'timeIndex': None,
                'heap': None,
                "magIndex": None,
                'dateHash':None}
    
    analyzer['temblores'] = lt.newList('ARRAY_LIST',compareCodes)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',cmpfunction=compareDates)
    analyzer['dateIndex_1'] = om.newMap(omaptype='RBT',cmpfunction=compareDates)
    analyzer['sigIndex'] = om.newMap(omaptype='RBT',cmpfunction=cmp_sig_may_a_men)
    analyzer['depthIndex'] = om.newMap(omaptype='RBT', cmpfunction=compareAny)
    analyzer['timeIndex'] = om.newMap(omaptype='RBT', cmpfunction=compareAny)
    analyzer['heap'] = mpq.newMinPQ(cmpfunction=compareHeap5)
    analyzer['magIndex'] = om.newMap(omaptype='RBT', cmpfunction=compareAny)
    analyzer['dateHash'] = mp.newMap(150000,maptype='CHAINING', loadfactor=4, cmpfunction=compareMap)
    return analyzer


# Funciones para agregar informacion al modelo

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    updateDateIndex(data_structs['dateIndex'], data)
    updateDateIndex_1(data_structs['dateIndex_1'], data)
    updateMagIndex(data_structs['magIndex'],data)
    updateAnyIndex(data_structs, 'sigIndex', 'gapIndex', data) 
    updateAnyIndex(data_structs, 'depthIndex', 'nstIndex',data)
    updateAnyIndex(data_structs, 'timeIndex', 'depthIndex',data)
    updateDate(data_structs['dateHash'],data)
    return data_structs

def updateDate(date, data):
    if data['time'].year != None:
        year = data['time'].year
    else:
        year = 'unknown'
    existyear = mp.contains(date,year)
    if existyear:
            entry = mp.get(date, year)
            year_present = me.getValue(entry)
    else:
        year_present = new_year(year)
        mp.put(date, year, year_present)
    lt.addLast(year_present['temblores'], data)

def updateDateIndex(dateIndex, data):
    """
    Función para agregar nuevos elementos a la tabla de símbolos
    """
    temblordate = data['time']
    entry = om.get(dateIndex, temblordate.date())
    if entry is None:
        datentry = newDateEntry(data)
        om.put(dateIndex, temblordate.date(),datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry,data)
    return dateIndex

def updateAnyIndex(data_structs, key, sub_key, data):
    """
    Función para agregar nuevos elementos a la tabla de símbolos
    """
    main_key = data[key[:len(key)-5]]
    entry = om.get(data_structs[key], main_key)
    if entry is None:
        datentry = newAnyEntry(sub_key)
        om.put(data_structs[key], main_key, datentry)
    else:
        datentry = me.getValue(entry)
    addAnyIndex(datentry, sub_key, data)
    return data_structs

def updateDateIndex_1(dateIndex, data):
    """
    Función para agregar nuevos elementos a la tabla de símbolos
    """
    temblordate = data['time']
    entry = om.get(dateIndex, temblordate)
    if entry is None:
        datentry = newDateEntry_1(data)
        om.put(dateIndex, temblordate,datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry,data)
    return dateIndex

def updateHeap(data_structs):
    times = om.keySet(data_structs['timeIndex'])
    for key in lt.iterator(times):
        elemento  = om.get(data_structs['timeIndex'],key)
        mpq.insert(data_structs['heap'],elemento)
    return data_structs

def updateMagIndex(magIndex, data):
    """
    Función para agregar nuevos elementos a la tabla de símbolos
    """
    temblormag = round(data['mag'],3)
    entry = om.get(magIndex, temblormag)
    if entry is None:
        magentry = newMagEntry(data)
        om.put(magIndex,round(temblormag,3),magentry)
    else:
        magentry = me.getValue(entry)
    addMagIndex(magentry,data)
    return magIndex

def addMagIndex(datentry, data):
    """
    Actualiza un indice de tipo de temblores.  Este indice tiene una lista
    de temblores y una tabla de hash cuya llave es la magnitud del temblor y
    el valor es una lista con los temblores de dicha magnitud en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstemblores']
    lt.addLast(lst, data)
    return datentry


def addAnyIndex(datentry, sub_key, data):
    """
    Actualiza un indice de tipo de temblores.  Este indice tiene una lista
    de temblores y una tabla de hash cuya llave es la magnitud del temblor y
    el valor es una lista con los temblores de dicha magnitud en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstemblores']
    lt.addLast(lst, data)
    sub_map = datentry[sub_key]
    sub_entry = om.get(sub_map,data[sub_key[:len(sub_key)-5]])
    if sub_entry is None:
        entry = {'lstemblores':lt.newList('SINGLE_LINKED',cmpfunction=compareCodes)}
        lt.addLast(entry['lstemblores'], data)
        om.put(sub_map, data[sub_key[:len(sub_key)-5]], entry)
    else:
        entry = me.getValue(sub_entry)
        lt.addLast(entry['lstemblores'],data)
    return datentry

def addDateIndex(datentry, data):
    """
    Actualiza un indice de tipo de temblores.  Este indice tiene una lista
    de temblores y una tabla de hash cuya llave es la magnitud del temblor y
    el valor es una lista con los temblores de dicha magnitud en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstemblores']
    lt.addLast(lst, data)
    return datentry

# Funciones para creacion de datos

def newDateEntry_1(data):
    """
    Crea una entrada en el árbol binario por fechas
    """
    #TODO: Crear la función para estructurar los datos
    entry = {'lstemblores': None}
    entry['lstemblores'] = lt.newList('ARRAY_LIST',compareCodes)
    return entry

def newDateEntry(data):
    """
    Crea una entrada en el árbol binario por fechas
    """
    #TODO: Crear la función para estructurar los datos
    entry = {'lstemblores': None}
    entry['lstemblores'] = lt.newList('ARRAY_LIST',compareCodes)
    return entry

def newAnyEntry(sub_key):
    tembentry = {sub_key:None, 'lstemblores': None}
    tembentry[sub_key] = om.newMap(omaptype='RBT', cmpfunction=compareAny)
    tembentry['lstemblores'] = lt.newList('ARRAY_LIST', compareCodes)
    return tembentry

def new_year(year):
    entry = {'year':"", 'temblores':None}
    entry['year'] = year
    entry['temblores'] = lt.newList('ARRAY_LIST', compareCodes)
    return entry

def newMagEntry(mag):
    """
    Crea una entrada en el indice por magnitud del temblor, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    magentry = {'lstemblores':None}
    magentry['lstemblores'] = lt.newList('ARRAY_LIST', compareCodes)
    return magentry

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

def req_1(data_structs, initialDate, finalDate):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    dateIndex = data_structs['dateIndex_1']
    lst = om.values(dateIndex, initialDate, finalDate)
    size = 0
    for date in lt.iterator(lst):
        size += lt.size(date['lstemblores'])
    
    return lst, size
        
    
def req_2(data_structs, magMin, magMax):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    
    magMin = round(float(magMin),1)
    magMax = round(float(magMax),1)
    magIndex = data_structs['magIndex']
    lst = om.values(magIndex,magMin,magMax)
    size = 0
    for mag in lt.iterator(lst):
        size += lt.size(mag['lstemblores'])
    return lst, size  


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass
def req_3(data_structs, magMin, depthMax):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    magIndex = data_structs['magIndex']
    fechas = lt.newList('ARRAY_LIST')
    
    resultado = {"resul": lt.newList("SINGLE_LINKED"), 
                 "total": 0}
    magMax = om.maxKey(magIndex)
    magni = om.keys(magIndex, magMin, magMax) #lista con magnitudes de interes 
    
    
    for magnitud in lt.iterator(magni): 
        entry = om.get(magIndex, magnitud)
        entryTemb = me.getValue(entry)
        temblores = entryTemb["lstemblores"]
        for temb in  lt.iterator(temblores):
            if float(temb["depth"])<= float(depthMax):
                lt.addLast(fechas, temb)
    sortReq2(fechas)
    
    tamaño = lt.size(fechas) 
    
    if tamaño <= 10: 
        prim_temblores = lt.subList(fechas,1,tamaño)
    else:
        prim_temblores = lt.subList(fechas,1,10)
           
    tama = lt.size(prim_temblores)
    if tama <= 6: 
        prim_tres_temblores = lt.subList(prim_temblores,1,tama)
        ulti_tres_temblores = lt.newList()
    else:
        prim_tres_temblores = lt.subList(prim_temblores,1,3)
        ulti_tres_temblores = lt.subList(prim_temblores,tama-2,3)
        
    lt.addLast(resultado['resul'], prim_tres_temblores)
    lt.addLast(resultado['resul'], ulti_tres_temblores)
    resultado['total'] = tamaño
    return resultado


def req_4(data_structs, sig, gap):
    """
    Función que soluciona el requerimiento 4: Consultar los 15 eventos sísmicos 
    más recientes, mayores o iguales a una significancia sig y menores o iguales 
    a una distancia azimutal gap.
    """
    sigIndex = data_structs['sigIndex']
    size = 0
    lt_15 = lt.newList()
    sig_values = om.values(sigIndex, sig, om.maxKey(sigIndex)) # Entradas en el rango de significancia
    for sig_info in lt.iterator(sig_values): # Registros en el rango de significancia
        gap_values = om.values(sig_info['gapIndex'],0,gap) # Entradas en el rango de distancia azimutal
        for gap_info in lt.iterator(gap_values): # Registros en el rango de distancia azimutal
            for eq in lt.iterator(gap_info['lstemblores']):
                # Agregar valor la lista y sumar la unidad a la consulta
                lt_15 = update_lt_15(lt_15, eq)
                size += 1
    return lt_15, size

def update_lt_15(lt_15, eq):
    # Ver si hay elementos en la lista
    if lt.isEmpty(lt_15):
        lt.addLast(lt_15, eq)
    else:
        # Ver si el nuevo elemento ocurrió después de los demás
        size_lt_15 = lt.size(lt_15)
        if size_lt_15 == 1:
            lt.addLast(lt_15,eq)
        for i in range(1, size_lt_15+1):
            eq15 = lt.getElement(lt_15, i)
            if eq['time']>eq15['time']:
                lt.insertElement(lt_15,eq,i)
                break
        if lt.lastElement(lt_15)['time'] > eq['time']:
            lt.addLast(lt_15,eq)
        if lt.size(lt_15) > 15:
            lt_15 = lt.subList(lt_15,1,15)
    return lt_15

def req_5(data_structs, depth, nst):
    """
    Función que soluciona el requerimiento 5
    """
    respuesta = lt.newList('ARRAY_LIST', compareCodes)
    size = 0
    mags = data_structs['depthIndex']
    lst_p = om.values(mags, depth, om.maxKey(mags))

    for rbt in lt.iterator(lst_p):
        ord_m = rbt['nstIndex']
        lst_n = om.values(ord_m, nst, om.maxKey(ord_m))
        for lst in lt.iterator(lst_n):
            size += lt.size(lst['lstemblores'])
    
    dep = data_structs['heap']
    for i in range(1,mpq.size(dep)+1):
        elemento = mpq.delMin(dep)
        elemento = me.getValue(elemento)
        elementos = om.values(elemento['depthIndex'],depth,om.maxKey(elemento['depthIndex']))
        for dato in lt.iterator(elementos):
            for dato1 in lt.iterator(dato['lstemblores']):
                if dato1['nst'] >= nst:
                    lt.addLast(respuesta,dato1)
                if lt.size(respuesta) == 20:
                    return respuesta, size
    return respuesta, size
    

def req_6(data_structs, year, lat, long, radio, n):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    year_entry = me.getValue(mp.get(data_structs['dateHash'],year))
    lst = lt.newList('ARRAY_LIST', compareCodes)
    mayor_sig = -100000000
    mayor = None 
    for elemento in lt.iterator(year_entry['temblores']):
        d = distancia(elemento['lat'], elemento['long'], lat, long)
        if d <= radio:
            lt.addLast(lst, elemento)
            if elemento['sig'] > mayor_sig:
                mayor_sig = elemento['sig']
                mayor = elemento
    pos = lt.isPresent(lst, mayor)
    if (lt.size(lst) - pos) >= n:
        if pos - 1 >= n:
            r = lt.subList(lst,pos-n,2*n+1)
        else:
            r = lt.subList(lst,1,pos+n)
    else:
        if pos - 1 >= n:
            r = lt.subList(lst,pos-n,lt.size(lst)-(pos-n)+1)
        else:
            r = lst
    return r, mayor, lst


def distancia(lat1, long1, lat2, long2):
    lat1 = lat1 * math.pi/180
    lat2 = lat2 * math.pi/180
    long1 = long1 * math.pi/180
    long2 = long2 * math.pi/180
    a = math.sin((lat2-lat1)/2)
    b = math.cos(lat1)
    c = math.cos(lat2)
    d = math.sin((long2-long1)/2)
    e = a**2
    f = d**2
    g = e + b*c*f
    h = g**(1/2)
    i = math.asin(h)
    r = 2*i*6371
    return r


def req_7(data_structs, year, area, prop, bins):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    # Obtener los registros en el año
    st_date = datetime.date(year=year, month=1, day=1)
    end_date = datetime.date(year=year, month=12, day=31)
    eq_year = om.values(data_structs['dateIndex'], st_date, end_date)
    #Obtener los registros en el área
    lt_hist_data = lt.newList(cmpfunction=compareCodes)
    total = lt.newList('ARRAY_LIST',cmpfunction=compareCodes)
    num_eq_year = 0
    num_eq_year_title = 0
    if not lt.isEmpty(eq_year):
        for eq_info in lt.iterator(eq_year):
            eq_lst = eq_info['lstemblores']
            for eq in lt.iterator(eq_lst):
                num_eq_year += 1
                if area.lower() in eq['title'].lower():
                    num_eq_year_title += 1
                    #Agregar los registros que cumplen a la lista 
                    lt.addLast(lt_hist_data, eq)
                lt.addLast(total,eq)
    h_bins, h_values, min_val, max_val = histogram_data_req7(lt_hist_data, prop, bins)
    lt_hist_data = merg.sort(lt_hist_data, compareReq4)
    return num_eq_year, num_eq_year_title, h_bins, h_values, min_val, max_val, lt_hist_data, total


def histogram_data_req7(data, prop, bins):
    data = sortReq7(data, prop)
    # Valores mínimo y máximo
    if not lt.isEmpty(data):
        min_val = lt.firstElement(data)[prop]
        max_val = lt.lastElement(data)[prop]
        # Intervalos
        len_bins = (max_val-min_val)/bins
        h_bins = lt.newList('ARRAY_LIST')
        lim = min_val
        for i in range(bins):
            lt.addLast(h_bins, lim)
            lim += len_bins
        lt.addLast(h_bins, max_val)
        # Valores histograma
        h_values = lt.newList('ARRAY_LIST')
        for eq in lt.iterator(data):
            if not eq[prop] == 'unknown':
                lt.addLast(h_values, eq[prop])
    else:
        h_bins = lt.newList('ARRAY_LIST')
        h_values = lt.newList('ARRAY_LIST')
        min_val = 0
        max_val = 0
    return h_bins, h_values, min_val, max_val


def req_8(data_structs, req, parametros):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    locations = lt.newList("ARRAY_LIST")
    msg = lt.newList('ARRAY_LIST')
    
    if req == 1:
        r = req_1(data_structs, lt.getElement(parametros,1),lt.getElement(parametros,2))[0]
        m = folium.Map( zoom_start=100)
        for date in lt.iterator(r):
            for dato in lt.iterator(date['lstemblores']):
                lt.addLast(locations,(dato['lat'],dato['long']))
                lt.addLast(msg,dato)
        MarkerCluster(locations=locations['elements'],popups=msg['elements']).add_to(m)

    elif req == 2:
        r = req_2(data_structs, lt.getElement(parametros,1),lt.getElement(parametros,2))[0]
        m = folium.Map( zoom_start=100)
        for date in lt.iterator(r):
            for dato in lt.iterator(date['lstemblores']):
                lt.addLast(locations,(dato['lat'],dato['long']))
                lt.addLast(msg,dato)
        MarkerCluster(locations=locations['elements'],popups=msg['elements']).add_to(m)

    elif req == 4:
        r = req_4(data_structs,lt.getElement(parametros,1),lt.getElement(parametros,2))[0]
        if lt.size(r) < 15:
            r = r
        else:
            r = lt.subList(r,1,15)
        m = folium.Map( zoom_start=100)
        for dato in lt.iterator(r):
            lt.addLast(locations,(dato['lat'],dato['long']))
            lt.addLast(msg,dato)
        MarkerCluster(locations=locations['elements'],popups=msg['elements']).add_to(m)
        
    elif req == 5:
        r = req_5(data_structs, lt.getElement(parametros,1),lt.getElement(parametros,2))[0]
        m = folium.Map( zoom_start=100)
        for dato in lt.iterator(r):
            lt.addLast(locations,(dato['lat'],dato['long']))
        MarkerCluster(locations=locations['elements'],popups=r['elements']).add_to(m)
    
    elif req == 6:
        r = req_6(data_structs,lt.getElement(parametros,1),lt.getElement(parametros,2),lt.getElement(parametros,3),lt.getElement(parametros,4),lt.getElement(parametros,5))[0]
        m = folium.Map( zoom_start=100)
        folium.Circle(location=[lt.getElement(parametros,2),lt.getElement(parametros,3)],radius=lt.getElement(parametros,4)*1000).add_to(m)
        for dato in lt.iterator(r):
            lt.addLast(locations,(dato['lat'],dato['long']))
        MarkerCluster(locations=locations['elements'],popups=r['elements']).add_to(m)

    elif req == 7:
        r = req_7(data_structs, lt.getElement(parametros,1),'Alaska',lt.getElement(parametros,2), 1)[7]
        m = folium.Map( zoom_start=100)
        for dato in lt.iterator(r):
            lt.addLast(locations,(dato['lat'],dato['long']))
        MarkerCluster(locations=locations['elements'],popups=r['elements']).add_to(m)
    return m


# Funciones utilizadas para comparar elementos dentro de una lista

def compareCodes(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    r = 1
    if data_1['code'] == data_2['code']:
        r = 0
    elif data_1['code'] < data_2['code']:
        r = -1
    return r

def compareDates(date1, date2):
    """
    Función encargada de comparar dos fechas
    """
    r = 1
    if date1 == date2:
        r = 0
    elif date1 < date2:
        r = -1
    return r

def compareTemblores(temblor1, temblor2):
    """
    Compara dos temblores por magnitud
    """
    mag = me.getKey(temblor2)
    r = 1
    if temblor1 == mag:
        r = 0
    elif temblor1 < mag:
        r = -1
    return r

def compareMag(dato1, dato2):
    if dato1['mag'] > dato2['mag']:
        return 1
    elif dato1['mag'] == dato2['mag']:
        return 0
    else:
        return -1

def cmp_mag_men_a_may(evento1, evento2):
    """
    Compara dos eventos por el criterio indicado para ordenarlos de menor a mayor. 
    Retorna true si el criterio 1 es "menor" (debe ir primero en la lista)
    al criterio 2, y false de lo contrario.
    """
    if evento1['mag'] < evento2['mag']:
        return True
    else:
        return False
    
def compareAny(key1, key2):
    """
    Función encargada de comparar dos magnitudes (RBT)
    """
    r = 1
    if key1 == key2:
        r = 0
    elif key1 < key2:
        r = -1
    return r


def cmp_gap_men_a_may(evento1, evento2):
    """
    Compara dos eventos por el criterio indicado para ordenarlos de menor a mayor. 
    Retorna true si el criterio 1 es "menor" (debe ir primero en la lista)
    al criterio 2, y false de lo contrario.
    """
    if evento1['gap'] < evento2['gap']:
        return True
    else:
        return False
    
def cmp_depth_men_a_may(evento1, evento2):
    """
    Compara dos eventos por el criterio indicado para ordenarlos de menor a mayor. 
    Retorna true si el criterio 1 es "menor" (debe ir primero en la lista)
    al criterio 2, y false de lo contrario.
    """
    if evento1['depth'] < evento2['depth']:
        return True
    else:
        return False

def cmp_sig_men_a_may(evento1, evento2):
    """
    Compara dos eventos por el criterio indicado para ordenarlos de menor a mayor. 
    Retorna true si el criterio 1 es "menor" (debe ir primero en la lista)
    al criterio 2, y false de lo contrario.
    """
    if evento1['sig'] < evento2['sig']:
        return True
    else:
        return False
    
def cmp_sig_may_a_men(evento1, evento2):
    """
    Compara dos eventos por el criterio indicado para ordenarlos de menor a mayor. 
    Retorna true si el criterio 1 es "mayor" (debe ir primero en la lista)
    al criterio 2, y false de lo contrario.
    """
    if evento1 > evento2:
        return 1
    elif evento1 < evento2:
        return -1
    else:
        return 0
    
    
def compareReq4(evento1, evento2):
    """
    Función encargada de comparar dos fechas, para ordenar una lista de
    más reciente a más antigua.
    """
    if evento1['time'] == evento2['time']:
        if evento1['felt'] > evento2['felt']:
            return True
    elif evento1['time'] > evento2['time']:
        return True
    else:
        return False

def compareHeap2(evento1, evento2):
    """
    Función encargada de comparar dos eventos para agragarlos a la cola de prioridad
    por fechas del requerimiento 4.
    """
    if evento1['mag'] == evento2['mag']:
        if evento1['time'] < evento2['time']:
            return 1
        else:
            return 0
    elif evento1['mag'] < evento2['mag']:
        return 1
    else:
        return -1
    
def compareHeap4(evento1, evento2):
    """
    Función encargada de comparar dos eventos para agragarlos a la cola de prioridad
    por fechas del requerimiento 4.
    """
    if evento1['time'] == evento2['time']:
        if evento1['felt'] < evento2['felt']:
            return 1
        else:
            return 0
    elif evento1['time'] < evento2['time']:
        return 1
    else:
        return -1

def compareHeap5(evento1,evento2):
    key1 = me.getKey(evento1)
    key2 = me.getKey(evento2)
    if key1 < key2:
        return 1
    elif key1 == key2:
        return 0
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

def sortbygap(sigIndex):
    """
    Función encargada de ordenar la lista con las distancias azimutales dentro 
    de cada elemento del árbol por significancias.
    """
    for sig_key in lt.iterator(om.keySet(sigIndex)):
        merg.sort(me.getValue(om.get(sigIndex, sig_key))['lstemblores'],cmp_gap_men_a_may)

def sortbydate(dateIndex):
    lst = om.values(dateIndex, om.minKey(dateIndex), om.maxKey(dateIndex))
    for date in lt.iterator(lst):
        merg.sort(date['lstemblores'], sort_criteria_date)

def sort_criteria_date(dato1, dato2):
    r = False
    if dato1['time'] > dato2['time']:
        r = True
    elif dato1['time'] == dato2['time']:
        if dato1['mag'] > dato2['mag']:
            r = True
    return r

def sort_criteria_date_2(dato1, dato2):
    r = False
    if dato1['time'] > dato2['time']:
        r = True
    elif dato1['time'] == dato2['time']:
        if dato1['felt'] > dato2['felt']:
            r = True
    return r
    
def sortReq2(lst): 
    lst = merg.sort(lst, compareReq2)
    return lst

def compareReq2(temblor_1, temblor_2):
    
    if temblor_1["time"] < temblor_2["time"]:
        return True 
    else:
        return False
def sortReq4(lst):
    lst = se.sort(lst, compareReq4)
    return lst

def sortReq5(lst):
    lst = merg.sort(lst, sort_crit=sort_criteria_date)
    return lst
    
def sortReq7(lst, prop):
    if prop == 'sig':
        lst = merg.sort(lst, cmp_sig_men_a_may)
    elif prop == 'depth':
        lst = merg.sort(lst, cmp_depth_men_a_may)
    elif prop == 'mag':
        lst = merg.sort(lst, cmp_mag_men_a_may)
    return lst

def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    data_structs['temblores'] = merg.sort(data_structs['temblores'],sort_criteria_date_2)
    return data_structs

def compareMap(key, entry):

    key_entry = me.getKey(entry)
    respuesta = -1
    if key == key_entry:
        respuesta = 0
    if key > key_entry:
        respuesta = 1
    return respuesta