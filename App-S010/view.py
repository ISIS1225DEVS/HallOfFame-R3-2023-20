"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
import folium
import matplotlib.pyplot as plt

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    control = controller.new_controller()

    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Conocer los eventos sísmicos entre dos fechas")
    print("3- Conocer los eventos sísmicos entre dos magnitudes")
    print("4- Consultar los 10 eventos más recientes según una magnitud y profundidad indicadas ")
    print("5-  Consultar los 15 eventos sísmicos más recientes según su significancia y una distancia azimutal ")
    print("6- Consultar los 20 eventos más antiguos para una profundidad dada y registrados por un cierto número de estaciones ")
    print("7- Reportar el evento más significativo y los N eventos más próximos cronológicamente ocurridos dentro del área alrededor de un punto ")
    print("8- Graficar un histograma anual de los eventos ocurridos según la región y propiedades de los eventos ")
    print("9- Visualizar los eventos sísmicos de cada requerimiento en un mapa interactivo ")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    tamanho = ''
    c = int(input('Elija el tamaño del archivo que desea usar: \n 1-5pct\n 2-10pct\n 3-20pct\n 4-30pct\n 5-50pct\n 6-80pct\n 7-large\n 8-small\n'))
    if c == 1:
        tamanho = '5pct'
    elif c == 2:
        tamanho = '10pct'
    elif c == 3:
        tamanho = '20pct'
    elif c == 4:
        tamanho = '30pct'
    elif c == 5:
        tamanho = '50pct'
    elif c == 6:
        tamanho = '80pct'
    elif c == 7:
        tamanho = 'large'
    elif c == 8:
        tamanho = 'small'
    else:
        tamanho = 'small'

    
    controller.load_data(control, tamanho)

    



def print_data(control):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    
    print("-----------------------")
    print("Temblores count: " + str(lt.size(control['temblores'])))
    print("-----------------------")


    print("==============================================")
    print("==========EARTHQUAKES RECORDS REPORT==========")
    print("==============================================")

    print("Información de los cinco primeros y cinco últimos temblores:")

    lista = lt.newList('ARRAY_LIST')
    prnt = []
    for j in control['temblores']['elements']:
        lt.addLast(lista,{'code':j['code'],'time':j['time'], 'lat':j['lat'], 'long':j['long'], 'mag':j['mag'], 
                              'title': j['title'], 'depth': j['depth'], 'felt': j['felt'], 'cdi': j['cdi'],
                                'mmi': j['mmi'],'tsunami': j['tsunami']})
        
    r = lista['elements']
    a = len(r) - 1
    b = len(r) - 2 
    c = len(r)- 3
    d = len(r)- 4
    e = len(r)- 5

    prnt = [r[0], r[1], r[2],r[3],r[4], r[a], r[b], r[c],r[d],r[e]]
    m = folium.Map([prnt[0]['lat'], prnt[0]['long']], zoom_start=12)
    for i in prnt:
            mensaje = str(i['mag']) + i['title'] + i['time'] +  i['depth'] + i['cdi'] + i['mmi'] + i['tsunami'] + i['code']
            lat = float(j['lat'])
            long = float(j['long'])
            folium.Marker(
            location=[lat, long],
            tooltip="Click me!",
            popup=mensaje,
            icon=folium.Icon(icon="green"),
            ).add_to(m)

    m.save("mapa_carga_de_datos.html")


    print(tabulate(prnt, headers = 'keys', tablefmt = 'grid'))

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    fecha_inicial = input('Ingrese la fecha inicial del intervalo en el formato ("%Y-%m-dT%H:%M") ejemplo (2018-09-01T08:30): ')
    fecha_final = input('Ingrese la fecha final del intervalo en el formato ("%Y-%m-dT%H:%M") ejemplo: (2018-09-01T08:30): ')

    lista,delta_time_r = controller.req_1(control, fecha_inicial, fecha_final)

    print('==========req No 1 inputs ========== ')
    print('Fecha inicial: ' + fecha_inicial)
    print('Fecha final: ' + fecha_final)

    print('==========req No 1 results ========== ')
    print('Total fechas: ' +  str(len(lista)))
    print("El tiempo de ejecución es: "+ str(round(delta_time_r,2))+" milisegundos")

   
    a = len(lista) - 1
    b = len(lista) - 2
    c = len(lista) - 3
    if len(lista) > 6:
        prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]
        m = folium.Map([prnt[0]['detalles'][0]['lat'], prnt[0]['detalles'][0]['long']], zoom_start=12)
        for i in prnt:
            for j in i['detalles']:
                mensaje = str(j['mag']) + j['title'] + i['time'] + j['nst'] + j['depth'] + j['cdi'] + j['mmi'] + j['magType'] + j['code'] + j['type'] 
                lat = float(j['lat'])
                long = float(j['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

        m.save("mapa_req1.html")
        for i in prnt:
            if len(i['detalles']) > 6:
                i['detalles'] = [i['detalles'][0],i['detalles'][1],i['detalles'][2],i['detalles'][len(i['detalles'])-1],i['detalles'][len(i['detalles'])-2],i['detalles'][len(i['detalles'])-3]]
            i['detalles'] = tabulate(i['detalles'],headers = 'keys', tablefmt = 'pretty')
        tab = tabulate(prnt,headers = 'keys', tablefmt = 'pretty')
        print(tab)


        
    else:
        for i in lista:
            if len(i['detalles']) > 6:
                i['detalles'] = [i['detalles'][0],i['detalles'][1],i['detalles'][2],i['detalles'][len(i['detalles'])-1],i['detalles'][len(i['detalles'])-2],i['detalles'][len(i['detalles'])-3]]
            i['detalles'] = tabulate(i['detalles'],headers = 'keys', tablefmt = 'pretty')
        m = folium.Map([lista[0]['detalles'][0]['lat'], lista[0]['detalles'][0]['long']], zoom_start=12)
        for i in lista:
            for j in i['detalles']:
                mensaje = str(j['mag']) + j['title'] + i['time'] + j['nst'] + j['depth'] + j['cdi'] + j['mmi'] + j['magType'] + j['code'] + j['type'] 
                lat = float(j['lat'])
                long = float(j['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

        m.save("mapa_req1.html")
        tab = tabulate(lista,headers = 'keys', tablefmt = 'pretty')
        print(tab)


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    mag1 = input("Ingrese el limite inferior de la magnitud: ")
    mag2=input("Ingrese el limite superior de la magnitud: ") 
    lista,delta_time_r=controller.req_2(control,mag1,mag2)  
    print('==========req No 2 inputs ========== ')
    print('Magnitud minima: ' + mag1)
    print('Magnitud maxima: ' + mag2)

    print('==========req No 2 results ========== ')
    print('Longitud de la consulta: ' +  str(len(lista)))



    print("El tiempo de ejecución es: "+ str(round(delta_time_r,2))+" milisegundos")
    a = len(lista) - 1
    b = len(lista) - 2
    c = len(lista) - 3
    if len(lista) > 6:
        prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]
        m = folium.Map([prnt[0]['detalles'][0]['lat'], prnt[0]['detalles'][0]['long']], zoom_start=12)
        for i in prnt:
            for j in i['detalles']:
                mensaje = str(i['mag']) + j['title'] + j['time'] + j['nst'] + j['depth'] + j['cdi'] + j['mmi'] + j['magType'] + j['code'] + j['type'] 
                lat = float(j['lat'])
                long = float(j['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

        m.save("mapa_req2.html")

        for i in prnt:
            if len(i['detalles']) > 6:
                i['detalles'] = [i['detalles'][0],i['detalles'][1],i['detalles'][2],i['detalles'][len(i['detalles'])-1],i['detalles'][len(i['detalles'])-2],i['detalles'][len(i['detalles'])-3]]
            i['detalles'] = tabulate(i['detalles'],headers = 'keys', tablefmt = 'pretty')
        tab = tabulate(prnt,headers = 'keys', tablefmt = 'pretty')
        print(tab)
        
    else:
        m = folium.Map([lista[0]['detalles'][0]['lat'], lista[0]['detalles'][0]['long']], zoom_start=12)
        for i in lista:
            for j in i['detalles']:
                mensaje = str(i['mag']) + j['title'] + j['time'] + j['nst'] + j['depth'] + j['cdi'] + j['mmi'] + j['magType'] + j['code'] + j['type'] 
                lat = float(j['lat'])
                long = float(j['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

        m.save("mapa_req2.html")
        for i in lista:
            if len(i['detalles']) > 6:
                i['detalles'] = [i['detalles'][0],i['detalles'][1],i['detalles'][2],i['detalles'][len(i['detalles'])-1],i['detalles'][len(i['detalles'])-2],i['detalles'][len(i['detalles'])-3]]
            i['detalles'] = tabulate(i['detalles'],headers = 'keys', tablefmt = 'pretty')
        tab = tabulate(lista,headers = 'keys', tablefmt = 'pretty')
        print(tab)
 



def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    magnitud = input("Ingrese la magnitud de consulta: ")
    profundidad = input('Ingrese la profundida de consulta: ')
    

    lista,delta_time_r = controller.req_3(control, magnitud, profundidad)
    print('==========req No 3 inputs ========== ')
    print('Magnitud: ' + magnitud)
    print('Profundidad: ' + profundidad)

    print('==========req No 3 results ========== ')
    print('Total encontrados: ' +  str(len(lista)))

    print("El tiempo de ejecución es: "+ str(round(delta_time_r,2))+" milisegundos")

    a = len(lista) - 1
    b = len(lista) - 2
    c = len(lista) - 3
    if len(lista) > 6:
        prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]
        m = folium.Map([prnt[0]['detalles'][0]['lat'], prnt[0]['detalles'][0]['long']], zoom_start=12)
        for i in prnt:
            for j in i['detalles']:
                mensaje = str(j['mag']) + j['title'] + i['time'] + j['nst'] + j['depth'] + j['cdi'] + j['mmi'] + j['magType'] + j['code'] + j['type'] 
                lat = float(j['lat'])
                long = float(j['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

        m.save("mapa_req3.html")
        for i in prnt:
            if len(i['detalles']) > 6:
                i['detalles'] = [i['detalles'][0],i['detalles'][1],i['detalles'][2],i['detalles'][len(i['detalles'])-1],i['detalles'][len(i['detalles'])-2],i['detalles'][len(i['detalles'])-3]]
            i['detalles'] = tabulate(i['detalles'],headers = 'keys', tablefmt = 'pretty')
        tab = tabulate(prnt,headers = 'keys', tablefmt = 'pretty')
        print(tab)
        
    else:
        m = folium.Map([lista[0]['detalles'][0]['lat'], lista[0]['detalles'][0]['long']], zoom_start=12)
        for i in lista:
            for j in i['detalles']:
                mensaje = str(j['mag']) + j['title'] + i['time'] + j['nst'] + j['depth'] + j['cdi'] + j['mmi'] + j['magType'] + j['code'] + j['type'] 
                lat = float(j['lat'])
                long = float(j['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

        m.save("mapa_req3.html")
        for i in lista:
            if len(i['detalles']) > 6:
                i['detalles'] = [i['detalles'][0],i['detalles'][1],i['detalles'][2],i['detalles'][len(i['detalles'])-1],i['detalles'][len(i['detalles'])-2],i['detalles'][len(i['detalles'])-3]]
            i['detalles'] = tabulate(i['detalles'],headers = 'keys', tablefmt = 'pretty')
        tab = tabulate(lista,headers = 'keys', tablefmt = 'pretty')
        print(tab)
    


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    sig=input("Dijite la significancia mínima del evento (sig): ")
    gap=input("Dijite la distancia azimutal máxima del evento (gap): ")
    lista,delta_time_r = controller.req_4(control, sig, gap)
    
    print('==========req No 4 inputs ========== ')
    print('Significancia mínima: ' + sig)
    print('Distancia azimutal: ' + gap)

    print('==========req No 4 results ========== ')
    print('Total encontrados: ' +  str(len(lista)))
    print("El tiempo de ejecución es: "+ str(round(delta_time_r,2))+" milisegundos")

    a = len(lista) - 1
    b = len(lista) - 2
    c = len(lista) - 3
    if len(lista) > 6:
        prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]
        m = folium.Map([prnt[0]['detalles'][0]['lat'], prnt[0]['detalles'][0]['long']], zoom_start=12)
        for i in prnt:
            for j in i['detalles']:
                mensaje = str(j['mag']) + j['title'] + i['time'] + j['nst'] + j['depth'] + j['cdi'] + j['mmi'] + j['magType'] + j['code'] + j['type'] 
                lat = float(j['lat'])
                long = float(j['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

        m.save("mapa_req4.html")
        for i in prnt:
            if len(i['detalles']) > 6:
                i['detalles'] = [i['detalles'][0],i['detalles'][1],i['detalles'][2],i['detalles'][len(i['detalles'])-1],i['detalles'][len(i['detalles'])-2],i['detalles'][len(i['detalles'])-3]]
            i['detalles'] = tabulate(i['detalles'],headers = 'keys', tablefmt = 'pretty')
        tab = tabulate(prnt,headers = 'keys', tablefmt = 'pretty')
        print(tab)
    else:
        for i in lista:
            if len(i['detalles']) > 6:
                i['detalles'] = [i['detalles'][0],i['detalles'][1],i['detalles'][2],i['detalles'][len(i['detalles'])-1],i['detalles'][len(i['detalles'])-2],i['detalles'][len(i['detalles'])-3]]
            i['detalles'] = tabulate(i['detalles'],headers = 'keys', tablefmt = 'pretty')
        m = folium.Map([lista[0]['detalles'][0]['lat'], lista[0]['detalles'][0]['long']], zoom_start=12)
        for i in lista:
            for j in i['detalles']:
                mensaje = str(j['mag']) + j['title'] + i['time'] + j['nst'] + j['depth'] + j['cdi'] + j['mmi'] + j['magType'] + j['code'] + j['type'] 
                lat = float(j['lat'])
                long = float(j['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

        m.save("mapa_req4.html")
        tab = tabulate(lista,headers = 'keys', tablefmt = 'pretty')
        print(tab)



def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    num_estaciones = input("Ingrese las estaciones que detectan el evento: ")
    profundidad = input('Ingrese la profundida desde la que desea consultar: ')

    lista,delta_time, delta_memory = controller.req_5(control, num_estaciones, profundidad)
    print('==========req No 5 inputs ========== ')
    print('Numero minimo de estaciones: ' + num_estaciones)
    print('Profundidad minima: ' + profundidad)

    print('==========req No 5 results ========== ')
    print('Total encontrados: ' +  str(len(lista)))

    print("El tiempo de ejecución es: "+ str(round(delta_time,2))+" milisegundos")
    print("El uso de memoria es: "+ str(round(delta_memory,2))+" milisegundos")
    a = len(lista) - 1
    b = len(lista) - 2
    c = len(lista) - 3
    if len(lista) > 6:
        prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]
        m = folium.Map([prnt[0]['detalles'][0]['lat'], prnt[0]['detalles'][0]['long']], zoom_start=12)
        for i in prnt:
            for j in i['detalles']:
                mensaje = str(j['mag']) + j['title'] + i['time'] + j['nst'] + j['depth'] + j['cdi'] + j['mmi'] + j['magType'] + j['type'] + j['code']
                lat = float(j['lat'])
                long = float(j['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

        m.save("mapa_req5.html")
        for i in prnt:
            if len(i['detalles']) > 6:
                i['detalles'] = [i['detalles'][0],i['detalles'][1],i['detalles'][2],i['detalles'][len(i['detalles'])-1],i['detalles'][len(i['detalles'])-2],i['detalles'][len(i['detalles'])-3]]
            i['detalles'] = tabulate(i['detalles'],headers = 'keys', tablefmt = 'grid')
        tab = tabulate(prnt,headers = 'keys', tablefmt = 'grid')
        print(tab)
        
    else:
        m = folium.Map([lista[0]['detalles'][0]['lat'], lista[0]['detalles'][0]['long']], zoom_start=12)
        for i in lista:
            for j in i['detalles']:
                mensaje = str(j['mag']) + j['title'] + i['time'] + j['nst'] + j['depth'] + j['cdi'] + j['mmi'] + j['magType'] + j['type'] + j['code']
                lat = float(j['lat'])
                long = float(j['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

        m.save("mapa_req5.html")
        for i in lista:
            if len(i['detalles']) > 6:
                i['detalles'] = [i['detalles'][0],i['detalles'][1],i['detalles'][2],i['detalles'][len(i['detalles'])-1],i['detalles'][len(i['detalles'])-2],i['detalles'][len(i['detalles'])-3]]
            i['detalles'] = tabulate(i['detalles'],headers = 'keys', tablefmt = 'grid')
        tab = tabulate(lista,headers = 'keys', tablefmt = 'grid')
        print(tab)

def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    anio = input("Ingrese el año relevante del evento: ")
    latitud = float(input('Ingrese la latitud que desea consultar: '))
    longitud = float(input('Ingrese la longitud que desea consultar: '))
    radio = float(input('Ingrese el radio de consulta: '))
    num_eventos = int(input('Ingrese el numero de eventos de magnitud más cercana: '))

    evento_prominente, numero_de_eventos, lista, delta_time, delta_memory = controller.req_6(control, anio, latitud, longitud, radio, num_eventos)
    print('==========req No 6 inputs ========== ')
    print('Año: ' + anio)
    print('Latitud de posicion: ' + str(latitud))
    print('Longitud de posicion : ' + str(longitud))
    print('Radio de busqueda : ' + str(radio))
    print('Numero de eventos mas importantes: ' + str(num_eventos))

    print('==========req No 6 results ========== ')
    print('Numero de eventos dentro del radio: ' +  str(numero_de_eventos))
    print('Evento prominente: ')
    e_lista = [evento_prominente]
    print(tabulate(e_lista, headers = 'keys', tablefmt = 'grid'))

    print("El tiempo de ejecución es: "+ str(round(delta_time,2))+" milisegundos")
    print("El uso de memoria es: "+ str(round(delta_memory,2))+" milisegundos")
    a = len(lista) - 1
    b = len(lista) - 2
    c = len(lista) - 3
    if len(lista) > 6:
        prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]
        m = folium.Map([prnt[0]['detalles'][0]['lat'], prnt[0]['detalles'][0]['long']], zoom_start=12)
        for i in prnt:
            for j in i['detalles']:
                mensaje = str(j['mag']) + j['title'] + i['time'] + j['nst'] + j['depth'] + j['cdi'] + j['mmi'] + j['magType'] + j['type'] + j['code']
                lat = float(j['lat'])
                long = float(j['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

        m.save("mapa_req6.html")
        for i in prnt:
            if len(i['detalles']) > 6:
                i['detalles'] = [i['detalles'][0],i['detalles'][1],i['detalles'][2],i['detalles'][len(i['detalles'])-1],i['detalles'][len(i['detalles'])-2],i['detalles'][len(i['detalles'])-3]]
            i['detalles'] = tabulate(i['detalles'],headers = 'keys', tablefmt = 'grid')
        tab = tabulate(prnt,headers = 'keys', tablefmt = 'grid')
        print(tab)
        
    else:
        m = folium.Map([lista[0]['detalles'][0]['lat'], lista[0]['detalles'][0]['long']], zoom_start=12)
        for i in lista:
            for j in i['detalles']:
                mensaje = str(j['mag']) + j['title'] + i['time'] + j['nst'] + j['depth'] + j['cdi'] + j['mmi'] + j['magType'] + j['type'] + j['code']
                lat = float(j['lat'])
                long = float(j['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

        m.save("mapa_req6.html")
        for i in lista:
            if len(i['detalles']) > 6:
                i['detalles'] = [i['detalles'][0],i['detalles'][1],i['detalles'][2],i['detalles'][len(i['detalles'])-1],i['detalles'][len(i['detalles'])-2],i['detalles'][len(i['detalles'])-3]]
            i['detalles'] = tabulate(i['detalles'],headers = 'keys', tablefmt = 'grid')
        tab = tabulate(lista,headers = 'keys', tablefmt = 'grid')
        print(tab)


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    
    anio = input('Ingrese el año relevante: ')
    region = input('Ingrese el titulo de la region: ')
    p = int(input("Seleccione: \n 1-Intensidad maxima\n 2-Intensidad minima \n 3-magnitud \n 4-profundiad\n"))

    lista, delta_time_r = controller.req_7(control, anio, region, p)
    print('==========req No 7 inputs ========== ')
    print("Año: " + str(anio))
    print("Area de interes: " + str(anio))
    
    print('==========req No 7 results ========== ')
    print('Tamaño consulta: ' + str(len(lista)))



    mag_values = []

    if p == 1:

        for entry in lista:
            cdi = entry['cdi']
            if cdi != 'desconocido':
                try:
                    mag_values.append(float(cdi))
                except ValueError:
                    pass
    
        if mag_values:

            plt.hist(mag_values, bins=10, color='blue', edgecolor='black')
            plt.xlabel('Intensidad maxima (cdi)')
            plt.ylabel('No events')
            plt.title('Histograma de intensidad maxima en' + anio + "en " + region)
            plt.grid(True)

            # Muestra el histograma
            plt.show()
        else:
            print("No se encontraron valores de magnitud válidos en los datos.")
            

        print("El tiempo de ejecución es: "+ str(round(delta_time_r,2))+" milisegundos")
        a = len(lista) - 1
        b = len(lista) - 2
        c = len(lista) - 3
        if len(lista) > 6:
            prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]
            m = folium.Map([prnt[0]['lat'], prnt[0]['long']], zoom_start=12)
            for i in prnt:
                mensaje = str(i['time']) + i['depth'] + i['sig'] + i['nst'] + i['gap'] + i['title']
                lat = float(i['lat'])
                long = float(i['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

            m.save("mapa_req7.html")
            print(tabulate(prnt,headers = 'keys', tablefmt = 'pretty'))
            
        else:
            m = folium.Map([lista[0]['lat'], lista[0]['long']], zoom_start=12)
            for i in lista:
                mensaje = str(i['time']) + i['depth'] + i['sig'] + i['nst'] + i['gap'] + i['title']
                lat = float(i['lat'])
                long = float(i['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

            m.save("mapa_req7.html")
            print(tabulate(lista,headers = 'keys', tablefmt = 'pretty'))

    elif p == 2:
         
        for entry in lista:
            cdi = entry['mmi']
            if cdi != 'desconocido':
                try:
                    mag_values.append(float(cdi))
                except ValueError:
                    pass
    
        if mag_values:

            plt.hist(mag_values, bins=10, color='blue', edgecolor='black')
            plt.xlabel('Intensidad minima (mmi)')
            plt.ylabel('No events')
            plt.title('Histograma de intensidad minima en' + anio + "en " + region)
            plt.grid(True)

        
            plt.show()
        else:
            print("No se encontraron valores de magnitud válidos en los datos.")

        print("El tiempo de ejecución es: "+ str(round(delta_time_r,2))+" milisegundos")
        a = len(lista) - 1
        b = len(lista) - 2
        c = len(lista) - 3
        if len(lista) > 6:
            prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]
            m = folium.Map([prnt[0]['lat'], prnt[0]['long']], zoom_start=12)
            for i in prnt:
                mensaje = str(i['time']) + i['depth'] + i['sig'] + i['nst'] + i['gap'] + i['title']
                lat = float(i['lat'])
                long = float(i['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

            m.save("mapa_req7.html")
            print(tabulate(prnt,headers = 'keys', tablefmt = 'pretty'))
            
        else:
            m = folium.Map([lista[0]['lat'], lista[0]['long']], zoom_start=12)
            for i in lista:
                mensaje = str(i['time']) + i['depth'] + i['sig'] + i['nst'] + i['gap'] + i['title']
                lat = float(i['lat'])
                long = float(i['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

            m.save("mapa_req7.html")
            print(tabulate(lista,headers = 'keys', tablefmt = 'pretty'))

    elif p == 3:
        for entry in lista:
            cdi = entry['mag']
            if cdi != 'desconocido':
                try:
                    mag_values.append(float(cdi))
                except ValueError:
                    pass
    
        if mag_values:

            plt.hist(mag_values, bins=10, color='blue', edgecolor='black')
            plt.xlabel('Magnitud (mag)')
            plt.ylabel('No events')
            plt.title('Histograma de magnitud en' + anio + "en " + region)
            plt.grid(True)

        
            plt.show()
        else:
            print("No se encontraron valores de magnitud válidos en los datos.")

        print("El tiempo de ejecución es: "+ str(round(delta_time_r,2))+" milisegundos")

        a = len(lista) - 1
        b = len(lista) - 2
        c = len(lista) - 3
        if len(lista) > 6:
            prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]
            m = folium.Map([prnt[0]['lat'], prnt[0]['long']], zoom_start=12)
            for i in prnt:
                mensaje = str(i['time']) + i['depth'] + i['sig'] + i['nst'] + i['gap'] + i['title']
                lat = float(i['lat'])
                long = float(i['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

            m.save("mapa_req7.html")
            print(tabulate(prnt,headers = 'keys', tablefmt = 'pretty'))
            
        else:
            m = folium.Map([lista[0]['lat'], lista[0]['long']], zoom_start=12)
            for i in lista:
                mensaje = str(i['time']) + i['depth'] + i['sig'] + i['nst'] + i['gap'] + i['title']
                lat = float(i['lat'])
                long = float(i['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

            m.save("mapa_req7.html")
            print(tabulate(lista,headers = 'keys', tablefmt = 'pretty'))

    else:
            
        for entry in lista:
            cdi = entry['depth']
            if cdi != 'desconocido':
                try:
                    mag_values.append(float(cdi))
                except ValueError:
                    pass
    
        if mag_values:

            plt.hist(mag_values, bins=10, color='blue', edgecolor='black')
            plt.xlabel('profundidad (depth)')
            plt.ylabel('No events')
            plt.title('Histograma de profundidad en' + anio + "en " + region)
            plt.grid(True)

        
            plt.show()
        else:
            print("No se encontraron valores de magnitud válidos en los datos.")

        
        print("El tiempo de ejecución es: "+ str(round(delta_time_r,2))+" milisegundos")

        a = len(lista) - 1
        b = len(lista) - 2
        c = len(lista) - 3
        if len(lista) > 6:
            prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]
            m = folium.Map([prnt[0]['lat'], prnt[0]['long']], zoom_start=12)
            for i in prnt:
                mensaje = str(i['time']) + i['depth'] + i['sig'] + i['nst'] + i['gap'] + i['title']
                lat = float(i['lat'])
                long = float(i['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

            m.save("mapa_req7.html")
            print(tabulate(prnt,headers = 'keys', tablefmt = 'pretty'))
            
        else:
            m = folium.Map([lista[0]['lat'], lista[0]['long']], zoom_start=12)
            for i in prnt:
                mensaje = str(i['time']) + i['depth'] + i['sig'] + i['nst'] + i['gap'] + i['title']
                lat = float(i['lat'])
                long = float(i['long'])
                folium.Marker(
                location=[lat, long],
                tooltip="Click me!",
                popup=mensaje,
                icon=folium.Icon(icon="green"),
                ).add_to(m)

            m.save("mapa_req7.html")
            print(tabulate(lista,headers = 'keys', tablefmt = 'pretty'))

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
            print_data(control)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
