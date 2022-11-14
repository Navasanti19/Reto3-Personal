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
import math
import config as cf
import time
import folium
from tabulate import tabulate
from folium.plugins import MarkerCluster
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
    
    catalog["records_fecha"] = om.newMap(omaptype="RBT", comparefunction=compareCantidad)
    
    catalog["records_fecha2"] = om.newMap(omaptype="RBT", comparefunction=compareCantidad)
                                      
    catalog["record_intentos"] = om.newMap(omaptype="RBT",comparefunction=compareCantidad)
                                      
    catalog["record_tiempo"] = om.newMap(omaptype="RBT",comparefunction=compareCantidad)

    catalog['id_juego'] = mp.newMap(100,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=None)
    catalog['jugadores'] = mp.newMap(100,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=None)
    
    catalog['Platforms'] = mp.newMap(5,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=None)
    
    catalog['paises'] = mp.newMap(100,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=None)
    
    return catalog


# Funciones para agregar informacion al catalogo

def addPais(analyzer,pais):
    exist = mp.contains(analyzer['paises'], pais['name'].lower())
    if not exist:
        mp.put(analyzer['paises'], pais['name'].lower(), [pais['latitude'],pais['longitude']])

def addJuego(analyzer, juego):
    lt.addLast(analyzer["juegos"], juego)
    addMapNombreJuego(analyzer,juego['Game_Id'],[juego,1])
    return analyzer

def addRecord(analyzer, record,id):
    lst=["Abbreviation","Genres","Name",'Platforms','Release_Date','Total_Runs']
    for i in lst:
        record[i] = me.getValue(mp.get(analyzer['id_juego'],id))[0][i]
    lt.addLast(analyzer["records"], record)
    updateJuegoFecha(analyzer["juegos_fecha"], record, analyzer['id_juego'])
    updateRecordIntentos(analyzer["record_intentos"], record)
    updateRecordTiempo(analyzer["record_tiempo"], record)
    updateRecordFecha(analyzer["records_fecha"], record)
    updateRecordFecha2(analyzer["records_fecha2"], record)
    addMapJugador(analyzer,record['Players_0'],record)
    addMapPlatform(analyzer,record['Platforms'],record)
    return analyzer

def addMapNombreJuego(catalog,key,value):
    exist = mp.contains(catalog['id_juego'], key)
    if not exist:
        mp.put(catalog['id_juego'], key, value)

def addMapJugador(catalog,key,value):
    exist = mp.contains(catalog['jugadores'], key)
    if exist:
        dicci = mp.get(catalog['jugadores'], key)
        valor = me.getValue(dicci)
    else:
        valor = newEntry()
        mp.put(catalog['jugadores'], key, valor)
    lt.addLast(valor['lstcrimes'], value)

def addMapPlatform(catalog,key,value):
    plat=key
    if ',' in plat:
        plat=plat.split(', ')
        for i in plat:
            exist = mp.contains(catalog['Platforms'], i)
            if exist:
                dicci = mp.get(catalog['Platforms'], i)
                valor = me.getValue(dicci)
            else:
                valor = newEntry()
                mp.put(catalog['Platforms'], i, valor)
            lt.addLast(valor['lstcrimes'], value)
    elif plat=='':
        exist = mp.contains(catalog['Platforms'], 'Unknown')
        if exist:
            dicci = mp.get(catalog['Platforms'], 'Unknown')
            valor = me.getValue(dicci)
        else:
            valor = newEntry()
            mp.put(catalog['Platforms'], 'Unknown', valor)
        lt.addLast(valor['lstcrimes'], value)
    else:
        exist = mp.contains(catalog['Platforms'], plat)
        if exist:
            dicci = mp.get(catalog['Platforms'], plat)
            valor = me.getValue(dicci)
        else:
            valor = newEntry()
            mp.put(catalog['Platforms'], plat, valor)
        lt.addLast(valor['lstcrimes'], value)

def updateJuegoFecha(map, juego, mapid):
    
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
    
    entry=mp.get(mapid,juego['Game_Id'])
    
    if me.getValue(entry)[1] !=0:
        addIndex(fechaentry, juego)
    me.setValue(entry,[juego,0])
    
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

def updateRecordFecha(map, juego):
    
    if juego["Record_Date_0"] in [''," ", None]:
        fecha='00-00-00T00:00:00Z'
    else:
        fecha=juego['Record_Date_0']

    entry = om.get(map, fecha)
    if entry is None:
        fechaentry = newEntry()
        om.put(map, fecha, fechaentry)
    else:
        fechaentry = me.getValue(entry)
    
    addIndex(fechaentry, juego)
    return map

def updateRecordFecha2(map, juego):
    
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

def newEntry():
    entry = {"lstcrimes": None, }
    entry['lstcrimes']=lt.newList('ARRAY_LIST')
    return entry

