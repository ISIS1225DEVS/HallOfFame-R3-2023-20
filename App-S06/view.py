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
import threading
from datetime import datetime
import matplotlib.pyplot as plt

default_limit=1000
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


def load_data(control,tamaño):
    """
    Carga los datos
    """
    if tamaño == 1:
        filename= 'Challenge-3/earthquakes/temblores-utf8-small.csv'
    elif tamaño == 5:
        filename= 'Challenge-3/earthquakes/temblores-utf8-5pct.csv'
    elif tamaño == 10:
        filename= 'Challenge-3/earthquakes/temblores-utf8-10pct.csv'
    elif tamaño == 20:
        filename= 'Challenge-3/earthquakes/temblores-utf8-20pct.csv'
    elif tamaño == 30:
        filename= 'Challenge-3/earthquakes/temblores-utf8-30pct.csv'
    elif tamaño == 50:
        filename= 'Challenge-3/earthquakes/temblores-utf8-50pct.csv'
    elif tamaño == 80:
        filename= 'Challenge-3/earthquakes/temblores-utf8-80pct.csv'
    elif tamaño == 100:
        filename= 'Challenge-3/earthquakes/temblores-utf8-large.csv'
    datos=controller.load_data(control,filename)
    return datos 


def print_Data(earthquakes, sample=5):
    """
        Función que imprime un dato dado su ID
    """
    size=lt.size(earthquakes)
    i=1
    table=[]
    headers = ["code", "time","lat","long","mag","title","depth","felt","cdi","mmi","tsunami"]
    while i <= sample:
        datos=[]
        temblor= lt.getElement(earthquakes,i)
        if temblor["code"] == "":
            datos.append("Unknown")
        else:
            datos.append(temblor["code"])
        if temblor["time"] == "":
            datos.append("Unknown")
        else:
            t= datetime.strptime(temblor["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
            t= datetime.strftime(t, "%Y-%m-%dT%H:%M")
            datos.append(t)
        if temblor["lat"] == "":
            datos.append("Unknown")
        else:
            datos.append(f"{float(temblor['lat']):.3f}")
        if temblor["long"] == "":
            datos.append("Unknown")
        else:
            datos.append(f"{float(temblor['long']):.3f}")
        if temblor["mag"] == "":
            datos.append("Unknown")
        else:
            datos.append(f"{float(temblor['mag']):.3f}")
        if temblor["title"] == "":
            datos.append("Unknown")
        else:
            datos.append(temblor["title"])
        if temblor["depth"] == "":
            datos.append("Unknown")
        else:
            datos.append(f"{float(temblor['depth']):.3f}")
        if temblor["felt"] == "":
            datos.append("Unknown")
        else:
            datos.append(temblor["felt"])
        if temblor["cdi"] == "":
            datos.append("Unknown")
        else:
            datos.append(temblor["cdi"])
        if temblor["mmi"] == "":
            datos.append("Unknown")
        else:
            datos.append(temblor["mmi"])
        if temblor["tsunami"] == "":
            datos.append("Unknown")
        else:
            if temblor["tsunami"] == "0":
                datos.append("False")
            else:
                datos.append("True")
        
        table.append(datos)
        i+=1
    i=size-sample+1
    while i<=size:
        datos=[]
        temblor= lt.getElement(earthquakes,i)
        if temblor["code"] == "":
            datos.append("Unknown")
        else:
            datos.append(temblor["code"])
        if temblor["time"] == "":
            datos.append("Unknown")
        else:
            t= datetime.strptime(temblor["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
            t= datetime.strftime(t, "%Y-%m-%dT%H:%M")
            datos.append(t)
        if temblor["lat"] == "":
            datos.append("Unknown")
        else:
            datos.append(f"{float(temblor['lat']):.3f}")
        if temblor["long"] == "":
            datos.append("Unknown")
        else:
            datos.append(f"{float(temblor['long']):.3f}")
        if temblor["mag"] == "":
            datos.append("Unknown")
        else:
            datos.append(f"{float(temblor['mag']):.3f}")
        if temblor["title"] == "":
            datos.append("Unknown")
        else:
            datos.append(temblor["title"])
        if temblor["depth"] == "":
            datos.append("Unknown")
        else:
            datos.append(f"{float(temblor['depth']):.3f}")
        if temblor["felt"] == "":
            datos.append("Unknown")
        else:
            datos.append(temblor["felt"])
        if temblor["cdi"] == "":
            datos.append("Unknown")
        else:
            datos.append(temblor["cdi"])
        if temblor["mmi"] == "":
            datos.append("Unknown")
        else:
            datos.append(temblor["mmi"])
        if temblor["tsunami"] == "":
            datos.append("Unknown")
        else:
            if temblor["tsunami"] == "0":
                datos.append("False")
            else:
                datos.append("True")

        table.append(datos)
        i+=1 
    print(tabulate(table, headers, tablefmt="grid")) 

def print_req_1(resultado, sample=3):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    size=lt.size(resultado)
    i=1
    table=[]
    headers = ["time","events","details"]
    if size <=sample*2:
        while i<= size:
            datos=[]
            temblor= lt.getElement(resultado,i)
            datos.append(temblor["time"])
            datos.append(temblor["events"])
            datos.append(print_table1(temblor["details"]))
            table.append(datos)
            i+=1
    else:     
        while i <= sample:
            datos=[]
            temblor= lt.getElement(resultado,i)
            datos.append(temblor["time"])
            datos.append(temblor["events"])
            datos.append(print_table1(temblor["details"]))
            table.append(datos)
            i+=1
        i=size-sample+1
        while i<=size:
            datos=[]
            temblor= lt.getElement(resultado,i)
            datos.append(temblor["time"])
            datos.append(temblor["events"])
            datos.append(print_table1(temblor["details"]))
            table.append(datos)
            i+=1 
    print(tabulate(table, headers, tablefmt="grid"))

def print_table1(earthquakes,sample=3):
    size=lt.size(earthquakes)
    i=1
    table=[]
    headers = ["mag","lat","long","depth","sig","gap","nst","title","cdi","mmi","magType","type","code"]
    if size <=sample*2:
        while i<= size:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            if temblor["mag"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mag"])
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["depth"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["depth"])
            if temblor["sig"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["sig"])
            if temblor["gap"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["gap"])
            if temblor["nst"] == "":
                datos.append("1")
            else:
                datos.append(temblor["nst"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["cdi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["cdi"])
            if temblor["mmi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mmi"])
            if temblor["magType"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["magType"])
            if temblor["type"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["type"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])

            table.append(datos)
            i+=1
    else:     
        while i <= sample:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            if temblor["mag"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mag"])
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["depth"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["depth"])
            if temblor["sig"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["sig"])
            if temblor["gap"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["gap"])
            if temblor["nst"] == "":
                datos.append("1")
            else:
                datos.append(temblor["nst"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["cdi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["cdi"])
            if temblor["mmi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mmi"])
            if temblor["magType"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["magType"])
            if temblor["type"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["type"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])
            table.append(datos)
            i+=1
        i=size-sample+1
        while i<=size:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            if temblor["mag"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mag"])
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["depth"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["depth"])
            if temblor["sig"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["sig"])
            if temblor["gap"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["gap"])
            if temblor["nst"] == "":
                datos.append("1")
            else:
                datos.append(temblor["nst"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["cdi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["cdi"])
            if temblor["mmi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mmi"])
            if temblor["magType"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["magType"])
            if temblor["type"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["type"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])
            table.append(datos)
            i+=1 
    return tabulate(table, headers, tablefmt="grid")


def print_req_2(earthquakes, sample=3):
    """
        Función que imprime un dato dado su ID
    """
    size=lt.size(earthquakes)
    i=1
    table=[]
    headers = ["mag","events","details"]
    if size <=sample*2:
        while i<= size:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            datos.append(temblor["mag"])
            datos.append(temblor["events"])
            datos.append(print_table2(temblor["details"]))
            table.append(datos)
            i+=1
    else:     
        while i <= sample:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            datos.append(temblor["mag"])
            datos.append(temblor["events"])
            datos.append(print_table2(temblor["details"]))
            table.append(datos)
            i+=1
        i=size-sample+1
        while i<=size:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            datos.append(temblor["mag"])
            datos.append(temblor["events"])
            datos.append(print_table2(temblor["details"]))
            table.append(datos)
            i+=1 
    print(tabulate(table, headers, tablefmt="grid"))

def print_table2(earthquakes,sample=3):
    size=lt.size(earthquakes)
    i=1
    table=[]
    headers = ["time","lat","long","depth","sig","gap","nst","title","cdi","mmi","magType","type","code"]
    if size <=sample*2:
        while i<= size:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            if temblor["time"] == "":
                datos.append("Unknown")
            else:
                t= datetime.strptime(temblor["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
                t= datetime.strftime(t, "%Y-%m-%d %H:%M:%S")
                datos.append(t)
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["depth"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["depth"])
            if temblor["sig"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["sig"])
            if temblor["gap"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["gap"])
            if temblor["nst"] == "":
                datos.append("1")
            else:
                datos.append(temblor["nst"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["cdi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["cdi"])
            if temblor["mmi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mmi"])
            if temblor["magType"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["magType"])
            if temblor["type"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["type"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])

            table.append(datos)
            i+=1
    else:     
        while i <= sample:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            if temblor["time"] == "":
                datos.append("Unknown")
            else:
                t= datetime.strptime(temblor["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
                t= datetime.strftime(t, "%Y-%m-%d %H:%M:%S")
                datos.append(t)
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["depth"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["depth"])
            if temblor["sig"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["sig"])
            if temblor["gap"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["gap"])
            if temblor["nst"] == "":
                datos.append("1")
            else:
                datos.append(temblor["nst"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["cdi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["cdi"])
            if temblor["mmi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mmi"])
            if temblor["magType"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["magType"])
            if temblor["type"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["type"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])
            table.append(datos)
            i+=1
        i=size-sample+1
        while i<=size:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            if temblor["time"] == "":
                datos.append("Unknown")
            else:
                t= datetime.strptime(temblor["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
                t= datetime.strftime(t, "%Y-%m-%d %H:%M:%S")
                datos.append(t)
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["depth"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["depth"])
            if temblor["sig"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["sig"])
            if temblor["gap"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["gap"])
            if temblor["nst"] == "":
                datos.append("1")
            else:
                datos.append(temblor["nst"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["cdi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["cdi"])
            if temblor["mmi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mmi"])
            if temblor["magType"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["magType"])
            if temblor["type"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["type"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])
            table.append(datos)
            i+=1 
    return tabulate(table, headers, tablefmt="grid")


def print_req_3(resultado, sample=3):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    size=lt.size(resultado)
    i=1
    table=[]
    headers = ["time","events","details"]
    if size <=sample*2:
        while i<= size:
            datos=[]
            temblor= lt.getElement(resultado,i)
            datos.append(temblor["time"])
            datos.append(temblor["events"])
            datos.append(print_table3(temblor["details"]))
            table.append(datos)
            i+=1
    else:     
        while i <= sample:
            datos=[]
            temblor= lt.getElement(resultado,i)
            datos.append(temblor["time"])
            datos.append(temblor["events"])
            datos.append(print_table3(temblor["details"]))
            table.append(datos)
            i+=1
        i=10-sample+1
        while i<=10:
            datos=[]
            temblor= lt.getElement(resultado,i)
            datos.append(temblor["time"])
            datos.append(temblor["events"])
            datos.append(print_table3(temblor["details"]))
            table.append(datos)
            i+=1 
    print(tabulate(table, headers, tablefmt="grid"))

def print_table3(earthquakes,sample=3):
    size=lt.size(earthquakes)
    i=1
    table=[]
    headers = ["mag","lat","long","depth","sig","gap","nst","title","cdi","mmi","magType","type","code"]
    if size <=sample*2:
        while i<= size:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            if temblor["mag"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mag"])
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["depth"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["depth"])
            if temblor["sig"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["sig"])
            if temblor["gap"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["gap"])
            if temblor["nst"] == "":
                datos.append("1")
            else:
                datos.append(temblor["nst"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["cdi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["cdi"])
            if temblor["mmi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mmi"])
            if temblor["magType"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["magType"])
            if temblor["type"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["type"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])

            table.append(datos)
            i+=1
    else:     
        while i <= sample:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            if temblor["mag"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mag"])
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["depth"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["depth"])
            if temblor["sig"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["sig"])
            if temblor["gap"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["gap"])
            if temblor["nst"] == "":
                datos.append("1")
            else:
                datos.append(temblor["nst"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["cdi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["cdi"])
            if temblor["mmi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mmi"])
            if temblor["magType"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["magType"])
            if temblor["type"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["type"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])
            table.append(datos)
            i+=1
        i=10-sample+1
        while i<=10:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            if temblor["mag"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mag"])
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["depth"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["depth"])
            if temblor["sig"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["sig"])
            if temblor["gap"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["gap"])
            if temblor["nst"] == "":
                datos.append("1")
            else:
                datos.append(temblor["nst"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["cdi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["cdi"])
            if temblor["mmi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mmi"])
            if temblor["magType"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["magType"])
            if temblor["type"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["type"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])
            table.append(datos)
            i+=1 
    return tabulate(table, headers, tablefmt="grid")


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    minsig = float(input("Ingrese la significancia mínima: "))
    maxgap = float(input("Ingrese la distancia azitumal máxima: "))
    print("\n")
    resultado, cantidad_de_sismos, delta= controller.req_4(control,minsig,maxgap)
    print("Tiempo", delta)
    print("Total events between dates", cantidad_de_sismos)
    primer_elemento = lt.getElement(resultado, 1)
    segundo_elemento = lt.getElement(resultado, 2)
    tercer_elemento = lt.getElement(resultado, 3)
    trelemento = lt.getElement(resultado, -3)
    catorelemento = lt.getElement(resultado, -2)
    ultelemento = lt.getElement(resultado, -1)
    
    
    lista_tabulate = [primer_elemento, segundo_elemento, tercer_elemento, trelemento, catorelemento, ultelemento]
    
    if len(resultado) >= 6:
        print(tabulate(lista_tabulate,  headers="keys", tablefmt='grid'))
    else:
        print(tabulate(resultado,  headers="keys", tablefmt='grid'))
        
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(earthquakes, sample=3):
    """
        Función que imprime un dato dado su ID
    """
    size=lt.size(earthquakes)
    i=1
    table=[]
    headers = ["time","events","details"]
    if size <=sample*2:
        while i<= size:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            t= datetime.strptime(temblor["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
            t= datetime.strftime(t, "%Y-%m-%dT%H:%M")
            datos.append(t)
            datos.append(temblor["events"])
            datos.append(print_table5(temblor["details"]))
            table.append(datos)
            i+=1
    else:     
        while i <= sample:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            t= datetime.strptime(temblor["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
            t= datetime.strftime(t, "%Y-%m-%dT%H:%M")
            datos.append(t)
            datos.append(temblor["events"])
            datos.append(print_table5(temblor["details"]))
            table.append(datos)
            i+=1
        i=size-sample+1
        while i<=size:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            t= datetime.strptime(temblor["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
            t= datetime.strftime(t, "%Y-%m-%dT%H:%M")
            datos.append(t)
            datos.append(temblor["events"])
            datos.append(print_table5(temblor["details"]))
            table.append(datos)
            i+=1 
    print(tabulate(table, headers, tablefmt="grid"))

def print_table5(earthquakes,sample=3):
    size=lt.size(earthquakes)
    i=1
    table=[]
    headers = ["mag","lat","long","depth","sig","gap","nst","title","cdi","mmi","magType","type","code"]
    if size <=sample*2:
        while i<= size:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            if temblor["mag"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mag"])
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["depth"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["depth"])
            if temblor["sig"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["sig"])
            if temblor["gap"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["gap"])
            if temblor["nst"] == "":
                datos.append("1")
            else:
                datos.append(temblor["nst"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["cdi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["cdi"])
            if temblor["mmi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mmi"])
            if temblor["magType"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["magType"])
            if temblor["type"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["type"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])

            table.append(datos)
            i+=1
    else:     
        while i <= sample:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            if temblor["mag"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mag"])
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["depth"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["depth"])
            if temblor["sig"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["sig"])
            if temblor["gap"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["gap"])
            if temblor["nst"] == "":
                datos.append("1")
            else:
                datos.append(temblor["nst"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["cdi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["cdi"])
            if temblor["mmi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mmi"])
            if temblor["magType"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["magType"])
            if temblor["type"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["type"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])
            table.append(datos)
            i+=1
        i=size-sample+1
        while i<=size:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            if temblor["mag"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mag"])
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["depth"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["depth"])
            if temblor["sig"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["sig"])
            if temblor["gap"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["gap"])
            if temblor["nst"] == "":
                datos.append("1")
            else:
                datos.append(temblor["nst"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["cdi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["cdi"])
            if temblor["mmi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mmi"])
            if temblor["magType"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["magType"])
            if temblor["type"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["type"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])
            table.append(datos)
            i+=1 
    return tabulate(table, headers, tablefmt="grid")


def print_req_6(earthquakes, sample=3):
    """
        Función que imprime un dato dado su ID
    """
    size=lt.size(earthquakes)
    i=1
    table=[]
    headers = ["time","events","details"]
    if size <=sample*2:
        while i<= size:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            t= datetime.strptime(temblor["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
            t= datetime.strftime(t, "%Y-%m-%dT%H:%M")
            datos.append(t)
            datos.append(temblor["events"])
            datos.append(print_table6(temblor["details"]))
            table.append(datos)
            i+=1
    else:     
        while i <= sample:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            t= datetime.strptime(temblor["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
            t= datetime.strftime(t, "%Y-%m-%dT%H:%M")
            datos.append(t)
            datos.append(temblor["events"])
            datos.append(print_table6(temblor["details"]))
            table.append(datos)
            i+=1
        i=size-sample+1
        while i<=size:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            t= datetime.strptime(temblor["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
            t= datetime.strftime(t, "%Y-%m-%dT%H:%M")
            datos.append(t)
            datos.append(temblor["events"])
            datos.append(print_table6(temblor["details"]))
            table.append(datos)
            i+=1 
    print(tabulate(table, headers, tablefmt="grid"))

def print_table6(earthquakes,sample=3):
    size=lt.size(earthquakes)
    i=1
    table=[]
    headers = ["mag","lat","long","depth","sig","gap","distance","nst","title","cdi","mmi","magType","type","code"]
    if size <=sample*2:
        while i<= size:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            if temblor["mag"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mag"])
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["depth"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["depth"])
            if temblor["sig"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["sig"])
            if temblor["gap"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["gap"])
            datos.append(round(temblor["hav"],3))
            if temblor["nst"] == "":
                datos.append("1")
            else:
                datos.append(temblor["nst"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["cdi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["cdi"])
            if temblor["mmi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mmi"])
            if temblor["magType"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["magType"])
            if temblor["type"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["type"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])

            table.append(datos)
            i+=1
    else:     
        while i <= sample:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            if temblor["mag"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mag"])
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["depth"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["depth"])
            if temblor["sig"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["sig"])
            if temblor["gap"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["gap"])
            datos.append(round(temblor["hav"],3))
            if temblor["nst"] == "":
                datos.append("1")
            else:
                datos.append(temblor["nst"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["cdi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["cdi"])
            if temblor["mmi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mmi"])
            if temblor["magType"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["magType"])
            if temblor["type"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["type"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])
            table.append(datos)
            i+=1
        i=size-sample+1
        while i<=size:
            datos=[]
            temblor= lt.getElement(earthquakes,i)
            if temblor["mag"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mag"])
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["depth"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["depth"])
            if temblor["sig"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["sig"])
            if temblor["gap"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["gap"])
            datos.append(round(temblor["hav"],3))
            if temblor["nst"] == "":
                datos.append("1")
            else:
                datos.append(temblor["nst"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["cdi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["cdi"])
            if temblor["mmi"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["mmi"])
            if temblor["magType"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["magType"])
            if temblor["type"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["type"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])
            table.append(datos)
            i+=1 
    return tabulate(table, headers, tablefmt="grid")

def print_sig6(temblor):
    table=[]
    headers = ["time","mag","lat","long","depth","sig","gap","distance","nst","title","cdi","mmi","magType","type","code"]
    datos=[]
    if temblor["time"] == "":
                datos.append("Unknown")
    else:
        t= datetime.strptime(temblor["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        t= datetime.strftime(t, "%Y-%m-%dT%H:%M")
        datos.append(t)
    if temblor["mag"] == "":
        datos.append("Unknown")
    else:
        datos.append(temblor["mag"])
    if temblor["lat"] == "":
        datos.append("Unknown")
    else:
        datos.append(temblor["lat"])
    if temblor["long"] == "":
        datos.append("Unknown")
    else:
        datos.append(temblor["long"])
    if temblor["depth"] == "":
        datos.append("Unknown")
    else:
        datos.append(temblor["depth"])
    if temblor["sig"] == "":
        datos.append("Unknown")
    else:
        datos.append(temblor["sig"])
    if temblor["gap"] == "":
        datos.append("0.000")
    else:
        datos.append(temblor["gap"])
    datos.append(round(temblor["hav"],3))
    if temblor["nst"] == "":
        datos.append("1")
    else:
        datos.append(temblor["nst"])
    if temblor["title"] == "":
        datos.append("Unknown")
    else:
        datos.append(temblor["title"])
    if temblor["cdi"] == "":
        datos.append("Unknown")
    else:
        datos.append(temblor["cdi"])
    if temblor["mmi"] == "":
        datos.append("Unknown")
    else:
        datos.append(temblor["mmi"])
    if temblor["magType"] == "":
        datos.append("Unknown")
    else:
        datos.append(temblor["magType"])
    if temblor["type"] == "":
        datos.append("Unknown")
    else:
        datos.append(temblor["type"])
    if temblor["code"] == "":
        datos.append("Unknown")
    else:
        datos.append(temblor["code"])
    table.append(datos)
    print(tabulate(table, headers, tablefmt="grid"))

def print_req_7(tabla, histo, title, anio, prop, bin, sample=3):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    size=lt.size(histo)
    i=1
    table=[]
    if size <=sample*2:
        while i<= size:
            datos=[]
            temblor= lt.getElement(tabla,i)
            if temblor["time"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["time"])
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])
            if temblor["mag"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["mag"])

            table.append(datos)
            i+=1
    else:     
        while i <= sample:
            datos=[]
            temblor= lt.getElement(tabla,i)
            if temblor["time"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["time"])
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])
            if temblor["mag"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["mag"])
            table.append(datos)
            i+=1
        i=size-sample+1
        while i<=size:
            datos=[]
            temblor= lt.getElement(tabla,i)
            if temblor["time"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["time"])
            if temblor["lat"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["lat"])
            if temblor["long"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["long"])
            if temblor["title"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["title"])
            if temblor["code"] == "":
                datos.append("Unknown")
            else:
                datos.append(temblor["code"])
            if temblor["mag"] == "":
                datos.append("0.000")
            else:
                datos.append(temblor["mag"])
            table.append(datos)
            i+=1

    histograma = []
    j = 1
    while j <= lt.size(histo):
        sismo = lt.getElement(histo, j)
        if prop == "mag":
            propiedad = sismo["mag"]
        elif prop == "depth":
            propiedad = sismo["depth"]
        elif prop == "sig":
            propiedad = sismo["sig"]
        histograma.append(propiedad)
        j += 1
    histograma.reverse()
    #INTERVALOS HISTOGRAMA
    min = float(histograma[0])
    max = float(histograma[lt.size(histo)-1])
    rango = max-min
    rango = rango/bin  

    fig,ax = plt.subplots(2,1)
    plt.subplots_adjust(hspace=0.5)
    colorbar=(0.6588,0.8235,0.7804)
    #HISTOGRAMA
    ax[0].set_title("Histogram of "+prop+" in "+title+" in "+anio)
    diseño1 = ax[0].hist(histograma, bins=bin, color=colorbar, edgecolor="black", width=0.8)
    for i in range(len(diseño1[2])):
        rect = diseño1[2][i]
        label = diseño1[0][i]
        height = rect.get_height()
        ax[0].text(rect.get_x() + rect.get_width() / 2, height, f'{int(label)}', ha='center', va='bottom')

    # Configuraciones adicionales
    ax[0].set_xlabel(prop)
    ax[0].set_ylabel('No. Events')

    #TABLA
    columnas = ["time","lat","long","title","code","mag"]
    data = table
    ax[1].axis("tight")
    ax[1].axis("off")
    ax[1].set_title("Events details in "+title+ " in "+anio)
    diseño2 = ax[1].table(cellText=data,colLabels=columnas, loc="center")
    diseño2.auto_set_column_width([0,1,2,3,4,5])
    diseño2.auto_set_font_size(False)
    diseño2.set_fontsize(7)
    plt.show()


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
    def menu_cycle():
        """
        Menu principal
        """
        working = True
        #ciclo del menu
        while working:
            print_menu()
            inputs = input('Seleccione una opción para continuar\n')
            if int(inputs) == 1:
                tamaño_archivo=int(input("Seleccione el tamaño del archivo que quiere cargar en numero ENTERO segun el porcentaje, inserte '1','5','10','20','30','50','80' o '100': "))
                print("Cargando información de los archivos ....\n")
                data = load_data(control,tamaño_archivo)  #ANALIZADOR CON DATOS CARGADOS DATA
                temblores = lt.size(data["earthquakes"])
                print("-"*40) 
                print("El tamaño de archivo cargado fue de "+str(tamaño_archivo)+"%")
                print("Se cargaron",temblores,"temblores")
                print("-"*40)
                print("")
                print("="*70)
                print("="*17,"INFORMES DE REGISTROS DE TEMBLORES","="*17)
                print("="*70)
                print("")
                print("----- RESULTADOS DE TEMBLORES ----")
                print("     Hay un total de",temblores,"temblores")
                print("Estos son los 5 primeros y ultimos temblores cargados...")
                print_Data(data["earthquakes"])
                print("")
                print("-"*70)
                print("")

            elif int(inputs) == 2:
                print("="*15,"Req No.1","="*15)
                fecha_ini = input("Escriba la fecha inicial de la busqueda: ")
                fecha_fin = input("Escriba la fecha inicial de la busqueda: ")
                print("Cargando información....")
                resultado,sismos,delta = controller.req_1(data,fecha_ini,fecha_fin)
                delta=f"{delta:.3f}"
                print("")
                print("="*15,"RESULTS","="*15)
                print("Total de sismos encontrados entre",fecha_ini,"y",fecha_fin,":",sismos)
                print("")
                print_req_1(resultado)
                print("")
                print("-"*70)
                print("Tiempo:",delta,"ms")
                print("")
                print("-"*70)
                print("")

            elif int(inputs) == 3:
                print("="*15,"Req No.2","="*15)
                magnitudI=float(input("Digite el rango inferior de la magnitud a buscar: "))
                magnitudF=float(input("Digite el rango superior de la magnitud a buscar: "))
                print("")
                print("Cargando información....")
                resultados ,delta= controller.req_2(data["magnitudes"],magnitudI,magnitudF)
                lista=resultados[0]
                tmag= resultados[1]
                teve= resultados[2]
                print("")
                print("="*15,"RESULTS","="*15)
                print("Total de magnitudes diferentes:",tmag)
                print("Total de eventos dentro del rango:",teve)
                print("")
                if lt.size(lista)<=6:
                    print("Mostrando",lt.size(lista),"resultados...")
                else: 
                    print("Hay mas de 6 resultados, mostrando los 3 primeros y ultimos resultados...")
                print_req_2(lista)
                print("")
                print("-"*70)
                print("Tiempo:",round(delta,3),"ms")
                print("")

            elif int(inputs) == 4:
                print("="*15,"Req No.3","="*15)
                mag = float(input("Escriba la magnitud minima de busqueda: "))
                depth = float(input("Escriba la profundidad maxima de busqueda: "))
                print("Cargando información....")
                resultado,sismos,delta = controller.req_3(data,mag,depth)
                delta=f"{delta:.3f}"
                print("")
                print("="*15,"RESULTS","="*15)
                print("Total de sismos encontrados entre:",sismos)
                print("")
                print_req_3(resultado)
                print("")
                print("-"*70)
                print("Tiempo:",delta,"ms")
                print("")
                print("-"*70)
                print("")

            elif int(inputs) == 5:
                print_req_4(control)

            elif int(inputs) == 6:
                print("="*15,"Req No.5","="*15)
                depth=float(input("Digite la profundidad minima del temblor: "))
                nst=float(input("Digite las estaciones de deteccion minimas del temblor: "))
                print("")
                print("Cargando información....")
                resultados = controller.req_5(data["earthquakes"],depth,nst)
                lista=resultados[0]
                tmag= resultados[1]
                teve= resultados[2]
                delta=resultados[3]
                print("")
                print("="*15,"RESULTS","="*15)
                print("Total de fechas diferentes:",tmag)
                print("Total de eventos dentro de las fechas:",teve)
                print("Seleccionando los 20 eventos mas recientes...")
                print("")
                if lt.size(lista)<=6:
                    print("Mostrando",lt.size(lista),"resultados...")
                else: 
                    print("Mostrando los 3 primeros y ultimos resultados...")
                print_req_5(lista)
                print("")
                print("-"*70)
                print("Tiempo:",round(delta,3),"ms")
                print("")

            elif int(inputs) == 7:
                print("="*15,"Req No.6","="*15)
                anio=input("Ingrese el año de consulta: ")
                lat=float(input("Ingrese el valor de la latitud: "))
                longitud=float(input("Ingrese el valor de la longitud: "))
                rad=float(input("Ingrese el valor del radio [km]: "))
                N=int(input("Ingrese el numero de eventos a consultar: "))
                print("")
                print("Cargando información....")
                resultados,delta=controller.req_6(data["earthquakes"],anio,lat,longitud,rad,N)
                sig=resultados[0]
                lgrande= resultados[1]
                teve= resultados[2]
                
                print("")
                print("="*15,"RESULTS","="*15)
                print("Total de eventos dentro del area:",teve)
                print("")
                print("-"*7,"Evento mas significativo","-"*7)
                print_sig6(sig)
                print("")
                print("-"*7,"Eveventos cronologicamente cerca al evento significativo","-"*7)
                print("Tamaño de consulta:",N, "Seleccionando los 3 primeros y ultimos eventos...")
                print_req_6(lgrande)
                print("")
                print("-"*70)
                print("Tiempo:",round(delta,3),"ms")
                print("")

            elif int(inputs) == 8:
                print("="*15,"Req No.7","="*15)
                anio = input("Escriba el año que quiere buscar: ")
                title = input("Escriba el titulo de la region asociada: ")
                prop = input("Escriba mag, depth o sig segun su interes: ")
                bin = int(input("Escriba el numero de segmentos de division del hsitograma: "))
                print("Cargando información....")
                tabla, histo ,delta = controller.req_7(data, anio, title, prop)
                delta=f"{delta:.3f}"
                print("")
                print("="*15,"RESULTS","="*15)
                print("Total de sismos encontrados entre:",lt.size(histo))
                print("")
                print_req_7(tabla, histo, title, anio, prop, bin)
                print("")
                print("-"*70)
                print("Tiempo:",delta,"ms")
                print("")
                print("-"*70)
                print("")

            elif int(inputs) == 9:
                print_req_8(control)

            elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa")
            else:
                print("Opción errónea, vuelva a elegir.\n")
        sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864*2)
    sys.setrecursionlimit(default_limit*1000000)
    thread=threading.Thread(target= menu_cycle)
    thread.start()
