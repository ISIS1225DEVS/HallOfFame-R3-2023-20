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
import gc
import pro as pr
import matplotlib.pyplot as plt
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
    control=controller.new_controller()
    return control


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


def askSizemenu():
    print()
    print("Seleccione el tamaño de archivo que desea usar para continuar")
    print("1 - small")
    print("2 - 5pct")
    print("3 - 10pct")
    print("4 - 20pct")
    print("5 - 30pct")
    print("6 - 50pct")
    print("7 - 80pct")
    print("8 - large")
    print()


def askSize():
    size = ""
    while True:
        askSizemenu()
        choice = input()
        if choice.isdigit():  # Verifica si la entrada es un número
            choice = int(choice)
            if 1 <= choice <= 8:
                if choice == 1:
                    size = "-small"
                elif choice == 2:
                    size = "-5pct"
                elif choice == 3:
                    size = "-10pct"
                elif choice == 4:
                    size = "-20pct"
                elif choice == 5:
                    size = "-30pct"
                elif choice == 6:
                    size = "-50pct"
                elif choice == 7:
                    size = "-80pct"
                elif choice == 8:
                    size = "-large"
                break  # Sale del bucle si se hizo una elección válida
            else:
                print("Opción errónea, vuelva a elegir.\n")
        else:
            print("Entrada inválida, por favor ingrese un número del 1 al 8.\n")
    return size

def printmem():
    """
    Pregunta si se quiere observar el uso de memoria
    """
    print()
    print("Desea observar el uso de memoria? (True/False)")
    mem = input("Respuesta: ")
    ans = castBoolean(mem)
    print()
    return ans


def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    pass
    
def process_earthquakes(earthquakes):
    # Hacer el sort de los terremotos por fecha
    earthquakes.sort(key=lambda x: x['time'])

    # Tomar los primeros y ultimos 5 terremotos
    first_5 = earthquakes[:5]
    last_5 = earthquakes[-5:]

    # Combinar las dos listas
    final_earthquakes = first_5 + last_5

    return final_earthquakes

def print_tabload(datastructure, time, memory):
    """
    Función que imprime con tabulate los datos cargados
    """
    earthquakes = datastructure['earthquakes']
    size1 = lt.size(earthquakes)

    sampleEarthquakes = process_earthquakes(earthquakes["elements"])

    finalEarthquakes = []
    for item in sampleEarthquakes:
        tsunami = "False"
        if item["tsunami"] == 1:    
            tsunami = "True"
        newitem = {"time": item["time"], "lat": item["lat"], "long": item["long"], "depth": item["depth"], "sig": item["sig"], 
                                "nst": item["nst"], "title": item["title"], "felt": item["felt"], "cdi": item["cdi"], "mmi": item["mmi"], 
                                "tsunami": tsunami}
        controller.fill_empty_values(newitem)
        finalEarthquakes.append(newitem) 


    print("--------------------------------")
    print("Cantidad de terremotos:", size1)
    print("--------------------------------")
    print()
    print("==========================================================")
    print("=============INFORME DE RÉCORDS DE TERREMOTOS=============")
    print("==========================================================")
    print()
    print("Los primeros y últimos 3 registros de cada lista son:")	
    print()
    print("---------RESULTADO DE TERREMOTOS---------")
    print("Terremotos cargados:", size1)
    print(tabulate(finalEarthquakes, headers="keys", tablefmt="fancy_grid", showindex=False))
    print()

    if memory != 0:
        print("Tiempo [ms]: ", f"{time:.3f}", "||",
              "Memoria [kB]: ", f"{memory:.3f}")
    else:
        print("Tiempo [ms]: ", f"{time:.3f}")

    print()


def print_req_1(control, ini, fin, mem):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    info, size,time, memory= controller.req_1(control, ini, fin, mem)

    print("cantidad de evnetos ocurrdos:", size  )
    print(tabulate(info, headers="keys", tablefmt="fancy_grid", showindex=False))

    if memory != 0:
        print("Tiempo [ms]: ", f"{time:.3f}", "||",
              "Memoria [kB]: ", f"{memory:.3f}")
    else:
        print("Tiempo [ms]: ", f"{time:.3f}")