def addIndex(areaentry, crime):
    lst = areaentry["lstcrimes"]
    lt.addLast(lst, crime)
    return areaentry


# Funciones de consulta

def getReq1(catalog, plat, f_ini,f_fin):
    start_time=getTime()
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
    end_time=getTime()
    times=deltaTime(start_time,end_time)
    return lista_juegos, cuenta, n_plats, round(times,3)

def getReq2 (catalog, nombre):
    start_time=getTime()
    series = mp.get(catalog['jugadores'],nombre)
    series = me.getValue(series)['lstcrimes']
    mer.sort(series, cmpReleaseTime)
    end_time=getTime()
    times=deltaTime(start_time,end_time)
    return series, round(times,3)

def getReq3(catalog,f_ini,f_fin):
    start_time=getTime()
    lst = om.values(catalog["record_intentos"], f_ini, f_fin)
    cuenta={}
    lista_juegos=lt.newList('ARRAY_LIST')
    for i in lt.iterator(lst):
        for j in lt.iterator(i['lstcrimes']):
            if j['Num_Runs'] in cuenta:
                lt.addLast(cuenta[j['Num_Runs']],j)
            else:
                lt.addLast(lista_juegos,j)
                cuenta[j['Num_Runs']]=lt.newList('ARRAY_LIST')
                lt.addLast(cuenta[j['Num_Runs']],j)
            num=j['Num_Runs']
        mer.sort(cuenta[num], cmpReleaseTime)
    mer.sort(lista_juegos, cmpNumRuns)
    end_time=getTime()
    times=deltaTime(start_time,end_time)
    return lista_juegos, cuenta, round(times,3)

def getReq4(catalog,f_ini,f_fin):
    start_time=getTime()
    lst = om.values(catalog["records_fecha"], f_ini, f_fin)
    cuenta={}
    lista_juegos=lt.newList('ARRAY_LIST')
    for i in lt.iterator(lst):
        for j in lt.iterator(i['lstcrimes']):
            if j['Record_Date_0'] in cuenta:
                lt.addLast(cuenta[j['Record_Date_0']],j)
            else:
                lt.addLast(lista_juegos,j)
                cuenta[j['Record_Date_0']]=lt.newList('ARRAY_LIST')
                lt.addLast(cuenta[j['Record_Date_0']],j)
            num=j['Record_Date_0']
        mer.sort(cuenta[num], cmpReleaseTime)
    mer.sort(lista_juegos, cmpRecordDate)
    end_time=getTime()
    times=deltaTime(start_time,end_time)
    return lista_juegos, cuenta, round(times,3)

def getReq5(catalog,f_ini,f_fin):
    start_time=getTime()
    lst = om.values(catalog["record_tiempo"], f_ini, f_fin)
    cuenta={}
    lista_juegos=lt.newList('ARRAY_LIST')
    for i in lt.iterator(lst):
        for j in lt.iterator(i['lstcrimes']):
            if j['Time_0'] in cuenta:
                lt.addLast(cuenta[j['Time_0']],j)
            else:
                lt.addLast(lista_juegos,j)
                cuenta[j['Time_0']]=lt.newList('ARRAY_LIST')
                lt.addLast(cuenta[j['Time_0']],j)
            num=j['Time_0']
        mer.sort(cuenta[num], cmpRecordDate)
    mer.sort(lista_juegos, cmpReleaseTime)
    end_time=getTime()
    times=deltaTime(start_time,end_time)
    return lista_juegos, cuenta, round(times,3)

def getReq6(catalog,f_ini,f_fin,opcion,segmentos):
    start_time=getTime()
    lst = om.values(catalog["records_fecha2"], f_ini, f_fin)
    arbol=om.newMap(omaptype="RBT", comparefunction=compareCantidad)
    for i in lt.iterator(lst):
        for j in lt.iterator(i['lstcrimes']):
            
            times=[]
            times.append(float(j['Time_0'])) if j['Time_0']!='' else None
            times.append(float(j['Time_1'])) if j['Time_1']!='' else None
            times.append(float(j['Time_2'])) if j['Time_2']!='' else None

            if opcion=='Time_Avg':
                avg=(sum(times))/len(times)
                om.put(arbol,avg,j)
            else:
                om.put(arbol,j[opcion],j)
    rango=(om.maxKey(arbol)-om.minKey(arbol))/segmentos+0.002
    listica=[]
    inicial=round(om.minKey(arbol),2)
    for _ in range(segmentos):
        lista_rango=om.values(arbol, round(inicial,2), round(inicial+rango,2))
        
        listica.append([round(inicial,2),round(inicial+rango,2), lt.size(lista_rango)])
        inicial+=rango
    
    end_time=getTime()
    times=deltaTime(start_time,end_time)

    return arbol, listica, round(times,3)

