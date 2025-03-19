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
import numpy as np #Para exportar a un CSV

import tkinter as tk
from tkinter import simpledialog, messagebox #Para mostrar mensajes de error y la ventana


# Función para Obtener las Filas de los DBF y guardar el archivo CSV
def Obtener_Filas_Guardar_csv():
    
    #Primero voy a Seleccionar la carpeta donde estan los archivos DBF
    #Seleccionar una carpeta
    directory = filedialog.askdirectory()
    #print(directory)

    #Muestra  los nombres de los archivos que se encuentran en la carpeta en una lista
    with os.scandir(directory) as ficheros:
        #Genero la lista con solo extension DBF
        ficheros = [fichero.name for fichero in ficheros if fichero.is_file() and fichero.name.endswith('.dbf')]
    # print(ficheros)

    # Recorro la lista imprimiendo los nombres
    #for nombre in ficheros:
    #   print (nombre)

    Lista_Archivo=[] #Lista de Archivos
    Cantidad_Registros=[] #Lista de Cantidad de Registros
    Lista_Completa=[] #Lista de Listas concatenando los nombres de los archivos y la cantidad de registros


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
    
    # Solicitar al usuario el nombre del archivo
    nombre_archivo = simpledialog.askstring("Guardar archivo", "Introduce el nombre del archivo (con extensión .csv):")

    #Exporto a un CSV mediante Numpy
    #np.savetxt("cantidad_archivos.csv", 
    np.savetxt(nombre_archivo, 
        Lista_Completa, delimiter =";",  # Seteo el delimitador sin espacio para que me exporte como número.
        fmt ='% s')  # Pero otros datos como String
    
    # Control de errores para verificar que el nombre no está vacío
    if not nombre_archivo:
        messagebox.showerror("Error", "El nombre del archivo no puede estar vacío.")
        return
    
    # Control de errores para verificar que tiene la extensión .csv
    if not nombre_archivo.endswith(".csv"):
        messagebox.showerror("Error", "El archivo debe tener la extensión .csv.")
        return
    
    # Intentar crear y guardar el archivo
    try:
        # Verificar si el archivo ya existe
        if os.path.exists(nombre_archivo):
            respuesta = messagebox.askyesno("Archivo existente", "El archivo ya existe. ¿Deseas reemplazarlo?")
            if not respuesta:
                return
        messagebox.showinfo("Éxito", f"El archivo '{nombre_archivo}' se ha guardado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al guardar el archivo: {e}")        






    #Falta control de errores de carpeta.

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Crear CSV a partir de una carpeta con DBF")

# Definir el tamaño de la ventana
ventana.geometry("400x150")  # Ancho 400, Alto 150
# Desactiva la opción de redimensionar
ventana.resizable(False, False)  

# Función que se ejecuta cuando se hace clic en el botón "Cancelar"
def funcion_cancelar():
    ventana.quit()  # Cierra la ventana

# Crear un contenedor (frame) para los botones y alinearlos
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=40)

# Crear los botones con tamaño específico
boton_aceptar = tk.Button(frame_botones, text="Procesar", command=Obtener_Filas_Guardar_csv, width=15, height=2)
boton_aceptar.pack(side=tk.LEFT, padx=10)  # Botón Procesar alineado a la izquierda

boton_cancelar = tk.Button(frame_botones, text="Cancelar", command=funcion_cancelar, width=15, height=2)
boton_cancelar.pack(side=tk.LEFT, padx=10)  # Botón Cancelar alineado a la derecha



# Mostrar la ventana para ejecutar el programa hasta que se presione el botón "Cancelar"
ventana.mainloop()

