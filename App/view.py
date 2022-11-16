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
import webbrowser
from tabulate import tabulate
import os
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
assert cf
from datetime import datetime



"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# Funciones de Print

def printMoviesDetails(lista,cuenta,head1,head2,cant=3):
    size = lt.size(lista)
    
    if size:
        cont=1
        table=['']
        for i in lt.iterator(lista):
            if str(i[head1[0]]) not in table[-1]:
                aux=[]
                for j in lt.iterator(cuenta[i[head1[0]]]):
                    info=[]
                    for k in range(len(head2)):
                        info.append(j[head2[k]])
                    aux.append(info)
                table.append([i[head1[0]],lt.size(cuenta[i[head1[0]]]),tabulate(aux,head2,tablefmt="grid",maxcolwidths=20)])
            if cont==cant:
                break
            else:
                cont+=1
        if size>=cant*2:
            cont=0
            for i in lt.iterator(lista):
                
                if i[head1[0]] not in table[-1] and size-cont<=cant:
                    aux=[]
                    for j in lt.iterator(cuenta[i[head1[0]]]):
                        info=[]
                        for k in range(len(head2)):
                            info.append(j[head2[k]])
                        aux.append(info)
                    table.append([i[head1[0]],lt.size(cuenta[i[head1[0]]]),tabulate(aux,head2,tablefmt="grid",maxcolwidths=20)])
                if size-cont==0:
                    break
                else:
                    cont+=1

        print(tabulate(table[1:],head1,tablefmt="grid"))    
        print('\n')    
    else:
        print('No hay contenido')

def printMoviesCant(movies,cant,head):
    size = lt.size(movies)
    if size:
        table=[]
        i=1
        for movie in lt.iterator(movies):
            headers = []
            for j in range(len(head)):
                headers.append(movie[head[j]])
            table.append(headers)
            if i==cant:
                break
            else:
                i+=1
        if size>=cant*2:
            i=0
            for movie in lt.iterator(movies):
                headers = []
                if size-i<=cant:
                    for j in range(len(head)):
                        headers.append(movie[head[j]])
                    table.append(headers)
                if size-i==0:
                    break
                else:
                    i+=1
                    
        print(tabulate(table,head,tablefmt="grid",maxcolwidths=10))    
        print('\n')

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Consultar los videojuegos de una plataforma en un rango de tiempo.")
    print("2- Consultar records por jugador")
    print("3- Consultar los juegos que estén entre un rango de intentos de record")
    print("4- Consultar los records que estén entre un rango de fecha")
    print("5- Consultar los records mas recientes entre un rango de tiempos")
    print("6- Diagramar un histograma según añp y propiedad deseada")
    print("7- Consultar el top N de los juegos más rentables para retransmitir")
    print("8- Graficar la distribución de los mejores tiempos en un año por país")
    print("9- Salir")


# Función crear controlador

def newController():
    control = controller.newController()
    return control

# Función Cargar Datos

def loadData(control,archiv,memory):
    movies= controller.loadData(control,archiv,memory)
    return movies

# Funciones para ejecutar el menú
def playLoadData():
    print('\nCuántos datos desea cargar?')
    print('1: 0.5% de los datos')
    print('2: 5% de los datos')
    print('3: 10% de los datos')
    print('4: 20% de los datos')
    print('5: 30% de los datos')
    print('6: 50% de los datos')
    print('7: 80% de los datos')
    print('8: 100% de los datos')
    resp=int(input())
    if resp==1:
        archiv='small.csv'
    elif resp==2:
        archiv='5pct.csv'
    elif resp==3:
        archiv='10pct.csv'
    elif resp==4:
        archiv='20pct.csv'
    elif resp==5:
        archiv='30pct.csv'
    elif resp==6:
        archiv='50pct.csv'
    elif resp==7:
        archiv='80pct.csv'
    elif resp==8:
        archiv='large,.csv'
    
    resp=input(('\nDesea Conocer la memoria utilizada? '))
    resp=castBoolean(resp)
    juegos,records,time,memory= loadData(catalog,archiv,resp)
    os.system('cls')
    print('----------------------------------')
    print('Loaded speedruning data properties: ')
    print('Total loaded games: '+str(lt.size(juegos)))
    print('Total loaded speedruns: '+str(lt.size(records)))
    print('----------------------------------')
    
    print('\n------ Game Content ------')   
    head=['Game_Id','Release_Date',"Name",'Abbreviation','Platforms','Total_Runs','Genres']
    printMoviesCant(juegos,3,head)
    
    print('\n------ SpeedRuns Content ------')   
    head=['Game_Id','Record_Date_0','Num_Runs',"Name",'Category','Subcategory','Country_0','Players_0','Time_0']
    printMoviesCant(records,3,head)
    print(f'Tiempo de ejecución: {time:.3f}')
    print(f'Memoria Utilizada: {memory}\n')

