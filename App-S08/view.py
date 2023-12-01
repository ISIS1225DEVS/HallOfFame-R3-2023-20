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
import folium
import webbrowser
from folium.plugins import MarkerCluster
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
import threading
import gc
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
default_limit = 1000
sys.setrecursionlimit(default_limit*10)

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
    return controller.new_controller()


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control, filename):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    d_time, cont = controller.load_data(control, filename)
    return d_time, cont


def print_load_data(data, d_time):
    """
    Imprime los datos para mostrar al usuario en la carga de datos
    """
    total_data = lt.size(data['temblores'])
    print('--------------------------------------')
    print(f'Earthquake event size: {total_data}')
    print('--------------------------------------\n\n')

    print('===================================================')
    print('============ EARTHQUAKE RECORDS REPORT ============')
    print('===================================================\n')

    print('Printing the first 5 and last 5 records...\n')

    print('---- EARTHQUAKE RESULTS ----')
    print(f'Total earthquakes: {total_data}')
    print('Loaded Earthquake ADT have more than 10 records...')

    #Seleccionar los 5 primeros registros
    respuesta = lt.newList('ARRAY_LIST')
    for i in range(1,6):
        elemento = lt.getElement(data['temblores'],i)
        copy = elemento.copy()
        del copy['magType']
        del copy['type']
        lt.addLast(respuesta,copy)
    
    #Seleccionar los últimos 5 registros
    for i in range(total_data-4,total_data+1):
        elemento = lt.getElement(data['temblores'],i)
        copy = elemento.copy()
        del copy['magType']
        del copy['type']
        lt.addLast(respuesta,copy)
        
    tabla = tabulate(respuesta['elements'], headers='keys', tablefmt="grid", stralign="center")
    print(tabla)
    print(f'Δt = {d_time} ms')


def ver_dato(dato):
    return (dato == '' or dato == ' ' or dato == None)

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control, initialDate, finalDate):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    lst, size, d_time = controller.req_1(control, initialDate, finalDate)
    respuesta = lt.newList('ARRAY_LIST')
    print('===========================================')
    print('============ Req No. 1 Results ============')
    print('===========================================\n')
    if size == 0:
        print('No se encontraron sismos entre las fechas dadas.\n')
    else:
        print(f'Sismos totales entre las fechas indicadas: {size}\n')
        for i in range(lt.size(lst),0,-1):
            fecha = lt.getElement(lst,i)
            lista = fecha['lstemblores']
            for temblor in lt.iterator(lista):
                lt.addLast(respuesta,temblor)
                if lt.size(respuesta) == 3:
                    break
            else:
                continue
            break

        for fecha  in lt.iterator(lst):
            lista = fecha['lstemblores']
            for i in range(lt.size(lista),0,-1):
                elemento = lt.getElement(lista,i)
                lt.insertElement(respuesta,elemento,4)
                if lt.size(respuesta) == 6:
                    break
            else:
                continue
            break

        table = tabulate(respuesta['elements'], headers='keys', tablefmt="grid", stralign="center")
        print(table)
        print(f'Δt = {d_time} ms')


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    
    respuesta = lt.newList('ARRAY_LIST')
    print('===========================================')
    print('============ Req No. 2 Inputs ============')
    print('===========================================\n')      
    magMin = float(input("Límite inferior de la magnitud: "))
    magMax = float(input("Límite superior de la magnitud: "))
    r2,d_time, size = controller.req_2(control, magMin, magMax)            
    print('===========================================')
    print('============ Req No. 2 Results ============')
    print('===========================================\n')  
    print("Total de eventos sísmicos ocurridos entre las magnitudes indicadas: "+ str(size) +"\n")
    if size == 0:
        print('No se encontraron sismos entre las fechas dadas.\n')
    else:
        print(f'Sismos totales entre las magnitudes indicadas: {size}\n')
        for i in range(lt.size(r2),0,-1):
            fecha = lt.getElement(r2,i)
            lista = fecha['lstemblores']
            for temblor in lt.iterator(lista):
                lt.addLast(respuesta,temblor)
                if lt.size(respuesta) == 3:
                    break
            else:
                continue
            break

        for fecha  in lt.iterator(r2):
            lista = fecha['lstemblores']
            for i in range(lt.size(lista),0,-1):
                elemento = lt.getElement(lista,i)
                lt.insertElement(respuesta,elemento,4)
                if lt.size(respuesta) == 6:
                    break
            else:
                continue
            break
        table = tabulate(respuesta['elements'], headers='keys', tablefmt="grid", stralign="center")
        print(table)
    print('Δt = ',d_time)



def print_req_3(control):
    
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass

def print_req_3(control):
    
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    tiempo_i = controller.get_time()
    
    magMin = float(input("Ingrese la magnitud mínima del evento que desea solicitar: \n"))
    depthMax = float(input("Ingrese la profundidad máxima del evento que desea solicitar: \n"))
    
    
    r3 = controller.req_3(control, magMin, depthMax)
    resultados = r3["resul"]
    totales = r3["total"]
    
    encabezados = ["time","mag","lat","long","depth","sig","gap","nst",
                   "title","cdi","mmi","magType","type","code"]
    
    encaFin = ["tiempo", "eventos", "detalles"]
    tabla_magnitud = []
    for magnitud in lt.iterator(resultados):
        

        for temblor in lt.iterator(magnitud):
            fila_tem = [temblor["time"],temblor["mag"],temblor["lat"],temblor["long"],
                    temblor["depth"],temblor["sig"],temblor["gap"],temblor["nst"],
                    temblor["title"],temblor["cdi"],temblor["mmi"],temblor["magType"],
                    temblor["type"],temblor["code"]]
            tabla_magnitud.append(fila_tem)
            
        tabla = tabulate(tabla_magnitud, headers = encabezados, tablefmt="grid")
        
    
    
    print('===========================================')
    print('============ Req No. 3 Inputs ============')
    print('===========================================\n')                  
    print("Límite inferior de la magnitud: "+ str(magMin) +"\n")
    print("Límite superior de la magnitud: "+ str(depthMax) +"\n")
    
    print('===========================================')
    print('============ Req No. 3 Results ============')
    print('===========================================\n')  
    print("Total de eventos sísmicos ocurridos entre las magnitudes indicadas: "+ str(totales) +"\n")
  
    print(tabla)
    
    tiempo_f=controller.get_time()
    print('Δt = ',controller.delta_time(tiempo_i,tiempo_f))


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    print('=============== Req No. 4 Inputs =============== \n')
    sig = float(input('Min significance: '))
    gap = float(input('Max gap: '))
    print('\n=============== Req No. 4 Results =============== \n')
    print('Searching query events...')
    req_lst, size, d_time = controller.req_4(control, sig, gap)
    print(f'\nTotal events: {size}\n')
    req_tab = tabulate(lt.iterator(req_lst), headers='keys', tablefmt="grid", stralign="center")
    print(f'{req_tab}\n')
    print(f'Δt = {d_time} ms')
    


def print_req_5(control, mag, nst):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    print('\n=============== Req No. 5 Results =============== \n')
    respuesta, size, d_time = controller.req_5(control, mag, nst)
    print(f'Total events: {size}\n')
    answer = lt.newList('ARRAY_LIST')
    if size <= 6:
        answer = respuesta
    else:
        for i in range(1,4):
            elemento = lt.getElement(respuesta,i)
            lt.addLast(answer,elemento)
        for i in range(18,21):
            elemento = lt.getElement(respuesta,i)
            lt.addLast(answer,elemento)
    table = tabulate(answer['elements'], headers='keys', tablefmt="grid", stralign="center")
    print(table)
    print(f'Δt = {d_time} ms')


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    year = input('year: ')
    lat = input('lat: ')
    long = input('long: ')
    radio = input('radio: ')
    n = input('n: ')

    resp, t = controller.req_6(control, year, lat, long, radio, n)
    r1 = lt.newList('ARRAY_LIST')

    if lt.size(resp[0]) <= 6:
        r1 = resp[0]
    else:
        for i in range(1, 4):
            elemento = lt.getElement(resp[0],i)
            lt.addLast(r1, elemento)

        for i in range(lt.size(resp[0])-2, lt.size(resp[0])+1):
            elemento = lt.getElement(resp[0],i)
            lt.addLast(r1, elemento)
    table1 = None
    table0 = None
    if resp[1] is not None:
        table1 = tabulate(r1['elements'], headers='keys', tablefmt="grid", stralign="center")
        table0 = tabulate([resp[1]], headers='keys', tablefmt="grid", stralign="center")
    print(table0)
    print(table1)
    print(f'{t} ms')


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    print('=============== Req No. 7 Inputs =============== \n')
    year = int(input('Year: '))
    area = input('Area of interest: ')
    prop = input('Property of interest ("mag", "depth", "sig"): ')
    bins = int(input('Number of bins: '))
    print('\n=============== Req No. 7 Results =============== \n')
    num_eq_year, num_eq_year_title, h_bins, h_values, min_val, max_val, lt_hist_data, d_time =controller.req_7(control, year, area, prop, bins)
    print(f'Total earthquakes in {year}: {num_eq_year}')
    print(f'Earthquakes in {area}: {num_eq_year_title}')
    if not lt.isEmpty(lt_hist_data):
        print(f'Min {prop}: {min_val}')
        print(f'Max {prop}: {max_val}')
        if lt.size(h_values)<=6:
            print(f'\nResults found: \n')
        else:
            print(f'\nOnly first and last 3 results are: \n')
        req_tab = sample_req_7(lt_hist_data, prop)
        print(req_tab)
        plt.hist(h_values['elements'], bins=h_bins['elements'], color='goldenrod')
        plt.title(f'Histogram of {prop} in {area} in {year}')
        plt.xlabel(f'{prop}')
        plt.ylabel('No. Events')
        plt.xticks(h_bins['elements'])
        plt.show()
        print(f'Δt = {d_time} ms')