def getReq7(catalog, plat, top):
    start_time=getTime()
    series = mp.get(catalog['Platforms'],plat)
    series = me.getValue(series)['lstcrimes']
    cuenta={}
    total=0
    for i in lt.iterator(series):
        if i['Misc']!='True':
            total+=1
    for i in lt.iterator(series):

        if i['Misc']!='True':
            contador=0
            if i['Name'] not in cuenta:
                for j in lt.iterator(series):
                    if j['Misc']!='True' and j['Name']==i['Name']:
                        contador+=1
            
                cuenta[i['Name']]=round(contador/total,2)


            anio=int(i['Release_Date'][:2])
            if anio>=0 and anio<=23:
                anio=2000+anio
            else:
                anio=1900+anio

            if anio>=2018:
                antiquity=anio-2017
            elif anio>=1998:
                antiquity= round(((-0.2)*anio)+404.6,2)
            else:
                antiquity=5
            
            popularity=round(math.log(float(i['Total_Runs'])),2)
            times=[]
            times.append(float(i['Time_0'])) if i['Time_0']!='' else None
            times.append(float(i['Time_1'])) if i['Time_1']!='' else None
            times.append(float(i['Time_2'])) if i['Time_2']!='' else None
            time_avg=round(sum(times)/len(times),2)

            revenue=round((popularity*time_avg/60)/antiquity,2)
        
            marketshare=cuenta[i['Name']]

            streamrevenue=round(revenue*marketshare,2)
            
            i['Market_Share']=marketshare
            i['Time_Avg']=time_avg
            i['Stream_Revenue']=streamrevenue
        else:
            i['Stream_Revenue']=0
            i['Market_Share']=0
            i['Time_Avg']=0
    
    mer.sort(series, cmpRevenue)
    top_n=lt.subList(series,1,top)
    end_time=getTime()
    times=deltaTime(start_time,end_time)

    return top_n, cuenta,total, round(times,3)

def getReq8(catalog,fecha, t_ini,t_fin):
    start_time=getTime()
    lst = om.values(catalog["record_tiempo"], t_ini, t_fin)
    cuenta={}
    cantidad=0
    for i in lt.iterator(lst):
        for j in lt.iterator(i['lstcrimes']):
            if fecha[2:] == j['Release_Date'][:2]:
                
                pais=j['Country_0'].lower()
                if ',' in pais:
                    pais=pais.split(',')
                    listica=[]
                    for k in pais:
                        if k!='Unknown' and k not in listica:
                            cantidad+=1
                            if k not in cuenta:
                                cuenta[k]=lt.newList('ARRAY_LIST')
                                lt.addLast(cuenta[k],j)
                            else:
                                lt.addLast(cuenta[k],j)
                            listica.append(k)
                else:

                    if pais not in cuenta:
                        cuenta[pais]=lt.newList('ARRAY_LIST')
                        lt.addLast(cuenta[pais],j)
                    else:
                        lt.addLast(cuenta[pais],j)
                    cantidad+=1
               
    m = folium.Map(location=[22,0],zoom_start=1, tiles="cartodbpositron")
    mc=MarkerCluster()
    
    for i in cuenta:
        for j in lt.iterator(cuenta[i]):
            try:
                info_geo=mp.get(catalog['paises'],i)
                mc.add_child(folium.CircleMarker(popup=j['Name']+'\n'+j['Players_0']+'\n'+j['Time_0'],location=me.getValue(info_geo),radius=5,color="#3186cc",fill=True,fill_color="#3186cc"))
            except:
                pass
    m.add_child(mc)
    m.save("paises.html")
    end_time=getTime()
    times=deltaTime(start_time,end_time)
    return cantidad, round(times,3)


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

def cmpRecordDate(movie1, movie2):

    if movie1['Record_Date_0']<movie2['Record_Date_0']:
        return 0
    else:
        return 1

def cmpRevenue(movie1, movie2):

    if movie1['Stream_Revenue']<movie2['Stream_Revenue']:
        return 0
    else:
        return 1

def cmpReleaseTime(movie1, movie2):
    if movie1['Time_0']==movie2['Time_0']:
        if datetime.strptime(movie1['Release_Date'],"%y-%m-%d")==datetime.strptime(movie2['Release_Date'],"%y-%m-%d"):
            if movie1['Name'].lower() < movie2['Name'].lower():
                return 0
            else:
                return 1
        elif datetime.strptime(movie1['Release_Date'],"%y-%m-%d")<datetime.strptime(movie2['Release_Date'],"%y-%m-%d"):
            return 0
    elif float(movie1['Time_0'])<float(movie2['Time_0']):
        return 1
    else:
        return 0

def cmpNumRuns(movie1, movie2):
    if movie1['Num_Runs']<movie2['Num_Runs']:
        return 1
    else:
        return 0
    
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


#Funciones de Tiempo

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)

def deltaTime(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed