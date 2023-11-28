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
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import webbrowser
import traceback

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
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    pass

def loadData(control,numero):
    dataSize = controller.loadData(control,numero)
    print("El numero de eventos cargados fueron: " + str(dataSize))
    headers = ["code", "time", "lat", "long", "mag", "title", "depth", "felt", "cdi", "mmi", "tsunami"]
    print(tabulatedData(controller.getFirstAndLastN(control["seismicEvents"], 5), headers))

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def tabulatedData(registers, headers, detailHeaders=None, detailSize=None):
    width = 12
    if detailSize:
        width = detailSize
    table = []
    for register in lt.iterator(registers):
        row = []
        for header in headers:
            datum = register[header] if register[header] != "" and register[header] != " " else "Unknown"
            if detailHeaders and type(datum) == dict:
                datum = tabulatedData(controller.getFirstAndLastN(datum, 3), detailHeaders)
            row.append(datum)
        table.append(row)
    return tabulate(table, [header.title() for header in headers], tablefmt="fancy_grid", maxcolwidths=width[:len(headers)-1] if detailSize and detailHeaders else width, maxheadercolwidths=width)

def displayMap(metaData):
    if metaData["map"]:
        print("Do you want to watch the interactive map?\n1- Yes\n2- No")
        if input("Response: ") == "1":
            webbrowser.open_new_tab(f'{metaData["path"]}.html')
def print_req_1(control, date1, date2):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    startTime = controller.get_time()
    filtered, metaData, deltaMemory = controller.req_1(control, date1, date2)
    finishTime = controller.get_time()
    deltaTime = controller.delta_time(startTime, finishTime)
    print("El tiempo que tomó la ejecución del requerimiento fue de: " + str(deltaTime))
    print("La memoria que ocupó la ejecución del requerimiento fue: " + str(deltaMemory))
    print("El número total de fechas diferentes encontrados fue: " + str(metaData["totalDates"]))
    print("El número total de eventos sísmicos ocurridos durante las fechas indicadas fue: " + str(metaData["totalSeismicEvents"]))
    headers = ["time", "events", "details"]
    detailHeaders = ["mag", "lat", "long", "depth", "sig", "gap", "nst", "title", "cdi", "mmi", "magType", "type", "code"]
    detailSize = [12,12,12]
    print(tabulatedData(controller.getFirstAndLastN(filtered, 3), headers, detailHeaders, detailSize))
    displayMap(metaData)


def print_req_2(control, inferiorMagLimit, superiorMagLimit):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    startTime = controller.get_time()
    filtered, metaData, deltaMemory = controller.req_2(control, inferiorMagLimit, superiorMagLimit)
    finishTime = controller.get_time()
    deltaTime = controller.delta_time(startTime, finishTime)
    print("El tiempo que tomó la ejecución del requerimiento fue de: " + str(deltaTime))
    print("La memoria que ocupó la ejecución del requerimiento fue: " + str(deltaMemory))
    print("El número total de magnitudes encontradas fue: " + str(metaData["totalMagnitudes"]))
    print("El número total de eventos sísmicos ocurridos entre las magnitudes indicadas fue: " + str(metaData["totalSeismicEvents"]))
    headers = ["mag", "events", "details"]
    detailHeaders = ["time", "lat", "long", "depth", "sig", "gap", "nst", "title", "cdi", "mmi", "magType", "type", "code"]
    detailSize = [12,12,12]
    print(tabulatedData(controller.getFirstAndLastN(filtered, 3), headers, detailHeaders, detailSize))
    displayMap(metaData)

