* El problema a Solucionar es que me enviaban archivos DBF por mail.
* El otro problema es que el sistema que uso en la empresa (propio de la empresa) está hecho en FoxPro por lo que la mayoria de las salidas son DBF
* Finalmente, no me dieron otra herramienta para poder contar las filas. 

* El Obejtivo es no abrir uno por uno archivos DBF con Excel, OpenOffice u otro aplicativo para saber cuantas filas tiene cada uno.

*Este programa lo que va a hacer es:

1. Elegir la carpeta donde estan los archivos y solo tomar en cuenta archivos DBF
2. Obtener el nombre de todos los archivos DBF y meterlos en una lista.
3. Para cada uno de los nombres, llamar al metodo "obtener_filas" para saber cuantas filas tiene ese DBF sin contar la fila 1  que es la cabecera.
4. Mostrar por pantalla las diferentes cantidades.
5. Guardarlas en un CSV con el formato: NombreDBF;Filas
6. Si no hay ningun DBF en esa carpeta, mostrar mensaje de error.
7. Si no se puede crear el CSV, mostrar mensaje  de error.
