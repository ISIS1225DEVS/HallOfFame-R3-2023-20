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
import matplotlib.pyplot as plt

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
default_limit = 1000
sys.setrecursionlimit(default_limit*10)

def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    data_structs = controller.new_controller()
    return data_structs


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


def load_data(control,archivo):
    """
    Carga los datos
    """
    datos= controller.load_data(control,archivo)
    return datos


def cantidad_datos(control):
    archivo=""
    print("\n ¿Cuantos datos desea cargar?")
    print("1: 0.5% de los datos")
    print("2: 5% de los datos")
    print("3: 10% de los datos")
    print("4: 20% de los datos")
    print("5: 30% de los datos")
    print("6: 50% de los datos")
    print("7: 80% de los datos")
    print("8: 100% de los datos")
    opcion=int(input("\n Ingrese cuantos datos desea cargar: "))
    if opcion==1:
        archivo="small.csv"
    elif opcion==2:
        archivo="5pct.csv"
    elif opcion==3:
        archivo="10pct.csv"
    elif opcion==4:
        archivo="20pct.csv"
    elif opcion==5:
        archivo="30pct.csv"
    elif opcion==6:
        archivo="50pct.csv" 
    elif opcion==7:
        archivo="80pct.csv"
    elif opcion==8:
        archivo="large.csv"
    temblores = load_data(control, archivo)
    respuesta=controller.sort(control)
    print(respuesta)
    print("\n------------------------------------------------------------")
    print("\n Earthquake event size: ",temblores)
    print("\n -----------------------------------------------------------\n")
    print("\n ==============================================================================================================")
    print("\n ============================= EARTHQUAKE RECORDS REPORT ======================================================")
    print("\n ==============================================================================================================\n")
    print("\nPrinting the first 5 and last 5 records...\n")
    print("\n---- EARTHQUAKES RESULTS ----\n")
    print("\n        Total Earthquakes: ",temblores)
    print("\n Loaded Earthquake ADT have more tan 10 records...")
    l_temblores=controller.resumir_lista(control["model"]["temblores"],5,0)
    print(controller.creartabla(l_temblores),"\n")