def print_req_2(control, low, high, mem):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    info,event, time, memory= controller.req_2(control, low, high, mem)
    print("Cantidad de eventos de esas magnitudes:",event)
    print(tabulate(info, headers="keys", tablefmt="fancy_grid", showindex=False))

    if memory != 0:
        print("Tiempo [ms]: ", f"{time:.3f}", "||",
              "Memoria [kB]: ", f"{memory:.3f}")
    else:
        print("Tiempo [ms]: ", f"{time:.3f}")


def print_req_3(control, mag, pro, mem):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    info, time, memory= controller.req_3(control, mag, pro, mem)
    print(tabulate(info, headers="keys", tablefmt="fancy_grid", showindex=False))

    if memory != 0:
        print("Tiempo [ms]: ", f"{time:.3f}", "||",
              "Memoria [kB]: ", f"{memory:.3f}")
    else:
        print("Tiempo [ms]: ", f"{time:.3f}")


def print_req_4(control, sig, gap):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    events, tevents, time, memory = controller.req_4(control, sig, gap)
    
    if events != None:
        print("====================== Req No. 5 Inputs ============================")
        print("significancia minima:", sig)
        print("distancia maxima azimutual:", gap)
        print()
        print("====================== Req No. 5 Results ============================")
        print("Total de eventos entre fechas:", tevents)
        print("Seleccionando los primeros", str(15) , "eventos que cumplan con los criterios de búsqueda...")
        print()
        print("Tamaño de la consulta:", tevents) 
        print("Los primeros y ultimos '3' resultados son:")
        print()
        print(tabulate(events, headers="keys", tablefmt="fancy_grid", showindex=False ))
        print()
    else:
        print()
        print("No se ha encontrado al jugador en la base de datos...")
        print()
        
        
    if memory != 0:
        print("Tiempo [ms]: ", f"{time:.3f}", "||",
              "Memoria [kB]: ", f"{memory:.3f}")
    else:
        print("Tiempo [ms]: ", f"{time:.3f}")
   


def print_req_5(control, depth, nst, consultnum, mem):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    ndates, nevents, printlist, time, memory = controller.req_5(control, depth, nst, consultnum, mem)

    if ndates != None:
        print("====================== Req No. 5 Inputs ============================")
        print("Profundidad mínima:", depth)
        print("Mínimo número de estaciones:", nst)
        print()
        print("====================== Req No. 5 Results ============================")
        print("Total de fechas:", ndates)
        print("Total de eventos entre fechas:", nevents)
        print("Seleccionando los primeros", consultnum, "eventos que cumplan con los criterios de búsqueda...")
        print()
        print("Tamaño de la consulta:", ndates) 
        print("Los primeros y ultimos '3' de los", consultnum, "resultados son:")
        print()
        print(tabulate(printlist, headers="keys", tablefmt="fancy_grid", showindex=False))
        print()
    else:
        print()
        print("No se ha encontrado al jugador en la base de datos...")
        print()

    if memory != 0:
        print("Tiempo [ms]: ", f"{time:.3f}", "||",
              "Memoria [kB]: ", f"{memory:.3f}")
    else:
        print("Tiempo [ms]: ", f"{time:.3f}")

    print()


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