def print_req_3(control, minMag, maxDepth):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    startTime = controller.get_time()
    filtered, metaData, deltaMemory = controller.req_3(control, minMag, maxDepth)
    finishTime = controller.get_time()
    deltaTime = controller.delta_time(startTime, finishTime)
    print("El tiempo que tomó la ejecución del requerimiento fue de: " + str(deltaTime))
    print("La memoria que ocupó la ejecución del requerimiento fue: " + str(deltaMemory))
    print("El total de diferentes fechas encontradas fue: " + str(metaData["totalDifferentDates"]))
    print("El número total de eventos sísmicos registrados dentro de los limites de magnitud y profundidad indicados fue: " + str(metaData["totalEventsBetweenDates"]))
    headers = ["time", "events", "details"]
    detailHeaders = ["mag", "lat", "long", "depth", "sig", "gap", "nst", "title", "cdi", "mmi", "magType", "type", "code"]
    detailSize = [12,12,12]
    print(tabulatedData(controller.getFirstAndLastN(filtered, 3), headers, detailHeaders, detailSize))
    displayMap(metaData)

def print_req_4(control, minSig, maxGap):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    startTime = controller.get_time()
    filtered, metaData, deltaMemory = controller.req_4(control, minSig, maxGap)
    finishTime = controller.get_time()
    deltaTime = controller.delta_time(startTime, finishTime)
    print("El tiempo que tomó la ejecución del requerimiento fue de: " + str(deltaTime))
    print("La memoria que ocupó la ejecución del requerimiento fue: " + str(deltaMemory))
    print("El total de diferentes fechas encontradas fue: " + str(metaData["totalDifferentDates"]))
    print("El número total de eventos sísmicos registrados mayores a la significancia y menores a la distancia azimutal indicada fue: " + str(metaData["totalEventsBetweenDates"]))
    headers = ["time", "events", "details"]
    detailHeaders = ["mag", "lat", "long", "depth", "sig", "gap", "nst", "title", "cdi", "mmi", "magType", "type", "code"]
    detailSize = [12,12,12]
    print(tabulatedData(controller.getFirstAndLastN(filtered, 3), headers, detailHeaders, detailSize))
    displayMap(metaData)

def print_req_5(control, minDepth, minNst):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    startTime = controller.get_time()
    filtered, metaData, deltaMemory = controller.req_5(control, minDepth, minNst)
    finishTime = controller.get_time()
    deltaTime = controller.delta_time(startTime, finishTime)
    print("El tiempo que tomó la ejecución del requerimiento fue de: " + str(deltaTime))
    print("La memoria que ocupó la ejecución del requerimiento fue: " + str(deltaMemory))
    print("El total de diferentes fechas encontradas fue: " + str(metaData["totalDifferentDates"]))
    print("El número total de eventos sísmicos registrados mayores a la significancia y menores a la distancia azimutal indicada fue: " + str(metaData["totalEventsBetweenDates"]))
    headers = ["time", "events", "details"]
    detailHeaders = ["mag", "lat", "long", "depth", "sig", "gap", "nst", "title", "cdi", "mmi", "magType", "type", "code"]
    detailSize = [12,12,12]
    print(tabulatedData(controller.getFirstAndLastN(filtered, 3), headers, detailHeaders, detailSize))
    displayMap(metaData)

def print_req_6(control, date, lat, lon, r, n):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    startTime = controller.get_time()
    filtered, metaData, deltaMemory = controller.req_6(control, date, lat, lon, r, n)
    finishTime = controller.get_time()
    deltaTime = controller.delta_time(startTime, finishTime)
    headersHighest = ["time", "mag", "lat", "long", "depth", "sig", "gap", "nst", "title", "cdi", "mmi", "magType", "type", "code"]
    print("El tiempo que tomó la ejecución del requerimiento fue de: " + str(deltaTime))
    print("La memoria que ocupó la ejecución del requerimiento fue: " + str(deltaMemory))
    print("El número de eventos dentro del radio fue: " + str(metaData["eventsInRange"]))
    print("La máxima cantidad de eventos posibles fue: " + str(metaData["maxNPossibleEvents"]))
    print("El número de fechas diferentes encontradas fue: " + str(metaData["differentDates"]))
    print("El número de eventos encontrados fue: " + str(metaData["totalEvents"]))
    print("")
    print("El evento más significativo fue: ")
    print(tabulatedData(metaData["highestEvent"], headersHighest))
    print("")
    print("Eventos más cercanos al evento más significativo: ")
    headers = ["time", "events", "details"]
    detailHeaders = ["mag", "lat", "long", "depth", "sig", "gap", "nst", "title", "cdi", "mmi", "magType", "type", "code"]
    detailSize = [12,12,12]
    print(tabulatedData(controller.getFirstAndLastN(filtered, 3), headers, detailHeaders, detailSize))
    displayMap(metaData)