def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    inicial = input("\nIngrese la fecha inicial:")
    final = input("\nIngrese la fecha final:")
    
    respuesta= controller.req_1(control,inicial,final)
    lista_resumida,total_sismos,total_fechas=respuesta
    print("\n====================== Req No. 1 Inputs ======================")
    print("Start date: ",inicial)
    print("End date: ",final)
    print("\n====================== Req No. 1 Results ======================")
    print("Total different dates: ", total_fechas)
    print("Total events between dates: ",total_sismos )
    print("Consult size:",total_sismos)
    if total_sismos==0:
        print("No results")
    elif total_sismos<=6:
        print("\nConsult size has 6 records or less...")
        tabla=controller.creartabla(lista_resumida)
        print(tabla)
    elif total_sismos>6:
        print("\nConsult size has more than 6 records...")
        print("Only first and last 3 results are: ")
        tabla=controller.creartabla(lista_resumida)
        print(tabla)


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    inferior = float(input("\nIngrese la magnitud inferior:"))
    superior = float(input("\nIngrese la magnitud superior:"))
    
    respuesta= controller.req_2(control,inferior,superior)
    lista_resumida,total_sismos,total_llaves,elementos,tamaño=respuesta
    print("\n====================== Req No. 2 Inputs ======================")
    print("Min magnitude: ",inferior)
    print("Max magnitude: ",superior)
    print("\n====================== Req No. 2 Results ======================")
    print("Total different magnitudes: ", total_llaves)
    print("Total events between magnitudes: ",total_sismos )
    print("Consult size:",total_sismos)
    if total_sismos==0:
        print("No results")
    elif total_sismos<=6:
        print("\nConsult size has 6 records or less...")
        tabla=controller.creartabla(lista_resumida)
        print(tabla)
    elif total_sismos>6:
        print("\nConsult size has more than 6 records...")
        print("Only first and last 3 results are: ")
        tabla=controller.creartabla(lista_resumida)
        print(tabla)


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    minima = float(input("\n Ingresa la magnitud mínima del evento:"))
    maxima = float(input("\n Ingresa la profundidad máxima del evento:"))
    
    respuesta= controller.req_3(control,minima,maxima)
    fechas_diferentes,total_eventos,lista_resumida=respuesta
    print("\n====================== Req No. 3 Inputs ======================")
    print("Min magnitude: ",minima)
    print("Max depth: ",maxima)
    print("\n====================== Req No. 3 Results ======================")
    print("Total different dates: ", fechas_diferentes)
    print("Total events between dates: ",total_eventos )
    print("Selecting the first 10 results...")

    print("\nConsult size:",total_eventos)
    if total_eventos==0:
        print("No results")
    elif total_eventos<=6:
        print("\nConsult size has 6 records or less...")
        tabla=controller.creartabla(lista_resumida)
        print(tabla)
    elif total_eventos>6:
        print("\nConsult size has more than 6 records...")
        print("Only first and last 3 results are: ")
        tabla=controller.creartabla(lista_resumida)
        print(tabla)


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    minima = int(input("\n Ingresa la significancia mínima del evento:"))
    maxima = float(input("\n Ingresa la distancia azimutal máxima del evento:"))
    
    respuesta= controller.req_4(control,minima,maxima)
    lista_resumida,total_eventos,total_fechas=respuesta
    print("\n====================== Req No. 4 Inputs ======================")
    print("Min significance: ",minima)
    print("Max gap: ",maxima)
    print("\n====================== Req No. 4 Results ======================")
    print("Total different dates: ", total_fechas)
    print("Total events between dates: ",total_eventos )
    print("Selecting the first 15 results....")
    if total_eventos==0:
        print("No results")
    elif total_eventos<=6:
        print("\nConsult size",total_fechas ,"has 6 records or less...")
        tabla=controller.creartabla(lista_resumida)
        print(tabla)
    elif total_eventos>6:
        print("\nConsult size",total_fechas ,"has more than 6 records...")
        print("Only first and last 3 results are: ")
        tabla=controller.creartabla(lista_resumida)
        print(tabla)


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    depth_min = float(input("\nIngrese la profundidad minima: "))
    nst_min = float(input("\nIngrese el número minimo de estaciones:"))
    
    respuesta= controller.req_5(control,depth_min,nst_min)
    fechas_diferentes,total_eventos,lista_resumida=respuesta
    print("\n====================== Req No. 5 Inputs ======================")
    print("Min depth: ",depth_min)
    print("Min nst (seismic stations): ",nst_min)
    print("\n====================== Req No. 5 Results ======================")
    print("Total different dates: ", fechas_diferentes)
    print("Total events between dates: ",total_eventos )
    print("Selecting the first 20 results...")
    print("\nConsult size:",total_eventos)
    if total_eventos==0:
        print("No results")
    elif total_eventos<=6:
        print("\nConsult size has 6 records or less...")
        tabla=controller.creartabla(lista_resumida)
        print(tabla)
    elif total_eventos>6:
        print("\nConsult size has more than 6 records...")
        print("Only first and last 3 results are: ")
        tabla=controller.creartabla(lista_resumida)
        print(tabla)


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    anio = input("\nIngrese el año que desea consultar: ")
    latitud = float(input("\nIngrese la latitud de referencia: "))
    longitud = float(input("\nIngrese la longitud de referencia: "))
    radio=float(input("\nIngrese el radio(km) del area circundante: "))
    n=int(input("\nIngrese el numero de eventos de magnitud mas cercana a mostrar: "))
    
    respuesta= controller.req_6(control,anio, latitud, longitud, radio, n)
    total_eventos_en_area,evento_mas_sig, pre_events,pos_events,lista_resumida,codigo,cant_eventos,dif_fechas=respuesta
    print("\n====================== Req No. 6 Inputs ======================")
    print("Year: ",anio)
    print("Focus Latitude: ",latitud)
    print("MFocus Longitud: ",longitud)
    print("Relevant Radius: ",radio)
    print("Number of most important events: ",n)
    print("\nMax event code: ", codigo)
    print("Pre n events ",pre_events-1 )
    print("Post n events ",pos_events )
    print("\n====================== Req No. 6 Results ======================")
    print("Number of events within radius: ", total_eventos_en_area)
    print("Max number of possible events: ",n*2+1)
    print("Total diferent dates ",dif_fechas )
    print("Total events between dates ",cant_eventos )
    print("\n----- Max Event -------")
    tabla=controller.creartabla(evento_mas_sig)
    print(tabla)
    print("\n----- Nearest Events in chronological order -------")
    print("Most important events relate to the max event: ",codigo)

    print("\nConsult size:",cant_eventos)
    if cant_eventos==0:
        print("No results")
    elif cant_eventos<=6:
        print("\nConsult size has 6 records or less...")
        tabla=controller.creartabla(lista_resumida)
        print(tabla)
    elif cant_eventos>6:
        print("\nConsult size has more than 6 records...")
        print("Only first and last 3 results are: ")
        tabla=controller.creartabla(lista_resumida)
        print(tabla)
    


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    #### cambiar datos de impresion 
    anio = input("\n Ingresa el año de interes:")
    title = input("\n Ingresa el titulo de la región:")
    propiedad = input("\n Ingresa la propiedad de conteo:")
    casillas = int(input("\n Ingresa el numero de segmentos o casillas del histograma:"))
    respuesta= controller.req_7(control,anio,title,propiedad,casillas)
    total_sis_anio,total_sis_his,prop_min,prop_max,titulos,valores,lista_val_hist,intervalos,marcas,nombres,conteos=respuesta
    print("\n====================== Req No. 4 Inputs ======================")
    print("Year: ",anio)
    print("Area of interest: ",title)
    print("Property of interest: ",propiedad)
    print("Number of bins: ",casillas)
    print("\n====================== Req No. 4 Results ======================")
    print("Total events in the year : ", total_sis_anio)
    print("Total events in histogram: ",total_sis_his)
    print("Minimun ", prop_min, "maximun:", prop_max," ",propiedad," value")
    print("Histogram and table:")
    fig,(ax_hist,ax_tabla) = plt.subplots(2,1,gridspec_kw={'height_ratios': [5, 4]})
    ax_tabla.axis("off")
    ax_hist.hist(lista_val_hist["elements"],bins = intervalos["elements"],edgecolor='black',color='green', rwidth=0.8)
    ax_hist.set_xticks(marcas["elements"])
    ax_hist.set_xticklabels(nombres["elements"],rotation=45, ha='right')
    ax_hist.xaxis.set_ticks_position('bottom')
    for i in range(1,lt.size(conteos)+1):
        marca = lt.getElement(marcas,i)
        nombre = lt.getElement(nombres,i)
        conteo = lt.getElement(conteos,i)
        ax_hist.text(marca,conteo,str(conteo),ha = "center",va="bottom")


    ax_hist.set_xlabel(propiedad)
    ax_hist.set_ylabel('No.Events')
    ax_hist.set_title(f'Histogram of {propiedad} in {title} in {anio}')


    ax_tabla.set_title(f'Events details in {title} in {anio}')
    tabla = ax_tabla.table(cellText=valores, colLabels=titulos,loc="center",cellLoc="center")
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1.2,1.2)
    tabla.auto_set_column_width([3])
    plt.subplots_adjust(hspace=0.8)
    plt.show()

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass




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
            data = cantidad_datos(control)
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