def print_req_7(control, year, area, property, binsnum, mem):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    num_filtered_events, num_histogram_events, min_property_value, max_property_value, property_values, histogram_events, time, memory = controller.req_7(control, year, area, property, mem)

    fig = plt.figure(figsize=(10, 8))

    ax1 = fig.add_subplot(211)
    counts, bins, patches = ax1.hist(property_values, bins=binsnum, edgecolor='black', color='purple', rwidth=0.8)
    title = "Histograma de '" + property + "' en '" + area + "' en el año '" + year + "'"
    plt.title(title)
    plt.xlabel(property, labelpad=50)
    plt.ylabel("Número de eventos")
    plt.xticks([])
    x_positions = [patch.get_x() + patch.get_width() / 2 for patch in patches]
    ax1.set_xticks(x_positions)
    ax1.set_xticklabels([])
    i = -1
    for count, bin, patch in zip(counts, bins, patches):
        i += 1
        plt.text(patch.get_x() + patch.get_width() / 2, patch.get_height(), str(int(count)), 
             ha='center', va='bottom')
        plt.text(patch.get_x() + patch.get_width() / 2, -3, f'({bin:.2f}, {bins[i + 1]:.2f}]', ha='center', rotation=45, fontsize=8)
    plt.gca().set_ylim([0, max(counts)*1.2])

    ax2 = fig.add_subplot(212)
    ax2.axis('tight')
    ax2.axis('off')
    tabletitle = "Detalles de eventos en '" + area + "' en el año '" + year + "'"
    ax2.set_title(tabletitle, pad=-50)   
    col_labels = list(histogram_events[0].keys())
    cell_text = [list(d.values()) for d in histogram_events]
    table = ax2.table(cellText=cell_text, colLabels=col_labels, cellLoc='center', loc='center')
    table.auto_set_column_width(col=list(range(len(col_labels))))
    table.auto_set_font_size(False)
    table.set_fontsize(8)

    plt.subplots_adjust(hspace=0.5)
    
    if num_filtered_events != None:
        print("====================== Req No. 7 Inputs ============================")
        print("Año:", year)
        print("Área:", area)
        print("Propiedad:", property)
        print("Número de bins:", binsnum)
        print()
        print("====================== Req No. 7 Results ============================")
        print("Total de eventos en el año:", num_filtered_events)
        print("Total de eventos usados en el histograma:", num_histogram_events)
        print("Propiedad de interes:", property)
        print("Valor mínimo de la propiedad:", min_property_value)
        print("Valor máximo de la propiedad:", max_property_value)
        print("Numero de bins:", binsnum)
        print()
        print("Tamaño de la consulta:", num_filtered_events) 
        print("Los primeros y ultimos '3' resultados son:")
        print()
        plt.show()
        print()
    else:
        print()
        print("No se ha encontrado al jugador en la base de datos...")
        print()

    if memory != 0:
        print("Tiempo [ms]: ", f"{time:.3f}", "||",
              "Memoria [kB]: ", f"{memory:.3f}")
    else:
        print("Tiempo [ms]: ", f"{time:.3f}")

def print_req_8(mem):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    time, memory = controller.req_8(mem)
    print()
    print("====================== Req No. 8 ============================")
    if memory != 0:
        print("Tiempo [ms]: ", f"{time:.3f}", "||",
              "Memoria [kB]: ", f"{memory:.3f}")
    else:
        print("Tiempo [ms]: ", f"{time:.3f}")
    print()

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
            size = askSize()
            print("Cargando información de los archivos ....\n")
            mem = printmem()
            time, memory = controller.loadData(control, size, memflag=mem)
           
            print_tabload(control['model'], time, memory)

        elif int(inputs) == 2:
            low = input("Ingrese la fecha inicial de busqueda: ")
            high= input("Ingrese la fecha final del busqueda: ")
            mem = printmem()
            print_req_1(control, low, high, mem)

        elif int(inputs) == 3:
            low = input("Ingrese la magnitud inicial de busqueda: ")
            high= input("Ingrese la magnitud final del busqueda: ")
            mem = printmem()
            print_req_2(control,low, high,mem)

        elif int(inputs) == 4:
            mag= input("Ingrese la magnitud: ")
            pro= input("Ingrese la profundidad: ")
            mem = printmem()
            print_req_3(control, mag, pro, mem)

        elif int(inputs) == 5:
            gap = input("Ingrese la dstancia(gap): ")
            sig = input("Ingrese distancia (sig): "  )
            mem = printmem
            print_req_4(control, sig, gap)

        elif int(inputs) == 6:
            depth = input("Ingrese la profundidad min de los eventos de la búsqueda: ")
            nst = input("Ingrese el número mínimo de estaciones que detectan el evento a buscar: ")
            consultnum = input("Ingrese el número de consultas a realizar: ")
            mem = printmem()
            print_req_5(control, float(depth), float(nst), int(consultnum), mem)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            year = input("Ingrese el año a buscar: ")
            area = input("Ingrese el área a buscar: ")
            property = input("Ingrese la propiedad a buscar: ")
            binsnum = input("Ingrese el número de bins a usar: ")
            mem = printmem()
            print_req_7(control, year, area, property, int(binsnum), mem)

        elif int(inputs) == 9:
            mem = printmem()
            print_req_8(mem)
            
        elif int(inputs) == 10:
            print('Desea eliminar la información')
            respuesta = (input())
            if respuesta.lower == "si": #Poner funcion de bolean
                del time, memory
                gc.collect()
                print("Exitoso")
                
            else:
                print("cancelado")

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
