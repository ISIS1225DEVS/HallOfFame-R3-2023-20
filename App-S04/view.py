﻿"""
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
import threading
import model as md
import matplotlib as ml
import matplotlib.pyplot as plt
import math as m


default_limit = 1000
sys.setrecursionlimit(default_limit*10)


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

### Controlador

def new_controller():
    """
        Se crea una instancia del controlador
    """
    # Llamar la función del controlador donde se crean las estructuras de datos
    control = controller.new_controller()
    return control


def print_menu():
    print("Welcome")
    print("1- Load data")
    print("2- Consult seismic events between two dates")
    print("3- Consult seismic events between two magnitudes")
    print("4- Consult 10 most recent seismic events depending on magnitude and depth")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Consult N most recent seismic events in an area")
    print("8- Consult seismic events according to place and property")
    print("9- Ejecutar Requerimiento 8")
    print("0- Exit")


def load_data(control, size, memflag):
    """
    Carga los datos
    """
    # Realizar la carga de datos
    print('\nChoose an option:')
    print('1- Load all functionalities (not recommended for large data sizes)')
    print('2- Choose a functionality')

    choiceInput = int(input('What do you prefer?: \n'))

    
    if choiceInput == 1:
        choice = 0
    else:
        print('\nChoose an option:')
        print('1- Consult seismic events between two dates')
        print('2- Consult seismic events between two magnitudes')
        print('3- Consult 10 most recent seismic events depending on magnitude and depth')
        print('4- req4')
        print('5- req5')
        print('6- Consult N most recent seismic events in an area')
        print('7- Consult seismic events according to place and property')
        print('8- req8')
        choice = int(input('What requisite do you wish to load?: \n'))
        
    print('\nLoading data...')

    size, time, delta_time, delta_memory = controller.load_data(control, size, memflag, choice)
    
    return size, time, delta_time, delta_memory, choice

def ask_load_info():
    #Choose size
    print('\nAvailable sizes:')
    print('1- Smallest')
    print('2- 5 % de los datos')
    print('3- 10 % of all data')
    print('4- 20 % of all data')
    print('5- 30 % of all data')
    print('6- 50 % of all data')
    print('7- 80 % of all data')
    print('8- 100 % of all data')
    #Choose sorting algorithm


    size_input = int(input('Choose the size:\n'))

    print("\nDo you wish to monitor memory usage?")
    print('1- No')
    print('2- Yes')

    meminput = int(input("Choose: \n"))
    
    if size_input == 1:
        size='small'
    elif size_input == 2:
        size='5pct'
    elif size_input == 3:
        size='10pct'
    elif size_input == 4:
        size='20pct'
    elif size_input == 5:
        size='30pct'
    elif size_input == 6:
        size='50pct'
    elif size_input == 7:
        size='80pct'
    elif size_input == 8:
        size='large'
        
    if meminput == 2:
        memflag = True
    else:
        memflag = False
      
    return size, memflag


def print_earthquakes_table(control, time, r_size):
    data_structs = control['model']
    sorted_t = data_structs['temblores']
    print('\n'+'---- EARTHQUAKE RESULTS ----')
    print(' '*8 + 'Total earthquake results in '+str(round(time, 3))+' [ms]: '+str(r_size))
    sorted_t_sublist = controller.create_data_list(sorted_t, 5)
    columns = ['code','time','lat','long','mag','title','depth','sig','nst','gap','felt','cdi','mmi','tsunami']
    create_table(sorted_t, sorted_t_sublist, columns)


def create_table(list, sublist, columns):
    """creates and prints a table based on an original list and its sublist

    Args:
        list (list): original list
        sublist (list): sub list containing first and last 3 elements. can be None
        columns (list): list containing the headers of the table's columns
    """
    if sublist == None:
        table = list
        print('Results struct has less than 6 records...')
    else:
        table = sublist
        print('Results struct has more than 6 records...')
    print(tabulate(lt.iterator(table), tablefmt="grid", headers=columns)+'\n')

# impresión de tiempo y memoria

def delta_time_and_memory(delta_time, delta_memory):
    if delta_memory is not None:
        print("\nTime [ms]: "+ str(round(delta_time, 3)))
        print("Memory [kb]: "+ str(round(delta_memory, 3)) + '\n')
    else:
        print("\nTime [ms]: "+ str(round(delta_time, 3)) + '\n')


# REQUERIMIENTOS

def print_req_1(control, memflag, n=3):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # Imprimir el resultado del requerimiento 1
    start_date = input('\nStarting what date (earliest) would you like to evaluate? (%Y-%m-%dT%H:%M):\n')
    end_date = input('\nUntil what date (latest) would you like to evaluate? (%Y-%m-%dT%H:%M):\n')

    print('\n' + '='*15 + ' Showing results for all events between '+ start_date + ' and ' + end_date + ' ' + '='*15 + '\n')
    
    events_list, events_sublist, count, time, memory = controller.req_1(control, start_date, end_date, memflag, n)
    
    total_dates = count['total_dates']
    events_in_range = count['events_in_range']
    
    delta_time_and_memory(time, memory)
    
    #print("Total different dates: " + str(total_dates))
    print("Total events in range: " + str(events_in_range))
    
    columns = ['time', 'events', 'details']
    
    create_table(events_list, events_sublist, columns)


def print_req_2(control, memflag, n=3):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # Imprimir el resultado del requerimiento 2
    start_mag = input('\nStarting what magnitude (lowest) would you like to evaluate?:\n')
    end_mag = input('\nUntil what magnitude (highest) would you like to evaluate?:\n')

    print('\n' + '='*15 + ' Showing results for all events between '+ start_mag + ' and ' + end_mag + ' ' + '='*15 + '\n')
    
    events_list, events_sublist, count, time, memory = controller.req_2(control, start_mag, end_mag, memflag, n)
    
    #total_magnitudes = count['total_magnitudes']
    events_in_range = count['events_in_range']
    
    delta_time_and_memory(time, memory)
    
    #print("Total different magnitudes: " + str(total_magnitudes))
    print("Total events in range: " + str(events_in_range))
    
    columns = ['mag', 'events', 'details']
    
    create_table(events_list, events_sublist, columns)


def print_req_3(control, memflag, n=3):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # Imprimir el resultado del requerimiento 3
    min_mag = input('\nStarting what magnitude (lowest) would you like to evaluate?:\n')
    max_depth = input('\nUntil what depth (deepest) would you like to evaluate?:\n')

    print('\n' + '='*15 + ' Showing results for all events with a minimum magnitude of '+ min_mag + ' and a maximum depth of ' + max_depth + ' ' + '='*15 + '\n')
    
    events_list, events_sublist, count, time, memory = controller.req_3(control, min_mag, max_depth, memflag, n)
    
    events_in_range = count['events_in_range']
    
    delta_time_and_memory(time, memory)
    
    print("Total events in range: " + str(events_in_range))
    
    columns = ['time', 'events', 'details']
    
    create_table(events_list, events_sublist, columns)


def print_req_4(control, memflag):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    #Imprimir el resultado del requerimiento 4
    min_sig = float(input("\nIngrese la significancia mínima del evento: "))
    #min_sig = 300.0
    max_gap = float(input("\nIngrese la distancia azimutal máxima del evento: "))
    #max_gap = 45.0
    file = controller.req_4(control,memflag,min_sig,max_gap)
    #print(file)
    return print(tabulate(lt.iterator(file),headers= "keys" ,tablefmt='grid'))


def print_req_5(control, memflag):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    stations = input('\nHow many stations would you like to evaluate?\n')
    min_depth = input('\nStarting what depth (deepest) would you like to evaluate?:\n')
    
    events_list, events_sublist, count, time, memory = controller.req_5(control,stations, min_depth, memflag)
    
    print('\n' + '='*15 + 'Req No. 5 Inputs' + '='*15)
    
    print('Min depth: ' + str(min_depth) + '\n')
    print('Max nst (seismic stations): ' + str(stations) + '\n')
    
    print('\n' + '='*15 + 'Req No. 5 Results' + '='*15)
    print('Total different dates: ' + str(count))
    print('Total events between dates: ' + str(count))
    print('Selecting the first 20 results...' + '\n')
    
    print('Consult size: ' + str(count) + ' The first and last 3 of the 20 results are: ' + '\n')
    
    titulos = ['time', 'events', 'details']
    
    delta_time_and_memory(time, memory)
    
    
        
    print(tabulate(lt.iterator(events_sublist), tablefmt="grid", headers=titulos)+'\n')
    
    #print(tabulate(lt.iterator(resultado[1]),headers='keys', tablefmt='grid'))
    
    
    


def print_req_6(control, memflag, nn=3):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    year = input('\nWhat year would you like to consult?:\n')
    r = input('\nWhat radius do you wish to evaluate?\n')
    n = input('\nHow many events do you wish to evaluate?\n')
    latref = input('\nProvide a latitude:\n')
    longref = input('\nProvide a longitude:\n')

    print('\n' + '='*15 + ' Showing results' + '='*15 + '\n')
    
    events_list, events_sublist, count, time, memory, sig_event = controller.req_6(control, year, r, n, latref, longref, memflag, nn)
    
    events_in_range = count['events_in_range']
    size = count['size']
    
    delta_time_and_memory(time, memory)
    
    print("Total events in range: " + str(events_in_range) + '\n')
    print('----- Most Significant Event -----')
    sig_columns = ['time','mag','lat','long','depth','sig','gap','distance','nst','title',
                   'cdi','mmi','magType','type','code']
    print(tabulate(lt.iterator(sig_event), tablefmt="grid", headers=sig_columns)+'\n')
    
    print('----- Nearest '+str(size)+' events in chronological order -----')
    
    columns = ['time', 'events', 'details']
    
    create_table(events_list, events_sublist, columns)


def print_req_7(control, memflag, n=3):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    year = input('\nWhat year would you like to consult?:\n')
    title = input('\nWhat place would you like to evaluate?:\n')
    print('\nAvaliable properties: ')
    print('1- Significance')
    print('2- Magnitude')
    print('3- Depth')
    prop_input = int(input('Choose one of the properties to evaluate:\n'))
    if prop_input == 1:
        prop = 'sig'
    elif prop_input == 3:
        prop = 'depth'
    else:
        prop = 'mag'
    bins = int(input('\nHow many bins do you want?:\n'))

    print('\n' + '='*15 + ' Showing results' + '='*15 + '\n')
    
    events_list, events_sublist, count, time, memory, histogram_list = controller.req_7(control, year, title, prop, bins, memflag, n)
    
    total_events = count['total_events']
    events_in_range = count['events_in_range']
    mini = count['min']
    maxi = count['max']
    
    delta_time_and_memory(time, memory)
    
    print("Total events in "+year+ ": " + str(total_events))
    print("Events in histogram: " + str(events_in_range))
    print("Minimum "+prop+": " + str(mini))
    print("Maximum "+prop+": " + str(maxi) + '\n')
    
    print('----- Showing event details in '+title+' in '+year+'-----\n')
    columns = ['time','lat','long','depth','sig','gap','nst','title',prop]
    create_table(events_list, events_sublist, columns)

    if lt.size(events_list) > 6:
        events = create_list(events_sublist)
    else:
        events = create_list(events_list)   

    fig, (ax1, ax2) = plt.subplots(2)
    counts, edges, bars = ax1.hist(histogram_list, bins, color='skyblue', edgecolor='black')
    ax1.set_xlabel(prop, fontsize=12)
    ax1.set_ylabel('No. Events', fontsize=12)
    ax1.set_title('Histogram of '+prop+' in '+title+' in '+year+'\n', fontsize=14)
    ax1.bar_label(bars, fontsize=10)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    
    ax2.set_axis_off()
    table = ax2.table(cellText=events,
              colLabels=columns,
              colWidths=[0.15,0.1,0.1,0.1,0.1,0.1,0.1,0.25,0.1],
              loc='bottom',
              cellLoc='center',
              rowLoc='center')
    table.scale(1,2)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    
    plt.subplots_adjust(bottom=0.373, hspace=0)
    plt.show()
    
    print('----- End -----\n')
    
def create_list(list):
    new_list = []
    for elem in lt.iterator(list):
        new_list.append(elem)
    return new_list

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


### Controlador

# Se crea el controlador asociado a la vista
control = new_controller()

#### main cycle
def menu_cycle():
    """
    Menu principal
    """
    working = True
    choice = 10
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Select an option to continue\n')
        if int(inputs) == 1:
            size = 'small'
            memflag = False
            control = new_controller()
            size, memflag = ask_load_info()
            size, time, delta_time, delta_memory, choice = load_data(control, size, memflag)
            print('-'*38)
            print ('Earthquake count: ' + str(size))
            print('-'*38 + '\n')
            print('='*51)
            print('='*15 + ' EARTHQUAKE RECORD RESULTS ' + '='*15)
            print('='*51 + '\n')
            print('Printing results for the first 5 and last 5 records on file.')
            delta_time_and_memory(delta_time, delta_memory)
            print_earthquakes_table(control, time, size)
        elif int(inputs) == 2:
            if choice == 1 or choice == 0:
                print_req_1(control,memflag)
            else: 
                print('\nPlease reload data to use this functionality\n')

        elif int(inputs) == 3:
            if choice == 2 or choice == 0:
                print_req_2(control,memflag)
            else: 
                print('\nPlease reload data to use this functionality\n')

        elif int(inputs) == 4:
            if choice == 3 or choice == 0:
                print_req_3(control,memflag)
            else: 
                print('\nPlease reload data to use this functionality\n')

        elif int(inputs) == 5:
            if choice == 4 or choice == 0:
                print_req_4(control,memflag)
            else: 
                print('\nPlease reload data to use this functionality\n')

        elif int(inputs) == 6:
            if choice == 5 or choice == 0:
                print_req_5(control,memflag)
            else: 
                print('\nPlease reload data to use this functionality\n')

        elif int(inputs) == 7:
            if choice == 6 or choice == 0:
                print_req_6(control,memflag)
            else: 
                print('\nPlease reload data to use this functionality\n')

        elif int(inputs) == 8:
            if choice == 7 or choice == 0:
                print_req_7(control,memflag)
            else: 
                print('\nPlease reload data to use this functionality\n')

        elif int(inputs) == 9:
            if choice == 8 or choice == 0:
                print_req_8(control,memflag)
            else: 
                print('\nPlease reload data to use this functionality\n')
        
        elif int(inputs) == 10:
            memflag = change_memory_usage(memflag)

        elif int(inputs) == 0:
            working = False
            print("\nThank you for using the program")
        else:
            print("Option unavailable. Please choose again.\n")
    sys.exit(0)


# main del reto
if __name__ == "__main__":
    
    threading.stack_size(67108864*2) # 128MB stack
    sys.setrecursionlimit(default_limit*1000000)
    thread = threading.Thread(target=menu_cycle())
    thread.start()