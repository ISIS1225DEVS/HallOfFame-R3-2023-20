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
from haversine import haversine

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
    data_structs = {'temblores':None,
                    'fechaindex':None,
                    "magnitud":None,
                    "significancia":None,
                    'profundidad':None,
                    'fecha':None
                    }
    

    data_structs['temblores'] = lt.newList('ARRAY_LIST')

    data_structs['fechaindex'] = om.newMap(omaptype='RBT', cmpfunction=compareDates)
    data_structs['magnitud'] = om.newMap(omaptype='RBT')
    data_structs['significancia'] = om.newMap(omaptype='RBT')
    data_structs['profundidad'] = om.newMap(omaptype='RBT')

    data_structs['fecha'] = mp.newMap(100/0.5, loadfactor=0.5,maptype='PROBING')

    
    return data_structs
    

# Funciones para agregar informacion al modelo

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    
    for clave, valor in data.items():
        if valor == '':
            data[clave] = 'desconocido'

    

    lt.addLast(data_structs['temblores'],data)

    #Fecha tree-----------------------------------------------------------------
    if om.contains(data_structs['fechaindex'], data['time']) is False:
        lista = lt.newList('ARRAY_LIST', cmpfunction=sort_criteria)
        om.put(data_structs['fechaindex'], data['time'], lista)
    else:
        lista = me.getValue(om.get(data_structs['fechaindex'], data['time']))
        lt.addLast(lista, data)
        om.put(data_structs['fechaindex'], data['time'], lista)
    #Magnitud tree-----------------------------------------------------------------
    if om.contains(data_structs['magnitud'], data['mag']) is False:
        lista = lt.newList('ARRAY_LIST', cmpfunction=compare_mag)
        om.put(data_structs['magnitud'], data['mag'], lista)
    else:
        lista = me.getValue(om.get(data_structs['magnitud'], data['mag']))
        lt.addLast(lista, data)
        om.put(data_structs['magnitud'], data['mag'], lista)
    #Significancia tree-----------------------------------------------------------------
    if om.contains(data_structs['significancia'], data['sig']) is False:
        lista = lt.newList('ARRAY_LIST', cmpfunction=compare_mag)
        om.put(data_structs['significancia'], data['sig'], lista)
    else:
        lista = me.getValue(om.get(data_structs['significancia'], data['sig']))
        lt.addLast(lista, data)
        om.put(data_structs['significancia'], data['sig'], lista)
    #Profundidad tree-----------------------------------------------------------------
    if om.contains(data_structs['profundidad'], data['depth']) is False:
        lista = lt.newList('ARRAY_LIST', cmpfunction=compare_depth)
        om.put(data_structs['profundidad'], data['depth'], lista)
    else:
        lista = me.getValue(om.get(data_structs['profundidad'], data['depth']))
        lt.addLast(lista, data)
        om.put(data_structs['profundidad'], data['depth'], lista)
    
    #Fecha hash-----------------------------------------------------------------
    if (mp.contains(data_structs['fecha'], data['time'][:4]))==False:
        lista_nueva = lt.newList(datastructure = 'ARRAY_LIST')
        lt.addLast(lista_nueva,data)
        mp.put(data_structs['fecha'], data['time'][:4], lista_nueva)
    else:
        lista = me.getValue(mp.get(data_structs['fecha'], data['time'][:4]))
        lt.addLast(lista, data)
        mp.put(data_structs['fecha'], data['time'][:4], lista)

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
    # TODO: Realizar el requerimiento 1
    

    lista = lt.newList('ARRAY_LIST')

    datos = om.valueSet(control['fechaindex'])

    for i in lt.iterator(datos):
        for j in lt.iterator(i):
            lt.addLast(lista,{'time':j['time'],'mag':j['mag'], 'lat':j['lat'], 'long':j['long'], 'depth':j['depth'], 
                              'sig': j['sig'], 'gap': j['gap'], 'nst': j['nst'], 'title': j['title'],
                                'cdi': j['cdi'],'mmi': j['mmi'], 'magType': j['magType'], 'code': j['code'], 'type':j['type']})
    r = lt.newList('ARRAY_LIST')        
    for e in lista['elements']: 
        if e['time'] >= fecha_inicial and e['time'] <= fecha_final:
            lt.addLast(r,e)
    
    quk.sort(r, compare)

    return r['elements']




def req_2(control,mag1,mag2):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    lista = lt.newList('ARRAY_LIST')
    
    datos = om.values(control['magnitud'], mag1, mag2)

    for i in lt.iterator(datos):
        for j in lt.iterator(i):
            lt.addLast(lista,{'time':j['time'],'mag':j['mag'], 'lat':j['lat'], 'long':j['long'], 'depth':j['depth'], 
                              'sig': j['sig'], 'gap': j['gap'], 'nst': j['nst'], 'title': j['title'],
                                'cdi': j['cdi'],'mmi': j['mmi'], 'magType': j['magType'], 'code': j['code'], 'type':j['type']})
    
    
    merg.sort(lista, compare_mag)

    return lista['elements']

    
    



def req_3(control,magnitud,profundidad):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    lista = lt.newList('ARRAY_LIST')
    r = lt.newList('ARRAY_LIST')
    
    datos = om.values(control['magnitud'], magnitud, om.maxKey(control['magnitud']))

    for i in lt.iterator(datos):
        for j in lt.iterator(i):
            lt.addLast(lista,{'time':j['time'],'mag':j['mag'], 'lat':j['lat'], 'long':j['long'], 'depth':j['depth'], 
                              'sig': j['sig'], 'gap': j['gap'], 'nst': j['nst'], 'title': j['title'],
                                'cdi': j['cdi'],'mmi': j['mmi'], 'magType': j['magType'], 'code': j['code'], 'type':j['type']})
    
    for e in lista['elements']:
        if e['depth'] <= profundidad:
            lt.addLast(r, e)
    
    
    quk.sort(r, compare)

    return r['elements']


