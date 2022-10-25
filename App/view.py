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
from tabulate import tabulate
import os
from DISClib.ADT import list as lt
assert cf
from datetime import datetime



"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# Funciones de Print

def printMovies(movies):
    size = lt.size(movies)
    if size:
        headers = [list(movies['first']['info'].keys())]
        table=[]
        for movie in lt.iterator(movies):
            table.append([movie['show_id'],movie['type'],movie['title'],movie['director'],movie['cast'],movie['country'],movie['date_added'],movie['release_year'],movie['rating'],movie['duration'],movie['listed_in'],movie['description'],movie['stream_service']])
        print(tabulate(table,headers[0],tablefmt="grid",maxcolwidths=14))    
        print('\n')    
    else:
        print('No se encontraron peliculas')

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
    print("1- Examinar las películas estrenadas en un año")
    print("2- Examinar los programas de televisión agregados en un año ")
    print("3- Encontrar el contenido donde participa un actor")
    print("4- Encontrar el contenido por un genero particular")
    print("5- Encontrar el contenido producido en un país")
    print("6- Encontrar el contenido con un director involucrado")
    print("7- Listar el TOP (N) de los géneros con más contenido")
    print("8- Listar el TOP (N) de los actores con más participaciones")
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
        archiv='large.csv'
    
    resp=input(('\nDesea Conocer la memoria utilizada? '))
    resp=castBoolean(resp)
    juegos,records,time,memory= loadData(catalog,archiv,resp)
    os.system('cls')
    print('----------------------------------')
    print('Loaded straming service info: ')
    print('Total loaded games: '+str(lt.size(juegos)))
    print('Total loaded speedruns: '+str(lt.size(records)))
    print('----------------------------------')
    
    print('\n------ Game Content ------')   
    head=["Name",'Genres','Platforms','Total_Runs','Release_Date']
    printMoviesCant(juegos,3,head)
    
    print('\n------ SpeedRuns Content ------')   
    head=["Name",'Category','Subcategory','Players_0','Country_0','Time_0','Record_Date_0']
    printMoviesCant(records,3,head)
    print(f'Tiempo de ejecución: {time:.3f}')
    print(f'Memoria Utilizada: {memory}')

def playReq1():
    pass

def playReq2():
    pass

def playReq3():
    pass

def playReq4():
    pass

def playReq5():
    pass

def playReq6():
    pass

def playReq7():
    pass

def playReq8():
    pass
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