def print_req_7(control, year, place, feature, N):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    startTime = controller.get_time()
    filtered, histogram, metaData, deltaMemory = controller.req_7(control, year, place, feature, N)
    finishTime = controller.get_time()
    deltaTime = controller.delta_time(startTime, finishTime)
    print("El tiempo que tomó la ejecución del requerimiento fue de: " + str(deltaTime))
    print("La memoria que ocupó la ejecución del requerimiento fue: " + str(deltaMemory))
    print("El total de eventos encontrados fue: " + str(lt.size(filtered)))
    headers = ["time", "lat", "long", "title", "code", feature.lower()]
    print(tabulatedData(controller.getFirstAndLastN(filtered, 3), headers))
    dataTable = []
    for event in lt.iterator(controller.getFirstAndLastN(filtered, 3)):
        row = []
        row.append(event["time"])
        row.append(event["lat"])
        row.append(event["long"])
        row.append(event["title"])
        row.append(event["code"])
        row.append(event["mag"])
        dataTable.append(row)
    if histogram:
        fig = plt.figure(figsize=(10, 8))
        gs = gridspec.GridSpec(2, 1, height_ratios=[5, 1], hspace=0.9, figure=fig)
        ax = fig.add_subplot(gs[0])
        bars = ax.bar(histogram["x"], histogram["y"])
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 0.5, yval, ha='center', va='bottom')
        ax.set_title(histogram["title"])
        ax.set_xlabel(histogram["xLabel"])
        ax.set_ylabel(histogram["yLabel"])
        ax.set_xticklabels(histogram["x"],rotation= 45)
        ax2 = fig.add_subplot(gs[1])
        ax2.set_title(histogram["tableTitle"])
        table_ax = ax2.table(cellText=dataTable, colLabels=headers, loc='bottom', cellLoc='center')
        ax2.axis('off')
        table_ax.auto_set_font_size(False)
        table_ax.set_fontsize(10)
        table_ax.scale(1, 1.5)
        for col in range(len(headers)):
            table_ax.auto_set_column_width(col=col)
        #table_ax.set_transform(tabla_axes.transAxes)
        plt.subplots_adjust(left=0.2, bottom=0.3, right=0.8, top=0.9)
        plt.show()
    displayMap(metaData)

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista


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
            control = new_controller()
            print("Cargando información de los archivos ....\n")
            print("seleccione el archivo que quiere cargar: \n 1. Small \n 2. 5 pct \n 3. 10 pct \n 4. 20 pct \n 5. 30 pct \n 6. 50 pct \n 7. 80 pct \n 8. large ")
            numero=int(input("Ingrese el numero: "))
            data = loadData(control,numero)
        elif int(inputs) == 2:
            print_req_1(control, input("a: "), input("a: "))

        elif int(inputs) == 3:
            print_req_2(control, input("a: "), input("a: "))

        elif int(inputs) == 4:
            print_req_3(control, input("a: "), input("a: "))

        elif int(inputs) == 5:
            print_req_4(control, input("a: "), input("a: "))
 
        elif int(inputs) == 6:
            print_req_5(control, input("a: "), input("a: "))

        elif int(inputs) == 7:
            print_req_6(control, input("a: "), input("a: "), input("a: "), input("a: "), input("a: "))

        elif int(inputs) == 8:
            print_req_7(control, input("a: "), input("a: "), input("a: "), input("a: "))

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
