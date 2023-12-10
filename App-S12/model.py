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
import datetime
from tabulate import tabulate
import controller
from math import sin, cos, sqrt, atan2, radians, asin
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
    #TODO: Inicializar las estructuras de datos
    data_structs = {
        'temblores': None,
        'anio': None, 
        'magnitud': None, 
        'fecha' : None,
        'depth' : None
    }   
    data_structs['temblores'] = lt.newList()
    data_structs['anio'] = om.newMap(omaptype='RBT', cmpfunction=comparedate)
    data_structs['magnitud'] = om.newMap(omaptype='RBT', cmpfunction=comparemag)
    data_structs['fecha'] = om.newMap(omaptype='RBT', cmpfunction=comparedate)
    data_structs['depth'] = om.newMap(omaptype='RBT', cmpfunction=comparedepth)
    data_structs['sig'] = om.newMap(omaptype='RBT', cmpfunction=comparedate)

    return data_structs

# Funciones para agregar informacion al modelo

def updateDate(data_structs, temblor):
    fecha = str(temblor["time"].date())
    date = fecha[0:4]
    date = int(date)
    entry = om.get(data_structs, date)
    if entry == None:
        dateentry = newdateEntry(temblor)
        om.put(data_structs, date, dateentry)
    else:
        dateentry = me.getValue(entry)
    addDate(dateentry, temblor)
    return data_structs


def newdateEntry(temblor):
    entry = {"lsttemblores" : None,
             "arbol_signifancia" : None}
    entry["lsttemblores"] = lt.newList("SINGLE_LINKED", comparedate)
    entry["arbol_signifancia"] = om.newMap(omaptype='RBT', cmpfunction=comparedate)
    return entry

def addDate(dateentry, temblor):
    lt.addLast(dateentry["lsttemblores"], temblor)
    
    sig = temblor["sig"]
    if sig == 'Unknown':
        sig = 0
    else:
        sig = float(sig)
        
    if om.contains(dateentry["arbol_signifancia"],sig):
        value = me.getValue(om.get(dateentry["arbol_signifancia"], sig))
    else:
        value = lt.newList()
        om.put(dateentry["arbol_signifancia"], sig, value) 
    lt.addLast(value, temblor) 


def updateMag(data_structs, temblor):
    mag = float(temblor["mag"])
    entry = om.get(data_structs, mag)
    if entry == None:
        magentry = newmagEntry(temblor)
        om.put(data_structs, mag, magentry)
    else:
        magentry = me.getValue(entry)
    addMag(magentry, temblor)
    return data_structs

def newmagEntry(temblor):
    entry = {"lsttemblores" : None,
             "arbol_profundidad" : None}
    entry["lsttemblores"] = lt.newList("SINGLE_LINKED", comparemag)
    entry['arbol_profundidad'] = om.newMap(omaptype='RBT')
    return entry

def addMag(magentry, temblor):
    lst = magentry["lsttemblores"]
    depth = temblor['depth']
    if depth == 'Unknown':
        depth= 0
    else:
        depth = float(depth)
        
    if om.contains(magentry["arbol_profundidad"],depth):
        value = me.getValue(om.get(magentry["arbol_profundidad"], depth))
    else:
        value = lt.newList()
        om.put(magentry["arbol_profundidad"], depth, value)
    lt.addLast(value, temblor)
    lt.addLast(lst, temblor)
    return magentry

def add_temblor(data_structs, temblor):
    lt.addLast(data_structs['temblores'], temblor)

def updateDate_fecha(data_structs, temblor):
    fecha = temblor["time"]
    entry = om.get(data_structs, fecha)
    if entry == None:
        dateentry = newdateEntry_fecha(temblor)
        om.put(data_structs, fecha, dateentry)
    else:
        dateentry = me.getValue(entry)
    addDate_fecha(dateentry, temblor)
    return data_structs

def newdateEntry_fecha(temblor):
    entry = {"lsttemblores" : None}
    entry["lsttemblores"] = lt.newList("SINGLE_LINKED")
    return entry

def addDate_fecha(dateentry, temblor):
    lst = dateentry["lsttemblores"]
    lt.addLast(lst, temblor)
    return dateentry    

def updatedepth(data_structs, temblor):
    depth = float(temblor['depth'])
    entry = om.get(data_structs, depth)
    if entry == None:
        depthentry = newdepthentry(temblor)
        om.put(data_structs, depth, depthentry)
    else:
        depthentry = me.getValue(entry)
    addDepth(depthentry, temblor)
    return data_structs
        
