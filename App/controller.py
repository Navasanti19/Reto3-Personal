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
 """

import tracemalloc
import config as cf
import model
import csv
import time
import tracemalloc

csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def newController():
    """
    Crea una instancia del modelo
    """
    control = {
        'model': None
    }
    control['model'] = model.newCatalog()
    return control

# Funciones para la carga de datos
def loadData(control,archiv, memory = False):
    start_time = getTime()
    if memory:
        tracemalloc.start()
        start_memory = getMemory()

    catalog = control['model']
    juegos= loadJuegos(catalog,archiv)
    record = loadRecords(catalog,archiv)
    loadPaises(catalog)

    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memory:
        stop_memory = getMemory()
        tracemalloc.stop()
        stop_time = getTime()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return juegos, record, delta_time, delta_memory

    else:
        return juegos, record, delta_time,None

def loadJuegos(catalog,archiv):
    booksfile = cf.data_dir + 'game_data_utf-8-'+archiv
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for juego in input_file:
        model.addJuego(catalog, juego)
    return catalog['juegos']

def loadRecords(catalog,archiv):
    booksfile = cf.data_dir + 'category_data_utf-8-'+archiv
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for juego in input_file:
        model.addRecord(catalog, juego,juego['Game_Id'])
    return catalog['records']

def loadPaises(catalog):
    booksfile = cf.data_dir + 'paises_2016_geom_10.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for juego in input_file:
        model.addPais(catalog, juego)
    

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def dataSize(analyzer,mapa):
    """
    Numero de crimenes leidos
    """
    return model.crimesSize(analyzer,mapa)

def indexHeight(analyzer,mapa):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer,mapa)

def indexSize(analyzer,mapa):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer,mapa)

def minKey(analyzer,mapa):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer,mapa)

def maxKey(analyzer,mapa):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer,mapa)

def getReq1(control, plat, f_ini,f_fin):
    movies_anio=model.getReq1(control['model'],plat,f_ini,f_fin)
    return movies_anio

def getReq2(control,nombre):
    movies_anio=model.getReq2(control['model'],nombre)
    return movies_anio

def getReq3(control,f_ini,f_fin):
    movies_anio=model.getReq3(control['model'],f_ini,f_fin)
    return movies_anio

def getReq4(control,f_ini,f_fin):
    movies_anio=model.getReq4(control['model'],f_ini,f_fin)
    return movies_anio

def getReq5(control,f_ini,f_fin):
    movies_anio=model.getReq5(control['model'],f_ini,f_fin)
    return movies_anio

def getReq6(control,f_ini,f_fin, opcion, segmentos):
    movies_anio=model.getReq6(control['model'],f_ini,f_fin,opcion,segmentos)
    return movies_anio

def getReq7(control,plat,top):
    movies_anio=model.getReq7(control['model'],plat,top)
    return movies_anio

def getReq8(control,anio,t_ini,t_fin):
    movies_anio=model.getReq8(control['model'],anio,t_ini,t_fin)
    return movies_anio

# Funciones de tiempo

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)

def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()

def deltaMemory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