def playReq1():
    plat= input("Ingrese la plataforma de interés: ")
    f_ini= datetime.strptime(input("Ingrese la fecha inicial: "), '%Y-%m-%d')
    f_fin= datetime.strptime(input("Ingrese la fecha final: "),"%Y-%m-%d")
    f_ini=datetime.strftime(f_ini,'%y-%m-%d')
    f_fin=datetime.strftime(f_fin,'%y-%m-%d')
    lista_juegos,cuenta,num_plats,time= controller.getReq1(catalog, plat, f_ini, f_fin)
    os.system('cls')
    print('============ Req No. 1 Inputs ============')
    print(f'Games released between {f_ini} and {f_fin}')
    print(f'In platform: "{plat}"')
    
    print('\n============ Req No. 1 Answer ============')
    print(f'Available games in {plat}: {num_plats}')
    print(f'Date range between {f_ini} and {f_fin}')
    print(f'Released Games: {lt.size(lista_juegos)}')

    head=['Release_Date','Count','Details']
    head_2=["Total_Runs",'Name','Abbreviation','Platforms','Genres']
    printMoviesDetails(lista_juegos,cuenta,head,head_2,3) 
    print('Tiempo de ejecución:',time,'ms')

def playReq2():
    nombre= input("Ingrese el nombre del jugador a consultar: ")
    lista_juegos,time= controller.getReq2(catalog, nombre)
    os.system('cls')
    print('============ Req No. 2 Inputs ============')
    print(f'Speedrun records for player: {nombre}')
    
    print('\n============ Req No. 2 Answer ============')
    print(f'Player {nombre} has {lt.size(lista_juegos)} Speedrun record attemps')
    print(f'Total records: {lt.size(lista_juegos)}')

    head=['Time_0','Record_Date_0','Name','Players_0','Country_0','Num_Runs','Platforms','Genres','Category','Subcategory']
    
    printMoviesCant(lista_juegos, 5, head) 
    print('Tiempo de ejecución:',time,'ms')

def playReq3():
    f_ini= int(input("Ingrese el límite inferior de intentos: "))
    f_fin= int(input("Ingrese el límite superior de intentos: "))
    lista_juegos,cuenta,time= controller.getReq3(catalog, f_ini, f_fin)
    os.system('cls')
    print('============ Req No. 3 Inputs ============')
    print(f'Category records between {f_ini} and {f_fin} attemps')
    
    print('\n============ Req No. 3 Answer ============')
    print(f'Attemps between {f_ini} and {f_fin}')
    print(f'Total records: {len(cuenta)}')

    head=['Num_Runs','Count','Details']
    head_2=["Time_0",'Record_Date_0','Name','Players_0','Country_0','Platforms','Genres','Category','Subcategory','Release_Date']
    printMoviesDetails(lista_juegos,cuenta,head,head_2,5) 
    print('Tiempo de ejecución:',time,'ms')

def playReq4():
    f_ini= input("Ingrese la fecha inicial: ")
    f_ini=f_ini+'T'+input('Ingrese la hora de la fecha inicial: ')+':00Z'
    f_fin= input("Ingrese la fecha final: ")
    f_fin=f_fin+'T'+input('Ingrese la hora de la fecha final: ')+':00Z'
    lista_juegos,cuenta,time= controller.getReq4(catalog, f_ini, f_fin)
    os.system('cls')
    print('============ Req No. 4 Inputs ============')
    print(f'Category records between {f_ini} and {f_fin} datetime')
    
    print('\n============ Req No. 4 Answer ============')
    print(f'Attemps between {f_ini} and {f_fin}')
    print(f'Total records: {lt.size(lista_juegos)}')

    head=['Record_Date_0','Count','Details']
    head_2=["Num_Runs",'Time_0','Name','Players_0','Country_0','Platforms','Genres','Category','Subcategory','Release_Date']
    printMoviesDetails(lista_juegos,cuenta,head,head_2,3) 
    print('Tiempo de ejecución:',time,'ms')

def playReq5():
    f_ini= float(input("Ingrese el límite inferior de tiempo: "))
    f_fin= float(input("Ingrese el límite superior de tiempo: "))
    lista_juegos,cuenta,time= controller.getReq5(catalog, f_ini, f_fin)
    os.system('cls')
    print('============ Req No. 3 Inputs ============')
    print(f'Category records between {f_ini} and {f_fin} runtime')
    
    print('\n============ Req No. 3 Answer ============')
    print(f'Attemps between {f_ini} and {f_fin}')
    print(f'Total records: {lt.size(lista_juegos)}')

    head=['Time_0','Count','Details']
    head_2=['Record_Date_0','Num_Runs','Name','Players_0','Country_0','Platforms','Genres','Category','Subcategory','Release_Date']
    printMoviesDetails(lista_juegos,cuenta,head,head_2,3) 
    print('Tiempo de ejecución:',time,'ms')