def newdepthentry(temblor):
    entry = {'lsttemblores':None}
    entry['lsttemblores'] = lt.newList('SINGLE_LINKED')
    return entry

def addDepth(depthentry, temblor):
    lst = depthentry['lsttemblores']
    lt.addLast(lst, temblor)
    return depthentry
# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def size_data(data_structs):
    return lt.size(data_structs['temblores'])


def req_1(data_structs, date1, date2):
    """
    Función que soluciona el requerimiento 1S
    """
    # TODO: Realizar el requerimiento 1
    arbol_fecha = data_structs['fecha']
    lista_rangos = om.values(arbol_fecha, date1, date2)
    tamaño_rangos = lt.size(lista_rangos) 
    llaves = om.keys(arbol_fecha, date1, date2)
    lista_retorno = lt.newList()
    
    if tamaño_rangos > 6:
        lista_rangos = get3(lista_rangos)
        keys_1=6
        for mag in range(1,keys_1+1):
            sig = lt.getElement(llaves, mag)
            lista = me.getValue(om.get(arbol_fecha, sig))
            merg.sort(lista['lsttemblores'],sort_criteria_date)
            
    else:
        for mag in range(1,tamaño_rangos+1):
            sig = lt.getElement(llaves, mag)
            lista = me.getValue(om.get(arbol_fecha, sig))
            merg.sort(lista['lsttemblores'],sort_criteria_date)

    titulos = ['mag', 'lat', 'long', 'depth', 'sig', 'gap','nst', 'title', 'cdi', 'mmi', 'magType', 'type', 'code']
    
    for dato in lt.iterator(lista_rangos):
        diccionario = {}
        diccionario['time'] = dato['lsttemblores']['first']['info']['time']
        diccionario['eventos'] = lt.size(dato['lsttemblores'])
        filtro = filtrar(dato['lsttemblores'], titulos)
        diccionario['details'] = tabulate(lt.iterator(filtro), headers='keys', tablefmt= 'fancy_grid')
        lt.addLast(lista_retorno, diccionario)
    
    merg.sort(lista_retorno, comparedate_req1)
    return tamaño_rangos, lista_retorno

def req_2(data_structs,limite_inf, limite_sup):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    datos = data_structs['magnitud']
    magnitudes = om.values(datos, limite_inf, limite_sup)
    llaves = om.keys(datos, limite_inf, limite_sup)
    keys = om.size(magnitudes) #retorna el la cantidad de magnitudes en el rango
    size = 0 #Cantidad total de temblores en el rango
    lista_retorno = lt.newList()
    
    for mag in lt.iterator(magnitudes):
        size += om.size(mag['lsttemblores'])

    if keys > 6:
        magnitudes = get3(magnitudes)
        llave3 = 0
        keys_1=6
        for mag in range(1,keys_1+1):
            sig = lt.getElement(llaves, mag)
            lista = me.getValue(om.get(datos, sig))
            merg.sort(lista['lsttemblores'],sort_criteria_date)
        for mg in lt.iterator(magnitudes):
            llave3 += om.size(mg['lsttemblores'])

    else:
        llave3 = llaves
        for mag in range(1,keys+1):
            sig = lt.getElement(llaves, mag)
            lista = me.getValue(om.get(datos, sig))
            merg.sort(lista['lsttemblores'],sort_criteria_date)

    titulos = ['time', 'lat', 'long', 'depth', 'sig', 'gap', 'nst', 'title', 'cdi', 'mmi', 'magType', 'type', 'code']
    
    for dato in lt.iterator(magnitudes):
        lst = lt.newList()
        lt.addFirst(lst, dato['lsttemblores']['first']['info']['mag'])
        diccionario = {}
        diccionario['mag'] = dato['lsttemblores']['first']['info']['mag']
        diccionario['events'] = lt.size(dato['lsttemblores'])
        filtro = filtrar(dato['lsttemblores'], titulos)
        if lt.size(filtro)>6:
            filtro = get3(filtro)
        quk.sort(filtro, sort_criteria_date)
        diccionario['details'] = tabulate(lt.iterator(filtro), headers='keys', tablefmt= 'fancy_grid')
        lt.addFirst(lista_retorno, diccionario)


    return size, keys, lista_retorno, llave3


def req_3(data_structs, mags, profundidad):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    arbol_mags = data_structs['magnitud']
    mayor = lt.lastElement(om.keySet(arbol_mags))
    keys_mag = om.keys(arbol_mags, mags, mayor)
    lista_requisito = lt.newList()
    lista_retorno = lt.newList()
    numero_total = 0
    for mayores in lt.iterator(keys_mag):
        value_mag = me.getValue(om.get(arbol_mags, mayores))
        arbol_depth = value_mag['arbol_profundidad']
        prof = om.keySet(arbol_depth)
        for i in range(1,(lt.size(arbol_depth)+1)):
            dep = lt.getElement(prof, i)
            lista = me.getValue(om.get(arbol_depth, dep))
            for elemento in lt.iterator(lista):
                if float(elemento['depth']) <= profundidad:
                    lt.addLast(lista_requisito, elemento)
                    numero_total += 1
     
    merg.sort(lista_requisito, comparedate_req1)
    lista_10 = lt.subList(lista_requisito,1,10)
    titulos = ['mag','lat', 'long', 'depth', 'sig', 'gap', 'nst', 'title', 'cdi', 'mmi', 'magType', 'type', 'code']

    for finales in lt.iterator(lista_10):
        dicc = {}
        papa_inoa =lt.newList()
        lt.addLast(papa_inoa, finales)
        filtro = filtrar(papa_inoa, titulos)
        dicc['time'] = finales['time']
        dicc['events'] = lt.size(filtro)
        dicc['details'] = tabulate(lt.iterator(filtro),headers='keys', tablefmt='fancy_grid')
        lt.addLast(lista_retorno, dicc)
    
    return lista_retorno, numero_total
    


def req_4(data_structs, sigMin, gapMax):
    """
    Función que soluciona el requerimiento 4
    """
    values_sig = om.values(data_structs['sig'], sigMin, om.maxKey(data_structs['sig']))
    dates = om.newMap()

    for value_sig in lt.iterator(values_sig):
        values_gap = om.values(value_sig['gap'], om.minKey(value_sig['gap']),gapMax)
        for value_gap in lt.iterator(values_gap):
            for temblor in lt.iterator(value_gap['lsttemblores']):
                date = temblor['time']
                if om.contains(dates, date):
                    value_date = me.getValue(om.get(dates, date))
                else:
                    value_date = lt.newList()
                    om.put(dates, date, value_date)
                lt.addLast(value_date, temblor)

    lista_retorno = lt.newList()
    fechas = om.keySet(dates)
    values = om.valueSet(dates)

    eventos = 0
    for i in range(1, (lt.size(fechas)+1)):
        date = lt.getElement(fechas, i)
        value = lt.getElement(values, i)
        diccionario = {}
        diccionario["date"] = date
        diccionario["events"] = lt.size(value)
        diccionario["details"] = value
        eventos += lt.size(value)
        lt.addFirst(lista_retorno, diccionario)            

    return lt.size(fechas), eventos, lista_retorno

def updateSig(data_structs, temblor):
    sig = float(temblor["sig"])
    entry = om.get(data_structs, sig)
    if entry == None:
        sigentry = newsigEntry(temblor)
        om.put(data_structs, sig, sigentry)
    else:
        sigentry = me.getValue(entry)
    addSig(sigentry, temblor)
    return data_structs

def newsigEntry(temblor):
    entry = {"gap" : None}
    entry["gap"] = om.newMap(omaptype='RBT', cmpfunction=comparedate)
    return entry

def addSig(sigentry, temblor):
    if temblor["gap"] == '':
        temblor["gap"] = 0
    gap =float(temblor["gap"])
    entry = om.get(sigentry["gap"], gap)
    if entry == None:
        gapentry = newgapEntry(temblor)
        om.put(sigentry["gap"], gap, gapentry)
    else:
        gapentry = me.getValue(entry)
    addGap(gapentry, temblor)

def newgapEntry(temblor):
    entry = {"lsttemblores" : None}
    entry["lsttemblores"] = lt.newList("SINGLE_LINKED")
    return entry

def addGap(gapentry, temblor):
    lst = gapentry["lsttemblores"]
    lt.addLast(lst, temblor)


def req_5(data_structs, mindepth, minest):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    datos = data_structs['depth']
    maxi = lt.lastElement((om.keySet(datos)))
    depths = om.values(datos, mindepth, maxi)
    filtro1 = om.newMap('RBT', comparedate_inverse)
    lista_retorno = lt.newList()
    for dato in lt.iterator(depths):
        lst = dato['lsttemblores']
        for dato2 in lt.iterator(lst):
            nst = float(dato2['nst'])
            fecha = dato2['time']
            if nst >= minest:
                entry = om.get(filtro1, fecha)
                if entry == None:
                    fechentry = new_parareq5(fecha)
                    om.put(filtro1, fecha, fechentry)
                else:
                    fechentry = me.getValue(entry)
                add_parareq5(fechentry, dato2)
    mini = om.minKey(filtro1)
    maxi2 = om.maxKey(filtro1)
    filtro2 = om.values(filtro1, mini, maxi2)
    size = om.size(filtro2) #RETORNAR, cantidad de fechas diferentes
    eventos = 0

    for ev in lt.iterator(filtro2):
        eventos += om.size(ev['lstfecha']) #RETORNAR, Numero total de eventos

    if om.size(filtro2)>20:
        filtro3 = lt.subList(filtro2, 1, 20)

    titulos = ['mag', 'lat', 'long', 'depth', 'sig', 'gap', 'nst', 'title', 'cdi', 'mmi', 'magType', 'type', 'code']
    
    for dato in lt.iterator(filtro3):
        liste = lt.newList()
        lt.addLast(liste, dato['lstfecha']['first']['info']['time'])
        diccionario = {}
        diccionario['time'] = dato['lstfecha']['first']['info']['time']
        diccionario['events'] = lt.size(dato['lstfecha'])
        filtrera = filtrar(dato['lstfecha'], titulos)
        if lt.size(filtrera) > 6:
            filtrera = get3(filtrera)
        merg.sort(filtrera, comparedate)
        diccionario['details'] = tabulate(lt.iterator(filtrera), headers = 'keys', tablefmt= 'fancy_grid')
        lt.addLast(lista_retorno, diccionario)

    if lt.size(lista_retorno) > 6:
        lista_retorno = get3(lista_retorno)
    return size, eventos, lista_retorno


def new_parareq5(fecha):
    entry = {'lstfecha' : None}
    entry['lstfecha'] = lt.newList('SINGLE_LINKED', comparedate)
    return entry

def add_parareq5(fecha, dato):
    lst = fecha['lstfecha']
    lt.addLast(lst, dato)
    return fecha


def req_6(data_structs, anio, lat, long, radio, n):
    """
    Función que soluciona el requerimiento 6
    """
    arbol_anios = data_structs['anio']
    value_anio = me.getValue(om.get(arbol_anios, anio))
    arbol_signifancia = value_anio["arbol_signifancia"]
    sigs = om.keySet(arbol_signifancia)
    lista_nax = lt.newList()
    numero_eventos = 0
    lista_fechas = lt.newList()
    for i in range(1,(lt.size(arbol_signifancia)+1)):
        sig = lt.getElement(sigs, i)
        lista = me.getValue(om.get(arbol_signifancia, sig))
        for evento in lt.iterator(lista):
            lat_event = float(evento["lat"])
            long_event = float(evento["long"])
            d = haversine(lat_event, long_event, lat, long)
            if d <= radio and lt.size(lista_nax) == 0:
                lista_max = lista
                numero_eventos += 1
                lt.addLast(lista_fechas, [evento["time"], evento])
            elif d <= radio and lt.size(lista_nax) != 0:
                numero_eventos += 1
                lt.addLast(lista_fechas, [evento["time"], evento])
    merg.sort(lista_fechas, comparedate_req6)
    for i in range(1, (lt.size(lista_fechas)+1)):
        value_fecha = lt.getElement(lista_fechas, i)
        if value_fecha[1]["code"] == lt.firstElement(lista_max)["code"]:
            pos = i
    #n es el numero de eventos que se quieren antes y despues del evento mas significativo
    if pos < n: #Faltan elementos más viejos que pos
        primera_parte = lt.subList(lista_fechas, 1, pos)
    elif pos >= n: #Hay n elementos más viejos que pos
        primera_parte = lt.subList(lista_fechas, (pos-n+1), pos)
    if (pos+n) > lt.size(lista_fechas): #Faltan elementos más nuevos que pos
        segunda_parte = lt.subList(lista_fechas, pos+1, lt.size(lista_fechas))
    elif (pos+n) <= lt.size(lista_fechas): #Hay n elementos más nuevos que pos
        segunda_parte = lt.subList(lista_fechas, pos+1, (pos+n-2))
    lista_eventos = lt.newList()
    
    titulos = ['time', 'mag', 'lat', 'long', 'title', 'depth', 'felt', 'cdi', 'mmi', 'magType', 'type', 'code']
    for elemento in lt.iterator(primera_parte):
        lista = lt.newList()
        lt.addLast(lista,elemento[1])
        diccionario = {}
        diccionario["time"] = elemento[0]
        diccionario["events"] = lt.size(lista)
        diccionario["details"] = tabulate(lt.iterator(filtrar(lista,titulos)), headers='keys', tablefmt='fancy_grid')
        lt.addLast(lista_eventos, diccionario)
    for elemento in lt.iterator(segunda_parte):
        lista = lt.newList()
        lt.addLast(lista,elemento[1])
        diccionario = {}
        diccionario["time"] = elemento[0]
        diccionario["events"] = lt.size(lista)
        diccionario["details"] = tabulate(lt.iterator(filtrar(lista,titulos)), headers='keys', tablefmt='fancy_grid')
        lt.addLast(lista_eventos, diccionario)
             
    maximo_eventos = 2*n
    numero_fechas = lt.size(lista_eventos)
    eventos_entre_fechas = lt.size(lista_eventos)
    
    return numero_eventos, maximo_eventos, numero_fechas, eventos_entre_fechas, lista_max, lista_eventos

