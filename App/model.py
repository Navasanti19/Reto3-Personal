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


from csv import list_dialects
import config as cf
import time
from tabulate import tabulate
from datetime import datetime
import tracemalloc
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mer
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    
    catalog = {'juegos': None,
               'records': None,
               'juegos_fecha':None,
               'record_intentos':None,
               'crecord_tiempo':None,
               'id_game':None}

    catalog['juegos'] = lt.newList('ARRAY_LIST', None)
    catalog['records'] = lt.newList('ARRAY_LIST', None)
    

    catalog["juegos_fecha"] = om.newMap(omaptype="RBT", comparefunction=compareCantidad)
                                      
    catalog["record_intentos"] = om.newMap(omaptype="RBT",comparefunction=compareCantidad)
                                      
    catalog["record_tiempo"] = om.newMap(omaptype="RBT",comparefunction=compareCantidad)

    catalog['id_juego'] = mp.newMap(100,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=None)
    
    return catalog

# Funciones para agregar informacion al catalogo

def addJuego(analyzer, juego):
    lt.addLast(analyzer["juegos"], juego)
    updateJuegoFecha(analyzer["juegos_fecha"], juego)
    addMapNombreJuego(analyzer,juego['Game_Id'],juego['Name'])
    return analyzer

def addRecord(analyzer, record, id):
    record['Name'] = me.getValue(mp.get(analyzer['id_juego'],id))
    lt.addLast(analyzer["records"], record)
    updateRecordIntentos(analyzer["record_intentos"], record)
    updateRecordTiempo(analyzer["record_tiempo"], record)
    return analyzer

def addMapNombreJuego(catalog,key,value):
    exist = mp.contains(catalog['id_juego'], key)
    if not exist:
        mp.put(catalog['id_juego'], key, value)

def updateJuegoFecha(map, juego):
    
    if juego["Release_Date"] in [''," ", None]:
        fecha='00-00-00'
    else:
        fecha=juego['Release_Date']

    entry = om.get(map, fecha)
    if entry is None:
        fechaentry = newEntry()
        om.put(map, fecha, fechaentry)
    else:
        fechaentry = me.getValue(entry)
    addIndex(fechaentry, juego)
    return map

def updateRecordIntentos(map, record):
    
    if record["Num_Runs"] in [''," ", None]:
        intento=0
    else:
        intento=int(record['Num_Runs'])

    entry = om.get(map, intento)
    if entry is None:
        fechaentry = newEntry()
        om.put(map, intento, fechaentry)
    else:
        fechaentry = me.getValue(entry)
    addIndex(fechaentry, record)
    return map

def updateRecordTiempo(map, record):
    
    if record["Time_0"] in [''," ", None]:
        tiempo=0
    else:
        tiempo=float(record['Time_0'])

    entry = om.get(map, tiempo)
    if entry is None:
        fechaentry = newEntry()
        om.put(map, tiempo, fechaentry)
    else:
        fechaentry = me.getValue(entry)
    addIndex(fechaentry, record)
    return map

def newEntry():
    entry = {"lstcrimes": None, }
    entry['lstcrimes']=lt.newList('ARRAY_LIST')
    return entry

def addIndex(areaentry, crime):
    lst = areaentry["lstcrimes"]
    lt.addLast(lst, crime)
    return areaentry

# Funciones para creacion de datos


# Funciones de consulta

def getReq1(catalog, plat, f_ini,f_fin):
    lst = om.values(catalog["juegos_fecha"], f_ini, f_fin)
    cuenta={}
    n_plats=0
    lista_juegos=lt.newList('ARRAY_LIST')
    for i in lt.iterator(lst):
        
        for j in lt.iterator(i['lstcrimes']):
            
            if plat in j['Platforms']:
                n_plats+=1
                lt.addLast(lista_juegos,j)
                if j['Release_Date'] in cuenta:
                    lt.addLast(cuenta[j['Release_Date']],j)
                else:
                    cuenta[j['Release_Date']]=lt.newList('ARRAY_LIST')
                    lt.addLast(cuenta[j['Release_Date']],j)
    
    mer.sort(lista_juegos, cmpReleaseDate)
    return lista_juegos, cuenta, n_plats

def crimesSize(analyzer,mapa):
    """
    Número de crimenes
    """
    return lt.size(analyzer[mapa])

def indexHeight(analyzer,mapa):
    """
    Altura del arbol
    """
    return om.height(analyzer[mapa])

def indexSize(analyzer,mapa):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer[mapa])

def minKey(analyzer,mapa):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer[mapa])

def maxKey(analyzer,mapa):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer[mapa])

# Funciones de ordenamiento


# Funciones de comparación
def cmpReleaseDate(movie1, movie2):
    
    if datetime.strptime(movie1['Release_Date'],"%y-%m-%d")==datetime.strptime(movie2['Release_Date'],"%y-%m-%d"):
        if movie1['Name'].lower() < movie2['Name'].lower():
            return 0
        else:
            return 1
    elif datetime.strptime(movie1['Release_Date'],"%y-%m-%d")<datetime.strptime(movie2['Release_Date'],"%y-%m-%d"):
        return 0
    else:
        return 1
    
def compareCantidad(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1