def playReq6():
    opciones=['Time_0','Time_1','Time_2','Time_Avg','Num_Runs']
    opcion= int(input("Ingrese la Opcion que desea consultar\n(1) Tiempo1\n(2) Tiempo 2\n(3) Tiempo 3\n(4) Promedio Tiempos\n(5) Intentos\n OPCION: "))
    f_ini= input("Ingrese el límite inferior de año: ")
    f_fin= input("Ingrese el límite superior de año: ")
    segmentos= int(input('Ingrese numero de segmentos para el histograma: '))
    niveles= int(input('Ingrese el numero de niveles para las marcas: '))
    arbol, listica,maxi,time= controller.getReq6(catalog, f_ini[2:]+'-00-00T00:00:00Z', f_fin[2:]+'-12-31T23:59:59Z',opciones[opcion-1], segmentos)
    
    os.system('cls')
    print('============ Req No. 6 Inputs ============')
    print(f'Count map (histogram) of the feature {opciones[opcion-1]}')
    print(f'Data between release years {f_ini} and {f_fin}')
    print(f'Number of bins: {segmentos}')
    print(f'Registered attemps per scale: {niveles}')
    
    print('\n============ Req No. 6 Answer ============')
    print(f'There are {om.size(arbol)} attemps on record')
    print(f'Lowest value: {listica[0][0]}')
    print(f'Highest value: {maxi}')
    print(f'{opciones[opcion-1]} Histogram with {segmentos} bins and {niveles} attemps per mark lvl')

    head=['bin','count','lvl', 'mark']
    table=[]
    for i in range(segmentos):
        table.append([f'({listica[i][0]}, {listica[i][1]}]',listica[i][2],listica[i][2]//niveles,'*'*(listica[i][2]//niveles)])
    print(tabulate(table,head,tablefmt="grid",maxcolwidths=30))
    print('Tiempo de ejecución:',time,'ms')

def playReq7():
    nombre= input("Ingrese la plataforma de interés: ")
    top= int(input("Que top desea consultar: "))
    lista_juegos,cuenta,total,time= controller.getReq7(catalog, nombre, top)
    os.system('cls')
    print('============ Req No. 7 Inputs ============')
    print(f'Find the TOP {top} games for {nombre} platform')
    
    print('\nFiltering records by platform...')
    print('Removing miscelaneous streaming revenue...')

    print('\n============ Req No. 7 Answer ============')
    print(f'There are {total} records for {nombre}')
    print(f'There are {len(cuenta)} unique games for {nombre}')

    head=['Name','Release_Date','Platforms','Genres','Stream_Revenue','Market_Share','Time_Avg','Total_Runs']
    
    printMoviesCant(lista_juegos, top, head) 
    print('Tiempo de ejecución:',time,'ms')


def playReq8():
    anio=input('Ingrese el año de interés: ')
    f_ini= float(input("Ingrese el límite inferior de tiempo: "))
    f_fin= float(input("Ingrese el límite superior de tiempo: "))
    cantidad,time=controller.getReq8(catalog, anio,f_ini,f_fin)

    os.system('cls')
    print('============ Req No. 8 Inputs ============')
    print(f'Find the games in {anio} that its better time is between {f_ini} minutes and {f_fin} minutes')
    
    print('\nFiltering records by year and time...')
    print('Rendering the map...')

    print('\n============ Req No. 8 Answer ============')
    print(f'There are {cantidad} games in {anio} that its better time is between {f_ini} minutes and {f_fin} minutes')
    print(f'Open the browser to see the map\n')
    print('Tiempo de ejecución:',time,'ms')

    webbrowser.open_new_tab('paises.html')
    


# Funciones Auxiliares

def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("Cargando información de los archivos ....")
        catalog = newController()
        playLoadData() 
    elif int(inputs[0])==1:
        playReq1()
    elif int(inputs[0])==2:
        playReq2()
    elif int(inputs[0])==3:
        playReq3()
    elif int(inputs[0])==4:
        playReq4()
    elif int(inputs[0])==5:
        playReq5()
    elif int(inputs[0])==6:
        playReq6()
    elif int(inputs[0])==7:
        playReq7()
    elif int(inputs[0])==8:
        playReq8() 
    else:
        sys.exit(0)