def filtrar(lista,titulos):
    lista_r = lt.newList()
    for dato in lt.iterator(lista):
        diccionario = {}
        for titulo in titulos:
             diccionario[titulo] = dato[titulo]
        lt.addLast(lista_r,diccionario)
    return lista_r


def haversine(lat_event, long_event, lat, long):
    lat_event = radians(lat_event)
    long_event = radians(long_event)
    lat = radians(lat)
    long = radians(long)
    fact1 = sin((lat_event-lat)/2)**2
    fact2 = cos(lat_event)*cos(lat)*sin((long_event-long)/2)**2
    d = 2*asin(sqrt(fact1+fact2))*6371
    return d


def req_7(data_structs, anio, title, propiedad, div):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    start = controller.get_time()
    datos = data_structs['anio']
    dato_interes = me.getValue(om.get(datos, anio))
    lst_lugar = lt.newList()
    
    titulos = ['time', 'lat', 'long', 'title', 'code', propiedad]
    
    for dato in lt.iterator(dato_interes['lsttemblores']):
        place = dato['title'].lower()
        if title in place:
            lt.addLast(lst_lugar, dato)
   
    if propiedad == 'mag':
        arblo_usr = om.newMap('RBT', 
                              comparemag)
        
        for dato in lt.iterator(lst_lugar):
            updateDate_fecha(arblo_usr, dato)
        mini = om.minKey(arblo_usr)
        maxi = om.maxKey(arblo_usr)
        lista_usr = om.values(arblo_usr, mini, maxi)
        list3fyl = get3(lista_usr)
        dicc = {'keys':[], 'values':[]}
        for dato in lt.iterator(lista_usr):
            for dato2 in lt.iterator(dato['lsttemblores']):
                dicc['keys'].append(dato2['mag'])
        for dato in lt.iterator(list3fyl):
            value = filtrar(dato['lsttemblores'], titulos)
            for dato2 in lt.iterator(value):
                dicc['values'].append(dato2)

    if propiedad == 'sig':
        arblo_usr = om.newMap('RBT', 
                              comparesig)
        
        for dato in lt.iterator(lst_lugar):
            updateDate_fecha(arblo_usr, dato)
        mini = om.minKey(arblo_usr)
        maxi = om.maxKey(arblo_usr)
        lista_usr = om.values(arblo_usr, mini, maxi)
        list3fyl = get3(lista_usr)
        dicc = {'keys':[], 'values':[]}
        for dato in lt.iterator(lista_usr):
            for dato2 in lt.iterator(dato['lsttemblores']):
                dicc['keys'].append(dato2['sig'])
        for dato in lt.iterator(list3fyl):
            value = filtrar(dato['lsttemblores'], titulos)
            for dato2 in lt.iterator(value):
                dicc['values'].append(dato2)
                
    if propiedad == 'depth':
        arblo_usr = om.newMap('RBT', 
                              comparedepth)
        
        for dato in lt.iterator(lst_lugar):
            updateDate_fecha(arblo_usr, dato)
        mini = om.minKey(arblo_usr)
        maxi = om.maxKey(arblo_usr)
        lista_usr = om.values(arblo_usr, mini, maxi)
        list3fyl = get3(lista_usr)
        dicc = {'keys':[], 'values':[]}
        for dato in lt.iterator(lista_usr):
            for dato2 in lt.iterator(dato['lsttemblores']):
                dicc['keys'].append(dato2['depth'])
        for dato in lt.iterator(list3fyl):
            value = filtrar(dato['lsttemblores'], titulos)
            for dato2 in lt.iterator(value):
                dicc['values'].append(dato2)

    #Creacion de axis, estas lo que hacen es ser la diviosion de las partes de la imagen, siendo ax1 la grafica y ax2 la tabla
    
    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]}, figsize=(6, 6)) #Fig esta solo para poder obtener todos los valores
    n, bins, titulitos = ax1.hist(dicc['keys'], bins=div, color='purple', ec='black')  #n esta solo para poder obtener todos los valores
    ax1.set_xticks([])
    ax1.set_title('Historigram of {} in {} in {}'.format(propiedad, title, anio))
    ax1.set_ylabel('No. Events')
    ax1.set_xlabel(propiedad)

    # Añadir etiquetas de rango debajo de cada barra
    for i in range(len(titulitos)):
        ax1.text(titulitos[i].get_x() + titulitos[i].get_width() / 2, -1.4, f'{bins[i]:.2f}-{bins[i + 1]:.2f}', ha='center', rotation=45, fontsize=8)

    for i, rect in enumerate(titulitos):
        altura = rect.get_height()
        ax1.annotate(f'{int(altura)}', xy=(rect.get_x() + rect.get_width() / 2, altura), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
    # Segundo subplot para la tabla
    ax2.axis('off')

    # Crear la tabla
    tabla = plt.table(cellText=[[str(evento['time']), evento['lat'], evento['long'], evento['title'], evento['code'], str(evento[propiedad])] for evento in dicc['values']],
                    colLabels=["Time", "Latitude", "Longitude", "Title", "Code", "Magnitude"],
                    cellLoc='center',
                    loc='center')

    # Ajustar el formato y estilo de la tabla
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(5.5)
    tabla.scale(1.2, 1.2)
    ax2.set_title('Events in {} in {}'.format(title, anio))
    plt.tight_layout()
    stop = controller.get_time()
    delta = controller.delta_time(start, stop)
    plt.show()
    return delta

def updateSig(mapa, dato):
    sig = int(dato['sig'])
    entry = om.get(mapa, sig)
    if entry == None:
        sigentry = newsigentry(dato)
        om.put(mapa,sig, sigentry)
    else:
        sigentry= me.getValue(entry)
    addSig(sigentry, dato)
    return mapa
    
def newsigentry(dato):
    entry = {'lsttemblores': None}
    entry['lsttemblores'] = lt.newList()
    return entry

def addSig(sigentry, dato):
    lst = sigentry['lsttemblores']
    lt.addLast(lst, dato)
    return sigentry
    
    

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


def sort_criteria_date(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (type): description
        data2 (type): description

    Returns:
        type: description
    """
    date_1 = data_1['time']
    date_2 = data_2['time']
    if (date_1 == date_2):
        return 0
    else:
       return date_1>date_2
    
    
def comparemag(mag1, mag2):
    if (mag1 == mag2):
        return 0
    elif (mag1 > mag2):
        return 1
    else:
        return -1

def comparedate(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
    

def comparedate_inverse(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 < date2):
        return 1
    else:
        return -1

def comparedate_req6(list1, list2):
    return list1[0] < list2[0]

def comparedate_req1(list1, list2):
    return list1['time'] > list2['time']

def comparedepth(depth1, depth2):
    if depth1==depth2:
        return 0
    elif depth1 > depth2:
        return 1
    else:
        return -1

def get3(lista):
    first= lt.subList(lista, 1,3)
    last = lt.subList(lista, lt.size(lista)-2,3)
    
    for elementos in lt.iterator(last):
        lt.addLast(first, elementos)
    return first

def comparesig(sig1, sig2):
    if sig1==sig2:
        return 0
    elif sig1 > sig2:
        return 1
    else:
        return -1