def sample_req_7(data_lt, prop):
    info_tab = {'time':[], 'lat':[], 'long':[], 'title':[], 'code':[], prop:[]}
    if lt.size(data_lt)<=6:
        for eq in lt.iterator(data_lt):
            for key in info_tab:
                info_tab[key].append(eq[key])
    else:
        for i in range(2,-1,-1): #3 primeros
            eq = lt.getElement(data_lt,lt.size(data_lt)-i)
            for key in info_tab:
                info_tab[key].append(eq[key])
        for i in range(3,0,-1): #3 últimos
            eq = lt.getElement(data_lt,i)
            for key in info_tab:
                info_tab[key].append(eq[key])
    return tabulate(info_tab, headers='keys', tablefmt="grid", stralign="center")
        


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    print('\n=============== Req No. 8 Results =============== \n')
    parametros = lt.newList('ARRAY_LIST')
    print('=============== Carga de datos =============== \n')
    m = folium.Map( zoom_start=100)
    locations = lt.newList('ARRAY_LIST')
    for dato in lt.iterator(control['temblores']):
        lt.addLast(locations,(dato['lat'],dato['long']))
    MarkerCluster(locations=locations['elements'],popups=control['temblores']['elements']).add_to(m)
    m.save('req0.html')
    webbrowser.open('req0.html')

    parametros = lt.newList('ARRAY_LIST')
    print('=============== Req No. 1 Inputs =============== \n')
    start = input('Ingrese la fecha inicial: ')
    end = input('Ingrese la fecha final: ')
    lt.addLast(parametros,start)
    lt.addLast(parametros,end)
    req_1, time1 = controller.req_8(control, 1,parametros)
    req_1.save('req1.html')
    webbrowser.open('req1.html')

    parametros = lt.newList('ARRAY_LIST')
    print('=============== Req No. 2 Inputs =============== \n')
    start = input('Ingrese la magnitud mínima: ')
    end = input('Ingrese la magnitud máxima: ')
    lt.addLast(parametros,start)
    lt.addLast(parametros,end)
    req_2,time2 = controller.req_8(control, 2,parametros)
    req_2.save('req2.html')
    webbrowser.open('req2.html')

    parametros = lt.newList('ARRAY_LIST')
    print('=============== Req No. 4 Inputs =============== \n')
    sig = input('Ingrese la significancia mínima: ')
    d = input('Ingrese la distancia azimutal máxima: ')
    lt.addLast(parametros,sig)
    lt.addLast(parametros,d)
    req_4,time4 = controller.req_8(control, 4,parametros)
    req_4.save('req4.html')
    webbrowser.open('req4.html')

    parametros = lt.newList('ARRAY_LIST')
    print('=============== Req No. 5 Inputs =============== \n')
    depth = input('Ingrese la profundidad mínima: ')
    nst = input('Ingrese el número de estaciones mínimo: ')
    lt.addLast(parametros,depth)
    lt.addLast(parametros,nst)
    req_5,time5 = controller.req_8(control, 5,parametros)
    req_5.save('req5.html')
    webbrowser.open('req5.html')
    
    parametros = lt.newList('ARRAY_LIST')
    print('=============== Req No.6 Inputs =============== \n')
    year = input('year: ')
    lat = input('lat: ')
    long = input('long: ')
    radio = input('radio: ')
    n = input('n: ')
    lt.addLast(parametros,year)
    lt.addLast(parametros,lat)
    lt.addLast(parametros,long)
    lt.addLast(parametros,radio)
    lt.addLast(parametros,n)
    req_6, time6 = controller.req_8(control,6,parametros)
    req_6.save('req6.html')
    webbrowser.open('req6.html')
    
    parametros = lt.newList('ARRAY_LIST')
    print('=============== Req No. 7 Inputs =============== \n')
    anio = input('Ingrese el año: ')
    pc = input('Ingrese la propiedad de conteo: ')
    lt.addLast(parametros,anio)
    lt.addLast(parametros,pc)
    req_7, time7 = controller.req_8(control, 7,parametros)
    req_7.save('req7.html')
    webbrowser.open('req7.html')

    print(f'Time: {(time2+time4+time5+time6+time7)} ms')

# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
default_limit = 1000

def menu_cycle():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        gc.collect()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            filename = input('Elija cuál archivo desea cargar:\n1) small\n2) 5pct\n3) 10pct\n4) 20pct\n5) 30pct\n6) 50pct\n7) 80pct\n8) large\n')
            print("Cargando información de los archivos ....\n")
            data, d_time = load_data(control, filename)
            print_load_data(data, d_time)
        elif int(inputs) == 2:
            valido = False

            while not valido:
                initialDate = input('Fecha inicial: ')
                if len(initialDate) == 16:
                    valido = True
            
            valido = False
            while not valido:
                finalDate = input('Fecha final: ')
                if len(finalDate) == 16:
                    valido = True

            print_req_1(control, initialDate, finalDate)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            mag = input('Ingrese la profundidad mínima: ')
            nst = input('Ingrese la cantidad de estaciones mínima: ')
            print_req_5(control, mag, nst)

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

if __name__ == "__main__":
    threading.stack_size(67108864*2) # 128MB stack
    sys.setrecursionlimit(default_limit*1000000)
    thread = threading.Thread(target=menu_cycle)
    thread.start()
#Primer avance - Reto 3