"""
#El Obejtivo es no abrir uno por uno archivos DBF para saber cuantas filas tiene cada uno.

#Este programa lo que va a hacer es:

#1. Elegir la carpeta donde estan los archivos y solo tomar en cuenta archivos DBF
#2. Obtener el nombre de todos los archivos DBF y meterlos en una lista.
#3. Para cada uno de los nombres, llamar al metodo "obtener_filas" para saber cuantas filas tiene ese DBF sin contar la fila 1
# que es la cabecera.
#4. Mostrar por pantalla las diferentes cantidades.
#5. Guardarlas en un CSV con el formato: NombreDBF;Filas
#6. Si no hay ningun DBF en esa carpeta, mostrar mensaje de error.
#7. Si no se puede crear el CSV, mostrar mensaje  de error.
"""

import os # para  poder trabajar con el sistema operativo (lectura/escritura)
from tkinter import filedialog  # para elegir la carpeta donde esta guardado el DBF
from dbfread import DBF # para leer los DBF

import pandas as pd
import csv #Para exportar a un CSV
import numpy as np


#Primero voy a Seleccionar la carpeta
#Seleccionar una carpeta
directory = filedialog.askdirectory()
#print(directory)

#Muestra  los nombres de los archivos que se encuentran en la carpeta en una lista
with os.scandir(directory) as ficheros:
    #Genero la lista
    ficheros = [fichero.name for fichero in ficheros if fichero.is_file() and fichero.name.endswith('.dbf')]
# print(ficheros)

# Recorro la lista imprimiendo los nombres
#for nombre in ficheros:
#   print (nombre)

Lista_Archivo=[]
Cantidad_Registros=[]
Lista_Completa=[]


for nombre in ficheros:
    nombre_Completo = directory +('/') + nombre
    # Con esto hago que no me tome archivos con tamaño Cero
    if os.path.getsize(nombre_Completo) != 0:
        #print(nombre_Completo)
        Lista_Archivo.append(nombre_Completo)
        #Ahora por cada dato de la lista debo leer la cantidad de filas del archivo  correspondiente
        #y luego mostrarlo por pantalla.
        # finalmente guardo todo eso en un CSV
        I=1
        for record in DBF(nombre_Completo):
            I=I+1
        Cantidad_Registros.append(I-1)




        #print(record) # No imprimo el contenido del registro.
        #Este seria el nombre del archivo y la cantidad de registros.
        #print("El archivo es:",nombre_Completo, "y la cantidad de registros es: ",I-1, " porque el archivo tiene cabecera")
        
        
        # Genero una lista por cada archivo con el nombre y la cantidad de registros menos la cabecera
        Lista_Archivo_y_Tamanio=[nombre_Completo,I-1]
        
        #print(Lista_Archivo_y_Tamanio)
        
        #Creo la lista de Listas
        Lista_Completa.append(Lista_Archivo_y_Tamanio)
#Imprimo la lista de Listas
#print(Lista_Completa)
else:
    print("No hay archivos con tamaño Cero en la carpeta")


Lista_Completa_df=pd.DataFrame(Lista_Completa).transpose
print(Lista_Completa_df)

print("Creando archivo CSV...")
#Exporto a un CSV mediante Numpy
np.savetxt("cantidad_archivos.csv", 
    Lista_Completa, delimiter =";",  # Seteo el delimitador sin espacio para que me exporte como número.
    fmt ='% s')  # Pero otros datos como String


#Falta control de errores de carpeta.