def req_4(control,sig,gap):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    lista = lt.newList('ARRAY_LIST')
    r = lt.newList('ARRAY_LIST')
    
    datos = om.values(control['significancia'], sig, om.maxKey(control['significancia']))
   # datos2= om.values(control['gap'], gap, om.maxKey(control['gap']))

    for i in lt.iterator(datos):
        for j in lt.iterator(i):
            lt.addLast(lista,{'time':j['time'],'mag':j['mag'], 'lat':j['lat'], 'long':j['long'], 'depth':j['depth'], 
                              'sig': j['sig'], 'gap': j['gap'], 'nst': j['nst'], 'title': j['title'],
                                'cdi': j['cdi'],'mmi': j['mmi'], 'magType': j['magType'], 'code': j['code'], 'type':j['type']})
    
    for e in lista['elements']:
        if e['gap'] <= gap:
            lt.addLast(r, e)
    
    
    quk.sort(r, compare)

    return r['elements']


def req_5(data_structs, depth, nst):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    lista = lt.newList('ARRAY_LIST')
    respuesta = lt.newList('ARRAY_LIST')
    
    datos = om.values(data_structs['profundidad'], depth, om.maxKey(data_structs['profundidad']))

    for i in lt.iterator(datos):
        for j in lt.iterator(i):
            lt.addLast(lista,{'time':j['time'],'mag':j['mag'], 'lat':j['lat'], 'long':j['long'], 'depth':j['depth'], 
                              'sig': j['sig'], 'gap': j['gap'], 'nst': j['nst'], 'title': j['title'],
                                'cdi': j['cdi'],'mmi': j['mmi'], 'magType': j['magType'], 'type':j['type'], 'code': j['code']})
    
    for e in lista['elements']:
        if e['nst'] <= nst:
            lt.addLast(respuesta, e)
    
    
    quk.sort(respuesta, compare)

    return respuesta['elements']



def req_6(data_structs, anio, latitud, longitud, radio, num_eventos):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    lista = lt.newList('ARRAY_LIST')
    resultado = lt.newList('ARRAY_LIST')
    maxima_magnitud = 0
    datos = mp.get(data_structs['fecha'], anio)
    
    for i in datos['value']['elements']:
        if haversine((float(i['lat']), float(i['long'])), (latitud, longitud)) <= radio:
            lt.addLast(lista,{'time':i['time'],'mag':i['mag'], 'lat':i['lat'], 'long':i['long'], 'depth':i['depth'], 
                              'sig': i['sig'], 'gap': i['gap'], 'nst': i['nst'], 'title': i['title'],
                                'cdi': i['cdi'],'mmi': i['mmi'], 'magType': i['magType'], 'type':i['type'], 'code': i['code']})
            if maxima_magnitud <= float(i['mag']):
                maxima_magnitud = float(i['mag'])
                evento_prominente = i['code']

    quk.sort(lista, compare)
    numero_de_eventos = lt.size(lista)

    a=0 ; centinela = True
    while a < numero_de_eventos and centinela:
        elemento = lista['elements'][a]
        if evento_prominente == elemento['code']:
            evento_prominente = elemento
            centinela = False
        else:
            a+=1

    j = a - num_eventos 
    while j < a and j > 0: 
        lt.addLast(resultado, lista['elements'][j])
        j+=1

    k = a + 1 
    while k <= a + num_eventos and k < lt.size(lista): 
        lt.addLast(resultado, lista['elements'][k])
        k+=1

    
    return evento_prominente, numero_de_eventos, resultado

def req_7(control, anio, region):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7

    lista = lt.newList('ARRAY_LIST')
    c = control['fecha']

    map = mp.get(c, anio)

    control_r = me.getValue(map)

    for i in control_r['elements']:
        if region in i['title']:
            lt.addLast(lista, i)
    quk.sort(lista, compare)


    return lista


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    
    


# Funciones utilizadas para comparar elementos dentro de una lista

def compareDates(dicc1,dicc2):

    fecha1 = dicc1
    fecha2 = dicc2
    if fecha1 < fecha2:
        return 0
    elif fecha1 > fecha2:
        return 1
    
def compare_mag(dicc1,dicc2):

    fecha1 = dicc1['mag']
    fecha2 = dicc2['mag']
    if fecha1 < fecha2:
        return 0
    elif fecha1 > fecha2:
        return 1
    
def compare_depth(dicc1,dicc2):

    fecha1 = dicc1['depth']
    fecha2 = dicc2['depth']
    if fecha1 < fecha2:
        return 0
    elif fecha1 > fecha2:
        return 1
    
def compare(dicc1,dicc2):

    fecha1 = dicc1['time']  
    fecha2 = dicc2['time']
    if fecha1 < fecha2:
        return 0
    elif fecha1 > fecha2:
        return 1
    

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
    return compare(data_1, data_2)
def compare_mag(dicc1,dicc2):

    fecha1 = dicc1['mag']
    fecha2 = dicc2['mag']
    if fecha1 < fecha2:
        return 0
    elif fecha1 > fecha2:
        return 1

def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    
    data_structs['temblores'] = sa.sort(data_structs['temblores'], sort_criteria)
