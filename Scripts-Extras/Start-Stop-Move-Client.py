import os
import os, sys
import time
import datetime
from shutil import rmtree 
from os import makedirs
from os import remove
import shutil

NumerodeCiclos = 4
DuracionTest = 30
CountTest = 1
TestNumero = "XXYYZZ"
DateTest = str(datetime.datetime.now())
Fecha = DateTest[0:10]

#crear carpeta
try:
    # change the destination path
    FolderTest = "C:/Users/Mijail/Documents/VSBLTY-Identificacion-Log/Log-Result/"  + Fecha + " " + str(TestNumero)
    makedirs(FolderTest)
    print ("Creating Folder of Test-", TestNumero)
except FileExistsError:
    print ("folder Exists")


#////////////////////////////////////////
# Iniciar el Cliente
#///////////////////////////////////////
while CountTest <= NumerodeCiclos:

    StartTestCliente = str(datetime.datetime.now())
    Fecha = StartTestCliente[0:10]
    #
    #crear carpeta
    try:
        # change the destination path
        NewFolderTest = FolderTest + "/"  + Fecha  + " " + "CICLO -" + str(CountTest)
        makedirs(NewFolderTest)
        print ("Creating Folder of Result Ciclo-", CountTest)
    except FileExistsError:
        print ("Folder Exists")

    print ("Test Numero", CountTest)

    print ("Start Cliente", StartTestCliente) 
    print ("Fecha", Fecha)

    #input ()
    # Iniciar Client
    print ("Start Cliente", StartTestCliente)   
    os.startfile('C:\\Users/Mijail/Documents/VSBLTY-Identificacion-Log/Scripts-Extras/Start-Client.bat')

    
    # Tiempo de espera para cerrar el cliente
    time.sleep(DuracionTest)

    # close Client
    os.system('taskkill -f -im vsb*')
    StopTestCliente =  datetime.datetime.now()
    print ("Stop Client", StopTestCliente)
    CountTest +=1 
    time.sleep(1)

    #//////////////////////////////////
	# Verificar la cantidad de archivos que existen dentro del directorio
	# Indicamos la ruta de donde se quieren leer los archivos
    path= "C:/ProgramData/Vsblty/KingSalmon/"
    dirs = os.listdir(path)
    i = 0
    # ////////////////////////////////////////////////////////////
    # Por cada Archivo dentro del directorio, se realiza un ciclo for para recorrer cada linea y verificar hits  
    # ////////////////////////////////////////////////////////////
    for file in dirs:
        Archivo = path + file
        print ("Moviendo Archivo: ", Archivo)
        shutil.move(Archivo, NewFolderTest)
        


    print ("Sleep de 10 Segundo")
    time.sleep(10)
    #input() 

print ("End Task Ciclos") 